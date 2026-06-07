# Validación automática del paquete API instalable

Fecha: 2026-06-07 23:35:02

## Resumen

| Campo | Valor |
|---|---|
| Total comprobaciones | 50 |
| Correctas | 50 |
| Fallidas | 0 |

## Resultado

Resultado: OK.

El paquete API cumple las comprobaciones mínimas para seguir avanzando hacia instalación real.

## Comprobaciones

| Estado | Comprobación | Detalle |
|---|---|---|
| OK | Existe paquete API | Ruta esperada: deploy/api/package |
| OK | Existe instalador API | Ruta esperada: deploy/api/install_dasc_api.sh |
| OK | No existe config.env real en paquete | El paquete no debe incluir secretos reales. |
| OK | Existe config.env.example en paquete | El instalador debe crear config.env a partir de este ejemplo. |
| OK | config.env.example incluye BACKUP_DB_HOST | Debe permitir configurar host de backup. |
| OK | config.env.example incluye BACKUP_DB_USER | Debe permitir configurar usuario de backup. |
| OK | config.env.example incluye BACKUP_DB_PASS | Debe permitir configurar password de backup. |
| OK | config.env.example incluye BACKUP_OUTPUT_DIR | Debe permitir configurar salida de backups. |
| OK | config.env.example incluye BACKUP_RETENTION_KEEP | Debe permitir configurar retención de backups. |
| OK | config.env.example incluye RESTORE_DB_HOST | Debe permitir configurar host de restauración. |
| OK | config.env.example incluye RESTORE_DB_USER | Debe permitir configurar usuario de restauración. |
| OK | config.env.example incluye RESTORE_DB_PASS | Debe permitir configurar contraseña de restauración. |
| OK | config.env.example incluye RESTORE_TARGET_DB | Debe definir base destino de restauración controlada. |
| OK | Existe main.py | Archivo principal del API. |
| OK | Existe requirements.txt | Dependencias del API. |
| OK | Existe carpeta templates | Plantillas web. |
| OK | Existe carpeta static | Archivos estáticos. |
| OK | Existe generador Python de informe operativo | Herramienta de producto dentro del paquete. |
| OK | Informe operativo inspecciona backups | Debe consultar metadata de backups. |
| OK | Informe operativo lee BACKUP_OUTPUT_DIR | Debe usar directorio configurable de backups. |
| OK | Informe operativo muestra sección Backups completos | Debe incluir sección de backups en informe. |
| OK | Existe wrapper Bash de informe operativo | Wrapper para servidor Linux. |
| OK | Existe validador post-instalación API | Validador para Ubuntu instalado. |
| OK | Existe generador Python de backup completo | Herramienta de backup completo dentro del paquete. |
| OK | Existe wrapper Bash de backup completo | Wrapper para backup completo en servidor Linux. |
| OK | Existe herramienta Python de limpieza de backups | Herramienta de retención dentro del paquete. |
| OK | Existe wrapper Bash de limpieza de backups | Wrapper para limpieza de backups en Linux. |
| OK | Existe herramienta Python de restauración controlada | Herramienta de restauración segura dentro del paquete. |
| OK | Existe wrapper Bash de restauración controlada | Wrapper para restauración controlada en Linux. |
| OK | Existe reports/.gitkeep | Mantiene la carpeta reports sin versionar informes generados. |
| OK | No hay informes runtime versionables en reports | Los informes generados deben ignorarse y no subirse. |
| OK | Instalador requiere config.env.example | El instalador no debe depender de config.env real en el repo. |
| OK | Instalador crea config.env si falta | Debe crear config.env en la instalación real. |
| OK | Instalador prepara data | Debe crear directorio runtime data. |
| OK | Instalador prepara reports | Debe crear directorio runtime reports. |
| OK | Instalador prepara tools | Debe crear directorio tools. |
| OK | Instalador da permisos al wrapper | Debe dar permisos de ejecución al wrapper. |
| OK | Instalador da permisos al validador post-instalación | Debe dar permisos de ejecución al validador. |
| OK | Instalador da permisos al backup completo | Debe dar permisos de ejecución al backup completo. |
| OK | Instalador da permisos a limpieza de backups | Debe dar permisos de ejecución a la limpieza de backups. |
| OK | Instalador da permisos a restauración controlada | Debe dar permisos de ejecución a la restauración controlada. |
| OK | Instalador verifica cliente MariaDB | Debe asegurar mysqldump o mariadb-dump para backups. |
| OK | Instalador tiene mensaje SSH remoto no bloqueante | Debe mostrar un mensaje final correcto sobre SSH no bloqueante. |
| OK | Instalador mensaje SSH remoto bien cerrado | Evita líneas echo con comillas sin cerrar. |
| OK | install_dasc_api.sh usa LF | Los scripts Linux deben tener LF. |
| OK | generate_operational_report.sh usa LF | Los scripts Linux deben tener LF. |
| OK | check_api_installation.sh usa LF | Los scripts Linux deben tener LF. |
| OK | run_full_db_backup.sh usa LF | Los scripts Linux deben tener LF. |
| OK | cleanup_db_backups.sh usa LF | Los scripts Linux deben tener LF. |
| OK | restore_db_backup.sh usa LF | Los scripts Linux deben tener LF. |

## Conclusión

El paquete API está preparado a nivel estructural para una prueba de instalación real en Ubuntu.
