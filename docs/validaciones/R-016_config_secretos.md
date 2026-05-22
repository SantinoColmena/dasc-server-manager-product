# Validación R-016 - Protección de config.env y secretos

## Objetivo

Evitar que el repositorio incluya secretos reales y mejorar el instalador para generar y proteger el archivo `config.env` real durante la instalación.

## Estado inicial

Antes de esta tarea, el instalador del API esperaba encontrar un archivo `config.env` dentro del paquete de instalación.

Esto no era ideal para una versión producto, porque podía provocar que se subieran secretos reales al repositorio o que el paquete dependiera de credenciales concretas del laboratorio.

## Cambios realizados

- El paquete del API usa `config.env.example` como plantilla.
- El instalador ya no exige que exista `config.env` dentro del paquete.
- El instalador crea `config.env` a partir de `config.env.example` si no existe.
- Si ya existe un `config.env`, se conserva para no romper reinstalaciones.
- Se genera automáticamente una `SECRET_KEY` segura si falta o si tiene valor de ejemplo.
- Se pide la contraseña del administrador durante la instalación si falta o si tiene valor de ejemplo.
- La contraseña del administrador se guarda como hash bcrypt.
- Se aplican permisos restrictivos al archivo real `config.env`.
- El archivo real `config.env` queda ignorado por Git.
- Se importan los instaladores reales del API, base de datos y servidor de backups/servicios al repositorio producto.

## Archivos modificados o añadidos

- `deploy/api/install_dasc_api.sh`
- `deploy/api/uninstall_dasc_api.sh`
- `deploy/db/install_db.sh`
- `deploy/db/uninstall_db.sh`
- `deploy/backup-services/install_backup_services.sh`
- `deploy/backup-services/uninstall_backup_services.sh`
- `deploy/api/package/config.env.example`
- `.gitignore`

## Criterio de seguridad

El repositorio debe contener solamente:

    config.env.example

No debe contener:

    config.env

Tampoco deben subirse datos locales generados por ejecución del panel, como:

    alerts.db
    auth_logs.json
    users.json

## Validación estática realizada

Se comprueba mediante `git status` que no aparecen secretos reales para commit.

Estado esperado:

- Puede aparecer `config.env.example`.
- No debe aparecer `config.env`.
- No debe aparecer `data/users.json`.
- No debe aparecer `data/alerts.db`.
- No debe aparecer `data/auth_logs.json`.

## Pruebas pendientes en VM Ubuntu

| Prueba | Estado |
|---|---|
| Comprobar que `config.env` está ignorado por Git | Correcto a nivel local |
| Comprobar que el instalador no exige `config.env` en el paquete | Pendiente |
| Comprobar generación automática de `SECRET_KEY` | Pendiente |
| Comprobar petición de `ADMIN_PASSWORD` | Pendiente |
| Comprobar que `ADMIN_PASSWORD` queda como hash bcrypt | Pendiente |
| Comprobar permisos `640` sobre `/opt/dasc/api/config.env` | Pendiente |
| Comprobar que el servicio `dasc-api` arranca con systemd | Pendiente |
| Validación completa en VM Ubuntu | Pendiente |

## Estado de cierre

R-016 queda implementado a nivel de script y pendiente de validación en VM Ubuntu.

La validación real se realizará cuando se pruebe el instalador en la máquina del panel/API.
