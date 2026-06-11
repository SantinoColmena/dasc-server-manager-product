#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Instalador de Vigex para Windows via Docker.
    Descarga e instala Docker Desktop si no está presente, despliega el panel Vigex
    como contenedor y lo registra como servicio de inicio automático.

.NOTES
    R-099 — Vigex para Windows
    Requisitos: Windows 10 v1903+ / Windows Server 2019+, 4 GB RAM, 8 GB disco libre.
    El script debe ejecutarse como Administrador.
#>

[CmdletBinding()]
param(
    [string]$InstallDir   = "$env:ProgramData\Vigex",
    [string]$PanelPort    = "8000",
    [switch]$Unattended,
    [switch]$Uninstall,
    [switch]$Update
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$ProgressPreference    = "SilentlyContinue"   # acelera Invoke-WebRequest

# ── Constantes ─────────────────────────────────────────────────────────────────
$VIGEX_IMAGE       = "vigex/panel:latest"
$CONTAINER_NAME    = "vigex-panel"
$SERVICE_NAME      = "VigexDockerAutostart"
$LOG_FILE          = "$InstallDir\install.log"
$DOCKER_INSTALLER  = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
$MIN_RAM_MB        = 3800
$MIN_DISK_FREE_GB  = 6

# ── Utilidades ─────────────────────────────────────────────────────────────────
function Write-Step {
    param([string]$Msg)
    $ts = Get-Date -Format "HH:mm:ss"
    Write-Host "  [$ts] $Msg" -ForegroundColor Cyan
    Add-Content -Path $LOG_FILE -Value "[$ts] $Msg" -Encoding UTF8
}

function Write-Ok   { param([string]$Msg); Write-Host "  [OK] $Msg" -ForegroundColor Green }
function Write-Warn { param([string]$Msg); Write-Host "  [!]  $Msg" -ForegroundColor Yellow }
function Write-Err  { param([string]$Msg); Write-Host "  [X]  $Msg" -ForegroundColor Red; Add-Content -Path $LOG_FILE -Value "[ERR] $Msg" -Encoding UTF8 }

function Confirm-Continue {
    param([string]$Prompt)
    if ($Unattended) { return $true }
    $resp = Read-Host "$Prompt [S/n]"
    return ($resp -eq "" -or $resp -match "^[SsYy]")
}

function Assert-Prereqs {
    Write-Step "Verificando requisitos del sistema..."

    # RAM
    $ramMb = (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1MB
    if ($ramMb -lt $MIN_RAM_MB) {
        Write-Err "RAM insuficiente: $([int]$ramMb) MB detectados, mínimo $MIN_RAM_MB MB."
        exit 1
    }

    # Disco libre en C:
    $diskFreeGb = (Get-PSDrive C).Free / 1GB
    if ($diskFreeGb -lt $MIN_DISK_FREE_GB) {
        Write-Err "Espacio libre insuficiente: $([math]::Round($diskFreeGb,1)) GB en C:, mínimo $MIN_DISK_FREE_GB GB."
        exit 1
    }

    # Virtualización (Hyper-V o WSL2)
    $hvEnabled = (Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -ErrorAction SilentlyContinue).State -eq "Enabled"
    $wslEnabled = (Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -ErrorAction SilentlyContinue).State -eq "Enabled"
    if (-not $hvEnabled -and -not $wslEnabled) {
        Write-Warn "Virtualización no detectada. Docker puede necesitar activar WSL 2 o Hyper-V."
        Write-Warn "Si la instalación falla, activa 'Plataforma de máquina virtual' en Características de Windows."
    }

    Write-Ok "Requisitos verificados. RAM: $([int]$ramMb) MB  Disco libre: $([math]::Round($diskFreeGb,1)) GB"
}

function Install-DockerIfMissing {
    $dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
    if ($dockerCmd) {
        Write-Ok "Docker ya está instalado: $(docker --version)"
        return
    }

    Write-Step "Docker no encontrado. Descargando Docker Desktop..."
    if (-not (Confirm-Continue "¿Instalar Docker Desktop automáticamente?")) {
        Write-Err "Instalación cancelada. Instala Docker Desktop manualmente y vuelve a ejecutar este script."
        exit 1
    }

    $tmpInstaller = "$env:TEMP\DockerDesktopInstaller.exe"
    Write-Step "Descargando desde Docker, esto puede tardar varios minutos..."
    Invoke-WebRequest -Uri $DOCKER_INSTALLER -OutFile $tmpInstaller

    Write-Step "Instalando Docker Desktop (sin GUI, backend WSL2)..."
    Start-Process -FilePath $tmpInstaller -ArgumentList "install --quiet --accept-license --backend=wsl-2" -Wait -NoNewWindow

    Remove-Item $tmpInstaller -Force

    # Añadir docker al PATH de esta sesión
    $env:Path += ";$env:ProgramFiles\Docker\Docker\resources\bin"

    # Esperar a que el daemon arranque
    Write-Step "Esperando a que el daemon Docker inicie (hasta 60 s)..."
    $tries = 0
    do {
        Start-Sleep -Seconds 5
        $tries++
        $ready = (docker info 2>$null) -ne $null
    } while (-not $ready -and $tries -lt 12)

    if (-not $ready) {
        Write-Err "Docker no arrancó tras 60 segundos. Reinicia el equipo y vuelve a ejecutar."
        exit 1
    }

    Write-Ok "Docker Desktop instalado y operativo."
}

function Ensure-DockerRunning {
    Write-Step "Comprobando que Docker está en ejecución..."
    try {
        $null = docker info 2>&1
        Write-Ok "Docker activo."
    } catch {
        Write-Warn "Docker no responde. Intentando iniciar Docker Desktop..."
        Start-Process "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe" -WindowStyle Hidden
        Start-Sleep -Seconds 20
        try {
            $null = docker info 2>&1
            Write-Ok "Docker iniciado."
        } catch {
            Write-Err "No se pudo conectar con Docker. Asegúrate de que Docker Desktop esté abierto e inténtalo de nuevo."
            exit 1
        }
    }
}

function Deploy-VigexContainer {
    Write-Step "Preparando directorio de instalación: $InstallDir"
    New-Item -ItemType Directory -Force -Path "$InstallDir\data"    | Out-Null
    New-Item -ItemType Directory -Force -Path "$InstallDir\reports" | Out-Null
    New-Item -ItemType Directory -Force -Path "$InstallDir\.ssh"    | Out-Null

    # Config
    $configFile = "$InstallDir\config.env"
    if (-not (Test-Path $configFile)) {
        Write-Step "Creando config.env de ejemplo en $configFile"
        Copy-Item "$PSScriptRoot\config.env.example" $configFile
        Write-Warn "Edita $configFile con tus valores antes de usar el panel."
    } else {
        Write-Ok "config.env existente detectado — no se sobreescribe."
    }

    # Obtener la imagen
    Write-Step "Descargando imagen Vigex (puede tardar unos minutos la primera vez)..."
    docker pull $VIGEX_IMAGE

    # Parar contenedor anterior si existe
    $existing = docker ps -a --filter "name=$CONTAINER_NAME" --format "{{.Names}}" 2>$null
    if ($existing -eq $CONTAINER_NAME) {
        Write-Step "Deteniendo contenedor anterior..."
        docker stop $CONTAINER_NAME  | Out-Null
        docker rm   $CONTAINER_NAME  | Out-Null
    }

    Write-Step "Arrancando contenedor Vigex en puerto $PanelPort..."
    docker run -d `
        --name $CONTAINER_NAME `
        --restart unless-stopped `
        -p "${PanelPort}:8000" `
        --env-file "$configFile" `
        -v vigex-data:/app/data `
        -v vigex-reports:/app/reports `
        -v vigex-ssh:/app/.ssh `
        $VIGEX_IMAGE

    Write-Step "Esperando a que el panel responda (hasta 30 s)..."
    $tries = 0
    $ok    = $false
    do {
        Start-Sleep -Seconds 3
        $tries++
        try {
            $resp = Invoke-WebRequest -Uri "http://localhost:$PanelPort/health" -UseBasicParsing -TimeoutSec 4
            if ($resp.StatusCode -eq 200) { $ok = $true }
        } catch {}
    } while (-not $ok -and $tries -lt 10)

    if ($ok) {
        Write-Ok "Panel Vigex operativo en http://localhost:$PanelPort"
    } else {
        Write-Warn "El panel aún no responde. Puede estar iniciándose. Abre http://localhost:$PanelPort en unos segundos."
    }
}

function Register-AutostartTask {
    Write-Step "Registrando tarea de inicio automático..."

    $action  = New-ScheduledTaskAction -Execute "docker" -Argument "start $CONTAINER_NAME"
    $trigger = New-ScheduledTaskTrigger -AtStartup
    $settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 2) -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

    Register-ScheduledTask -TaskName $SERVICE_NAME `
        -Action $action -Trigger $trigger `
        -Settings $settings -Principal $principal `
        -Description "Inicia el contenedor Vigex al arrancar Windows." `
        -Force | Out-Null

    Write-Ok "Tarea '$SERVICE_NAME' registrada. Vigex arrancará automáticamente con Windows."
}

function Uninstall-Vigex {
    Write-Host "`n  Desinstalando Vigex..." -ForegroundColor Yellow
    if (-not (Confirm-Continue "¿Confirmas la desinstalación de Vigex?")) { exit 0 }

    # Tarea programada
    Unregister-ScheduledTask -TaskName $SERVICE_NAME -Confirm:$false -ErrorAction SilentlyContinue
    Write-Ok "Tarea de inicio eliminada."

    # Contenedor
    docker stop $CONTAINER_NAME 2>$null | Out-Null
    docker rm   $CONTAINER_NAME 2>$null | Out-Null
    Write-Ok "Contenedor eliminado."

    # Imagen (opcional)
    if (Confirm-Continue "¿Eliminar también la imagen Docker de Vigex (libera espacio)?") {
        docker rmi $VIGEX_IMAGE 2>$null | Out-Null
        Write-Ok "Imagen eliminada."
    }

    # Datos (opcional — NO por defecto)
    if (Confirm-Continue "¿Eliminar TAMBIÉN los datos y configuración en $InstallDir? (IRREVERSIBLE)") {
        Remove-Item -Recurse -Force $InstallDir -ErrorAction SilentlyContinue
        Write-Ok "Directorio de datos eliminado."
    } else {
        Write-Ok "Datos conservados en $InstallDir"
    }

    Write-Host "`n  Vigex desinstalado correctamente." -ForegroundColor Green
}

function Update-Vigex {
    Write-Step "Actualizando Vigex..."
    Ensure-DockerRunning
    Write-Step "Descargando última imagen..."
    docker pull $VIGEX_IMAGE
    Write-Step "Reiniciando contenedor con la nueva imagen..."
    docker stop  $CONTAINER_NAME | Out-Null
    docker rm    $CONTAINER_NAME | Out-Null
    Deploy-VigexContainer
    Write-Ok "Vigex actualizado."
}

# ── Punto de entrada ────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  ╔══════════════════════════════════════╗" -ForegroundColor White
Write-Host "  ║         Vigex Setup para Windows     ║" -ForegroundColor White
Write-Host "  ╚══════════════════════════════════════╝" -ForegroundColor White
Write-Host ""

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

if ($Uninstall) {
    Uninstall-Vigex
    exit 0
}

if ($Update) {
    Update-Vigex
    exit 0
}

# Instalación normal
Assert-Prereqs
Install-DockerIfMissing
Ensure-DockerRunning
Deploy-VigexContainer
Register-AutostartTask

Write-Host ""
Write-Host "  ╔═══════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "  ║  Vigex instalado correctamente                    ║" -ForegroundColor Green
Write-Host "  ║                                                   ║" -ForegroundColor Green
Write-Host "  ║  Panel:   http://localhost:$PanelPort               ║" -ForegroundColor Green
Write-Host "  ║  Config:  $InstallDir\config.env   ║" -ForegroundColor Green
Write-Host "  ║                                                   ║" -ForegroundColor Green
Write-Host "  ║  Edita config.env y reinicia el contenedor:       ║" -ForegroundColor Green
Write-Host "  ║    docker restart vigex-panel                     ║" -ForegroundColor Green
Write-Host "  ╚═══════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
