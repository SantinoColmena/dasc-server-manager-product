param(
    [string]$RepoRoot = ".",
    [switch]$SkipPipAudit
)

# R-057C: Smoke test de release -- ejecuta todas las validaciones estaticas
# y reporta un resultado consolidado (PASS / FAIL).
# Uso: .\tools\windows\smoke_test_release.ps1 [-RepoRoot <ruta>] [-SkipPipAudit]

$ErrorActionPreference = "Continue"

$root = (Resolve-Path -LiteralPath $RepoRoot).Path
$toolsDir = Join-Path $root "tools\windows"

$results = New-Object System.Collections.Generic.List[object]
$globalOk = $true

function Add-Result {
    param([string]$Name, [bool]$Ok, [string]$Detail)
    $results.Add([PSCustomObject]@{ Nombre = $Name; OK = $Ok; Detalle = $Detail })
    if (-not $Ok) { $script:globalOk = $false }
}

function Write-Status {
    param([bool]$Ok, [string]$Msg)
    if ($Ok) { Write-Host "[OK]  $Msg" -ForegroundColor Green }
    else      { Write-Host "[FAIL] $Msg" -ForegroundColor Red }
}

Write-Host ""
Write-Host "=== Vigex Server Manager -- Smoke Test Release ===" -ForegroundColor Cyan
Write-Host "  Raiz del repo: $root"
Write-Host "  Fecha        : $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
Write-Host ""

# -----------------------------------------------------------------------
# 1. git status limpio
# -----------------------------------------------------------------------
Write-Host "-- 1. Estado git --"
try {
    $gitRaw = git -C $root status --porcelain 2>&1
    # Ignorar los informes generados automaticamente por los sub-scripts de validacion
    $gitStatus = $gitRaw | Where-Object {
        $_ -notmatch "docs[/\\]validaciones[/\\]" -and
        $_ -notmatch "docs[/\\]auditoria[/\\]"
    }
    $gitOk = ($gitStatus -eq $null) -or ($gitStatus -join "").Trim() -eq ""
    $gitDetail = if ($gitOk) { "Arbol limpio (informes de validacion excluidos)" } else { $gitStatus -join "; " }
    Add-Result "git status limpio" $gitOk $gitDetail
    Write-Status $gitOk "git status limpio"
} catch {
    Add-Result "git status limpio" $false $_.Exception.Message
    Write-Status $false "git status: error - $($_.Exception.Message)"
}

# config.env real no commiteado
try {
    $tracked = git -C $root ls-files "config.env" 2>&1
    $noEnv = ($tracked -eq $null) -or ($tracked.Trim() -eq "")
    $envDetail = if ($noEnv) { "No rastreado" } else { "ALERTA: config.env esta commiteado" }
    Add-Result "config.env no commiteado" $noEnv $envDetail
    Write-Status $noEnv "config.env no commiteado"
} catch {
    Add-Result "config.env no commiteado" $false $_.Exception.Message
    Write-Status $false "config.env check: error"
}

Write-Host ""

# -----------------------------------------------------------------------
# 2. check_api_package_installable.ps1
# -----------------------------------------------------------------------
Write-Host "-- 2. Paquete API instalable --"
$installScript = Join-Path $toolsDir "check_api_package_installable.ps1"
if (Test-Path $installScript) {
    try {
        & $installScript -RepoRoot $root
        $installOk = ($LASTEXITCODE -eq 0)
        Add-Result "check_api_package_installable" $installOk ("Exit code: $LASTEXITCODE")
        Write-Status $installOk "check_api_package_installable.ps1"
    } catch {
        Add-Result "check_api_package_installable" $false $_.Exception.Message
        Write-Status $false "check_api_package_installable.ps1: excepcion"
    }
} else {
    Add-Result "check_api_package_installable" $false "Script no encontrado: $installScript"
    Write-Status $false "check_api_package_installable.ps1: no encontrado"
}

Write-Host ""

# -----------------------------------------------------------------------
# 3. check_repo_clean.ps1
# -----------------------------------------------------------------------
Write-Host "-- 3. Repo limpio (secretos / sensibles) --"
$cleanScript = Join-Path $toolsDir "check_repo_clean.ps1"
if (Test-Path $cleanScript) {
    try {
        & $cleanScript -RepoRoot $root
        $cleanOk = ($LASTEXITCODE -eq 0)
        Add-Result "check_repo_clean" $cleanOk ("Exit code: $LASTEXITCODE")
        Write-Status $cleanOk "check_repo_clean.ps1"
    } catch {
        Add-Result "check_repo_clean" $false $_.Exception.Message
        Write-Status $false "check_repo_clean.ps1: excepcion"
    }
} else {
    Add-Result "check_repo_clean" $false "Script no encontrado: $cleanScript"
    Write-Status $false "check_repo_clean.ps1: no encontrado"
}

Write-Host ""

