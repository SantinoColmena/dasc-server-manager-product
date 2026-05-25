# R-049L - Enviar tickets desde panel local hacia API central

## Objetivo

Conectar el panel local del cliente con la API central DASC para enviar tickets de soporte al panel central multi-cliente.

## Estado

En curso.

## Contexto

R-049I creó la API central local de soporte.

R-049J añadió detalle de ticket central.

R-049K añadió gestión de estado y prioridad en el panel central.

R-049L conecta el panel local con el panel central.

## Archivos modificados

~~~text
deploy/api/package/main.py
~~~

## Funcionamiento

Cuando se crea un ticket local en:

~~~text
POST /soporte
~~~

el sistema:

~~~text
1. Guarda el ticket local en SQLite.
2. Intenta enviarlo a la API central DASC.
3. Registra el resultado en logs.
4. No bloquea la creación local si falla la API central.
~~~

## Endpoint central usado

~~~text
POST /api/v1/support/tickets
~~~

## Cabecera usada

~~~text
X-DASC-Client-Token
~~~

## Variables de configuración

~~~text
CENTRAL_SUPPORT_ENABLED
CENTRAL_SUPPORT_URL
CENTRAL_SUPPORT_CLIENT_ID
CENTRAL_SUPPORT_CLIENT_NAME
CENTRAL_SUPPORT_TOKEN
CENTRAL_SUPPORT_TIMEOUT
~~~

## Ejemplo de configuración de laboratorio

~~~text
CENTRAL_SUPPORT_ENABLED=true
CENTRAL_SUPPORT_URL=http://127.0.0.1:8010/api/v1/support/tickets
CENTRAL_SUPPORT_CLIENT_ID=cliente-demo-a
CENTRAL_SUPPORT_CLIENT_NAME=Cliente Demo A
CENTRAL_SUPPORT_TOKEN=dasc-central-demo-token-lab
CENTRAL_SUPPORT_TIMEOUT=5
~~~

## Seguridad

El token usado en laboratorio no debe utilizarse en producción.

En producción debe existir un token único por cliente y rotación controlada.

## Comportamiento si la API central falla

El ticket local se mantiene creado.

El panel muestra aviso de que no se pudo enviar al panel central.

El error queda registrado en los logs.

## Criterio de validación

R-049L se considera preparada cuando:

- `main.py` compila.
- `dasc-api` arranca.
- `central-support` arranca.
- Se activa la integración central en `config.env`.
- Se crea un ticket nuevo desde `/soporte`.
- El ticket queda guardado localmente.
- El ticket aparece en el panel central.
- El panel central crea un nuevo `CENTRAL-2026-XXXX`.
- El ticket central conserva `ticket_local_id`.
- Los logs registran el envío.
- Si la API central está caída, el ticket local no se pierde.

## Límites

Esta tarea todavía no incluye:

- Sincronización de estado central hacia panel local.
- Guardar `central_ticket_id` dentro del SQLite local.
- Reintentos automáticos.
- Cola de envío offline.
- HTTPS real.
- Tokens rotables desde UI.
- Panel cliente separado definitivo.

## Próximo paso

Validar en `lab-pruebas`.

## Conclusión

R-049L inicia la conexión real entre el panel local del cliente y el panel central DASC, manteniendo coste de licencia cero.
