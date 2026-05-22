# R-011 - Validación de la mejora de logs internos

## Objetivo

Este documento define cómo validar la mejora del sistema de logs internos de DASC Server Manager.

La validación busca comprobar que los eventos registrados por el sistema son útiles, claros, consultables y preparados para soporte, auditoría y futuras alertas.

## Qué se quiere validar

El sistema de logs debe permitir entender qué ha pasado dentro del panel sin tener que revisar manualmente el código, la terminal o los servicios del sistema.

Debe responder a preguntas como:

- Quién ha iniciado sesión.
- Quién ha cerrado sesión.
- Quién ha intentado acceder sin permisos.
- Quién ha ejecutado un backup.
- Qué backup ha fallado.
- Qué servicio se ha reiniciado.
- Qué ruta ha generado error.
- Desde qué IP se hizo la acción.
- Qué usuario realizó la operación.
- Qué detalle técnico dejó el sistema.

## Validación de tipos de evento

Los tipos de evento recomendados son:

~~~text
login
access
permission
backup
service
admin
system
error
~~~

Resultado esperado:

- Cada evento debe tener un tipo claro.
- No todo debe registrarse como `acceso`.
- Las acciones importantes deben tener un tipo propio.
- Los errores deben poder filtrarse fácilmente.

## Validación de resultados

Los resultados principales deben ser:

~~~text
OK
ERROR
~~~

Resultado esperado:

- Las acciones correctas se guardan como `OK`.
- Las acciones fallidas se guardan como `ERROR`.
- No deben mezclarse textos distintos como `correcto`, `fallo`, `failed`, `success`, etc.
- El campo resultado debe ser fácil de filtrar.

## Validación de severidad futura

Aunque la tabla actual no tenga todavía severidad, queda definido el modelo futuro.

Severidades previstas:

~~~text
info
warning
error
critical
~~~

Uso esperado:

- `info`: evento normal.
- `warning`: evento que conviene revisar.
- `error`: fallo operativo.
- `critical`: fallo grave con posible impacto.

## Validación de login

Eventos que deben registrarse:

- Login correcto.
- Login fallido.
- Logout.
- Acceso bloqueado por no autenticado.

Ejemplo esperado:

~~~text
tipo: login
usuario: admin
resultado: OK
detalle: Inicio de sesión correcto
~~~

Ejemplo de error:

~~~text
tipo: login
usuario: anon
resultado: ERROR
detalle: Usuario o contraseña incorrectos
~~~

## Validación de permisos

Eventos que deben registrarse:

- Usuario sin permiso intentando acceder a una sección.
- Usuario no administrador intentando acceder a administración.
- Usuario no autenticado intentando acceder a una ruta protegida.

Ejemplo esperado:

~~~text
tipo: permission
usuario: daniel
resultado: ERROR
recurso: GET /admin/usuarios
detalle: Acceso denegado por falta de permisos
~~~

## Validación de backups

Eventos que deben registrarse:

- Backup iniciado.
- Backup correcto.
- Backup fallido.
- Error de SSH.
- Error de MariaDB.
- Parámetros incorrectos.

Ejemplo correcto:

~~~text
tipo: backup
usuario: admin
resultado: OK
detalle: Backup full de employees creado correctamente
~~~

Ejemplo con error:

~~~text
tipo: backup
usuario: admin
resultado: ERROR
detalle: Error ejecutando backups_api.sh en servidor remoto
~~~

## Validación de servicios

Eventos que deben registrarse:

- Servicio iniciado.
- Servicio detenido.
- Servicio reiniciado.
- Error al ejecutar acción.
- Servicio no encontrado.
- Acción no permitida.

Ejemplo esperado:

~~~text
tipo: service
usuario: admin
resultado: OK
detalle: Servicio cron.service reiniciado correctamente
~~~

Ejemplo con error:

~~~text
tipo: service
usuario: admin
resultado: ERROR
detalle: No se pudo reiniciar nginx.service
~~~

## Validación de administración

Eventos que deben registrarse:

- Usuario creado.
- Usuario eliminado.
- Intento de crear usuario duplicado.
- Intento de eliminar usuario inexistente.
- Cambio de permisos.
- Acceso rechazado a administración.

Ejemplo esperado:

~~~text
tipo: admin
usuario: admin
resultado: OK
detalle: Usuario daniel creado correctamente
~~~

## Validación de sistema

Eventos que deben registrarse:

- Arranque de la aplicación.
- Error de conexión con base de logs.
- Error leyendo usuarios.
- Error de configuración.
- Fallo interno no clasificado.

