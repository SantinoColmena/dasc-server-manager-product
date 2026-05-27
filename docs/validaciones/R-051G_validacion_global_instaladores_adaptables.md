# R-051G - Validación global de instaladores adaptables

## Objetivo

Validar globalmente los instaladores adaptados durante R-051 antes de cerrar la tarea completa.

## Estado

Cerrada.

## Contexto

Durante R-051 se adaptaron los instaladores para reducir dependencias de laboratorio y preparar DASC Server Manager para perfiles reales:

- Lite.
- Standard.
- Pro.
- Custom.
- Central DASC.

## Instaladores validados

Se validó la sintaxis Bash de:

- deploy/api/install_dasc_api.sh
- deploy/api/install_nginx_dasc_api.sh
- deploy/api/install_central_retry_timer.sh
- deploy/db/install_db.sh
- deploy/backup-services/install_backup_services.sh
- deploy/central-support/install_central_support.sh
- deploy/central-support/install_nginx_central_support.sh

Resultado:

- OK: sintaxis Bash válida en instaladores principales.

## Bloques R-051 validados

Se confirmó la presencia de:

- R-051D - PERFIL DE DESPLIEGUE API/PANEL LOCAL.
- R-051E - PERFIL Y SECRETOS DB.
- R-051F - PERFIL Y SECRETOS BACKUP-SERVICES.

## Perfiles detectados

Se confirmó la presencia de lógica DASC_PROFILE_VALUE en:

- instalador API/panel local.
- instalador DB.
- instalador backup-services.

## Seguridad de defaults

Se validó que no quedan defaults débiles activos en DB:

- BACKUP_PASS.
- RESTORE_PASS.
- LOGS_DB_PASS.

Se validó que no quedan defaults débiles activos en backup-services:

- DB_BACKUP_PASS.
- DB_RESTORE_PASS.

Los valores antiguos:

- dasc_backup_2026
- dasc_restore_2026
- dasc_logs_2026

solo permanecen como placeholders rechazados dentro de funciones de validación.

## Problema detectado durante R-051G

Durante la validación global se detectaron IPs fijas de laboratorio en:

- deploy/api/package/main.py

Valores detectados:

- 192.168.60.30
- 192.168.60.20

## Corrección aplicada

Se aplicó el fix:

- R-051G-FIX1 - Eliminar IPs fijas de laboratorio en defaults API.

Commit funcional:

- 3c4905c fix: eliminar ips laboratorio defaults api

Los defaults quedaron cambiados a:

- BACKUPS_HOST -> 127.0.0.1
- SERVICIOS_HOST -> 127.0.0.1
- LOGS_DB_HOST -> 127.0.0.1

## Validación posterior al fix

Se validó:

- No quedan IPs fijas 192.168.60.20, 192.168.60.30 ni 192.168.1.250 dentro de deploy.
- main.py conserva sintaxis Python válida.
- Los instaladores principales conservan sintaxis Bash válida.
- El entorno activo no se rompe.

## Servicios validados

En lab-pruebas se comprobó que siguen activos:

- dasc-api.
- nginx.
- dasc-central-support.
- dasc-central-retry.timer.

## Accesos validados

Se validó:

- Panel local directo 8000.
- Panel local por Nginx 8080.
- Panel central por Nginx 80.
- Central health 8010.

## Resultado

R-051G queda validada correctamente.

Los instaladores principales quedan coherentes con los perfiles reales y sin defaults críticos de laboratorio dentro de deploy.

## Próximo paso

Continuar con:

- R-051H - Cierre global de R-051.
