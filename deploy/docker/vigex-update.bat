@echo off
:: Vigex — Actualizar panel (R-099)
:: Ejecutar con clic derecho > "Ejecutar como administrador"

echo.
echo  =============================================
echo   Vigex Update — actualizando panel...
echo  =============================================
echo.

:: Verificar privilegios de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo  [!] Este script necesita permisos de Administrador.
    echo      Haz clic derecho y selecciona "Ejecutar como administrador".
    pause
    exit /b 1
)

:: Ejecutar el actualizador via PowerShell
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0VigexSetup.ps1" -Update

if %errorLevel% equ 0 (
    echo.
    echo  [OK] Actualizacion completada. Panel en http://localhost:8000
) else (
    echo.
    echo  [!] La actualizacion encontro un error. Revisa el log en:
    echo      %ProgramData%\Vigex\install.log
)

echo.
pause
