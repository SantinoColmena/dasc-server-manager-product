# R-012 - Validación de limpieza de navegación y mensajes

## Objetivo

Este documento define cómo validar que la navegación interna y los mensajes visibles de Vigex son claros, coherentes y adecuados para una versión más estable del producto.

La validación busca comprobar que el usuario entiende qué puede hacer, dónde está dentro del panel y qué ha ocurrido después de cada acción.

## Qué se quiere validar

La tarea R-012 debe validar principalmente:

- Coherencia del menú lateral.
- Visibilidad correcta según permisos.
- Mensajes claros de éxito.
- Mensajes claros de error.
- Mensajes claros de permisos.
- Navegación activa por sección.
- Botón de cierre de sesión disponible.
- Experiencia consistente entre páginas.

## Secciones principales

Las secciones principales del panel son:

| Sección | Ruta | Condición |
|---|---|---|
| Panel | `/` | Usuario autenticado |
| Copias | `/backups` | Permiso `backups` o admin |
| Logs | `/logs` | Permiso `logs` o admin |
| Servicios | `/servicios` | Permiso `servicios` o admin |
| Administración | `/admin/usuarios` | Solo admin |

## Validación del menú lateral

El menú debe cumplir:

- El administrador ve todas las secciones.
- Un usuario normal solo ve sus secciones permitidas.
- Una sección sin permiso no debe aparecer.
- El menú debe mantener un orden lógico.
- El menú debe ser similar en todas las páginas.
- La sección actual debe aparecer marcada como activa.

## Validación de usuario administrador

Caso de prueba:

~~~text
Iniciar sesión como admin.
~~~

Resultado esperado:

- Ve Panel.
- Ve Copias.
- Ve Logs.
- Ve Servicios.
- Ve Administración.
- Puede acceder a todas las rutas.
- El botón de cerrar sesión aparece disponible.

## Validación de usuario con permisos limitados

Caso de prueba:

~~~text
Usuario con permisos: logs, servicios.
~~~

Resultado esperado:

- Ve Panel.
- Ve Logs.
- Ve Servicios.
- No ve Copias si no tiene permiso.
- No ve Administración.
- Si intenta entrar manualmente en una ruta no permitida, recibe mensaje claro.

## Validación de acceso manual sin permisos

Caso de prueba:

~~~text
Usuario sin permiso de backups accede manualmente a /backups.
~~~

Resultado esperado:

~~~text
No tienes permisos para acceder a esta sección.
~~~

No debe mostrar:

~~~text
403
Forbidden
Traceback
Error interno
~~~

## Validación de mensajes de éxito

Los mensajes de éxito deben ser breves y entendibles.

Ejemplos válidos:

~~~text
Backup ejecutado correctamente.
Servicio reiniciado correctamente.
Usuario creado correctamente.
Usuario eliminado correctamente.
Sesión cerrada correctamente.
~~~

Resultado esperado:

- El mensaje se muestra en la página correcta.
- El usuario entiende que la acción se completó.
- El texto no es excesivamente técnico.

## Validación de mensajes de error

Los mensajes de error deben explicar el problema sin saturar al usuario.

Ejemplos válidos:

~~~text
No se pudo ejecutar el backup. Revisa la conexión con el servidor de backups.
No se pudo reiniciar el servicio. Revisa permisos o nombre del servicio.
No se pudo cargar la base de datos de logs.
Usuario o contraseña incorrectos.
Ese usuario ya existe.
~~~

Resultado esperado:

- El error es visible.
- El usuario entiende qué ha fallado.
- No se muestra información sensible.
- No se muestra un traceback de Python.

## Validación de tipos de mensaje

Los tipos previstos son:

~~~text
success
error
warning
info
~~~

Resultado esperado:

- `success` para acciones correctas.
- `error` para acciones fallidas.
- `warning` para avisos importantes.
- `info` para información general.

## Validación visual

Los mensajes deben distinguirse visualmente.

| Tipo | Resultado esperado |
|---|---|
| `success` | Mensaje positivo, normalmente verde |
| `error` | Mensaje de fallo, normalmente rojo |
| `warning` | Aviso destacado |
| `info` | Información neutra |

No hace falta que todos los estilos estén implementados en esta fase, pero el diseño debe quedar preparado.

## Validación de navegación activa

Cada página debe marcar su sección activa:

| Ruta | Sección activa esperada |
|---|---|
| `/` | Panel |
| `/backups` | Copias |
| `/logs` | Logs |
| `/servicios` | Servicios |
| `/admin/usuarios` | Administración |

Resultado esperado:

- El usuario sabe en qué sección está.
- No aparecen varias secciones activas a la vez.
- No falta la sección activa en páginas principales.

## Validación de logout

Todas las páginas privadas deben permitir cerrar sesión.

Páginas a comprobar:

