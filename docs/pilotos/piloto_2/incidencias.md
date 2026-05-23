# Registro de incidencias - Piloto 2

## Objetivo

Registrar todos los problemas detectados durante la ejecución del piloto 2 en perfil Lite de 1 servidor + externo.

## Tabla de incidencias

| Nº | Fecha | Área | Descripción | Gravedad | Estado | Solución aplicada |
|---|---|---|---|---|---|---|
| 1 | 23/05/2026 | Backups / dependencias | install_backup_services.sh instaló paquetes MySQL que sustituyeron MariaDB Server en el perfil Lite | Alta | Corregida | Se reinstaló mariadb-server y mariadb-client en el piloto. En el repo se sustituye default-mysql-client/mysql-client por mariadb-client |
| 2 | 23/05/2026 | SSH / panel | El panel rechazaba 192.168.60.40 con el error Host SSH no permitido | Media | Corregida | Se añadió 192.168.60.40 a DASC_SSH_ALLOWED_HOSTS |
| 3 | 23/05/2026 | Backups | Se generó un backup vacío de 0 bytes mientras MariaDB estaba caída | Media | Corregida | Se eliminó el archivo vacío y se repitió el backup tras recuperar MariaDB |
| 4 | 23/05/2026 | Copia externa | La primera copia externa falló porque todavía no existía ningún .sql.gz válido | Baja | Corregida | Se repitió tras generar un backup correcto |
| 5 | 23/05/2026 | Cacti | Cacti no se valida en este perfil Lite | Baja | Documentada | Se considera componente opcional/no bloqueante en este piloto |

## Clasificación de gravedad

| Gravedad | Significado |
|---|---|
| Baja | No bloquea el uso del sistema |
| Media | Molesta o requiere corrección, pero tiene alternativa |
| Alta | Bloquea una función importante |
| Crítica | Impide instalar, hacer backup o restaurar |

## Conclusión

Las incidencias principales del piloto 2 han sido corregidas.

No queda ninguna incidencia crítica abierta.

La incidencia más importante fue la sustitución de MariaDB por paquetes MySQL durante la instalación de backup-services en un perfil de 1 servidor. Esta incidencia se corrige en el repositorio para evitar que se repita en futuros pilotos.