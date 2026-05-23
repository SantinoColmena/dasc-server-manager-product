param(
    [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"

$resolvedRoot = Resolve-Path -LiteralPath $RepoRoot
$root = $resolvedRoot.Path

Set-Location -LiteralPath $root

$reportDir = Join-Path $root "docs\auditoria"
New-Item -ItemType Directory -Force $reportDir | Out-Null

$reportPath = Join-Path $reportDir "repo_clean_check.md"
$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$lines = New-Object System.Collections.Generic.List[string]

function Add-ReportLine {
    param(
        [string]$Text = ""
    )
    $script:lines.Add($Text) | Out-Null
}

function Get-RelativePath {
    param(
        [string]$FullPath
    )

    if ($FullPath.StartsWith($root)) {
        return $FullPath.Substring($root.Length).TrimStart("\", "/")
    }

    return $FullPath
}

$requiredPaths = @(
    "README.md",
    ".gitignore",
    "deploy",
    "docs",
    "scripts"
)

$recommendedPaths = @(
    "LICENSE",
    "config.env.example",
    "tools",
    "docs\validaciones",
    "docs\producto"
)

$dangerousFiles = @(
    "config.env",
    ".env",
    "id_rsa",
    "id_ed25519",
    "known_hosts",
    "users.json",
    "alerts.db"
)

$secretPatterns = @(
    "TELEGRAM_BOT_TOKEN=",
    "TELEGRAM_CHAT_ID=",
    "ADMIN_PASSWORD=",
    "LOGS_DB_PASS=",
    "DB_BACKUP_PASS=",
    "MYSQL_ROOT_PASSWORD=",
    "SECRET_KEY="
)

Add-ReportLine "# Auditoría Clean del repositorio DASC"
Add-ReportLine ""
Add-ReportLine "Fecha: $now"
Add-ReportLine ""
Add-ReportLine "Ruta revisada:"
Add-ReportLine ""
Add-ReportLine "~~~text"
Add-ReportLine $root
Add-ReportLine "~~~"
Add-ReportLine ""

Add-ReportLine "## 1. Estado Git"
Add-ReportLine ""

$gitStatus = git status --short

if ([string]::IsNullOrWhiteSpace($gitStatus)) {
    Add-ReportLine "- OK: el repositorio está limpio."
} else {
    Add-ReportLine "- AVISO: hay cambios pendientes."
    Add-ReportLine ""
    Add-ReportLine "~~~text"
    foreach ($line in $gitStatus) {
        Add-ReportLine $line
    }
    Add-ReportLine "~~~"
}

Add-ReportLine ""
Add-ReportLine "## 2. Estructura mínima obligatoria"
Add-ReportLine ""

foreach ($path in $requiredPaths) {
    if (Test-Path -LiteralPath $path) {
        Add-ReportLine "- OK: existe ``$path``."
    } else {
        Add-ReportLine "- FALTA: no existe ``$path``."
    }
}

Add-ReportLine ""
Add-ReportLine "## 3. Estructura recomendada"
Add-ReportLine ""

foreach ($path in $recommendedPaths) {
    if (Test-Path -LiteralPath $path) {
        Add-ReportLine "- OK: existe ``$path``."
    } else {
        Add-ReportLine "- REVISAR: no existe ``$path``."
    }
}

Add-ReportLine ""
Add-ReportLine "## 4. Archivos sensibles no recomendados"
Add-ReportLine ""

$dangerFound = $false

$allFiles = Get-ChildItem -Path $root -Recurse -Force -File -ErrorAction SilentlyContinue |
    Where-Object {
        $_.FullName -notmatch "\\.git\\"
    }

foreach ($name in $dangerousFiles) {
    $matches = $allFiles | Where-Object { $_.Name -eq $name }

    foreach ($match in $matches) {
        $dangerFound = $true
        $relative = Get-RelativePath -FullPath $match.FullName
        Add-ReportLine "- REVISAR: encontrado ``$relative``."
    }
}

if (-not $dangerFound) {
    Add-ReportLine "- OK: no se han encontrado archivos sensibles típicos."
}

Add-ReportLine ""
Add-ReportLine "## 5. Búsqueda básica de posibles secretos"
Add-ReportLine ""

$secretFindings = New-Object System.Collections.Generic.List[string]

$extensionsToScan = @(
    ".md",
    ".txt",
    ".env",
    ".example",
    ".sh",
    ".py",
    ".yml",
    ".yaml",
    ".json",
    ".ps1"
)

$filesToScan = $allFiles |
    Where-Object {
        $relative = Get-RelativePath -FullPath $_.FullName

        $_.Extension -in $extensionsToScan -and
        $relative -ne "tools\windows\check_repo_clean.ps1" -and
        $relative -notlike "docs\auditoria\*"
    }

foreach ($file in $filesToScan) {
    $relative = Get-RelativePath -FullPath $file.FullName

    foreach ($pattern in $secretPatterns) {
        $matches = Select-String -LiteralPath $file.FullName -SimpleMatch -Pattern $pattern -ErrorAction SilentlyContinue

        if ($matches) {
            $secretFindings.Add("$relative -> contiene patrón ``$pattern``") | Out-Null
        }
    }
}

if ($secretFindings.Count -eq 0) {
    Add-ReportLine "- OK: no se han encontrado patrones sensibles básicos."
} else {
    Add-ReportLine "- REVISAR: se han encontrado patrones que pueden ser ejemplos o secretos reales."
    Add-ReportLine ""

    foreach ($finding in $secretFindings) {
        Add-ReportLine "  - $finding"
    }

    Add-ReportLine ""
    Add-ReportLine "Nota: si son valores de ejemplo, deben quedar claramente marcados como ejemplo."
}

Add-ReportLine ""
Add-ReportLine "## 6. README"
Add-ReportLine ""

if (Test-Path -LiteralPath "README.md") {
    $readme = Get-Content -LiteralPath "README.md" -Raw

    if ($readme -match "Fase 6|v1\.0-rc1|MVP académico|base de producto") {
        Add-ReportLine "- OK: README contiene referencias al estado actual del producto."
    } else {
        Add-ReportLine "- REVISAR: README no parece reflejar claramente el estado actual."
    }

    if ($readme -match "producción crítica|validación adicional|no debe utilizarse") {
        Add-ReportLine "- OK: README incluye aviso de límites."
    } else {
        Add-ReportLine "- REVISAR: README debería incluir límites de uso antes de producción."
    }
} else {
    Add-ReportLine "- FALTA: README.md no existe."
}

Add-ReportLine ""
Add-ReportLine "## 7. Instaladores"
Add-ReportLine ""

$installerCandidates = @(
    "deploy\api\install_dasc_api.sh",
    "deploy\db\install_db.sh",
    "deploy\backup-services\install_backup_services.sh",
    "scripts\install_dasc_api.sh",
    "scripts\install_db.sh",
    "scripts\install_backup_services.sh"
)

$foundInstallers = 0

foreach ($installer in $installerCandidates) {
    if (Test-Path -LiteralPath $installer) {
        $foundInstallers++
        Add-ReportLine "- OK: existe ``$installer``."
    }
}

if ($foundInstallers -eq 0) {
    Add-ReportLine "- REVISAR: no se han encontrado instaladores en rutas esperadas."
}

Add-ReportLine ""
Add-ReportLine "## 8. Resultado provisional"
Add-ReportLine ""

Add-ReportLine "Esta auditoría no sustituye una validación manual, pero sirve como primera comprobación real antes de avanzar hacia clientes."
Add-ReportLine ""
Add-ReportLine "Acciones recomendadas:"
Add-ReportLine ""
Add-ReportLine "- Revisar cualquier línea marcada como REVISAR."
Add-ReportLine "- Confirmar que los valores sensibles son ejemplos."
Add-ReportLine "- Mantener clientes y ventas en curso hasta que el producto esté limpio."
Add-ReportLine "- Repetir esta auditoría antes de crear una release nueva."

$lines | Set-Content -Encoding UTF8 $reportPath

Write-Host "Auditoría generada en: $reportPath"
