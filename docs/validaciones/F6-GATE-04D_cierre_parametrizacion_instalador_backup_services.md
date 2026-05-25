# F6-GATE-04D - Cierre parametrizacion instalador backup-services

## Objetivo

Validar que el instalador de backup-services ya no depende de una IP fija de laboratorio para localizar el servidor de base de datos.

## Estado

Cerrada.

## Archivo validado

~~~text
deploy/backup-services/install_backup_services.sh
~~~

## Cambios principales

Se elimino el valor fijo:

~~~text
DB_HOST=192.168.60.20
~~~

El instalador ahora requiere `DB_HOST` por variable de entorno o lo solicita de forma interactiva.

Tambien se corrigio la instalacion de dependencias en Ubuntu limpio para usar cliente MySQL por defecto y comprobar:

~~~text
mysql
mysqldump
mysqlbinlog
~~~

## Entorno validado

| Rol | Maquina | IP |
|---|---|---|
| API / panel | lab-pruebas | 192.168.60.10 |
| DB / logs | lab-db-gate02 | 192.168.60.20 |
| Backups / servicios | lab-backups-gate04d | 192.168.60.30 |

## Validacion real

En `lab-backups-gate04d` se ejecuto:

~~~bash
sudo DB_HOST=192.168.60.20 bash deploy/backup-services/install_backup_services.sh
~~~

Resultado:

- Instalacion completada.
- Usuario `dasc` creado.
- SSH activo.
- Cron activo.
- Carpeta `/home/dasc/backups` creada.
- Scripts instalados en `/usr/local/bin`.
- `.my.cnf` y `.my_restore.cnf` creados con permisos restrictivos.
- Conexion a MariaDB remota validada.
- Usuario de backup validado.
- Usuario de restauracion validado.
- Dump de prueba validado.

## Evidencias principales

Comandos detectados:

~~~text
/usr/bin/mysql
/usr/bin/mysqldump
/usr/bin/mysqlbinlog
~~~

Configuracion generada:

~~~text
user=dasc_backup
host=192.168.60.20

user=dasc_restore
host=192.168.60.20
~~~

Dump de prueba:

~~~text
Host: 192.168.60.20
Database: employees
Server version: 5.5.5-10.6.23-MariaDB
Table structure for table empleados_demo
~~~

## Observaciones

Aparecieron avisos no bloqueantes:

- Aviso de contrasena debil para el usuario `dasc`.
- Aviso de `mysqldump` por `column statistics`.
- Aviso de compatibilidad `mysqlbinlog` con MariaDB.

No bloquean la puerta porque la instalacion, conexion y dump funcionan.

## Criterio de cierre

F6-GATE-04D se considera cerrada porque:

- `DB_HOST` ya no tiene IP fija por defecto.
- El instalador acepta `DB_HOST` por variable de entorno.
- El instalador puede solicitar `DB_HOST` si no se pasa.
- La instalacion fue validada en una maquina Ubuntu limpia.
- Backup-services se conecta correctamente a la DB remota.
- El dump de prueba funciona.

## Proxima puerta

~~~text
F6-GATE-04E - Revisar config.env.example y placeholders por perfil
~~~

## Conclusion

DASC Server Manager supera la validacion de parametrizacion del instalador backup-services.

El sistema ya puede desplegar una maquina de backups independiente apuntando a una DB remota mediante `DB_HOST` explicito, sin depender de una IP fija de laboratorio en el codigo.
