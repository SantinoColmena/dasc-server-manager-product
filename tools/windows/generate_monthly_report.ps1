param(
    [string]$RepoRoot = ".",
    [string]$Cliente = "DASC interno",
    [string]$Periodo = "",
    [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"

$resolvedRoot = Resolve-Path -LiteralPath $RepoRoot
$root = $resolvedRoot.Path
Set-Location -LiteralPath $root

if ([string]::IsNullOrWhiteSpace($Periodo)) {
    $Periodo = Get-Date -Format "yyyy-MM"
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $safePeriodo = $Periodo -replace "[^0-9A-Za-z_-]", "_"
    $OutputPath = "docs\informes\informe_mensual_v1_$safePeriodo.md"
}

$outDir = Split-Path $OutputPath -Parent
if (-not [string]::IsNullOrWhiteSpace($outDir)) {
    New-Item -ItemType Directory -Force $outDir | Out-Null
}

$fecha = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Add-Line {
    param(
        [System.Collections.Generic.List[string]]$Lines,
        [string]$Text = ""
    )
    $Lines.Add($Text) | Out-Null
}

function Run-GitCommand {
    param(
        [string[]]$GitArgs
    )

    try {
        $result = & git @GitArgs 2>$null
        if ($LASTEXITCODE -ne 0) {
            return @("No disponible")
        }
        return $result
    } catch {
        return @("No disponible")
    }
}

$lines = New-Object System.Collections.Generic.List[string]

$commit = (Run-GitCommand -GitArgs @("rev-parse", "--short", "HEAD")) -join " "
$branch = (Run-GitCommand -GitArgs @("branch", "--show-current")) -join " "
$tag = (Run-GitCommand -GitArgs @("describe", "--tags", "--always")) -join " "
$lastCommits = Run-GitCommand -GitArgs @("log", "--oneline", "-8")
$gitStatusRaw = Run-GitCommand -GitArgs @("status", "--short")

if ($gitStatusRaw.Count -eq 1 -and $gitStatusRaw[0] -eq "No disponible") {
    $gitStatusRaw = @()
}

$normalizedOutputPathA = $OutputPath.Replace("\", "/")
$normalizedOutputPathB = $OutputPath.Replace("/", "\")

$gitStatusFiltered = @()
foreach ($line in $gitStatusRaw) {
    if ($line -notmatch [regex]::Escape($normalizedOutputPathA) -and
        $line -notmatch [regex]::Escape($normalizedOutputPathB)) {
        $gitStatusFiltered += $line
    }
}

$auditPath = "docs\auditoria\repo_clean_check.md"
$auditExists = Test-Path -LiteralPath $auditPath
$auditResult = "No disponible"

if ($auditExists) {
    $auditContent = Get-Content -LiteralPath $auditPath -Raw

    if ($auditContent -match "Resultado: OK PARA SEGUIR") {
        $auditResult = "OK para seguir con limpieza y pulido"
    } elseif ($auditContent -match "ERROR:") {
        $auditResult = "Revisar errores de auditoría"
    } elseif ($auditContent -match "OK: no se han encontrado archivos sensibles típicos") {
        $auditResult = "OK parcial: sin archivos sensibles típicos"
    } else {
        $auditResult = "Revisión manual recomendada"
    }
}

Add-Line $lines "# Informe mensual v1 - DASC Server Manager"
Add-Line $lines ""
Add-Line $lines "## 1. Datos generales"
Add-Line $lines ""
Add-Line $lines "| Campo | Valor |"
Add-Line $lines "|---|---|"
Add-Line $lines "| Cliente / entorno | $Cliente |"
Add-Line $lines "| Periodo | $Periodo |"
Add-Line $lines "| Fecha de generación | $fecha |"
Add-Line $lines "| Rama | $branch |"
Add-Line $lines "| Commit | $commit |"
Add-Line $lines "| Versión / tag detectado | $tag |"
Add-Line $lines ""

Add-Line $lines "## 2. Resumen ejecutivo"
Add-Line $lines ""
Add-Line $lines "Este informe corresponde a la primera versión automática de informes mensuales de DASC Server Manager."
Add-Line $lines ""
Add-Line $lines "En esta fase el informe se usa como herramienta interna de producto, no como informe comercial definitivo para clientes."
Add-Line $lines ""
Add-Line $lines "Objetivos de esta versión:"
Add-Line $lines ""
Add-Line $lines "- Comprobar el estado del repositorio."
Add-Line $lines "- Registrar la versión o commit analizado."
Add-Line $lines "- Revisar el resultado de la auditoría clean."
Add-Line $lines "- Dejar una base reutilizable para futuros informes de cliente."
Add-Line $lines ""

Add-Line $lines "## 3. Estado del repositorio"
Add-Line $lines ""

if ($gitStatusFiltered.Count -eq 0) {
    Add-Line $lines "- OK: el repositorio está limpio o solo está pendiente este informe generado."
} else {
    Add-Line $lines "- AVISO: hay cambios pendientes."
    Add-Line $lines ""
    Add-Line $lines "~~~text"
    foreach ($line in $gitStatusFiltered) {
        Add-Line $lines $line
    }
    Add-Line $lines "~~~"
}

Add-Line $lines ""
Add-Line $lines "## 4. Últimos commits"
Add-Line $lines ""
Add-Line $lines "~~~text"
foreach ($line in $lastCommits) {
    Add-Line $lines $line
}
Add-Line $lines "~~~"
Add-Line $lines ""

Add-Line $lines "## 5. Auditoría clean"
Add-Line $lines ""
Add-Line $lines "| Elemento | Estado |"
Add-Line $lines "|---|---|"
Add-Line $lines "| Informe de auditoría encontrado | $auditExists |"
Add-Line $lines "| Resultado interpretado | $auditResult |"
Add-Line $lines ""

if ($auditExists) {
    Add-Line $lines "Archivo revisado:"
    Add-Line $lines ""
    Add-Line $lines "~~~text"
    Add-Line $lines $auditPath
    Add-Line $lines "~~~"
} else {
    Add-Line $lines "No existe todavía un informe de auditoría clean. Se recomienda ejecutar:"
    Add-Line $lines ""
    Add-Line $lines "~~~powershell"
    Add-Line $lines "powershell -ExecutionPolicy Bypass -File .\tools\windows\check_repo_clean.ps1"
    Add-Line $lines "~~~"
}

Add-Line $lines ""
Add-Line $lines "## 6. Estado funcional del informe v1"
Add-Line $lines ""
Add-Line $lines "Esta versión del informe todavía no conecta con servidores reales ni consulta directamente backups, restauraciones o alertas."
Add-Line $lines ""
Add-Line $lines "Pendiente para futuras versiones:"
Add-Line $lines ""
Add-Line $lines "- Leer estado real de backups."
Add-Line $lines "- Incluir última restauración de prueba."
Add-Line $lines "- Incluir alertas enviadas."
Add-Line $lines "- Incluir incidencias internas cerradas."
Add-Line $lines "- Generar resumen para cliente no técnico."
Add-Line $lines "- Exportar a PDF o enviar por email."
Add-Line $lines ""

Add-Line $lines "## 7. Conclusión"
Add-Line $lines ""

if ($gitStatusFiltered.Count -eq 0 -and $auditResult -match "OK") {
    Add-Line $lines "El entorno revisado está en buen estado para continuar con limpieza y pulido del producto."
} else {
    Add-Line $lines "El entorno requiere revisión antes de considerarse listo para pasos comerciales."
}

Add-Line $lines ""
Add-Line $lines "Este informe no debe presentarse todavía como informe final de cliente. Es una primera base automática para evolucionar R-050."

$lines | Set-Content -Encoding UTF8 $OutputPath

Write-Host "Informe generado en: $OutputPath"
