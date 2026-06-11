; Vigex Windows Installer — R-099
; Empaqueta VigexSetup.ps1 + config.env.example en un EXE de instalacion estandar.
;
; Compilar desde la raiz del repo:
;   "C:\Program Files (x86)\NSIS\makensis.exe" deploy\docker\vigex.nsi
; El EXE resultante se genera en deploy\docker\VigexSetup.exe

!define APPNAME       "Vigex"
!define APPVERSION    "1.0"
!define PUBLISHER     "Vigex"
!define PANEL_PORT    "8000"
!define UNINST_KEY    "Software\Microsoft\Windows\CurrentVersion\Uninstall\Vigex"

!include "MUI2.nsh"
!include "LogicLib.nsh"

; ── Metadatos del instalador ───────────────────────────────────────────────────
Name         "${APPNAME} ${APPVERSION}"
OutFile      "VigexSetup.exe"
InstallDir   "$PROGRAMFILES\Vigex"    ; sobrescrito en .onInit con $PROGRAMDATA
InstallDirRegKey HKLM "${UNINST_KEY}" "InstallLocation"
RequestExecutionLevel admin
Unicode true
SetCompressor /SOLID lzma

VIProductVersion  "1.0.0.0"
VIFileVersion     "1.0.0.0"
VIAddVersionKey   "ProductName"      "${APPNAME}"
VIAddVersionKey   "ProductVersion"   "${APPVERSION}"
VIAddVersionKey   "FileVersion"      "${APPVERSION}"
VIAddVersionKey   "CompanyName"      "${PUBLISHER}"
VIAddVersionKey   "FileDescription"  "Instalador de Vigex para Windows"
VIAddVersionKey   "LegalCopyright"   "(c) 2026 Vigex"

; ── Iconos y apariencia MUI2 ──────────────────────────────────────────────────
!define MUI_ICON   "..\..\web\favicon.ico"
!define MUI_UNICON "..\..\web\favicon.ico"

!define MUI_WELCOMEPAGE_TITLE "Bienvenido al instalador de Vigex"
!define MUI_WELCOMEPAGE_TEXT \
  "Este asistente instalara Vigex en tu equipo.$\r$\n$\r$\n\
  Vigex es un panel de gestion de servidores pensado para pymes.$\r$\n\
  Se ejecuta en Docker, de forma totalmente invisible.$\r$\n$\r$\n\
  La primera instalacion puede tardar varios minutos si Docker$\r$\n\
  Desktop no esta instalado (se descargara automaticamente).$\r$\n$\r$\n\
  Requisitos minimos:$\r$\n\
    - Windows 10 v1903+ / Windows Server 2019+$\r$\n\
    - 4 GB de RAM$\r$\n\
    - 8 GB de espacio libre en disco"

!define MUI_FINISHPAGE_TITLE "Vigex instalado correctamente"
!define MUI_FINISHPAGE_TEXT "El panel Vigex esta listo.$\r$\n$\r$\nAcceso:   http://localhost:${PANEL_PORT}$\r$\n$\r$\nAntes de usarlo, edita tu configuracion en:$\r$\nC:\ProgramData\Vigex\config.env$\r$\n$\r$\nTras editar config.env, reinicia el contenedor:$\r$\n  docker restart vigex-panel"
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_TEXT     "Abrir Vigex en el navegador"
!define MUI_FINISHPAGE_RUN_FUNCTION OpenBrowser

; ── Paginas del instalador ────────────────────────────────────────────────────
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Spanish"

; ── onInit: fijar directorio de instalacion en ProgramData ──────────────────
; InstallDir no evalua $PROGRAMDATA en compile-time; lo forzamos aqui.
Function .onInit
    ; Respetar ruta previa si ya fue instalado
    ReadRegStr $0 HKLM "${UNINST_KEY}" "InstallLocation"
    ${If} $0 != ""
        StrCpy $INSTDIR $0
    ${Else}
        ; Leer %PROGRAMDATA% del entorno (evita warning de NSIS con $PROGRAMDATA literal)
        ReadEnvStr $1 "PROGRAMDATA"
        StrCpy $INSTDIR "$1\Vigex"
    ${EndIf}
FunctionEnd

