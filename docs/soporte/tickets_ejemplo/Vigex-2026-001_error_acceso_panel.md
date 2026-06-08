# Ticket soporte Vigex-2026-001 - Error de acceso al panel

## Datos generales

| Campo | Valor |
|---|---|
| ID ticket | Vigex-2026-001 |
| Fecha apertura | 2026-05-25 |
| Cliente | PyME Demo |
| Persona contacto | Responsable IT cliente |
| Canal entrada | Email |
| Plan | PyME |
| Responsable Vigex | Equipo Vigex |
| Estado | Cerrado |

## Clasificación

| Campo | Valor |
|---|---|
| Tipo | Incidencia |
| Prioridad | Alta |
| Servicio afectado | API / Panel |
| Entorno | Piloto |

## Descripción del cliente

~~~text
Buenos días,

No podemos acceder correctamente al panel Vigex.
Al entrar en la URL del panel nos redirige al login, pero necesitamos confirmar si el servicio está funcionando bien.

¿Podéis revisarlo?

Gracias.
~~~

## Evidencias recibidas

~~~text
El cliente indica que el panel redirige al login.
No aporta captura.
No indica caída completa del servidor.
~~~

## Diagnóstico técnico

Se revisa el servidor API.

Comprobaciones realizadas:

~~~bash
sudo systemctl is-active vigex-api
curl -I http://127.0.0.1:8000
sudo journalctl -u vigex-api -n 25 --no-pager
~~~

Resultado:

~~~text
vigex-api active
HTTP/1.1 303 See Other
location: /login
~~~

Interpretación:

La redirección a `/login` es comportamiento esperado cuando se accede al panel sin sesión iniciada.

Durante la revisión también se comprueba que la API puede registrar eventos en la base de logs remota.

## Acciones realizadas

| Fecha/hora | Acción | Responsable | Resultado |
|---|---|---|---|
| 2026-05-25 11:47 | Revisión estado servicio API | Equipo Vigex | Servicio activo |
| 2026-05-25 11:47 | Prueba HTTP local | Equipo Vigex | Redirección correcta a login |
| 2026-05-25 11:48 | Revisión de logs remotos | Equipo Vigex | Eventos registrados correctamente |
| 2026-05-25 11:48 | Confirmación con base `vigex_logs` | Equipo Vigex | Eventos 21 y 22 registrados |

## Comunicación al cliente

~~~text
Hola,

Hemos revisado el panel Vigex y el servicio está funcionando correctamente.

La respuesta 303 hacia `/login` es normal cuando se accede al panel sin una sesión iniciada. El servicio API está activo y responde correctamente.

También hemos comprobado que el sistema de logs registra eventos nuevos en la base remota, por lo que no se detecta caída del panel.

Podéis acceder introduciendo las credenciales habituales.

Un saludo,
Equipo Vigex
~~~

## Cierre

| Campo | Valor |
|---|---|
| Fecha cierre | 2026-05-25 |
| Resultado | Resuelto |
| Evidencia final | Servicio activo, HTTP 303 a login, eventos registrados |
| Requiere mejora futura | Sí |

## Mejora futura asociada

Añadir una explicación en la documentación de cliente indicando que la redirección a `/login` es normal cuando no hay sesión activa.

## Observaciones internas

Este ticket demuestra el flujo de soporte sin GitHub:

~~~text
Cliente contacta por email
Equipo Vigex revisa internamente
Se registra ticket
Se diagnostica
Se responde en lenguaje claro
Se cierra con evidencia
~~~
