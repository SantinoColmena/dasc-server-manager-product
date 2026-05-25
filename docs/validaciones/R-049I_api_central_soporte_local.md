# R-049I - Prototipo local de API central de soporte

## Objetivo

Crear el primer prototipo gratuito de una API central DASC capaz de recibir incidencias desde paneles locales de cliente.

## Estado

Cerrada.

## Contexto

R-049H definió la arquitectura objetivo:

~~~text
Panel local del cliente
        ↓
API central DASC
        ↓
Panel central DASC
        ↓
Equipo técnico DASC
~~~

R-049I inicia la implementación local sin coste.

## Estructura creada

~~~text
deploy/central-support/package/
deploy/central-support/package/main.py
deploy/central-support/package/requirements.txt
deploy/central-support/package/templates/central_dashboard.html
deploy/central-support/package/data/
~~~

## Tecnología

~~~text
FastAPI
Uvicorn
SQLite
Jinja2
~~~

## Base de datos local

La API central crea:

~~~text
data/central_support.db
~~~

Tablas:

~~~text
central_clients
central_tickets
~~~

## Cliente demo

Se registra automáticamente un cliente demo:

~~~text
cliente-demo-a
Cliente Demo A
Token demo de laboratorio
~~~

## Endpoints creados

~~~text
GET /health
GET /
POST /api/v1/support/tickets
~~~

## Seguridad inicial

La recepción de tickets usa cabecera:

~~~text
X-DASC-Client-Token
~~~

El token se valida contra el cliente registrado en SQLite.

## Límite importante

El token incluido por defecto es solo de laboratorio.

No debe usarse en producción.

## Criterio de validación

R-049I se considera preparada cuando:

- `main.py` compila.
- La API central arranca localmente.
- `GET /health` responde OK.
- `GET /` muestra el panel central.
- `POST /api/v1/support/tickets` rechaza token incorrecto.
- `POST /api/v1/support/tickets` acepta token correcto.
- Se crea un ticket central.
- El ticket aparece en el panel central.
- Se confirma que no hay coste de licencia.

## Próximo paso

Validar localmente con `uvicorn` y `curl`.

## Conclusión

R-049I crea la primera base técnica del futuro panel central DASC multi-cliente sin depender de herramientas externas de pago.
