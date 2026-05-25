# R-049I - Cierre prototipo local de API central de soporte

## Objetivo

Cerrar la validación del primer prototipo local de API central DASC para recepción de incidencias multi-cliente.

## Estado

Cerrada.

## Funcionalidad implementada

Se creó una nueva estructura independiente para el futuro panel/API central DASC:

~~~text
deploy/central-support/package/
deploy/central-support/package/main.py
deploy/central-support/package/requirements.txt
deploy/central-support/package/templates/central_dashboard.html
~~~

## Tecnología usada

~~~text
FastAPI
Uvicorn
SQLite
Jinja2
~~~

## Endpoints validados

~~~text
GET /health
GET /
POST /api/v1/support/tickets
~~~

## Despliegue de laboratorio

La API central se ejecutó en `lab-pruebas` usando el puerto:

~~~text
8010
~~~

URL de validación:

~~~text
http://192.168.1.250:8010/
~~~

## Validación técnica

Se comprobó:

~~~text
main.py central compila: OK
API central arranca: OK
GET /health responde OK: OK
Panel central carga en navegador: OK
Base SQLite central creada: OK
Cliente demo creado: OK
~~~

## Validación de seguridad inicial

Se comprobó la validación por token de cliente mediante cabecera:

~~~text
X-DASC-Client-Token
~~~

Resultado:

~~~text
Token incorrecto: HTTP 401 Unauthorized
Token correcto: ticket aceptado
~~~

## Ticket central creado

Se creó correctamente el primer ticket centralizado:

~~~text
CENTRAL-2026-0001
~~~

Datos principales:

~~~text
cliente_id: cliente-demo-a
nombre_cliente: Cliente Demo A
ticket_local_id: DASC-2026-002
tipo: Consulta
prioridad: Alta
servicio: Soporte
estado: Nuevo
contacto: Responsable IT
email: soporte-sqlite@dasc.local
origen: panel-local
~~~

## Validación SQLite

La base:

~~~text
deploy/central-support/package/data/central_support.db
~~~

contiene:

~~~text
central_clients
central_tickets
~~~

Se confirmó que existe el cliente demo:

~~~text
cliente-demo-a
Cliente Demo A
activo: 1
~~~

Y el ticket:

~~~text
CENTRAL-2026-0001
~~~

## Validación visual

El panel central muestra:

~~~text
DASC Central Support
Total tickets: 1
Modo: Local
Coste licencia: 0 €
CENTRAL-2026-0001
Cliente Demo A
DASC-2026-002
Alta
Nuevo
Soporte
Responsable IT
~~~

## Fix aplicado

Durante la validación se detectó un error `Internal Server Error` al abrir `GET /`.

La causa fue la llamada antigua a `TemplateResponse`.

Se corrigió usando la firma moderna:

~~~text
templates.TemplateResponse(request, "central_dashboard.html", context)
~~~

Tras el fix, el panel central cargó correctamente en navegador.

## Resultado

R-049I queda validada correctamente.

DASC Server Manager ya dispone de una primera API central local capaz de:

- Registrar clientes demo.
- Validar token por cliente.
- Recibir incidencias por API.
- Guardar tickets centralizados en SQLite.
- Mostrar tickets en un panel central.
- Funcionar sin coste de licencia.

## Límites actuales

Esta versión todavía no incluye:

- Login del panel central.
- Roles `dasc_tecnico`, `dasc_admin`, `dasc_superadmin`.
- Detalle de ticket central.
- Cambio de estado central.
- Integración automática con el panel local.
- HTTPS real.
- Tokens seguros rotables desde UI.
- Despliegue como servicio systemd.
- Dominio o VPS público.
- Integración Jira/Zammad.

## Próxima tarea recomendada

~~~text
R-049J - Detalle de ticket en panel central
~~~

También se puede plantear después:

~~~text
R-049K - Envío desde panel local hacia API central
R-049L - Instalador/systemd para central-support
R-049M - Roles y login del panel central
~~~

## Conclusión

DASC Server Manager supera R-049I.

El proyecto ya tiene una primera base real y gratuita para evolucionar hacia soporte centralizado multi-cliente propio.
