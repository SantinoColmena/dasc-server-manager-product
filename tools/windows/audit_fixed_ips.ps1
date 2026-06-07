param(
    [string]$Root = ".",
    [string]$Output = "docs\auditoria\auditoria_ips_perfiles.md"
)

$ErrorActionPreference = "Stop"

$rootPath = (Resolve-Path $Root).Path
$outputPath = Join-Path $rootPath $Output
$outputFullPath = [System.IO.Path]::GetFullPath($outputPath)

$excludedDirs = @(
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "node_modules",
    "reports",
    "data"
)

$allowedExtensions = @(
    ".sh",
    ".py",
    ".ps1",
    ".md",
    ".yml",
    ".yaml",
    ".env",
    ".example",
    ".txt",
    ".json",
    ".html",
    ".css"
)

$ipRegex = '\b(?:10|127|172|192)\.(?:\d{1,3}\.){2}\d{1,3}\b'

function Test-IsExcludedPath {
    param([string]$Path)

    foreach ($dir in $excludedDirs) {
        if ($Path -match [regex]::Escape("\$dir\")) {
            return $true
        }
    }

    return $false
}

function Get-RelativePathCompat {
    param(
        [string]$BasePath,
        [string]$TargetPath
    )

    $baseFull = [System.IO.Path]::GetFullPath($BasePath)
    $targetFull = [System.IO.Path]::GetFullPath($TargetPath)

    if (-not $baseFull.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $baseFull = $baseFull + [System.IO.Path]::DirectorySeparatorChar
    }

    $baseUri = New-Object System.Uri($baseFull)
    $targetUri = New-Object System.Uri($targetFull)

    $relativeUri = $baseUri.MakeRelativeUri($targetUri)

    return [System.Uri]::UnescapeDataString($relativeUri.ToString()).Replace("/", "\")
}
function Get-Zone {
    param([string]$RelativePath)

    $normalized = $RelativePath.Replace("\", "/")

    if ($normalized -match "^docs/") {
        return "documentacion"
    }

    if ($normalized -match "^deploy/.*/package/config\.env\.example$") {
        return "ejemplo_configuracion"
    }

    if ($normalized -match "^deploy/.*/install_.*\.sh$") {
        return "instalador"
    }

    if ($normalized -match "^deploy/.*/package/tools/") {
        return "herramienta_producto"
    }

    if ($normalized -match "^tools/") {
        return "herramienta_interna"
    }

    if ($normalized -match "config\.env$") {
        return "config_real"
    }

    return "codigo_o_recurso"
}

function Get-Severity {
    param(
        [string]$Zone,
        [string]$RelativePath,
        [string]$Line
    )

    if ($Zone -eq "config_real") {
        return "ALTA"
    }

    if ($Zone -eq "instalador") {
        return "ALTA"
    }

    if ($Zone -eq "herramienta_producto") {
        return "MEDIA"
    }

    if ($Zone -eq "ejemplo_configuracion") {
        return "BAJA"
    }

    if ($Zone -eq "documentacion") {
        return "INFO"
    }

    return "MEDIA"
}

$files = Get-ChildItem -Path $rootPath -Recurse -File | Where-Object {
    -not (Test-IsExcludedPath $_.FullName) -and
    ([System.IO.Path]::GetFullPath($_.FullName) -ne $outputFullPath) -and
    (
        $allowedExtensions -contains $_.Extension -or
        $_.Name -like "*.env.example" -or
        $_.Name -like "*.example"
    )
}

$findings = New-Object System.Collections.Generic.List[object]

foreach ($file in $files) {
    $relative = Get-RelativePathCompat -BasePath $rootPath -TargetPath $file.FullName

    try {
        $lines = Get-Content -LiteralPath $file.FullName -Encoding UTF8
    } catch {
        continue
    }

    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]

        $matches = [regex]::Matches($line, $ipRegex)

        foreach ($match in $matches) {
            $zone = Get-Zone -RelativePath $relative
            $severity = Get-Severity -Zone $zone -RelativePath $relative -Line $line

            $findings.Add([pscustomobject]@{
                Severity = $severity
                Zone = $zone
                IP = $match.Value
                File = $relative
                LineNumber = $i + 1
                Line = $line.Trim()
            })
        }
    }
}

$ordered = $findings | Sort-Object Severity, Zone, File, LineNumber

$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$md = New-Object System.Collections.Generic.List[string]

$md.Add("# Auditoría de IPs fijas y perfiles")
$md.Add("")
$md.Add("Fecha: $now")
$md.Add("")
$md.Add("## Objetivo")
$md.Add("")
$md.Add("Detectar referencias a IPs fijas dentro del repositorio para preparar instaladores adaptables por perfil e IPs reales.")
$md.Add("")
$md.Add("## Resumen")
$md.Add("")
$md.Add("| Campo | Valor |")
$md.Add("|---|---|")
$md.Add("| Total referencias IP detectadas | $($findings.Count) |")
$md.Add("| Severidad ALTA | $(($findings | Where-Object Severity -eq 'ALTA').Count) |")
$md.Add("| Severidad MEDIA | $(($findings | Where-Object Severity -eq 'MEDIA').Count) |")
$md.Add("| Severidad BAJA | $(($findings | Where-Object Severity -eq 'BAJA').Count) |")
$md.Add("| Severidad INFO | $(($findings | Where-Object Severity -eq 'INFO').Count) |")
$md.Add("")
$md.Add("## Criterio de severidad")
$md.Add("")
$md.Add("| Severidad | Significado |")
$md.Add("|---|---|")
$md.Add("| ALTA | IP fija en instalador o configuración real. Debe revisarse antes de usar en cliente real. |")
$md.Add("| MEDIA | IP fija en herramienta de producto o código/recurso. Debe parametrizarse si afecta a ejecución. |")
$md.Add("| BAJA | IP en ejemplo de configuración. Puede mantenerse temporalmente si está claro que es ejemplo. |")
$md.Add("| INFO | IP en documentación o validaciones. No bloquea, pero debe quedar contextualizada. |")
$md.Add("")
$md.Add("## Hallazgos")
$md.Add("")

if ($findings.Count -eq 0) {
    $md.Add("No se han detectado IPs fijas.")
} else {
    $md.Add("| Severidad | Zona | IP | Archivo | Línea | Contenido |")
    $md.Add("|---|---|---|---|---:|---|")

    foreach ($item in $ordered) {
        $lineSafe = $item.Line.Replace("|", "/")
        $fileSafe = $item.File.Replace("|", "/")
        $md.Add(('| {0} | {1} | {2} | `{3}` | {4} | `{5}` |' -f $item.Severity, $item.Zone, $item.IP, $fileSafe, $item.LineNumber, $lineSafe))
    }
}

$md.Add("")
$md.Add("## Interpretación inicial")
$md.Add("")
$md.Add("Esta auditoría no corrige automáticamente las IPs.")
$md.Add("")
$md.Add("Sirve para decidir qué referencias deben transformarse en variables de instalación y cuáles pueden quedarse como documentación de laboratorio.")
$md.Add("")
$md.Add("## Próximo paso")
$md.Add("")
$md.Add("Clasificar los hallazgos en:")
$md.Add("")
$md.Add("- A mantener como evidencia histórica o documentación.")
$md.Add("- A convertir en valores de `config.env.example`.")
$md.Add("- A preguntar desde instaladores.")
$md.Add("- A derivar según perfil Lite, PyME 2 servidores o Pro 3 servidores.")
$md.Add("")
$md.Add("## Resultado")
$md.Add("")
if (($findings | Where-Object Severity -eq "ALTA").Count -gt 0) {
    $md.Add("Resultado: REVISAR. Hay IPs fijas de severidad ALTA.")
} else {
    $md.Add("Resultado: OK inicial. No se han detectado IPs fijas de severidad ALTA.")
}

$mdText = ($md -join "`n") + "`n"

$outputDir = Split-Path $outputPath -Parent
New-Item -ItemType Directory -Force $outputDir | Out-Null

[System.IO.File]::WriteAllText($outputPath, $mdText, [System.Text.UTF8Encoding]::new($false))

Write-Host "Auditoría generada en: $outputPath"
Write-Host "Total referencias IP detectadas: $($findings.Count)"
Write-Host "ALTA: $(($findings | Where-Object Severity -eq 'ALTA').Count)"
Write-Host "MEDIA: $(($findings | Where-Object Severity -eq 'MEDIA').Count)"
Write-Host "BAJA: $(($findings | Where-Object Severity -eq 'BAJA').Count)"
Write-Host "INFO: $(($findings | Where-Object Severity -eq 'INFO').Count)"
