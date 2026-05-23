# F6-GATE-02B - Cierre validación de eventos reales del panel contra DB remota

## Objetivo

Validar que las acciones reales realizadas desde el panel web de DASC Server Manager generan eventos en la base de datos remota `dasc_logs`.

## Estado

Cerrada.

## Entorno usado

| Rol | Máquina | IP privada DASC |
|---|---|---|
| API / Panel | lab-pruebas | 192.168.60.10 |
| DB / Logs | lab-db-gate02 | 192.168.60.20 |

## Tipo de prueba

Validación funcional de logs reales en arquitectura de 2 servidores.

Esta puerta continúa F6-GATE-02A, donde ya se había validado la conexión técnica API -> DB/logs.

En F6-GATE-02B se valida que el panel real genera eventos y que estos quedan registrados en la base remota.

## Situación inicial

Antes de usar el panel, la base `dasc_logs` contenía 3 eventos.

Consulta inicial:

~~~sql
USE dasc_logs;
SELECT COUNT(*) AS total_eventos FROM eventos;
~~~

Resultado inicial:

~~~text
total_eventos = 3
~~~

Los eventos existentes correspondían a:

- Validación inicial F6-GATE-02A.
- Inserción de prueba API -> DB.
- Acceso bloqueado no autenticado desde comprobación local.

## Acciones realizadas en el panel

Desde navegador se accedió al panel en:

~~~text
http://192.168.1.250:8000
~~~

Se realizaron acciones reales:

- Acceso al panel.
- Login correcto con usuario administrador.
- Entrada al panel principal.
- Acceso a la sección de logs.
- Acceso a la sección de servicios.
- Logout correcto.
- Intento de login fallido.

## Resultado en base de datos

Después de las acciones del panel, la base `dasc_logs` pasó de 3 a 16 eventos.

Consulta ejecutada:

~~~sql
USE dasc_logs;
SELECT COUNT(*) AS total_eventos FROM eventos;
~~~

Resultado:

~~~text
total_eventos = 16
~~~

## Eventos registrados

Se observaron eventos reales con:

- `origen = dasc-web`
- usuario real o `anon`
- IP de origen del navegador
- recurso solicitado
- resultado `OK` o `ERROR`
- detalle funcional

Ejemplos detectados:

~~~text
POST /login      OK      Inicio de sesión correcto
POST /logout     OK      Cierre de sesión correcto
POST /login      ERROR   Intento de inicio de sesión fallido
GET /logs        OK      HTTP 200
GET /servicios   OK      HTTP 200
GET /            ERROR   Acceso bloqueado por no autenticado
~~~

## Resumen por tipo y resultado

La consulta agrupada mostró:

~~~text
acceso          ERROR
acceso          OK
conexion_api_db OK
login           ERROR
login           OK
validacion      OK
~~~

Esto confirma que la tabla `eventos` recoge tanto eventos técnicos de validación como eventos reales del panel.

## Validación desde el panel

La vista de logs del panel mostró eventos cargados desde la base remota.

Se observaron:

- Total de eventos cargados.
- Eventos OK.
- Eventos ERROR.
- Listado de eventos DASC Web.
- Login correcto.
- Logout.
- Login fallido.
- Accesos a secciones del panel.

## Informe operativo

Desde `lab-pruebas` se ejecutó:

~~~bash
cd /opt/dasc/api
sudo ./tools/generate_operational_report.sh "DASC validacion eventos panel" "2026-05"
~~~

Resultado del informe:

~~~text
Estado: OK
Eventos totales: 16
Resultado: BASE OPERATIVA OK.
~~~

El informe operativo mostró últimos eventos reales del panel, incluyendo:

- Login fallido.
- Logout correcto.
- Accesos a `/logs`.
- Accesos a `/servicios`.
- Login correcto.
- Carga de recursos estáticos.

## Criterio de cierre

F6-GATE-02B se considera cerrada porque:

- El panel registra eventos reales.
- Los eventos se guardan en la base remota `dasc_logs`.
- La vista de logs del panel carga eventos desde la base.
- Se registran eventos OK y ERROR.
- Se registra login correcto.
- Se registra logout.
- Se registra login fallido.
- Se registran accesos bloqueados no autenticados.
- El informe operativo detecta la base de logs en estado OK.
- El informe operativo muestra eventos reales y concluye `BASE OPERATIVA OK`.

## Límites

Esta puerta no valida todavía:

- Backups reales.
- Restauraciones.
- SSH contra servidor de backups.
- Alertas Telegram reales.
- Informe final para cliente.
- Arquitectura Pro de 3 servidores.

## Próxima puerta recomendada

La siguiente puerta lógica es:

~~~text
F6-GATE-03 - Validación de backups en arquitectura de 2 servidores
~~~

También queda pendiente una mejora importante posterior:

~~~text
F6-GATE-04 - Instaladores parametrizables por perfil e IPs reales
~~~

## Conclusión

DASC Server Manager supera la validación de eventos reales del panel contra una base de datos remota.

Esto confirma que la arquitectura API + DB/logs en 2 servidores ya funciona a nivel operativo básico y no solo mediante pruebas artificiales.
