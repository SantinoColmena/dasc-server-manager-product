# F6-GATE-04C - Parametrización del instalador DB

## Objetivo

Eliminar dependencias reales de IPs fijas de laboratorio en el instalador de base de datos.

## Estado

En curso.

## Archivo modificado

~~~text
deploy/db/install_db.sh
~~~

## Problema detectado

La auditoría F6-GATE-04A detectó valores de laboratorio en el instalador DB:

~~~text
BACKUP_ALLOWED_HOST=192.168.60.30
LOGS_ALLOWED_HOST=192.168.60.10
~~~

Estos valores eran válidos para laboratorio, pero no deben ser valores por defecto rígidos para instalaciones reales.

## Cambio aplicado

Se eliminan esos valores por defecto y se obliga a definirlos mediante:

~~~text
BACKUP_ALLOWED_HOST
LOGS_ALLOWED_HOST
~~~

Si no se reciben como variables de entorno, el instalador los pregunta de forma interactiva.

## Variables

### BACKUP_ALLOWED_HOST

Host autorizado para ejecutar backups/restauraciones contra MariaDB.

Ejemplo laboratorio:

~~~bash
BACKUP_ALLOWED_HOST=192.168.60.10
~~~

### LOGS_ALLOWED_HOST

Host autorizado para escribir logs/eventos en la base `dasc_logs`.

Ejemplo laboratorio:

~~~bash
LOGS_ALLOWED_HOST=192.168.60.10
~~~

## Ejecución interactiva

~~~bash
sudo bash deploy/db/install_db.sh
~~~

El instalador preguntará los hosts necesarios.

## Ejecución no interactiva

~~~bash
sudo BACKUP_ALLOWED_HOST=IP_API_O_BACKUPS LOGS_ALLOWED_HOST=IP_API bash deploy/db/install_db.sh
~~~

## Relación con perfiles

### Lite

Puede usar `127.0.0.1` o la IP local si API y DB están en el mismo servidor.

### PyME 2 servidores

Normalmente ambos valores apuntan al servidor API/backups.

### Pro 3 servidores

`BACKUP_ALLOWED_HOST` puede apuntar al servidor de backups y `LOGS_ALLOWED_HOST` al servidor API.

## Criterio de validación

F6-GATE-04C se considera preparada cuando:

- `deploy/db/install_db.sh` no usa `192.168.60.30` como valor por defecto.
- `deploy/db/install_db.sh` no usa `192.168.60.10` como valor por defecto.
- El instalador acepta variables de entorno.
- El instalador puede preguntar valores si no se pasan.
- La auditoría de IPs refleja la reducción de hallazgos ALTA.

## Próximo paso

Validar este instalador en Ubuntu real usando variables explícitas.

## Conclusión

El instalador DB empieza a dejar de depender de IPs fijas de laboratorio y se acerca a un modelo adaptable por perfil.
