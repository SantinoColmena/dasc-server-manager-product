# R-030 - Corrección de codificación del asistente de perfiles

## Problema detectado

Durante la validación del script `scripts/generar_config_perfil.sh` en el servidor API / Panel Ubuntu, se detectó el siguiente aviso al ejecutar el script:

~~~text
scripts/generar_config_perfil.sh: línea 1: ﻿#!/usr/bin/env: No existe el archivo o el directorio
~~~

## Causa

El archivo `.sh` había sido generado desde PowerShell con codificación UTF-8 con BOM.

En Linux, ese carácter invisible al inicio del archivo puede provocar que el shebang `#!/usr/bin/env bash` no sea interpretado correctamente.

## Impacto

El script llegó a generar correctamente el archivo de configuración porque fue ejecutado con:

~~~bash
bash scripts/generar_config_perfil.sh distributed
~~~

Aun así, el problema debía corregirse para dejar el script limpio y portable.

## Corrección aplicada

Se reescribió el archivo `scripts/generar_config_perfil.sh` en UTF-8 sin BOM.

También se añadió un archivo `.gitattributes` para forzar finales de línea LF en scripts Bash y evitar problemas de compatibilidad entre Windows y Linux.

## Archivo añadido

~~~text
.gitattributes
~~~

Contenido principal:

~~~text
*.sh text eol=lf
*.md text eol=lf
*.env.example text eol=lf
~~~

## Servidores afectados

| Servidor | Acción |
|---|---|
| API / Panel - 192.168.60.10 | Se volverá a probar el script después de hacer `git pull` |
| DB / Logs - 192.168.60.20 | No requiere cambios |
| Backups / Servicios - 192.168.60.30 | No requiere cambios |

## Conclusión

La validación funcional de R-030 fue correcta, pero se detectó y corrigió un problema de portabilidad entre Windows y Linux.

R-030 queda más robusta para futuras ejecuciones en Ubuntu.
