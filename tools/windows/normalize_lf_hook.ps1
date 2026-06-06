# DASC - Hook PostToolUse para Claude Code
# Normaliza finales de linea CRLF -> LF en archivos .sh y .py tras editarlos.
# Motivo: .gitattributes obliga a LF en *.sh/*.py y
# tools/windows/check_api_package_installable.ps1 falla si un script bash tiene CRLF.
#
# Recibe por stdin el JSON del evento del hook (campo tool_input.file_path).
# No bloquea nunca: ante cualquier duda sale con codigo 0.

$ErrorActionPreference = "SilentlyContinue"

$raw = [Console]::In.ReadToEnd()
if (-not $raw) { exit 0 }

try {
    $payload = $raw | ConvertFrom-Json
} catch {
    exit 0
}

$path = $payload.tool_input.file_path
if (-not $path) { exit 0 }
if ($path -notmatch '\.(sh|py)$') { exit 0 }
if (-not (Test-Path -LiteralPath $path)) { exit 0 }

$bytes = [System.IO.File]::ReadAllBytes($path)

$hasCRLF = $false
for ($i = 0; $i -lt $bytes.Length - 1; $i++) {
    if ($bytes[$i] -eq 13 -and $bytes[$i + 1] -eq 10) {
        $hasCRLF = $true
        break
    }
}

if (-not $hasCRLF) { exit 0 }

$text = [System.IO.File]::ReadAllText($path)
$text = $text -replace "`r`n", "`n"

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($path, $text, $utf8NoBom)

$name = Split-Path -Leaf $path
$result = @{
    systemMessage = "DASC: finales de linea normalizados a LF en $name (requerido por .gitattributes)."
} | ConvertTo-Json -Compress

[Console]::Out.Write($result)
exit 0
