# R-049Q - Cierre login y roles del panel central

## Objetivo

Cerrar la validación del login básico y control de sesión del panel central DASC.

## Estado

Cerrada.

## Funcionalidad implementada

R-049Q protege las vistas HTML del panel central mediante autenticación de sesión.

El panel central ya no queda abierto directamente al acceder por navegador.

## Archivos modificados

~~~text
deploy/central-support/package/main.py
deploy/central-support/package/requirements.txt
deploy/central-support/package/templates/central_login.html
deploy/central-support/package/templates/central_dashboard.html
deploy/central-support/package/templates/central_ticket_detail.html
~~~

## Documento de validación

~~~text
docs/validaciones/R-049Q_login_roles_panel_central.md
~~~

## Dependencia añadida

Se añadió:

~~~text
itsdangerous>=2.1.2
~~~

para soportar sesiones mediante `SessionMiddleware`.

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

## Rutas API mantenidas por token

Las rutas API no se protegieron con sesión web para no romper la integración local-central:

~~~text
POST /api/v1/support/tickets
GET /api/v1/support/tickets/{ticket_id}
~~~

Estas rutas siguen funcionando mediante:

~~~text
X-DASC-Client-ID
X-DASC-Client-Token
~~~

## Validación sin sesión

Se comprobó:

~~~text
GET /
HTTP 303
location: /login?msg=Sesion+requerida
~~~

También:

~~~text
GET /tickets/CENTRAL-2026-0001
HTTP 303
location: /login?msg=Sesion+requerida
~~~

## Validación de login administrador

Se validó:

~~~text
POST /login admin/admin
HTTP 303
location: /
~~~

Con la cookie de sesión, se comprobó:

~~~text
GET /
HTTP 200

GET /tickets/CENTRAL-2026-0001
HTTP 200
~~~

## Validación de login técnico

Se validó:

~~~text
POST /login tecnico/tecnico
HTTP 303
location: /
~~~

Con la cookie de sesión del técnico, se comprobó:

~~~text
GET /
HTTP 200
~~~

También se validó una acción protegida:

~~~text
POST /tickets/CENTRAL-2026-0001/estado
HTTP 303
location: /tickets/CENTRAL-2026-0001?msg=Sin+cambios
~~~

El resultado `Sin cambios` no representa error. Indica que el ticket ya estaba en el estado y prioridad enviados.

## Validación de logout

Se comprobó:

~~~text
GET /logout
HTTP 303
location: /login?msg=Sesion+cerrada
set-cookie: session=null
~~~

## Validación en navegador

Se comprobó visualmente:

~~~text
/login muestra formulario de acceso.
dashboard autenticado muestra sesión activa.
dashboard muestra botón Cerrar sesión.
logout devuelve a la pantalla de login.
~~~

## Validación de API tras añadir login

Se comprobó que la API sigue funcionando sin sesión web:

~~~text
GET /api/v1/support/tickets/CENTRAL-2026-0001
ok: true
ticket_local_id: DASC-2026-005
estado: En curso
prioridad: Media
~~~

## Usuarios de laboratorio

Usuarios válidos de laboratorio:

~~~text
admin / admin
tecnico / tecnico
~~~

Estos valores no deben mantenerse en producción.

## Variables de entorno añadidas

~~~text
DASC_CENTRAL_AUTH_ENABLED
DASC_CENTRAL_SECRET_KEY
DASC_CENTRAL_ADMIN_USER
DASC_CENTRAL_ADMIN_PASSWORD
DASC_CENTRAL_TECH_USER
DASC_CENTRAL_TECH_PASSWORD
~~~

## Validación técnica

Se comprobó:

~~~text
central-support actualizado: OK
requirements instalados: OK
itsdangerous instalado: OK
main.py central compila: OK
central-support arranca: OK
health central: OK
SessionMiddleware cargado: OK
central_login.html detectado: OK
redirección sin sesión: OK
login admin/admin: OK
dashboard con sesión admin: OK
detalle con sesión admin: OK
login tecnico/tecnico: OK
dashboard con sesión técnico: OK
acción protegida con técnico: OK
logout: OK
API por token sigue funcionando: OK
~~~

## Resultado

R-049Q queda validada correctamente.

El panel central DASC ya no queda abierto sin autenticación y mantiene la integración API con los paneles locales.

## Límites actuales

Esta versión todavía no incluye:

- Hash de contraseñas.
- Usuarios guardados en base de datos.
- Gestión visual de usuarios.
- Separación estricta de permisos entre admin y técnico.
- Bloqueo por intentos fallidos.
- 2FA.
- HTTPS.
- Cookies seguras endurecidas para producción.

## Próxima tarea recomendada

~~~text
R-049R - Instalador systemd para central-support
~~~

También queda pendiente:

~~~text
R-049S - Reintento automático mediante systemd timer
R-049T - Mejoras visuales del panel central
R-049U - Endurecimiento de credenciales del panel central
~~~

## Conclusión

DASC Server Manager supera R-049Q.

El panel central queda protegido por login, sin romper las APIs de sincronización usadas por los paneles locales.
