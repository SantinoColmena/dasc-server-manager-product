# R-049G - Separar acceso cliente y soporte técnico

## Objetivo

Asegurar que la gestión interna de tickets de soporte queda reservada al equipo técnico DASC y no expuesta al cliente.

## Estado

En curso.

## Contexto

R-049A implementó formulario básico de soporte.

R-049B migró tickets a SQLite.

R-049C añadió vista interna.

R-049D añadió estado, prioridad e historial.

R-049E añadió plantillas de respuesta.

R-049F añadió resumen manual para Jira/Zammad.

Después se decide aclarar que estas funciones son internas y no deben exponerse como panel de cliente.

## Cambios aplicados

Archivo modificado:

~~~text
deploy/api/package/main.py
~~~

Templates modificados:

~~~text
deploy/api/package/templates/index.html
~~~

Documento creado:

~~~text
docs/soporte/separacion_cliente_tecnico_soporte.md
~~~

## Rutas restringidas

Se restringen a administradores/técnicos:

~~~text
GET /soporte
POST /soporte
GET /soporte/tickets
GET /soporte/tickets/{ticket_id}
POST /soporte/tickets/{ticket_id}/estado
~~~

## Motivo

El cliente no debe ver:

~~~text
Historial interno
Resumen Jira/Zammad
Plantillas internas
Prioridades internas
Tickets de otros clientes
Herramientas técnicas
~~~

## Panel cliente futuro

Queda pendiente una vista separada para cliente, orientada a:

~~~text
Historial de copias
Informes
Estado general
Solicitud simple
Mis solicitudes
~~~

## Criterio de validación

R-049G se considera preparada cuando:

- `main.py` compila.
- `dasc-api` arranca.
- Un usuario admin puede entrar a `/soporte`.
- Un usuario admin puede entrar a `/soporte/tickets`.
- Un usuario admin puede abrir `DASC-2026-002`.
- Un usuario no admin no ve la tarjeta de soporte.
- Un usuario no admin no puede acceder a `/soporte/tickets`.
- La ruta restringida redirige al panel con mensaje de permisos.
- No se rompe la gestión técnica ya creada.

## Conclusión

R-049G corrige el enfoque de producto: la gestión de soporte es interna del equipo DASC y el panel cliente deberá diseñarse aparte.
