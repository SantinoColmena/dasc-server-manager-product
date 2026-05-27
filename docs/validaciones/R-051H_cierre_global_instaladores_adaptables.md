# R-051H - Cierre global instaladores adaptables a IPs y perfiles reales

## Objetivo

Cerrar globalmente la tarea R-051, dedicada a preparar los instaladores de DASC Server Manager para IPs, hosts, perfiles y secretos reales.

## Estado

Cerrada.

## Contexto

R-051 se creó para corregir una limitación importante del proyecto: evitar que los instaladores y paquetes de despliegue dependieran de IPs fijas de laboratorio, contraseñas débiles por defecto o configuraciones pensadas solo para el entorno de pruebas.

El objetivo era preparar el producto para escenarios reales como:

- Lite.
- Standard.
- Pro.
- Custom.
- Central DASC.

## Subtareas realizadas

### R-051A - Auditoría de IPs, variables y valores de laboratorio

Se auditó el contenido de `deploy` para detectar:

- IPs fijas.
- Variables HOST/IP/PORT.
- Valores demo/lab.
- Passwords por defecto.
- Configuraciones heredadas.

Resultado:

- No había muchas IPs fijas en instaladores.
- Sí se detectaron defaults de laboratorio en el código API.
- Sí existían contraseñas por defecto en DB y backup-services.
- Se confirmó que varios instaladores ya estaban parcialmente parametrizados.

### R-051B - Documento de perfiles de despliegue

Se creó:

- docs/producto/perfiles_despliegue_dasc.md

Se documentaron los perfiles:

- Lite.
- Standard.
- Pro.
- Central DASC.

Decisión de producto:

- Standard queda como perfil recomendado para PyME.
- Lite queda como opción de entrada con copia externa obligatoria.
- Pro queda como opción avanzada.
- Central DASC no se instala en clientes.

### R-051C - Plantilla de configuración por perfil

Se creó:

- docs/plantillas/plantilla_configuracion_perfil_dasc.md

La plantilla incluye:

- Datos generales.
- Red.
- Variables Lite.
- Variables Standard.
- Variables Pro.
- Variables DB.
- Variables backup-services.
- Variables API/panel local.
- Variables Central DASC.
- Checklist previo.
- Checklist posterior.

### R-051D - Adaptar instalador API/panel local

Se modificó:

- deploy/api/install_dasc_api.sh

Se añadió soporte para:

- DASC_PROFILE=lite
- DASC_PROFILE=standard
- DASC_PROFILE=pro
- DASC_PROFILE=custom

También se añadió resolución de variables como:

- BACKUPS_HOST
- SERVICIOS_HOST
- LOGS_DB_HOST
- TERMINAL_DATABASE_HOST
- CENTRAL_SUPPORT_ENABLED
- CENTRAL_SUPPORT_URL
- CENTRAL_SUPPORT_CLIENT_ID
- CENTRAL_SUPPORT_CLIENT_NAME
- CENTRAL_SUPPORT_TOKEN
- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED
- CLIENT_ID
- CLIENT_NAME

Decisión de seguridad:

- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED=false como valor limpio para cliente.

### R-051E - Adaptar instalador DB

Se modificó:

- deploy/db/install_db.sh

Se eliminaron como defaults activos:

- BACKUP_PASS=dasc_backup_2026
- RESTORE_PASS=dasc_restore_2026
- LOGS_DB_PASS=dasc_logs_2026

Ahora, si no se proporcionan, se generan automáticamente mediante:

- secrets.token_urlsafe(32)

También se añadió soporte para perfiles y DB_SERVER_ID por perfil:

- lite -> 10
- standard -> 20
- pro -> 30
- custom -> 20

Se añadió fichero local de secretos:

- /root/dasc-db-install-secrets.env

con permisos esperados:

- root:root
- 600

### R-051F - Adaptar instalador backup-services

Se modificó:

- deploy/backup-services/install_backup_services.sh

Se eliminaron como defaults activos:

- DB_BACKUP_PASS=dasc_backup_2026
- DB_RESTORE_PASS=dasc_restore_2026

Decisión técnica:

Backup-services no genera contraseñas aleatorias automáticamente porque deben coincidir con las credenciales creadas en la DB.

Orden de resolución aplicado:

1. Cargar DB_SECRETS_FILE si existe.
2. Usar variables de entorno.
3. Pedir contraseñas por teclado sin mostrarlas.

### R-051G - Validación global de instaladores adaptables

Se validó globalmente:

- Sintaxis Bash de instaladores principales.
- Bloques R-051D, R-051E y R-051F.
- Lógica DASC_PROFILE_VALUE.
- Ausencia de defaults débiles activos.
- Servicios activos en lab-pruebas.
- Panel local directo 8000.
- Panel local por Nginx 8080.
- Panel central por Nginx 80.
- Central health 8010.
- Timer central retry.

Durante esta validación se detectaron IPs fijas en:

- deploy/api/package/main.py

### R-051G-FIX1 - Eliminar IPs fijas de laboratorio en defaults API

Se modificó:

- deploy/api/package/main.py

Se sustituyeron defaults de laboratorio:

- 192.168.60.30
- 192.168.60.20

por defaults neutros:

- 127.0.0.1

Validación posterior:

- main.py tiene sintaxis Python válida.
- No quedan IPs fijas de laboratorio en deploy.
- Repo limpio.

## Commits principales

- 21d1ca9 docs: iniciar instaladores adaptables
- f161c09 docs: definir perfiles despliegue
- 29745ab feat: adaptar instalador api a perfiles
- 9bf8b5f docs: cerrar instalador api perfiles
- 27fd367 feat: adaptar instalador db a perfiles
- 97d40dc docs: cerrar instalador db perfiles
- 39fcd62 feat: adaptar instalador backups a perfiles
- 026f87c docs: cerrar instalador backups perfiles
- 3c4905c fix: eliminar ips laboratorio defaults api
- 15d0a14 docs: validar instaladores adaptables

## Validaciones finales

Se validó:

- No quedan IPs fijas 192.168.60.20, 192.168.60.30 ni 192.168.1.250 dentro de deploy.
- No quedan defaults débiles activos de DB.
- No quedan defaults débiles activos de backup-services.
- Los valores antiguos solo permanecen como placeholders rechazados.
- main.py tiene sintaxis Python válida sin generar .pyc.
- Los instaladores principales tienen sintaxis Bash válida.
- El entorno activo no se rompe.
- dasc-api sigue activo.
- nginx sigue activo.
- dasc-central-support sigue activo.
- dasc-central-retry.timer sigue activo.
- Panel local 8000 responde.
- Panel local 8080 responde.
- Panel central 80 responde.
- Central health 8010 responde.

## Resultado

R-051 queda cerrada correctamente.

Los instaladores de DASC Server Manager quedan más preparados para despliegues reales y dejan de depender de valores fijos de laboratorio en los puntos principales revisados.

## Límites actuales

R-051 no incluye todavía:

- Reinstalación completa desde cero con los nuevos perfiles.
- Validación completa en máquinas limpias Lite, Standard y Pro.
- Automatización total de flujo multi-servidor.
- Cierre de puertos internos con firewall.
- Hardening final de SSH tras bootstrap.
- HTTPS real.
- Gestión visual de perfiles desde panel.

Estos puntos quedan para tareas posteriores.

## Próximo paso recomendado

Continuar con:

- R-052 - Revisión de seguridad de panel local y secretos

o, si se prefiere validar instalación antes de seguir seguridad:

- R-053 - Validación completa de instalación desde cero
