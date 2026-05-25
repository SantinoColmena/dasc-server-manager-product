# F6-GATE-04F - Cierre validación de instalación con perfiles e IPs explícitas

## Objetivo

Validar que DASC Server Manager puede funcionar usando un perfil de instalación con IPs explícitas, sin depender de valores rígidos internos de laboratorio en los instaladores.

## Estado

Cerrada.

## Perfil validado

Se validó un perfil equivalente a Pro 3 servidores.

| Rol | Máquina | IP |
|---|---|---|
| API / panel | lab-pruebas | 192.168.60.10 |
| DB / logs | lab-db-gate02 | 192.168.60.20 |
| Backups / servicios | lab-backups-gate04d | 192.168.60.30 |

## Contexto

En F6-GATE-04C se parametrizó el instalador DB.

En F6-GATE-04D se parametrizó el instalador backup-services.

En F6-GATE-04E se adaptó `config.env.example` a placeholders por perfil.

F6-GATE-04F valida que el conjunto funciona en un perfil real con IPs explícitas.

## Validación API / panel

En `lab-pruebas` se comprobó:

~~~text
hostname: lab-pruebas
IPs: 192.168.1.250 192.168.60.10
Servicio dasc-api: active
HTTP local: 303 See Other -> /login
~~~

Variables principales detectadas:

~~~env
SERVICIOS_HOST=192.168.60.30
BACKUPS_HOST=192.168.60.30
TERMINAL_DATABASE_HOST=192.168.60.20
LOGS_DB_HOST=192.168.60.20
BACKUP_DB_HOST=192.168.60.20
RESTORE_DB_HOST=192.168.60.20
DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.30,192.168.60.20
~~~

Conectividad validada:

~~~text
ping 192.168.60.20 OK
ping 192.168.60.30 OK
TCP 192.168.60.20:3306 OK
TCP 192.168.60.30:22 OK
~~~

## Validación DB / logs

En `lab-db-gate02` se comprobó:

~~~text
hostname: lab-db-gate02
IPs: 192.168.1.251 192.168.60.20
MariaDB: active
Puerto 3306: escuchando en 0.0.0.0
~~~

Usuarios DASC detectados:

~~~text
dasc_backup@192.168.60.10
dasc_backup@192.168.60.30
dasc_logs@192.168.60.10
dasc_restore@192.168.60.10
dasc_restore@192.168.60.30
~~~

Base de logs:

~~~text
Base: dasc_logs
Tabla: eventos
Eventos: 20
~~~

Base de ejemplo:

~~~text
Base: employees
Tabla: empleados_demo
~~~

## Validación backup-services

En `lab-backups-gate04d` se comprobó:

~~~text
hostname: lab-backups-gate04d
IPs: 192.168.1.141 192.168.60.30
~~~

Comandos cliente disponibles:

~~~text
/usr/bin/mysql
/usr/bin/mysqldump
/usr/bin/mysqlbinlog
~~~

Configuración MySQL generada:

~~~text
user=dasc_backup
host=192.168.60.20

user=dasc_restore
host=192.168.60.20
~~~

Conexión a DB remota:

~~~text
employees
information_schema
~~~

Dump de prueba:

~~~text
Host: 192.168.60.20
Database: employees
Server version: 5.5.5-10.6.23-MariaDB-0ubuntu0.22.04.1-log
Table structure for table empleados_demo
~~~

## Resultado

La instalación con tres servidores e IPs explícitas funciona correctamente.

Se confirma que:

- API/panel sigue activo.
- API puede alcanzar DB.
- API puede alcanzar backup-services por SSH.
- DB acepta usuarios desde API y backup-services.
- Backup-services puede conectar a DB.
- Backup-services puede generar un dump de prueba.
- Los instaladores parametrizados funcionan en una arquitectura de 3 servidores.

## Observaciones

En `DASC_SSH_ALLOWED_HOSTS` aparece `192.168.60.30` duplicada.

Esto no bloquea la validación porque la lista contiene los hosts necesarios, pero queda como mejora de limpieza futura.

También aparece el aviso:

~~~text
Warning: column statistics not supported by the server.
~~~

No bloquea la validación porque el dump se genera correctamente.

## Criterio de cierre

F6-GATE-04F se considera cerrada porque:

- Las tres máquinas tienen IPs correctas.
- La API responde correctamente.
- MariaDB está activo y accesible.
- Los usuarios de DB necesarios existen.
- La API puede llegar a DB y backup-services.
- Backup-services puede llegar a DB.
- El dump de prueba funciona.
- La arquitectura queda validada como perfil explícito de 3 servidores.

## Próxima puerta

~~~text
F6-GATE-04G - Cierre global de instaladores adaptables por perfil
~~~

## Conclusión

DASC Server Manager supera la validación de instalación con perfil e IPs explícitas.

El producto ya no depende únicamente de valores fijos de laboratorio y puede funcionar en una arquitectura separada de API, DB y backups.
