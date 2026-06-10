# instalar_vigex_windows.ps1 — Asistente de instalacion Vigex desde Windows
# R-067 / Ruta 8.2
# Ejecutar desde el directorio raiz del repositorio Vigex:
#   Set-ExecutionPolicy -Scope Process Bypass
#   .\tools\windows\instalar_vigex_windows.ps1

param(
    [string]$ServidorIP     = "",
    [string]$UsuarioSSH     = "root",
    [string]$Perfil         = "",
    [string]$AccionInstalar = "instalar"   # instalar | actualizar | backup
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# ── Banner ───────────────────────────────────────────────────────────────────

function Write-Banner {
    Write-Host ""
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host "  Vigex Server Manager - Asistente de despliegue desde Windows" -ForegroundColor Cyan
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host "  Este asistente copia los archivos al servidor Linux y ejecuta" -ForegroundColor Gray
    Write-Host "  el instalador de forma guiada. Necesitaras la contrasena SSH." -ForegroundColor Gray
    Write-Host ""
}

function Write-Step {
    param([int]$Num, [string]$Texto)
    Write-Host ""
    Write-Host "  [$Num] $Texto" -ForegroundColor Yellow
}

function Write-Ok   { param([string]$Msg) Write-Host "  [OK] $Msg" -ForegroundColor Green }
function Write-Warn { param([string]$Msg) Write-Host "  [!!] $Msg" -ForegroundColor Yellow }
function Write-Err  { param([string]$Msg) Write-Host "  [ERROR] $Msg" -ForegroundColor Red }
function Write-Info { param([string]$Msg) Write-Host "  [i]  $Msg" -ForegroundColor Gray }

# ── Verificar directorio del repositorio ─────────────────────────────────────

$RepoRoot = (Get-Location).Path
if (-not (Test-Path "$RepoRoot\deploy\api\install_vigex_api.sh")) {
    Write-Err "No se encuentra deploy\api\install_vigex_api.sh."
    Write-Err "Ejecuta este script desde el directorio raiz del repositorio Vigex."
    exit 1
}

# ── Verificar cliente SSH disponible ─────────────────────────────────────────

Write-Banner
Write-Step 1 "Verificando requisitos del sistema"

$sshCmd = Get-Command ssh -ErrorAction SilentlyContinue
$scpCmd = Get-Command scp -ErrorAction SilentlyContinue

if (-not $sshCmd) {
    Write-Err "SSH no encontrado."
    Write-Info "Activa 'Cliente OpenSSH' en: Configuracion > Apps > Caracteristicas opcionales."
    exit 1
}
if (-not $scpCmd) {
    Write-Err "SCP no encontrado."
    Write-Info "Activa 'Cliente OpenSSH' en: Configuracion > Apps > Caracteristicas opcionales."
    exit 1
}

Write-Ok "SSH: $($sshCmd.Source)"
Write-Ok "SCP: $($scpCmd.Source)"

# ── Seleccion de accion ───────────────────────────────────────────────────────

Write-Step 2 "Selecciona la accion"
Write-Host ""
Write-Host "    1. Instalar Vigex (servidor nuevo)" -ForegroundColor White
Write-Host "    2. Actualizar Vigex (preserva config.env y datos)" -ForegroundColor White
Write-Host "    3. Hacer backup del panel Vigex" -ForegroundColor White
Write-Host ""

if ($AccionInstalar -notin @("instalar","actualizar","backup")) {
    $opcion = Read-Host "  Elige una opcion (1/2/3)"
    switch ($opcion) {
        "1" { $AccionInstalar = "instalar" }
        "2" { $AccionInstalar = "actualizar" }
        "3" { $AccionInstalar = "backup" }
        default {
            Write-Err "Opcion no valida."
            exit 1
        }
    }
}
Write-Ok "Accion seleccionada: $AccionInstalar"

# ── Datos de conexion ─────────────────────────────────────────────────────────

Write-Step 3 "Datos de conexion al servidor Linux"
Write-Host ""

if (-not $ServidorIP) {
    $ServidorIP = Read-Host "  IP o hostname del servidor Linux"
}
if (-not $ServidorIP) {
    Write-Err "La IP del servidor no puede estar vacia."
    exit 1
}

if ($UsuarioSSH -eq "root") {
    $inputUser = Read-Host "  Usuario SSH [$UsuarioSSH]"
    if ($inputUser) { $UsuarioSSH = $inputUser }
}

Write-Ok "Servidor: ${UsuarioSSH}@${ServidorIP}"

# ── Perfil Vigex (solo para instalacion nueva) ─────────────────────────────────

if ($AccionInstalar -eq "instalar") {
    Write-Step 4 "Perfil de despliegue"
    Write-Host ""
    Write-Host "    lite     - todo en un solo servidor (recomendado para empezar)" -ForegroundColor White
    Write-Host "    standard - panel + BD en dos servidores" -ForegroundColor White
    Write-Host "    pro      - tres servidores separados" -ForegroundColor White
    Write-Host ""

    if (-not $Perfil) {
        $Perfil = Read-Host "  Perfil (lite/standard/pro) [lite]"
        if (-not $Perfil) { $Perfil = "lite" }
    }
    $Perfil = $Perfil.ToLower()
    if ($Perfil -notin @("lite","standard","pro","custom")) {
        Write-Err "Perfil no valido. Usa: lite, standard, pro o custom."
        exit 1
    }
    Write-Ok "Perfil seleccionado: $Perfil"
}

# ── Resumen y confirmacion ────────────────────────────────────────────────────

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor White
Write-Host "  Resumen de la operacion"
Write-Host "=====================================================================" -ForegroundColor White
Write-Host "  Accion  : $AccionInstalar"
Write-Host "  Servidor: ${UsuarioSSH}@${ServidorIP}"
if ($AccionInstalar -eq "instalar") {
    Write-Host "  Perfil  : $Perfil"
}
Write-Host "=====================================================================" -ForegroundColor White
Write-Host ""

$confirmar = Read-Host "  Continuar? (S/N)"
if ($confirmar.ToLower() -notin @("s","si","y","yes")) {
    Write-Warn "Operacion cancelada."
    exit 0
}

# ── Copia de archivos al servidor ─────────────────────────────────────────────

Write-Step 5 "Copiando archivos al servidor"
Write-Info "Se te pedira la contrasena SSH para copiar los archivos."
Write-Host ""

$EpochSeg = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$RemoteTmpDir = "/tmp/vigex-deploy-$EpochSeg"

# Crear directorio remoto
& ssh "${UsuarioSSH}@${ServidorIP}" "mkdir -p $RemoteTmpDir"
if ($LASTEXITCODE -ne 0) {
    Write-Err "No se pudo conectar al servidor. Verifica la IP y el usuario."
    exit 1
}

# Copiar deploy/ al servidor
& scp -r "$RepoRoot\deploy" "${UsuarioSSH}@${ServidorIP}:${RemoteTmpDir}/"
if ($LASTEXITCODE -ne 0) {
    Write-Err "Error copiando archivos al servidor."
    exit 1
}
Write-Ok "Archivos copiados a ${ServidorIP}:${RemoteTmpDir}"

# ── Ejecutar script en el servidor ───────────────────────────────────────────

Write-Step 6 "Ejecutando el script en el servidor"
Write-Info "Se te pedira la contrasena SSH de nuevo para la ejecucion remota."
Write-Host ""

$ScriptRemoto = switch ($AccionInstalar) {
    "instalar"   { "$RemoteTmpDir/deploy/api/install_vigex_api.sh" }
    "actualizar" { "$RemoteTmpDir/deploy/api/update_vigex_api.sh" }
    "backup"     { "$RemoteTmpDir/deploy/api/backup_vigex_api.sh" }
}

$EnvPrefix = ""
if ($AccionInstalar -eq "instalar") {
    $EnvPrefix = "export VIGEX_PROFILE=$Perfil;"
}
if ($AccionInstalar -eq "actualizar") {
    $EnvPrefix = "export VIGEX_UPDATE_NONINTERACTIVE=1;"
}

$RemoteCmd = "chmod +x $ScriptRemoto && $EnvPrefix sudo -E bash $ScriptRemoto"
Write-Info "Comando remoto: $RemoteCmd"
Write-Host ""

& ssh -t "${UsuarioSSH}@${ServidorIP}" $RemoteCmd
$SshExitCode = $LASTEXITCODE

# ── Limpieza de temporales ────────────────────────────────────────────────────

Write-Host ""
Write-Info "Limpiando archivos temporales del servidor..."
& ssh "${UsuarioSSH}@${ServidorIP}" "rm -rf $RemoteTmpDir" 2>$null
Write-Ok "Directorio temporal eliminado"

# ── Resultado final ───────────────────────────────────────────────────────────

Write-Host ""
if ($SshExitCode -eq 0) {
    Write-Host "=====================================================================" -ForegroundColor Green
    Write-Host "  Operacion completada: $AccionInstalar" -ForegroundColor Green
    Write-Host "=====================================================================" -ForegroundColor Green
    if ($AccionInstalar -eq "instalar") {
        Write-Host ""
        Write-Host "  Panel disponible en: http://${ServidorIP}:8000" -ForegroundColor Cyan
        Write-Host "  Para HTTPS activa el proxy inverso: install_nginx_vigex_api.sh" -ForegroundColor Gray
    }
} else {
    Write-Host "=====================================================================" -ForegroundColor Red
    Write-Host "  La operacion finalizo con errores (codigo: $SshExitCode)" -ForegroundColor Red
    Write-Host "  Revisa la salida anterior para diagnosticar el problema." -ForegroundColor Red
    Write-Host "=====================================================================" -ForegroundColor Red
    exit $SshExitCode
}
Write-Host ""
