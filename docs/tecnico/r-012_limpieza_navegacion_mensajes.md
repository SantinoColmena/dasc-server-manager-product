# R-012 - Limpieza de navegación y mensajes

## Objetivo

El objetivo de esta tarea es mejorar la navegación interna y los mensajes visibles de DASC Server Manager.

El MVP ya dispone de un panel funcional con secciones como:

- Panel principal.
- Copias.
- Logs.
- Servicios.
- Administración.

También existe control de permisos por usuario, de forma que no todos los usuarios ven las mismas secciones.

R-012 busca que esta navegación sea más coherente, más clara y más fácil de usar, evitando errores confusos o pantallas poco explicativas.

## Problema actual

Aunque el panel funciona, todavía pueden existir problemas de experiencia de usuario:

- Algunas páginas pueden tener menús diferentes.
- Algunos enlaces solo aparecen en unas vistas.
- Los mensajes de error pueden ser demasiado técnicos.
- Algunas redirecciones pueden no explicar bien qué ha pasado.
- No siempre se diferencia claramente entre error de permisos, error técnico y acción correcta.
- El usuario puede no entender si una sección no aparece por permisos o por fallo.
- Los mensajes de `ok` y `msg` están repartidos por varias vistas.

## Objetivo técnico

El sistema debe ofrecer una navegación coherente en todas las páginas.

El usuario debe entender siempre:

- Dónde está.
- Qué secciones tiene disponibles.
- Qué acciones puede realizar.
- Por qué no puede acceder a una sección.
- Si una acción ha funcionado.
- Si una acción ha fallado.
- Qué debe revisar en caso de error.

## Navegación esperada

Todas las páginas principales deben tener un menú lateral coherente.

Secciones previstas:

| Sección | Ruta | Permiso |
|---|---|---|
| Panel | `/` | Usuario autenticado |
| Copias | `/backups` | `backups` |
| Logs | `/logs` | `logs` |
| Servicios | `/servicios` | `servicios` |
| Administración | `/admin/usuarios` | Solo administrador |

## Reglas de visibilidad

El menú debe respetar estas reglas:

- El administrador ve todas las secciones.
- Un usuario normal solo ve las secciones para las que tiene permiso.
- Una sección no debe aparecer si el usuario no tiene permiso.
- Si el usuario intenta entrar manualmente por URL, debe recibir un mensaje claro.
- El botón de cerrar sesión debe estar disponible en todas las vistas privadas.

## Mensajes de permisos

Cuando un usuario no tenga permiso para acceder a una sección, el mensaje debe ser claro.

Ejemplo recomendado:

~~~text
No tienes permisos para acceder a esta sección.
~~~

No se recomienda mostrar mensajes técnicos como:

~~~text
403
Permission denied
Forbidden
~~~

El objetivo es que el usuario entienda el problema sin ver información interna.

## Mensajes de éxito

Las acciones correctas deben mostrar mensajes breves y claros.

Ejemplos:

~~~text
Backup ejecutado correctamente.
Servicio reiniciado correctamente.
Usuario creado correctamente.
Usuario eliminado correctamente.
~~~

## Mensajes de error

Los errores deben ser comprensibles.

Ejemplos:

~~~text
No se pudo ejecutar el backup. Revisa la conexión con el servidor de backups.
No se pudo reiniciar el servicio. Revisa permisos o nombre del servicio.
No se pudo cargar el historial de logs. Revisa la base de datos de logs.
Ese usuario ya existe.
Usuario o contraseña incorrectos.
~~~

## Tipos de mensajes

Se propone normalizar los mensajes visibles en estos tipos:

| Tipo | Uso |
|---|---|
| `success` | Acción completada correctamente |
| `error` | Acción fallida |
| `warning` | Aviso importante |
| `info` | Información general |

## Estilo visual recomendado

Los mensajes deberían tener colores y estilos consistentes:

