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

function Test-IsExampleFile {
    param(
        [string]$RelativePath
    )

    return (
        $RelativePath -like "*.example" -or
        $RelativePath -like "*.env.example" -or
        $RelativePath -like "*\config.env.example" -or
        $RelativePath -like "config\perfiles\*.example"
    )
}

function Test-IsDocumentationFile {
    param(
        [string]$RelativePath
    )

    return (
        $RelativePath -like "docs\*" -and
        $RelativePath -notlike "docs\auditoria\*"
    )
}

function Test-IsCodeExpectedFile {
    param(
        [string]$RelativePath
    )

    return (
        $RelativePath -like "*.py" -or
        $RelativePath -like "*.sh" -or
        $RelativePath -like "*.ps1"
    )
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

$gitStatusRaw = git status --short
$gitStatusFiltered = @()

foreach ($line in $gitStatusRaw) {
    if ($line -notmatch "docs/auditoria/repo_clean_check.md" -and $line -notmatch "docs\\auditoria\\repo_clean_check.md") {
        $gitStatusFiltered += $line
    }
}

if ($gitStatusFiltered.Count -eq 0) {
    Add-ReportLine "- OK: el repositorio está limpio o solo está pendiente el propio informe de auditoría."
} else {
    Add-ReportLine "- AVISO: hay cambios pendientes."
    Add-ReportLine ""
    Add-ReportLine "~~~text"
    foreach ($line in $gitStatusFiltered) {
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
        Add-ReportLine "- ERROR: encontrado archivo sensible o runtime ``$relative``."
    }
}

if (-not $dangerFound) {
    Add-ReportLine "- OK: no se han encontrado archivos sensibles típicos."
}

Add-ReportLine ""
Add-ReportLine "## 5. Variables sensibles por categoría"
Add-ReportLine ""

$exampleFindings = New-Object System.Collections.Generic.List[string]
$codeFindings = New-Object System.Collections.Generic.List[string]
$docFindings = New-Object System.Collections.Generic.List[string]
$riskFindings = New-Object System.Collections.Generic.List[string]

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
            $entry = "$relative -> contiene patrón ``$pattern``"

            if (Test-IsExampleFile -RelativePath $relative) {
                $exampleFindings.Add($entry) | Out-Null
            } elseif (Test-IsDocumentationFile -RelativePath $relative) {
                $docFindings.Add($entry) | Out-Null
            } elseif (Test-IsCodeExpectedFile -RelativePath $relative) {
                $codeFindings.Add($entry) | Out-Null
            } else {
                $riskFindings.Add($entry) | Out-Null
            }
        }
    }
}

Add-ReportLine "### 5.1 Ejemplos permitidos"
Add-ReportLine ""

if ($exampleFindings.Count -eq 0) {
    Add-ReportLine "- OK: no se han detectado variables sensibles en archivos de ejemplo."
} else {
    Add-ReportLine "- OK: variables sensibles detectadas en archivos `.example`. Deben mantenerse como valores ficticios."
    Add-ReportLine ""

    foreach ($finding in $exampleFindings) {
        Add-ReportLine "  - $finding"
    }
}

Add-ReportLine ""
Add-ReportLine "### 5.2 Código o instaladores"
Add-ReportLine ""

if ($codeFindings.Count -eq 0) {
    Add-ReportLine "- OK: no se han detectado patrones sensibles en código o instaladores."
} else {
    Add-ReportLine "- REVISAR: hay variables sensibles en código o instaladores. Es aceptable si se generan, se leen del entorno o se usan como nombre de variable, no como secreto real."
    Add-ReportLine ""

    foreach ($finding in $codeFindings) {
        Add-ReportLine "  - $finding"
    }
}

Add-ReportLine ""
Add-ReportLine "### 5.3 Documentación"
Add-ReportLine ""

if ($docFindings.Count -eq 0) {
    Add-ReportLine "- OK: no se han detectado patrones sensibles en documentación."
} else {
    Add-ReportLine "- REVISAR: hay variables sensibles mencionadas en documentación. Deben ser ejemplos o referencias, nunca secretos reales."
    Add-ReportLine ""

    foreach ($finding in $docFindings) {
        Add-ReportLine "  - $finding"
    }
}

Add-ReportLine ""
Add-ReportLine "### 5.4 Riesgo real"
Add-ReportLine ""

if ($riskFindings.Count -eq 0) {
    Add-ReportLine "- OK: no se han encontrado patrones sensibles en archivos inesperados."
} else {
    Add-ReportLine "- ERROR: se han encontrado patrones sensibles en archivos que no parecen ejemplo, documentación ni código esperado."
    Add-ReportLine ""

    foreach ($finding in $riskFindings) {
        Add-ReportLine "  - $finding"
    }
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

if ($dangerFound -or $riskFindings.Count -gt 0) {
    Add-ReportLine "Resultado: REVISAR ANTES DE AVANZAR."
    Add-ReportLine ""
    Add-ReportLine "Hay posibles archivos sensibles o secretos en ubicaciones inesperadas."
} else {
    Add-ReportLine "Resultado: OK PARA SEGUIR CON LIMPIEZA Y PULIDO."
    Add-ReportLine ""
    Add-ReportLine "No se han encontrado archivos sensibles típicos ni secretos en ubicaciones inesperadas."
}

Add-ReportLine ""
Add-ReportLine "Acciones recomendadas:"
Add-ReportLine ""
Add-ReportLine "- Mantener clientes y ventas en curso hasta completar limpieza funcional."
Add-ReportLine "- Revisar manualmente los avisos de código, instaladores y documentación."
Add-ReportLine "- Confirmar que los `.example` solo contienen valores ficticios."
Add-ReportLine "- Repetir esta auditoría antes de cada release nueva."

$lines | Set-Content -Encoding UTF8 $reportPath

Write-Host "Auditoría generada en: $reportPath"