# -----------------------------------------------------------------------
# 4. Ficheros clave de release
# -----------------------------------------------------------------------
Write-Host "-- 4. Ficheros clave de release --"
$requiredFiles = @(
    "README.md",
    "CHANGELOG.md",
    "docs\ROADMAP.md",
    "docs\release\checklist_regresion.md",
    "config.env.example",
    "deploy\api\package\requirements.txt",
    "deploy\api\package\main.py",
    "deploy\api\install_vigex_api.sh",
    "deploy\db\install_db.sh",
    "deploy\backup-services\install_backup_services.sh",
    "deploy\proxy\install_reverse_proxy.sh",
    "deploy\api\harden_ufw_api.sh",
    "deploy\api\harden_fail2ban_api.sh",
    "deploy\db\harden_ufw_db.sh",
    "deploy\backup-services\harden_ufw_backup.sh"
)

$allFilesOk = $true
foreach ($rel in $requiredFiles) {
    $full = Join-Path $root $rel
    $exists = Test-Path $full
    if (-not $exists) {
        $allFilesOk = $false
        Write-Host "  [FAIL] Falta: $rel" -ForegroundColor Red
    }
}
if ($allFilesOk) { Write-Host "  Todos los ficheros clave presentes." -ForegroundColor Green }
$filesDetail = if ($allFilesOk) { "Todos presentes" } else { "Algunos ficheros faltan (ver arriba)" }
Add-Result "Ficheros clave de release" $allFilesOk $filesDetail
Write-Status $allFilesOk "Ficheros clave de release"

Write-Host ""

# -----------------------------------------------------------------------
# 5. pip-audit (opcional con -SkipPipAudit)
# -----------------------------------------------------------------------
Write-Host "-- 5. pip-audit de dependencias --"
if ($SkipPipAudit) {
    Write-Host "  Omitido por parametro -SkipPipAudit." -ForegroundColor Yellow
    Add-Result "pip-audit API" $true "Omitido (-SkipPipAudit)"
    Add-Result "pip-audit Central Support" $true "Omitido (-SkipPipAudit)"
} else {
    $pipAuditAvail = $false
    try {
        python -m pip_audit --version 2>&1 | Out-Null
        $pipAuditAvail = ($LASTEXITCODE -eq 0)
    } catch {}

    if (-not $pipAuditAvail) {
        Write-Host "  pip-audit no disponible. Instalando..." -ForegroundColor Yellow
        python -m pip install pip-audit --quiet
    }

    foreach ($pkg in @("deploy\api\package", "deploy\central-support\package")) {
        $reqFile = Join-Path $root "$pkg\requirements.txt"
        $labelRaw = ($pkg -replace "\\", "/") -replace "deploy/", "" -replace "/package", ""
        if (Test-Path $reqFile) {
            python -m pip_audit -r $reqFile 2>&1 | Out-Null
            $auditOk = ($LASTEXITCODE -eq 0)
            $auditDetail = if ($auditOk) { "Sin vulnerabilidades" } else { "Vulnerabilidades detectadas - revisar requirements.txt" }
            Add-Result "pip-audit ${labelRaw}" $auditOk $auditDetail
            Write-Status $auditOk "pip-audit ${labelRaw}"
        } else {
            Add-Result "pip-audit ${labelRaw}" $false "requirements.txt no encontrado: $reqFile"
            Write-Status $false "pip-audit ${labelRaw}: requirements.txt no encontrado"
        }
    }
}

Write-Host ""

# -----------------------------------------------------------------------
# 6. Tags git
# -----------------------------------------------------------------------
Write-Host "-- 6. Tags de version --"
try {
    $tags = git -C $root tag 2>&1
    $hasRc1 = $tags -contains "v1.0-rc1"
    $tagDetail = if ($hasRc1) { "Presente" } else { "Tag no encontrado - ejecutar: git tag -f v1.0-rc1" }
    Add-Result "Tag v1.0-rc1 existe" $hasRc1 $tagDetail
    Write-Status $hasRc1 "Tag v1.0-rc1 presente"
    Write-Host "  Tags existentes: $($tags -join ', ')"
} catch {
    Add-Result "Tags git" $false $_.Exception.Message
    Write-Status $false "git tag: error"
}

Write-Host ""

# -----------------------------------------------------------------------
# Resumen final
# -----------------------------------------------------------------------
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  RESUMEN SMOKE TEST" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

$passed = ($results | Where-Object { $_.OK }).Count
$failed = ($results | Where-Object { -not $_.OK }).Count

foreach ($r in $results) {
    $icon  = if ($r.OK) { "[OK]  " } else { "[FAIL]" }
    $color = if ($r.OK) { "Green" } else { "Red" }
    Write-Host "  $icon $($r.Nombre)" -ForegroundColor $color
    if (-not $r.OK) {
        Write-Host "         --> $($r.Detalle)" -ForegroundColor Yellow
    }
}

Write-Host ""
$resultColor = if ($globalOk) { "Green" } else { "Red" }
Write-Host "  Resultado: $passed OK / $failed FAIL" -ForegroundColor $resultColor
Write-Host ""

if ($globalOk) {
    Write-Host "  SMOKE TEST PASADO -- listo para crear/actualizar el tag." -ForegroundColor Green
} else {
    Write-Host "  SMOKE TEST FALLADO -- corregir los errores antes de taggear." -ForegroundColor Red
}

Write-Host ""

# Codigo de salida: 0 si todo OK, 1 si hay fallos
if (-not $globalOk) { exit 1 }
exit 0