Ejemplo esperado:

~~~text
tipo: system
usuario: system
resultado: ERROR
detalle: No se pudo conectar con la base de logs
~~~

## Validación de relación con historial de backups

Cuando se ejecuta un backup deben existir dos niveles de información:

### Evento en logs

~~~text
El usuario admin ejecutó un backup con resultado OK.
~~~

### Registro en historial

~~~text
Backup full de employees guardado en /home/dasc/backups/backup-20260522.sql.gz.
~~~

Resultado esperado:

- El log registra la acción.
- El historial registra la copia concreta.
- No se sustituye una cosa por la otra.

## Validación de filtros futuros

La vista de logs debe quedar preparada para filtrar por:

- Fecha.
- Tipo.
- Usuario.
- Resultado.
- Recurso.
- Texto libre.
- Severidad futura.

Aunque no todos los filtros se implementen en esta tarea, deben estar previstos en el diseño.

## Validación visual

La vista de logs debe mostrar como mínimo:

| Fecha | Tipo | Usuario | IP | Recurso | Resultado | Detalle |
|---|---|---|---|---|---|---|

Resultado esperado:

- Los eventos OK se distinguen visualmente.
- Los eventos ERROR se distinguen visualmente.
- La tabla no debe ser confusa.
- El detalle debe ser corto pero útil.
- Los errores no deben mostrarse como mensajes técnicos imposibles de entender.

## Casos de prueba mínimos

### Caso 1 - Login correcto

Acción:

~~~text
Iniciar sesión como admin.
~~~

Resultado esperado:

- Evento tipo `login`.
- Resultado `OK`.
- Usuario `admin`.

### Caso 2 - Login fallido

Acción:

~~~text
Intentar iniciar sesión con contraseña incorrecta.
~~~

Resultado esperado:

- Evento tipo `login`.
- Resultado `ERROR`.
- Usuario `anon` o usuario indicado.
- Detalle claro.

### Caso 3 - Acceso sin permisos

Acción:

~~~text
Usuario sin permisos entra en /admin/usuarios.
~~~

Resultado esperado:

- Evento tipo `permission`.
- Resultado `ERROR`.
- Detalle de acceso denegado.

### Caso 4 - Backup correcto

Acción:

~~~text
Ejecutar backup desde el panel.
~~~

Resultado esperado:

- Evento tipo `backup`.
- Resultado `OK`.
- Detalle con tipo y base de datos.

### Caso 5 - Backup fallido

Acción:

~~~text
Ejecutar backup con base de datos incorrecta o servidor no disponible.
~~~

Resultado esperado:

- Evento tipo `backup`.
- Resultado `ERROR`.
- Detalle entendible.

### Caso 6 - Reinicio de servicio

Acción:

~~~text
Reiniciar un servicio desde el panel.
~~~

Resultado esperado:

- Evento tipo `service`.
- Resultado `OK` o `ERROR`.
- Detalle con nombre del servicio.

### Caso 7 - Crear usuario

Acción:

~~~text
Crear usuario desde administración.
~~~

Resultado esperado:

- Evento tipo `admin`.
- Resultado `OK`.
- Detalle con usuario creado.

## Validación de compatibilidad

La mejora de logs no debe romper:

- Login.
- Logout.
- Panel principal.
- Backups.
- Servicios.
- Administración de usuarios.
- Vista `/logs`.
- Base de datos actual de eventos.
- Funcionamiento del MVP.

## Checklist de cierre

R-011 se considerará validada cuando se pueda marcar:

- [ ] Existe documento de mejora de logs internos.
- [ ] Existe documento de validación.
- [ ] Están definidos los tipos de evento.
- [ ] Están definidos los resultados OK y ERROR.
- [ ] Está prevista la severidad futura.
- [ ] Están definidos eventos mínimos de login.
- [ ] Están definidos eventos mínimos de permisos.
- [ ] Están definidos eventos mínimos de backups.
- [ ] Están definidos eventos mínimos de servicios.
- [ ] Están definidos eventos mínimos de administración.
- [ ] Está clara la relación con historial de backups.
- [ ] Está clara la relación con futuras alertas.
- [ ] Se mantiene compatibilidad con la tabla actual.

## Estado

Estado actual: Diseño y validación documentados.

Prioridad: Alta.

Dependencias:

- R-008 - Motor centralizado de backups.
- R-009 - Historial persistente de backups.
- R-010 - Programación automática de backups.

Bloque siguiente:

- R-012 - Limpieza de navegación y mensajes.