- `/`
- `/backups`
- `/logs`
- `/servicios`
- `/admin/usuarios`

Resultado esperado:

- Existe botón de cerrar sesión.
- El botón funciona.
- Después de cerrar sesión, el usuario vuelve a `/login`.
- No puede volver al panel sin autenticarse.

## Validación de login

La pantalla de login debe mostrar:

- Campo de usuario.
- Campo de contraseña.
- Botón de entrada.
- Mensaje claro si las credenciales son incorrectas.

Resultado esperado:

~~~text
Usuario o contraseña incorrectos.
~~~

## Validación de backups

Acciones a comprobar:

- Entrar en `/backups`.
- Ejecutar backup correcto.
- Ejecutar backup con error.
- Enviar tipo no válido si se prueba desde backend.
- Comprobar mensaje final.

Resultado esperado:

- Mensaje correcto si funciona.
- Mensaje claro si falla.
- No se queda la pantalla en blanco.
- No aparece traceback.

## Validación de servicios

Acciones a comprobar:

- Entrar en `/servicios`.
- Reiniciar un servicio válido.
- Intentar acción no válida.
- Probar error de conexión SSH si aplica.

Resultado esperado:

- Mensaje claro.
- Tabla de servicios visible.
- Resultado OK o ERROR entendible.

## Validación de logs

Acciones a comprobar:

- Entrar en `/logs`.
- Ver eventos recientes.
- Comprobar caso sin eventos.
- Comprobar error de conexión con base de logs si aplica.

Resultado esperado:

- Si hay eventos, se muestran ordenados.
- Si no hay eventos, aparece mensaje claro.
- Si falla la carga, no se rompe la página.

## Validación de administración

Acciones a comprobar:

- Crear usuario.
- Crear usuario duplicado.
- Crear usuario sin contraseña.
- Eliminar usuario.
- Intentar eliminar admin.

Resultado esperado:

- Usuario creado correctamente.
- Ese usuario ya existe.
- Usuario y contraseña son obligatorios.
- Usuario eliminado correctamente.
- No puedes eliminar el usuario administrador.

## Validación de consistencia entre plantillas

Todas las páginas privadas deberían tener una estructura parecida:

~~~text
header
sidebar
topbar
contenido principal
mensaje de estado
logout
~~~

Resultado esperado:

- No parece que cada página pertenezca a una aplicación distinta.
- El usuario no se pierde al cambiar de sección.
- Los botones y mensajes mantienen estilo coherente.

## Validación de plantilla base futura

Aunque no se implemente todavía, debe quedar preparada la idea de una futura plantilla:

~~~text
base.html
~~~

Objetivo futuro:

- Evitar duplicar menú en cada HTML.
- Evitar inconsistencias entre páginas.
- Centralizar header, sidebar, mensajes y logout.

## Casos de prueba mínimos

### Caso 1 - Admin navega por todo el panel

Resultado esperado:

- Puede acceder a todas las secciones.
- Menú completo.
- Logout visible.

### Caso 2 - Usuario limitado navega por el panel

Resultado esperado:

- Solo ve sus secciones.
- No ve administración.
- No puede acceder manualmente a secciones prohibidas.

### Caso 3 - Acción correcta

Resultado esperado:

- Mensaje de éxito claro.
- Evento registrado en logs.

### Caso 4 - Acción con error

Resultado esperado:

- Mensaje de error claro.
- No aparece traceback.
- Evento registrado como ERROR.

### Caso 5 - Cierre de sesión

Resultado esperado:

- Sesión cerrada.
- Redirección a login.
- Rutas privadas protegidas.

## Validación de compatibilidad

La limpieza de navegación y mensajes no debe romper:

- Login.
- Logout.
- Permisos.
- Backups.
- Logs.
- Servicios.
- Administración.
- Estilos CSS actuales.
- Plantillas HTML actuales.

## Checklist de cierre

R-012 se considerará validada cuando se pueda marcar:

- [ ] Existe documento de limpieza de navegación y mensajes.
- [ ] Existe documento de validación.
- [ ] Está definido el menú esperado.
- [ ] Están definidas las reglas de visibilidad.
- [ ] Están definidos mensajes de permisos.
- [ ] Están definidos mensajes de éxito.
- [ ] Están definidos mensajes de error.
- [ ] Está definida la navegación activa.
- [ ] Está validado el logout en páginas privadas.
- [ ] Está preparada la futura plantilla base.
- [ ] Se mantiene compatibilidad con el MVP.

## Estado

Estado actual: Diseño y validación documentados.

Prioridad: Media-Alta.

Dependencias:

- R-011 - Mejora de logs internos.
- Sistema actual de permisos.
- Plantillas HTML del panel.

Bloques siguientes:

- R-013 - Laboratorio reproducible de pruebas.
- R-014 - Publicación versión interna 0.1.
