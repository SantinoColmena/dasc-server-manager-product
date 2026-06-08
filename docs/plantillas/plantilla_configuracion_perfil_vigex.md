# Plantilla de configuración por perfil Vigex

## Uso

Copiar esta plantilla y rellenarla antes de ejecutar instaladores.

No guardar secretos reales en GitHub.

## Datos generales

VIGEX_PROFILE=
CLIENT_NAME=
CLIENT_ID=
ENVIRONMENT=lab|pilot|production

## Red

API_HOST=
API_PUBLIC_URL=
LOCAL_PANEL_PORT=8000
NGINX_PUBLIC_PORT=80
SERVER_NAME=_

DB_HOST=
BACKUPS_HOST=
SERVICIOS_HOST=
LOGS_DB_HOST=

## Perfil Lite

Usar si VIGEX_PROFILE=lite:

API_HOST=127.0.0.1
DB_HOST=127.0.0.1
BACKUPS_HOST=127.0.0.1
SERVICIOS_HOST=127.0.0.1
LOGS_DB_HOST=127.0.0.1

## Perfil Standard

Usar si VIGEX_PROFILE=standard:

API_HOST=
DB_HOST=
BACKUPS_HOST=
SERVICIOS_HOST=
LOGS_DB_HOST=

Normalmente:

DB_HOST=BACKUPS_HOST=SERVICIOS_HOST=LOGS_DB_HOST

## Perfil Pro

Usar si VIGEX_PROFILE=pro:

API_HOST=
DB_HOST=
BACKUPS_HOST=
SERVICIOS_HOST=
LOGS_DB_HOST=

Normalmente:

DB_HOST != BACKUPS_HOST

## DB

DB_BIND_ADDRESS=0.0.0.0
DB_NAME=employees
DB_SERVER_ID=

BACKUP_ALLOWED_HOST=
LOGS_ALLOWED_HOST=

BACKUP_USER=vigex_backup
BACKUP_PASS=NO_GUARDAR_EN_GIT

RESTORE_USER=vigex_restore
RESTORE_PASS=NO_GUARDAR_EN_GIT

LOGS_DB_NAME=vigex_logs
LOGS_DB_USER=vigex_logs
LOGS_DB_PASS=NO_GUARDAR_EN_GIT

## Backup-services

BACKUP_DIR=/home/vigex/backups
DB_BACKUP_USER=vigex_backup
DB_BACKUP_PASS=NO_GUARDAR_EN_GIT
DB_RESTORE_USER=vigex_restore
DB_RESTORE_PASS=NO_GUARDAR_EN_GIT

## API / panel local

BACKUPS_HOST=
SERVICIOS_HOST=
LOGS_DB_HOST=
TERMINAL_DATABASE_HOST=

VIGEX_LOCAL_INTERNAL_SUPPORT_ENABLED=false

CENTRAL_SUPPORT_ENABLED=true
CENTRAL_SUPPORT_URL=
CENTRAL_SUPPORT_CLIENT_ID=
CENTRAL_SUPPORT_CLIENT_NAME=
CENTRAL_SUPPORT_TOKEN=NO_GUARDAR_EN_GIT

## Central Vigex

Vigex_CENTRAL_AUTH_ENABLED=true
Vigex_CENTRAL_LAB_MODE=false
Vigex_CENTRAL_ADMIN_USER=
Vigex_CENTRAL_ADMIN_PASSWORD=NO_GUARDAR_EN_GIT
Vigex_CENTRAL_TECH_USER=
Vigex_CENTRAL_TECH_PASSWORD=NO_GUARDAR_EN_GIT
Vigex_CENTRAL_SECRET_KEY=NO_GUARDAR_EN_GIT

## Checklist previo

- [ ] IPs reales confirmadas.
- [ ] Hostnames confirmados.
- [ ] Puertos confirmados.
- [ ] Firewall revisado.
- [ ] DNS local definido si aplica.
- [ ] Contraseñas generadas fuera del repo.
- [ ] Tokens generados fuera del repo.
- [ ] Perfil elegido.
- [ ] Responsable técnico confirmado.
- [ ] Ventana de instalación acordada.

## Checklist posterior

- [ ] vigex-api activo.
- [ ] nginx activo.
- [ ] panel local accesible.
- [ ] DB accesible desde backups.
- [ ] logs accesibles desde API.
- [ ] SSH con clave validado.
- [ ] backup completo validado.
- [ ] restauración de prueba validada.
- [ ] soporte central probado si aplica.
- [ ] documentación de cliente entregada.
