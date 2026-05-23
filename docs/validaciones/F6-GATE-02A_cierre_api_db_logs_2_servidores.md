# F6-GATE-02A - Cierre validación API + DB/logs en 2 servidores

## Objetivo

Validar la integración real entre el servidor API de DASC Server Manager y un servidor independiente de base de datos/logs.

## Estado

Cerrada.

## Entorno usado

| Rol | Máquina | IP privada DASC |
|---|---|---|
| API / Panel | lab-pruebas | 192.168.60.10 |
| DB / Logs | lab-db-gate02 | 192.168.60.20 |

## Tipo de prueba

Validación de arquitectura PyME inicial con 2 servidores:

- Servidor API ya validado previamente.
- Servidor DB/logs limpio configurado desde cero.
- Comunicación por red privada DASC `192.168.60.0/24`.

## Preparación de red

Se validó que las máquinas disponen de red privada:

~~~text
lab-pruebas: 192.168.60.10
lab-db-gate02: 192.168.60.20
~~~

## Preparación de MariaDB

En `lab-db-gate02` se instaló MariaDB y se configuró para escuchar en red:

~~~text
bind-address = 0.0.0.0
~~~

Se comprobó que MariaDB escuchaba en:

~~~text
0.0.0.0:3306
~~~

## Base de datos creada

Se creó la base de datos:

~~~text
dasc_logs
~~~

Se creó la tabla:

~~~text
eventos
~~~

Se creó el usuario:

~~~text
dasc_logs@192.168.60.10
~~~

Esto permite que el servidor API se conecte al servidor DB/logs desde su IP privada.

## Configuración del API

En `lab-pruebas` se actualizó `/opt/dasc/api/config.env` con:

~~~text
LOGS_DB_HOST=192.168.60.20
LOGS_DB_NAME=dasc_logs
LOGS_DB_USER=dasc_logs
LOGS_DB_PASS=***
~~~

Después se reinició el servicio:

~~~bash
sudo systemctl restart dasc-api
~~~

## Prueba Python desde API

Desde `/opt/dasc/api` se ejecutó una prueba con PyMySQL usando el entorno virtual real del API.

Resultado:

- Conexión correcta a `192.168.60.20`.
- Base de datos `dasc_logs` accesible.
- Tabla `eventos` detectada.
- Conteo de eventos correcto.
- Inserción de evento desde API correcta.
- Resultado final: `OK`.

## Informe operativo

Se ejecutó:

~~~bash
sudo ./tools/generate_operational_report.sh "DASC validacion 2 servidores" "2026-05"
~~~

Resultado:

~~~text
Resultado: BASE OPERATIVA OK.
~~~

El informe operativo detectó:

- Configuración mínima correcta.
- Variables sensibles enmascaradas.
- Runtime correcto.
- Base de datos de logs en estado OK.
- Eventos totales detectados.
- Últimos eventos registrados.

## Resultado de la base de datos de logs

El informe operativo mostró:

~~~text
Estado: OK
Eventos totales: 2
~~~

También mostró eventos de validación relacionados con F6-GATE-02A.

## Observación menor

Después de reiniciar `dasc-api`, una primera prueba con `curl` devolvió conexión rehusada.

Se considera una observación menor si una comprobación posterior confirma que el servicio queda activo y responde correctamente.

## Criterio de cierre

F6-GATE-02A se considera cerrada porque:

- Existe comunicación real API -> DB/logs.
- MariaDB escucha en la red privada DASC.
- El usuario remoto de logs funciona.
- El API puede leer e insertar eventos.
- El informe operativo ya no queda como operativo parcial por fallo de DB.
- El informe operativo queda como base operativa OK.

## Límites

Esta puerta no valida todavía:

- Servidor de backups.
- SSH real contra backups.
- Backups completos, incrementales o diferenciales.
- Restauraciones.
- Arquitectura Pro de 3 servidores.
- Informe final comercial para cliente.

## Próxima puerta recomendada

La siguiente puerta lógica es:

~~~text
F6-GATE-02B - Validación API + DB/logs + eventos reales del panel
~~~

Después:

~~~text
F6-GATE-03 - Validación de backups en arquitectura de 2 servidores
~~~

## Conclusión

DASC Server Manager supera la primera validación real de integración API + DB/logs en 2 servidores.

Esto acerca el producto a una arquitectura PyME realista, manteniendo separación entre servidor de aplicación y servidor de datos/logs.
