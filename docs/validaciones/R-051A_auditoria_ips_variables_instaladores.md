# R-051A - Auditoría de IPs, variables y valores de laboratorio en instaladores

## Objetivo

Auditar los instaladores actuales de DASC Server Manager para identificar dependencias de IPs fijas, variables configurables, valores de laboratorio y puntos que deben adaptarse a perfiles reales.

## Estado

Cerrada.

## Instaladores revisados

Se revisaron los instaladores principales dentro de deploy:

- deploy/api/install_dasc_api.sh
- deploy/api/install_nginx_dasc_api.sh
- deploy/api/install_central_retry_timer.sh
- deploy/api/uninstall_dasc_api.sh
- deploy/api/uninstall_nginx_dasc_api.sh
- deploy/backup-services/install_backup_services.sh
- deploy/backup-services/uninstall_backup_services.sh
- deploy/central-support/install_central_support.sh
- deploy/central-support/install_nginx_central_support.sh
- deploy/central-support/uninstall_central_support.sh
- deploy/central-support/uninstall_nginx_central_support.sh
- deploy/db/install_db.sh
- deploy/db/uninstall_db.sh
- deploy/proxy/install_reverse_proxy.sh
- deploy/proxy/uninstall_reverse_proxy.sh

## Resultado sobre IPs fijas

No se detectaron IPs fijas de laboratorio tipo:

- 192.168.60.20
- 192.168.60.30
- 192.168.1.250

dentro de deploy.

Sí aparecen referencias a:

- 127.0.0.1
- localhost

Estas referencias son correctas en varios casos, porque representan backends internos o pruebas locales de servicio.

Ejemplos aceptables:

- Nginx local reenviando a 127.0.0.1:8000.
- Nginx central reenviando a 127.0.0.1:8010.
- Comprobaciones curl contra 127.0.0.1.
- DASC_ALLOWED_HOSTS incluyendo 127.0.0.1 y localhost.

## Resultado sobre variables configurables

Se confirma que varios instaladores ya admiten configuración externa por variables de entorno.

### API / panel local

El instalador API ya trabaja con:

- BACKUPS_HOST
- SERVICIOS_HOST
- LOGS_DB_HOST
- TERMINAL_DATABASE_HOST
- DASC_SSH_ALLOWED_HOSTS
- DASC_SSH_KEY
- DASC_SSH_KNOWN_HOSTS
- DASC_SSH_TIMEOUT
- DASC_SSH_CONNECT_TIMEOUT

También genera SECRET_KEY automáticamente y guarda ADMIN_PASSWORD como hash bcrypt si necesita cambiarse.

### Nginx panel local

El instalador Nginx local acepta:

- SERVICE_NAME
- NGINX_SITE_NAME
- APP_HOST
- APP_PORT
- PUBLIC_PORT
- SERVER_NAME

### DB

El instalador DB acepta:

- DB_BIND_ADDRESS
- DB_NAME
- BACKUP_USER
- BACKUP_PASS
- BACKUP_ALLOWED_HOST
- RESTORE_USER
- RESTORE_PASS
- LOGS_DB_NAME
- LOGS_DB_USER
- LOGS_DB_PASS
- LOGS_ALLOWED_HOST
- DB_SERVER_ID

Además solicita de forma obligatoria:

- BACKUP_ALLOWED_HOST
- LOGS_ALLOWED_HOST

si no se proporcionan.

### Backup-services

El instalador de backups acepta:

- DB_HOST
- DB_NAME
- DB_BACKUP_USER
- DB_BACKUP_PASS
- DB_RESTORE_USER
- DB_RESTORE_PASS
- BACKUP_DIR

Además solicita de forma obligatoria:

- DB_HOST

si no se proporciona.

### Central Support

El instalador central acepta:

- INSTALL_DIR
- APP_HOST
- APP_PORT
- DASC_CENTRAL_ADMIN_USER
- DASC_CENTRAL_ADMIN_PASSWORD
- DASC_CENTRAL_TECH_USER
- DASC_CENTRAL_TECH_PASSWORD
- DASC_CENTRAL_DEMO_TOKEN

También genera claves, contraseñas y token si no se pasan desde el entorno.

## Valores de laboratorio o demo detectados

Se detectan valores que no son necesariamente inseguros por sí solos, pero deben clasificarse como laboratorio/demo o convertirse en variables de perfil.

### Central support

- DASC_CENTRAL_DEMO_CLIENT_ID=cliente-demo-a
- DASC_CENTRAL_DEMO_CLIENT_NAME=Cliente Demo A

Estos valores son útiles para laboratorio, pero deben evolucionar a cliente real configurable.

### DB

- TEST_TABLE=empleados_demo
- DB_SERVER_ID=20

La tabla demo puede mantenerse como muestra inicial si se documenta.
DB_SERVER_ID debe configurarse por perfil si hay replicación o escenarios avanzados.

### Passwords por defecto en DB/backups

En DB:

- BACKUP_PASS=dasc_backup_2026
- RESTORE_PASS=dasc_restore_2026
- LOGS_DB_PASS=dasc_logs_2026

En backup-services:

- DB_BACKUP_PASS=dasc_backup_2026
- DB_RESTORE_PASS=dasc_restore_2026

Estos valores deben reemplazarse por generación automática, solicitud interactiva o lectura desde fichero/variables de despliegue.

### SSH bootstrap

En DB y backup-services se fuerza temporalmente:

- PasswordAuthentication yes
- PubkeyAuthentication yes

Esto ayuda al primer despliegue, pero debe tratarse como bootstrap inicial.
A futuro debe existir una opción para endurecer SSH tras copiar claves.

### Proxy antiguo/alternativo

Existe deploy/proxy/install_reverse_proxy.sh con certificado autofirmado de laboratorio.

Debe revisarse si sigue siendo necesario o si queda sustituido por:

- deploy/api/install_nginx_dasc_api.sh
- deploy/central-support/install_nginx_central_support.sh

## Riesgos detectados

| Riesgo | Impacto | Acción recomendada |
|---|---:|---|
| Passwords DB por defecto | Alto | Generar o solicitar passwords |
| Cliente demo fijo central | Medio | Parametrizar cliente inicial |
| SSH PasswordAuthentication yes | Medio | Documentar bootstrap y endurecimiento futuro |
| Proxy antiguo con certificado lab | Bajo/Medio | Marcar como legado o adaptar |
| API depende de config.env previo | Medio | Crear plantilla por perfil |
| DB_SERVER_ID fijo | Bajo/Medio | Parametrizar por perfil |

## Conclusión

R-051A queda cerrada.

La auditoría confirma que el proyecto ya ha avanzado bastante: no hay IPs 192.168.x.x fijas en deploy y muchos instaladores son parametrizables.

La siguiente mejora debe centrarse en:

- Documentar perfiles reales.
- Crear plantilla de configuración por perfil.
- Eliminar passwords por defecto en DB/backups.
- Parametrizar cliente central inicial.
- Mejorar instaladores sin romper laboratorio.
