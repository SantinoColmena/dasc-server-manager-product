# Registro de incidencias - Piloto 1

## Objetivo

Registrar todos los problemas, dudas, fallos técnicos y mejoras detectadas durante la ejecución del primer piloto técnico.

Este documento sirve como base para R-041 y R-042.

## Tabla de incidencias

| Nº | Fecha | Área | Descripción | Gravedad | Estado | Solución aplicada |
|---|---|---|---|---|---|---|
| 1 | 23/05/2026 | Documentación | El plan inicial indicaba ejecutar install_db.sh, install_backup_services.sh e install_dasc_api.sh desde la raíz del repositorio, pero los instaladores reales estaban dentro de deploy | Media | Corregida | Se ejecutaron las rutas correctas: deploy/db, deploy/backup-services y deploy/api |
| 2 | 23/05/2026 | Base de datos | install_db.sh falló al crear dasc_logs porque Bash interpretaba las comillas invertidas como comandos | Alta | Corregida | Se escaparon las comillas invertidas en las referencias SQL a LOGS_DB_NAME y eventos |
| 3 | 23/05/2026 | Logs | El panel no podía guardar eventos por contraseña incorrecta en LOGS_DB_PASS | Alta | Corregida | Se configuró LOGS_DB_PASS=dasc_logs_2026 en /opt/dasc/api/config.env |
| 4 | 23/05/2026 | Terminal | Terminal Database fallaba por host key SSH no registrada para 192.168.60.20 | Media | Corregida | Se añadió la huella ED25519 al known_hosts dedicado de DASC |
| 5 | 23/05/2026 | Terminal | Terminal Database funcionaba con contraseña pero no con clave automática | Media | Corregida | Se copió la clave pública de la API al usuario dasc de la máquina DB |
| 6 | 23/05/2026 | Cacti | Cacti no funciona o no está validado en el perfil limpio de 2 servidores | Baja | Documentada | Se deja como limitación no bloqueante del piloto |
| 7 | 23/05/2026 | Cliente DB | Al validar MariaDB como usuario santino aparecía Access denied | Baja | Corregida | Se usó sudo mariadb para validaciones administrativas locales |
| 8 | 23/05/2026 | Backups | mysqldump mostró errno 32 al usar tubería con head | Baja | Aclarada | No era fallo real; head cerró la tubería tras las primeras líneas |

## Clasificación de gravedad

| Gravedad | Significado |
|---|---|
| Baja | No bloquea el uso del sistema |
| Media | Molesta o requiere corrección, pero tiene alternativa |
| Alta | Bloquea una función importante |
| Crítica | Impide instalar, hacer backup o restaurar |

## Conclusión

Las incidencias detectadas durante el piloto 1 han sido corregidas o documentadas.

Ninguna incidencia crítica queda abierta.

La incidencia de Cacti se acepta como limitación del perfil de 2 servidores y no bloquea el cierre de R-040.
