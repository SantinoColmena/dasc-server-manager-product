# Validación real de Fase 2 en laboratorio Ubuntu

## Objetivo

Validar en máquinas Ubuntu reales la Fase 2 de DASC Server Manager: seguridad, restauración, integridad, retención, auditoría, logs remotos y reverse proxy HTTPS.

## Arquitectura validada

| Máquina | Rol | IP laboratorio | IP accesible desde Windows |
|---|---|---|---|
| lab-api | API / Panel / Reverse proxy | 192.168.60.10 | 192.168.1.244 |
| lab-db | Base de datos MariaDB | 192.168.60.20 | 192.168.1.243 |
| lab-backup | Backups + Servicios | 192.168.60.30 | 192.168.1.245 |

## Estado inicial

| Comprobación | Estado |
|---|---|
| Repo actualizado en Windows | Correcto |
| Máquinas Ubuntu disponibles | Correcto |
| Conectividad entre máquinas por red 192.168.60.0/24 | Correcto |
| SSH activo en las tres máquinas | Correcto |
| Usuario con sudo disponible | Correcto |

## Validación DB

| Prueba | Estado |
|---|---|
| Instalación MariaDB | Correcto |
| Servicio `mariadb` activo | Correcto |
| Puerto 3306 escuchando en `0.0.0.0` | Correcto |
| Base `employees` creada | Correcto |
| Tabla demo `empleados_demo` creada | Correcto |
| Usuario `dasc_backup@192.168.60.30` creado | Correcto |
| Usuario `dasc_restore@192.168.60.30` creado | Correcto |
| Binary logs activos | Correcto |
| Binlog `dasc-bin.000001` generado | Correcto |
| Base `dasc_logs` creada | Correcto |
| Usuario `dasc_logs@192.168.60.10` creado | Correcto |
| Tabla `dasc_logs.eventos` creada | Correcto |

## Validación backup-services

| Prueba | Estado |
|---|---|
| Instalación de paquetes cliente MySQL | Correcto |
| Servicio SSH activo | Correcto |
| Servicio cron activo | Correcto |
| Script `/usr/local/bin/backups_api.sh` instalado | Correcto |
| Script `/usr/local/bin/restore_api.sh` instalado | Correcto |
| Script `/usr/local/bin/restore_drill_api.sh` instalado | Correcto |
| Script `/usr/local/bin/servicios_api.sh` instalado | Correcto |
| Archivo `/home/dasc/.my.cnf` creado | Correcto |
| Archivo `/home/dasc/.my_restore.cnf` creado | Correcto |
| Conexión a MariaDB con usuario backup | Correcto |
| Conexión a MariaDB con usuario restore | Correcto |
| Prueba `mysqldump` contra `employees` | Correcto |

## Validación backup real

| Prueba | Estado |
|---|---|
| Backup completo real | Correcto |
| Fichero `.sql.gz` generado | Correcto |
| `history.tsv` creado | Correcto |
| `checksums.sha256` creado | Correcto |
| `audit.log` creado | Correcto |
| SHA256 registrado | Correcto |
| Tamaño registrado | Correcto |

Backup validado:

    ID: 1
    Tipo: full
    BD: employees
    Archivo: /home/dasc/backups/fase2-full-YYYYMMDD-HHMM.sql.gz
    SHA256: 664e939364629ac48a9edfaa753d0c57ec28168217856a72c46d19289a2dfd14

## Validación de simulacro de recuperación

| Prueba | Estado |
|---|---|
| Ejecución de `restore_drill_api.sh` | Correcto |
| Validación de existencia del backup | Correcto |
| Validación de estado OK | Correcto |
| Validación de SHA256 | Correcto |
| Validación `gzip -t` | Correcto |
| Registro en `restore_drill.log` | Correcto |
| Registro en `audit.log` | Correcto |

## Validación de restauración real

| Prueba | Estado |
|---|---|
| Inserción de registro posterior al backup | Correcto |
| Ejecución de `restore_api.sh` con confirmación `SI` | Correcto |
| Validación de integridad antes de restaurar | Correcto |
| Restauración completada | Correcto |
| Registro posterior eliminado tras restaurar | Correcto |
| Registro en `restore.log` | Correcto |
| Registro en `audit.log` | Correcto |

Resultado observado:

    Antes de restaurar:
    registro-inicial
    registro-post-backup

    Después de restaurar:
    registro-inicial

## Validación API / Panel

