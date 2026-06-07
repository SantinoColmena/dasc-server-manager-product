param(
    [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path -LiteralPath $RepoRoot).Path
Set-Location -LiteralPath $root

$reportDir = Join-Path $root "docs\validaciones"
New-Item -ItemType Directory -Force $reportDir | Out-Null

$reportPath = Join-Path $reportDir "validacion_paquete_api_instalable.md"

$packageDir = Join-Path $root "deploy\api\package"
$installer = Join-Path $root "deploy\api\install_dasc_api.sh"

$checks = New-Object System.Collections.Generic.List[object]

function Add-Check {
    param(
        [string]$Name,
        [bool]$Ok,
        [string]$Detail
    )

    $checks.Add([PSCustomObject]@{
        Name = $Name
        Ok = $Ok
        Detail = $Detail
    }) | Out-Null
}

function Test-LFOnly {
    param(
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return $false
    }

    $bytes = [System.IO.File]::ReadAllBytes($Path)

    for ($i = 0; $i -lt $bytes.Length - 1; $i++) {
        if ($bytes[$i] -eq 13 -and $bytes[$i + 1] -eq 10) {
            return $false
        }
    }

    return $true
}

Add-Check "Existe paquete API" (Test-Path -LiteralPath $packageDir) "Ruta esperada: deploy/api/package"
Add-Check "Existe instalador API" (Test-Path -LiteralPath $installer) "Ruta esperada: deploy/api/install_dasc_api.sh"

Add-Check "No existe config.env real en paquete" (-not (Test-Path -LiteralPath (Join-Path $packageDir "config.env"))) "El paquete no debe incluir secretos reales."
Add-Check "Existe config.env.example en paquete" (Test-Path -LiteralPath (Join-Path $packageDir "config.env.example")) "El instalador debe crear config.env a partir de este ejemplo."

$configExamplePath = Join-Path $packageDir "config.env.example"
$configExampleContent = ""
if (Test-Path -LiteralPath $configExamplePath) {
    $configExampleContent = Get-Content -LiteralPath $configExamplePath -Raw
}

Add-Check "config.env.example incluye BACKUP_DB_HOST" ($configExampleContent -match "BACKUP_DB_HOST") "Debe permitir configurar host de backup."
Add-Check "config.env.example incluye BACKUP_DB_USER" ($configExampleContent -match "BACKUP_DB_USER") "Debe permitir configurar usuario de backup."
Add-Check "config.env.example incluye BACKUP_DB_PASS" ($configExampleContent -match "BACKUP_DB_PASS") "Debe permitir configurar password de backup."
Add-Check "config.env.example incluye BACKUP_OUTPUT_DIR" ($configExampleContent -match "BACKUP_OUTPUT_DIR") "Debe permitir configurar salida de backups."
Add-Check "config.env.example incluye BACKUP_RETENTION_KEEP" ($configExampleContent -match "BACKUP_RETENTION_KEEP") "Debe permitir configurar retención de backups."
Add-Check "config.env.example incluye RESTORE_DB_HOST" ($configExampleContent -match "RESTORE_DB_HOST") "Debe permitir configurar host de restauración."
Add-Check "config.env.example incluye RESTORE_DB_USER" ($configExampleContent -match "RESTORE_DB_USER") "Debe permitir configurar usuario de restauración."
Add-Check "config.env.example incluye RESTORE_DB_PASS" ($configExampleContent -match "RESTORE_DB_PASS") "Debe permitir configurar contraseña de restauración."
Add-Check "config.env.example incluye RESTORE_TARGET_DB" ($configExampleContent -match "RESTORE_TARGET_DB") "Debe definir base destino de restauración controlada."

Add-Check "Existe main.py" (Test-Path -LiteralPath (Join-Path $packageDir "main.py")) "Archivo principal del API."
Add-Check "Existe requirements.txt" (Test-Path -LiteralPath (Join-Path $packageDir "requirements.txt")) "Dependencias del API."
Add-Check "Existe carpeta templates" (Test-Path -LiteralPath (Join-Path $packageDir "templates")) "Plantillas web."
Add-Check "Existe carpeta static" (Test-Path -LiteralPath (Join-Path $packageDir "static")) "Archivos estáticos."

Add-Check "Existe generador Python de informe operativo" (Test-Path -LiteralPath (Join-Path $packageDir "tools\generate_operational_report.py")) "Herramienta de producto dentro del paquete."

$operationalReportPath = Join-Path $packageDir "tools\generate_operational_report.py"
$operationalReportContent = ""
if (Test-Path -LiteralPath $operationalReportPath) {
    $operationalReportContent = Get-Content -LiteralPath $operationalReportPath -Raw
}

Add-Check "Informe operativo inspecciona backups" ($operationalReportContent -match "inspect_backups") "Debe consultar metadata de backups."
Add-Check "Informe operativo lee BACKUP_OUTPUT_DIR" ($operationalReportContent -match "BACKUP_OUTPUT_DIR") "Debe usar directorio configurable de backups."
Add-Check "Informe operativo muestra sección Backups completos" ($operationalReportContent -match "Backups completos") "Debe incluir sección de backups en informe."
Add-Check "Existe wrapper Bash de informe operativo" (Test-Path -LiteralPath (Join-Path $packageDir "tools\generate_operational_report.sh")) "Wrapper para servidor Linux."
Add-Check "Existe validador post-instalación API" (Test-Path -LiteralPath (Join-Path $packageDir "tools\check_api_installation.sh")) "Validador para Ubuntu instalado."
Add-Check "Existe generador Python de backup completo" (Test-Path -LiteralPath (Join-Path $packageDir "tools\run_full_db_backup.py")) "Herramienta de backup completo dentro del paquete."
Add-Check "Existe wrapper Bash de backup completo" (Test-Path -LiteralPath (Join-Path $packageDir "tools\run_full_db_backup.sh")) "Wrapper para backup completo en servidor Linux."
Add-Check "Existe herramienta Python de limpieza de backups" (Test-Path -LiteralPath (Join-Path $packageDir "tools\cleanup_db_backups.py")) "Herramienta de retención dentro del paquete."
Add-Check "Existe wrapper Bash de limpieza de backups" (Test-Path -LiteralPath (Join-Path $packageDir "tools\cleanup_db_backups.sh")) "Wrapper para limpieza de backups en Linux."
Add-Check "Existe herramienta Python de restauración controlada" (Test-Path -LiteralPath (Join-Path $packageDir "tools\restore_db_backup.py")) "Herramienta de restauración segura dentro del paquete."
Add-Check "Existe wrapper Bash de restauración controlada" (Test-Path -LiteralPath (Join-Path $packageDir "tools\restore_db_backup.sh")) "Wrapper para restauración controlada en Linux."
Add-Check "Existe reports/.gitkeep" (Test-Path -LiteralPath (Join-Path $packageDir "reports\.gitkeep")) "Mantiene la carpeta reports sin versionar informes generados."

$generatedReports = Get-ChildItem -LiteralPath (Join-Path $packageDir "reports") -Filter "*.md" -File -ErrorAction SilentlyContinue
Add-Check "No hay informes runtime versionables en reports" ($generatedReports.Count -eq 0) "Los informes generados deben ignorarse y no subirse."

$installerContent = ""
if (Test-Path -LiteralPath $installer) {
    $installerContent = Get-Content -LiteralPath $installer -Raw
}

Add-Check "Instalador requiere config.env.example" ($installerContent -match "config\.env\.example") "El instalador no debe depender de config.env real en el repo."
Add-Check "Instalador crea config.env si falta" ($installerContent -match "cp.*config\.env\.example.*config\.env") "Debe crear config.env en la instalación real."
Add-Check "Instalador prepara data" ($installerContent -match 'mkdir -p "\$INSTALL_DIR/data"') "Debe crear directorio runtime data."
Add-Check "Instalador prepara reports" ($installerContent -match 'mkdir -p "\$INSTALL_DIR/reports"') "Debe crear directorio runtime reports."
Add-Check "Instalador prepara tools" ($installerContent -match 'mkdir -p "\$INSTALL_DIR/tools"') "Debe crear directorio tools."
Add-Check "Instalador da permisos al wrapper" ($installerContent -match "generate_operational_report\.sh") "Debe dar permisos de ejecución al wrapper."
Add-Check "Instalador da permisos al validador post-instalación" ($installerContent -match "check_api_installation\.sh") "Debe dar permisos de ejecución al validador."
Add-Check "Instalador da permisos al backup completo" ($installerContent -match "run_full_db_backup\.sh") "Debe dar permisos de ejecución al backup completo."
Add-Check "Instalador da permisos a limpieza de backups" ($installerContent -match "cleanup_db_backups\.sh") "Debe dar permisos de ejecución a la limpieza de backups."
Add-Check "Instalador da permisos a restauración controlada" ($installerContent -match "restore_db_backup\.sh") "Debe dar permisos de ejecución a la restauración controlada."
Add-Check "Instalador verifica cliente MariaDB" ($installerContent -match "Verificando cliente MariaDB para backups") "Debe asegurar mysqldump o mariadb-dump para backups."
Add-Check "Instalador tiene mensaje SSH remoto no bloqueante" ($installerContent -match 'echo "SSH remoto: modo no bloqueante\. Validacion completa en puerta posterior\."') "Debe mostrar un mensaje final correcto sobre SSH no bloqueante."
Add-Check "Instalador mensaje SSH remoto bien cerrado" ($installerContent -notmatch '(?m)^\s*echo "SSH remoto:[^"]*$') "Evita líneas echo con comillas sin cerrar."

Add-Check "install_dasc_api.sh usa LF" (Test-LFOnly $installer) "Los scripts Linux deben tener LF."
Add-Check "generate_operational_report.sh usa LF" (Test-LFOnly (Join-Path $packageDir "tools\generate_operational_report.sh")) "Los scripts Linux deben tener LF."
Add-Check "check_api_installation.sh usa LF" (Test-LFOnly (Join-Path $packageDir "tools\check_api_installation.sh")) "Los scripts Linux deben tener LF."
Add-Check "run_full_db_backup.sh usa LF" (Test-LFOnly (Join-Path $packageDir "tools\run_full_db_backup.sh")) "Los scripts Linux deben tener LF."
Add-Check "cleanup_db_backups.sh usa LF" (Test-LFOnly (Join-Path $packageDir "tools\cleanup_db_backups.sh")) "Los scripts Linux deben tener LF."
Add-Check "restore_db_backup.sh usa LF" (Test-LFOnly (Join-Path $packageDir "tools\restore_db_backup.sh")) "Los scripts Linux deben tener LF."

$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$total = $checks.Count
$okCount = ($checks | Where-Object { $_.Ok }).Count
$failCount = $total - $okCount

$lines = New-Object System.Collections.Generic.List[string]

function Add-Line {
    param([string]$Text = "")
    $lines.Add($Text) | Out-Null
}

Add-Line "# Validación automática del paquete API instalable"
Add-Line ""
Add-Line "Fecha: $now"
Add-Line ""
Add-Line "## Resumen"
Add-Line ""
Add-Line "| Campo | Valor |"
Add-Line "|---|---|"
Add-Line "| Total comprobaciones | $total |"
Add-Line "| Correctas | $okCount |"
Add-Line "| Fallidas | $failCount |"
Add-Line ""

Add-Line "## Resultado"
Add-Line ""

if ($failCount -eq 0) {
    Add-Line "Resultado: OK."
    Add-Line ""
    Add-Line "El paquete API cumple las comprobaciones mínimas para seguir avanzando hacia instalación real."
} else {
    Add-Line "Resultado: REVISAR."
    Add-Line ""
    Add-Line "Hay comprobaciones fallidas que deben corregirse antes de considerar el paquete preparado."
}

Add-Line ""
Add-Line "## Comprobaciones"
Add-Line ""
Add-Line "| Estado | Comprobación | Detalle |"
Add-Line "|---|---|---|"

foreach ($check in $checks) {
    $status = if ($check.Ok) { "OK" } else { "FALTA" }
    $safeDetail = $check.Detail.Replace("|", "/")
    Add-Line "| $status | $($check.Name) | $safeDetail |"
}

Add-Line ""
Add-Line "## Conclusión"
Add-Line ""

if ($failCount -eq 0) {
    Add-Line "El paquete API está preparado a nivel estructural para una prueba de instalación real en Ubuntu."
} else {
    Add-Line "El paquete API todavía requiere correcciones antes de probar instalación real."
}

$lines | Set-Content -Encoding UTF8 $reportPath

Write-Host "Validación generada en: $reportPath"

if ($failCount -gt 0) {
    exit 1
}
