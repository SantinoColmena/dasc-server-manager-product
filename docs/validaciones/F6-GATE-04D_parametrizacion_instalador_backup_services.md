# F6-GATE-04D - Parametrización del instalador backup-services

## Objetivo

Eliminar la dependencia real de IP fija de laboratorio en el instalador de servicios de backup.

## Estado

En curso.

## Archivo modificado

~~~text
deploy/backup-services/install_backup_services.sh
~~~

## Problema detectado

La auditoría F6-GATE-04A detectó un valor de laboratorio en el instalador de backup-services:

~~~text
DB_HOST=192.168.60.20
~~~

Este valor era válido para laboratorio, pero no debe ser un valor por defecto rígido para instalaciones reales.

## Cambio aplicado

Se elimina el valor por defecto rígido.

Ahora el instalador exige definir:

~~~text
DB_HOST
~~~

Si no se recibe como variable de entorno, el instalador lo pregunta de forma interactiva.

## Variable

### DB_HOST

IP o hostname del servidor de base de datos origen.

Ejemplo laboratorio:

~~~bash
DB_HOST=192.168.60.20
~~~

Ejemplo genérico:

~~~bash
DB_HOST=IP_SERVIDOR_DB
~~~

## Ejecución interactiva

~~~bash
sudo bash deploy/backup-services/install_backup_services.sh
~~~

El instalador preguntará el host de la base de datos.

## Ejecución no interactiva

~~~bash
sudo DB_HOST=IP_SERVIDOR_DB bash deploy/backup-services/install_backup_services.sh
~~~

## Relación con perfiles

### Lite

Puede usar `127.0.0.1` o la IP local si la base de datos está en el mismo servidor.

### PyME 2 servidores

`DB_HOST` apunta al servidor DB.

### Pro 3 servidores

`DB_HOST` apunta al servidor DB y backup-services puede vivir en servidor separado.

## Criterio de validación

F6-GATE-04D se considera preparada cuando:

- `deploy/backup-services/install_backup_services.sh` no usa `192.168.60.20` como valor por defecto.
- El instalador acepta `DB_HOST` como variable de entorno.
- El instalador pregunta `DB_HOST` si no se pasa.
- La auditoría de IPs refleja reducción de hallazgos ALTA.
- La instalación se valida en Ubuntu real usando `DB_HOST` explícito.

## Próximo paso

Validar este instalador en Ubuntu real usando:

~~~bash
sudo DB_HOST=192.168.60.20 bash deploy/backup-services/install_backup_services.sh
~~~

## Conclusión

El instalador backup-services empieza a dejar de depender de IPs fijas de laboratorio y se acerca a un modelo adaptable por perfil.