| Tipo | Color sugerido |
|---|---|
| `success` | Verde |
| `error` | Rojo |
| `warning` | Amarillo/Naranja |
| `info` | Azul/Gris |

El objetivo no es solo decorar, sino ayudar al usuario a entender rápidamente el estado de la acción.

## Mensajes por módulo

### Login

Mensajes recomendados:

- Usuario o contraseña incorrectos.
- Sesión cerrada correctamente.
- Debes iniciar sesión para acceder al panel.

### Backups

Mensajes recomendados:

- Backup ejecutado correctamente.
- Error al ejecutar el backup.
- Tipo de backup no válido.
- La base de datos es obligatoria.
- No se pudo conectar con el servidor de backups.

### Servicios

Mensajes recomendados:

- Servicio iniciado correctamente.
- Servicio detenido correctamente.
- Servicio reiniciado correctamente.
- Acción no válida.
- No se pudo conectar con el servidor de servicios.

### Logs

Mensajes recomendados:

- No hay eventos para mostrar.
- No se pudo cargar la base de datos de logs.
- Mostrando últimos eventos registrados.

### Administración

Mensajes recomendados:

- Usuario creado correctamente.
- Usuario eliminado correctamente.
- Ese usuario ya existe.
- No puedes eliminar el usuario administrador.
- Usuario y contraseña son obligatorios.

## Centralización de mensajes

A futuro sería recomendable centralizar los mensajes en una función o estructura común.

Ejemplo conceptual:

~~~text
flash_message(type="success", text="Usuario creado correctamente")
flash_message(type="error", text="No se pudo ejecutar el backup")
~~~

En el MVP actual se puede mantener el uso de parámetros `ok` y `msg`, pero conviene documentar una evolución más limpia.

## Navegación activa

Cada página debe marcar visualmente la sección activa.

Ejemplo:

- En `/backups`, la sección Copias debe aparecer activa.
- En `/logs`, la sección Logs debe aparecer activa.
- En `/servicios`, la sección Servicios debe aparecer activa.
- En `/admin/usuarios`, la sección Administración debe aparecer activa.

Esto ayuda al usuario a ubicarse dentro del panel.

## Consistencia entre plantillas

Todas las plantillas privadas deberían compartir una estructura parecida:

~~~text
header
sidebar
main
topbar
contenido
mensaje
logout
~~~

Esto evita que cada página parezca una aplicación distinta.

## Mejora futura recomendada

Para evitar duplicar código HTML en cada plantilla, se recomienda crear una plantilla base.

Ejemplo:

~~~text
base.html
~~~

Y que las demás páginas extiendan esa base:

~~~text
index.html
backups.html
logs.html
servicios.html
admin_users.html
~~~

Esto permitiría mantener un único menú y un único sistema visual.

## Criterio de salida

R-012 se considerará completada cuando:

- Quede documentada la navegación esperada.
- Queden definidos los mensajes por módulo.
- Quede claro cómo deben mostrarse errores y éxitos.
- Quede documentada la visibilidad por permisos.
- Quede definida la navegación activa.
- Quede preparada la futura plantilla base.
- No se rompa el funcionamiento actual del MVP.

## Decisión actual

Para mantener estabilidad, no se debe rehacer todo el frontend de golpe.

La mejora debe hacerse progresivamente:

1. Documentar navegación.
2. Revisar menús por plantilla.
3. Normalizar textos de mensajes.
4. Mejorar mensajes de permisos.
5. Preparar una plantilla base futura.
6. Evitar cambios visuales grandes antes de una release interna.

## Estado

Estado actual: Pendiente de implementación.

Prioridad: Media-Alta.

Dependencias:

- R-011 - Mejora de logs internos.
- Sistema actual de permisos.
- Plantillas HTML del panel.

Bloques siguientes:

- R-013 - Laboratorio reproducible de pruebas.
- R-014 - Publicación versión interna 0.1.
