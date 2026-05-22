# Fase 2 - Seguridad y restauración

## Objetivo de la fase

La Fase 2 tiene como objetivo reforzar la seguridad básica del producto DASC Server Manager y preparar un flujo más completo de restauración de backups.

Esta fase no busca únicamente añadir funciones nuevas, sino convertir lo ya existente en un sistema más seguro, trazable y defendible como producto.

## Alcance trabajado

Durante esta fase se han trabajado los siguientes bloques:

- Seguridad de usuarios.
- Protección de secretos.
- Reverse proxy y HTTPS.
- Endurecimiento de SSH.
- Restauración controlada.
- Validación de integridad.
- Retención segura.
- Auditoría de operaciones críticas.
- Simulacro de recuperación.

## Estado de requisitos

| Requisito | Nombre | Estado |
|---|---|---|
| R-015 | Hash de contraseñas de usuarios | Implementado y validado localmente |
| R-016 | Protección de config.env y secretos | Implementado |
| R-017 | Reverse proxy y HTTPS | Implementado a nivel de script |
| R-018 | Endurecimiento SSH y comandos remotos | Implementado |
| R-019 | Restauración controlada de backups | Implementado |
| R-020 | Validación de integridad de backups | Implementado |
| R-021 | Retención segura y limpieza de backups | Implementado |
| R-022 | Auditoría de operaciones críticas | Implementado |
| R-023 | Simulacro de recuperación | Implementado |
| R-024 | Cierre documental de Fase 2 | En curso |

## Decisiones técnicas principales

### Usuarios y contraseñas

Se sustituye el almacenamiento de contraseñas en texto plano por hashes bcrypt usando `passlib`.

Los usuarios nuevos se guardan con `password_hash` y se mantiene compatibilidad temporal con usuarios antiguos que todavía puedan tener `password`.

### Secretos y configuración

El repositorio no debe contener `config.env` real.

Solo debe mantenerse `config.env.example`.

El instalador del API genera o conserva el `config.env` real durante la instalación y aplica permisos restrictivos.

### Reverse proxy

Se añade una capa Nginx delante de Uvicorn.

El objetivo es evitar exponer directamente el servidor de desarrollo/aplicación y preparar el camino para HTTPS.

En laboratorio se contempla certificado autofirmado.

### SSH endurecido

La API deja de depender de una clave SSH global del usuario.

Se prepara una clave propia de DASC:

    /opt/dasc/api/.ssh/id_rsa_dasc

Y un archivo known_hosts propio:

    /opt/dasc/api/.ssh/known_hosts_dasc

También se añaden timeouts, validación de hosts permitidos y validación de comandos remotos permitidos.

### Restauración controlada

Se añade `restore_api.sh`.

La restauración no recibe rutas arbitrarias desde el panel. El panel envía un ID de backup y el script remoto busca la ruta real en el historial.

La restauración exige confirmación explícita:

    SI

### Integridad

Cada backup generado registra un hash SHA256 en:

    /home/dasc/backups/.dasc/checksums.sha256

Antes de restaurar, el sistema recalcula el hash y lo compara con el valor esperado.

Si el backup está comprimido, también se valida con:

    gzip -t

### Retención segura

La retención deja de borrar directamente con `find -delete`.

Ahora se usa una función de limpieza segura que:

- Solo actúa dentro de `/home/dasc/backups`.
- Marca backups purgados como `PRUNED`.
- Elimina checksums obsoletos.
- Evita borrar copias base todavía referenciadas por otras copias activas.

### Auditoría

Se añade auditoría local en:

    /home/dasc/backups/.dasc/audit.log

Registra operaciones críticas como:

- Creación de backup.
- Validación de integridad.
- Purgado por retención.
- Inicio de restauración.
- Restauración correcta.
- Error de restauración.
- Error de integridad.

### Simulacro de recuperación

Se añade `restore_drill_api.sh`.

Permite comprobar que un backup está listo para restaurarse sin modificar todavía la base de datos.

## Archivos principales añadidos o modificados

### API

- `deploy/api/package/main.py`
- `deploy/api/package/requirements.txt`
- `deploy/api/package/config.env.example`
- `deploy/api/install_dasc_api.sh`

### Proxy

- `deploy/proxy/install_reverse_proxy.sh`
- `deploy/proxy/uninstall_reverse_proxy.sh`

### Backups y servicios

- `deploy/backup-services/install_backup_services.sh`
- `deploy/backup-services/package/backups_api.sh`
- `deploy/backup-services/package/restore_api.sh`
- `deploy/backup-services/package/restore_drill_api.sh`
- `deploy/backup-services/package/servicios_api.sh`

### Base de datos

- `deploy/db/install_db.sh`

### Validaciones

- `docs/validaciones/R-015_hash_usuarios.md`
- `docs/validaciones/R-016_config_secretos.md`
- `docs/validaciones/R-017_reverse_proxy_https.md`
- `docs/validaciones/R-018_ssh_comandos_remotos.md`
- `docs/validaciones/R-019_restauracion_controlada.md`
- `docs/validaciones/R-020_integridad_backups.md`
- `docs/validaciones/R-021_retencion_limpieza_backups.md`
- `docs/validaciones/R-022_auditoria_operaciones_criticas.md`
- `docs/validaciones/R-023_simulacro_recuperacion.md`

## Checklist pendiente de validación en VM Ubuntu

| Prueba | Estado |
|---|---|
| Instalar API desde cero | Pendiente |
| Comprobar `config.env` real y permisos | Pendiente |
| Comprobar hash de contraseña admin | Pendiente |
| Instalar DB desde cero | Pendiente |
| Comprobar usuario `dasc_backup` | Pendiente |
| Comprobar usuario `dasc_restore` | Pendiente |
| Instalar backup-services desde cero | Pendiente |
| Comprobar instalación de scripts en `/usr/local/bin` | Pendiente |
| Comprobar clave SSH dedicada | Pendiente |
| Comprobar known_hosts dedicado | Pendiente |
| Crear backup completo | Pendiente |
| Crear backup incremental/diferencial | Pendiente |
| Comprobar `history.tsv` | Pendiente |
| Comprobar `checksums.sha256` | Pendiente |
| Ejecutar simulacro de recuperación | Pendiente |
| Ejecutar restauración controlada | Pendiente |
| Comprobar `restore.log` | Pendiente |
| Comprobar `audit.log` | Pendiente |
| Probar retención segura | Pendiente |
| Instalar reverse proxy Nginx | Pendiente |
| Acceder por HTTPS | Pendiente |

## Estado final de la fase

La Fase 2 queda implementada a nivel de repositorio y scripts.

Queda pendiente una validación completa en máquinas Ubuntu reales para marcar la fase como validada en entorno real.

## Conclusión

La Fase 2 mejora de forma importante la seguridad y trazabilidad del sistema.

El producto pasa de tener backups funcionales a tener un flujo más defendible:

1. Crear backup.
2. Registrar historial.
3. Calcular integridad.
4. Auditar operación.
5. Simular recuperación.
6. Restaurar de forma controlada.
7. Registrar resultado.

Esto acerca DASC Server Manager a una versión más seria como producto/servicio para PYMES.