| Prueba | Estado |
|---|---|
| Instalación API | Correcto |
| Servicio `dasc-api` activo | Correcto |
| Uvicorn escuchando en puerto 8000 | Correcto |
| `config.env` creado y protegido | Correcto |
| `SECRET_KEY` generada | Correcto |
| `ADMIN_PASSWORD` almacenada como hash bcrypt | Correcto |
| `BACKUPS_HOST=192.168.60.30` | Correcto |
| `SERVICIOS_HOST=192.168.60.30` | Correcto |
| `DASC_SSH_KEY` configurado | Correcto |
| `DASC_SSH_KNOWN_HOSTS` configurado | Correcto |
| Clave SSH dedicada generada | Correcto |
| `known_hosts_dasc` generado | Correcto |
| Copia de clave a `lab-backup` | Correcto |
| SSH sin contraseña contra `lab-backup` | Correcto |

## Validación de logs remotos

| Prueba | Estado |
|---|---|
| Conexión desde API a `dasc_logs` | Correcto |
| Tabla `eventos` creada | Correcto |
| Registro de accesos anónimos | Correcto |
| Registro de login correcto | Correcto |
| Registro de accesos autenticados | Correcto |

Evidencia principal:

    login admin desde 192.168.1.137
    recurso POST /login
    resultado OK
    detalle Inicio de sesión correcto

## Validación reverse proxy HTTPS

| Prueba | Estado |
|---|---|
| Instalación Nginx | Correcto |
| Certificado autofirmado creado | Correcto |
| Configuración Nginx válida con `nginx -t` | Correcto |
| Servicio `nginx` activo | Correcto |
| Puerto 80 abierto | Correcto |
| Puerto 443 abierto | Correcto |
| HTTP redirige a HTTPS | Correcto |
| HTTPS responde con `/login` | Correcto |
| Acceso desde Windows por `https://192.168.1.244` | Correcto |
| Login desde navegador Windows | Correcto |

## Incidencias detectadas durante la validación

### BOM UTF-8 en scripts

Se detectó que algunos scripts instalados conservaban BOM UTF-8, provocando errores de ejecución en Bash.

Solución aplicada:

- Normalización de scripts.
- Eliminación de BOM.
- Corrección en instalador de backup-services.

### Lectura incorrecta de `history.tsv`

Se detectó que `restore_api.sh` y `restore_drill_api.sh` leían mal el historial cuando el campo `base_id` estaba vacío.

Solución aplicada:

- Sustitución de lectura con `read` por extracción robusta con `awk`.

### Usuario incorrecto en restauración

Se detectó que la restauración podía usar credenciales no esperadas si se utilizaba `--defaults-extra-file`.

Solución aplicada:

- Uso de `--defaults-file` en `restore_api.sh`.

### Carpeta `.ssh` inexistente en usuario local de API

Se detectó que `ssh-copy-id` fallaba si `/home/<usuario>/.ssh` no existía.

Solución aplicada:

- `install_dasc_api.sh` crea la carpeta `.ssh` del usuario antes de ejecutar `ssh-copy-id`.

### Base y tabla de logs no creadas inicialmente

Se detectó que el panel podía conectar a MariaDB, pero faltaba la tabla `dasc_logs.eventos`.

Solución aplicada:

- `install_db.sh` crea `dasc_logs`.
- `install_db.sh` crea `dasc_logs.eventos`.
- `install_db.sh` crea el usuario `dasc_logs@192.168.60.10`.

## Fixes aplicados al repositorio

| Commit | Descripción |
|---|---|
| `6fb98c9` | Corrección de scripts de backups tras validación real |
| `f074d86` | Normalización de scripts `.sh` restantes |
| `edf0d63` | Creación de logs DB y preparación de SSH local en instaladores |

## Resultado final

La Fase 2 queda validada en laboratorio real Ubuntu con tres máquinas.

Estado final:

| Bloque | Estado |
|---|---|
| Seguridad de usuarios | Validado |
| Configuración segura | Validado |
| SSH endurecido | Validado |
| Backup real | Validado |
| Integridad SHA256 | Validado |
| Simulacro de recuperación | Validado |
| Restauración controlada | Validado |
| Auditoría local | Validado |
| Logs remotos | Validado |
| Reverse proxy HTTPS | Validado |

## Conclusión

La Fase 2 queda cerrada como implementada, documentada y validada en laboratorio real.

La validación ha demostrado que el sistema puede:

1. Instalar sus componentes en máquinas separadas.
2. Crear backups reales.
3. Registrar historial e integridad.
4. Simular recuperación.
5. Restaurar de forma controlada.
6. Auditar operaciones críticas.
7. Registrar eventos remotos del panel.
8. Exponer el panel mediante reverse proxy HTTPS.

## Validación adicional de retención segura

Después del cierre principal se ejecutó una validación específica de R-021.

Resultados:

| Prueba | Estado |
|---|---|
| Backup antiguo pasa a `PRUNED` | Correcto |
| Fichero físico purgado | Correcto |
| Checksum eliminado | Correcto |
| Auditoría `backup.prune` registrada | Correcto |
| Base referenciada por incremental conservada | Correcto |
| Checksum de base referenciada conservado | Correcto |

Con esta prueba, la retención segura queda validada también en laboratorio real.