; ── Seccion principal de instalacion ─────────────────────────────────────────
Section "Vigex" SecMain
    SetOutPath "$INSTDIR"

    ; --- Extraer archivos bundleados ---
    DetailPrint "Copiando archivos de Vigex..."
    File "VigexSetup.ps1"
    File "vigex-update.bat"

    ; config.env: crear solo si no existe (preserva configuracion previa en actualizaciones)
    IfFileExists "$INSTDIR\config.env" config_ok config_crear
    config_crear:
        File /oname=config.env "config.env.example"
        DetailPrint "config.env creado. Editalo con tus valores antes de usar el panel."
        Goto config_listo
    config_ok:
        DetailPrint "config.env existente conservado (no sobreescrito)."
    config_listo:

    ; --- Lanzar VigexSetup.ps1 en una ventana de PowerShell visible ---
    ; (el usuario ve el progreso: descarga Docker, arranca contenedor, etc.)
    DetailPrint ""
    DetailPrint "Iniciando instalacion de Vigex..."
    DetailPrint "Se abrira una ventana de progreso. No la cierres hasta que termine."
    DetailPrint ""
    ExecWait 'powershell.exe -NoProfile -ExecutionPolicy Bypass \
              -File "$INSTDIR\VigexSetup.ps1" -Unattended' $0

    IntCmp $0 0 install_ok install_error install_error
    install_error:
        MessageBox MB_ICONSTOP \
            "La instalacion de Vigex encontro un error (codigo $0).$\r$\n$\r$\n\
            Revisa el log de instalacion en:$\r$\n$INSTDIR\install.log"
        Abort
    install_ok:

    ; --- Registrar en Agregar/Quitar programas ---
    WriteUninstaller "$INSTDIR\uninstall.exe"
    WriteRegStr   HKLM "${UNINST_KEY}" "DisplayName"     "${APPNAME}"
    WriteRegStr   HKLM "${UNINST_KEY}" "DisplayVersion"  "${APPVERSION}"
    WriteRegStr   HKLM "${UNINST_KEY}" "Publisher"       "${PUBLISHER}"
    WriteRegStr   HKLM "${UNINST_KEY}" "UninstallString" '"$INSTDIR\uninstall.exe"'
    WriteRegStr   HKLM "${UNINST_KEY}" "InstallLocation" "$INSTDIR"
    WriteRegStr   HKLM "${UNINST_KEY}" "DisplayIcon"     '"$INSTDIR\uninstall.exe"'
    WriteRegDWORD HKLM "${UNINST_KEY}" "NoModify"        1
    WriteRegDWORD HKLM "${UNINST_KEY}" "NoRepair"        1

    ; --- Accesos directos en el Menu Inicio ---
    CreateDirectory "$SMPROGRAMS\Vigex"
    CreateShortCut "$SMPROGRAMS\Vigex\Panel Vigex.lnk"       "http://localhost:${PANEL_PORT}"
    CreateShortCut "$SMPROGRAMS\Vigex\Actualizar Vigex.lnk"  "$INSTDIR\vigex-update.bat"
    CreateShortCut "$SMPROGRAMS\Vigex\Desinstalar Vigex.lnk" "$INSTDIR\uninstall.exe"

    DetailPrint ""
    DetailPrint "Vigex instalado correctamente en $INSTDIR"
SectionEnd

; ── Funcion: abrir navegador al finalizar ────────────────────────────────────
Function OpenBrowser
    ExecShell "open" "http://localhost:${PANEL_PORT}"
FunctionEnd

; ── Seccion de desinstalacion ─────────────────────────────────────────────────
Section "Uninstall"
    ; Delegar la logica de desinstalacion al script PS (para Docker/tareas)
    ExecWait 'powershell.exe -NoProfile -ExecutionPolicy Bypass \
              -File "$INSTDIR\VigexSetup.ps1" -Uninstall -Unattended'

    ; Accesos directos
    Delete "$SMPROGRAMS\Vigex\Panel Vigex.lnk"
    Delete "$SMPROGRAMS\Vigex\Actualizar Vigex.lnk"
    Delete "$SMPROGRAMS\Vigex\Desinstalar Vigex.lnk"
    RMDir  "$SMPROGRAMS\Vigex"

    ; Archivos del instalador (no se eliminan datos del usuario: config.env, data/, reports/)
    Delete "$INSTDIR\VigexSetup.ps1"
    Delete "$INSTDIR\vigex-update.bat"
    Delete "$INSTDIR\install.log"
    Delete "$INSTDIR\uninstall.exe"
    ; Intentar eliminar el directorio solo si queda vacio
    RMDir  "$INSTDIR"

    ; Entrada de registro
    DeleteRegKey HKLM "${UNINST_KEY}"
SectionEnd
