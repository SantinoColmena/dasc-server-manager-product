# R-049Q - Login y roles del panel central

## Objetivo

Añadir autenticación básica al panel central DASC para evitar que las vistas HTML internas queden abiertas.

## Estado

En curso.

## Contexto

El panel central ya permite:

~~~text
Ver tickets centralizados.
Consultar detalle de tickets.
Cambiar estado y prioridad.
Exponer API de recepción y consulta para paneles locales.
~~~

Por tanto, las rutas HTML deben quedar protegidas con login.

## Archivos modificados

~~~text
deploy/central-support/package/main.py
deploy/central-support/package/templates/central_login.html
deploy/central-support/package/templates/central_dashboard.html
deploy/central-support/package/templates/central_ticket_detail.html
~~~

## Rutas añadidas

~~~text
GET /login
POST /login
GET /logout
~~~

## Rutas HTML protegidas

~~~text
GET /
GET /tickets/{ticket_id}
POST /tickets/{ticket_id}/estado
~~~

## Rutas API no modificadas

Las rutas API se mantienen protegidas mediante token de cliente:

~~~text
POST /api/v1/support/tickets
GET /api/v1/support/tickets/{ticket_id}
~~~

No se protegen con sesion web para no romper la comunicacion panel local -> panel central.

## Variables de entorno nuevas

~~~text
DASC_CENTRAL_AUTH_ENABLED
DASC_CENTRAL_SECRET_KEY
DASC_CENTRAL_ADMIN_USER
DASC_CENTRAL_ADMIN_PASSWORD
DASC_CENTRAL_TECH_USER
DASC_CENTRAL_TECH_PASSWORD
~~~

## Usuarios por defecto de laboratorio

~~~text
admin / admin
tecnico / tecnico
~~~

Estos valores son solo para laboratorio.

En producto real deben cambiarse obligatoriamente.

## Roles iniciales

~~~text
admin
tecnico
~~~

En esta primera version ambos pueden acceder al panel central y modificar tickets.

## Criterio de validacion

R-049Q queda preparada cuando:

- `main.py` compila.
- `central-support` arranca.
- `/` redirige a `/login` si no hay sesion.
- `/tickets/{id}` redirige a `/login` si no hay sesion.
- Login con admin/admin funciona.
- Login con tecnico/tecnico funciona.
- Logout cierra la sesion.
- Las rutas API siguen funcionando con token.
- El cambio de estado central sigue funcionando tras login.
- La sincronizacion local desde central sigue funcionando.

## Limites

Esta version todavia no incluye:

- Hash de contrasenas.
- Gestion de usuarios en base de datos.
- Politica avanzada de roles.
- Bloqueo por intentos fallidos.
- 2FA.
- HTTPS.
- Cookies seguras para produccion.

## Proximo paso

Validar en `lab-pruebas`.

## Conclusion

R-049Q protege el panel central con autenticacion basica sin romper las APIs usadas por los paneles locales.
