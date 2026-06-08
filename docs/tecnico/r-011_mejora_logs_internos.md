# R-011 - Mejora de logs internos

## Objetivo

El objetivo de esta tarea es mejorar el sistema de logs internos de Vigex para que sea más útil, más claro y más preparado para un entorno real de producto.

Actualmente el sistema ya registra eventos básicos del panel, accesos, rutas visitadas y resultados HTTP. Esta base es correcta para el MVP, pero debe evolucionar para ofrecer mejor trazabilidad, diagnóstico y soporte.

R-011 busca ordenar qué debe registrar Vigex, cómo debe registrarlo y cómo debe mostrarse después al usuario o al técnico.

## Situación actual

El proyecto ya dispone de un sistema de logs funcional.

Actualmente se registran eventos en una base de datos de logs mediante una tabla de eventos.

La API utiliza una función de registro y un middleware que intercepta peticiones para guardar información como:

- Origen.
- Tipo.
- Usuario.
- IP de origen.
- Recurso.
- Resultado.
- Detalle.

Esto permite saber qué acciones han ocurrido dentro del panel.

## Problema actual

Aunque el sistema de logs ya funciona, todavía tiene limitaciones:

- Algunos eventos son demasiado genéricos.
- No siempre se diferencia claramente una acción real de una simple visita.
- Los errores podrían ser más descriptivos.
- No existe todavía una clasificación avanzada por severidad.
- No se separan bien eventos de acceso, backups, servicios, administración y sistema.
- No todos los módulos generan logs con el mismo nivel de detalle.
- Todavía no existe una vista avanzada de diagnóstico.
- No hay una relación clara entre logs, historial de backups y futuras alertas.

## Objetivo técnico

El sistema de logs debe permitir responder preguntas como:

- Quién ha accedido al panel.
- Quién ha intentado acceder sin permisos.
- Qué usuario ejecutó un backup.
- Qué usuario reinició un servicio.
- Qué acción falló.
- Desde qué IP se hizo una operación.
- Qué recurso fue afectado.
- Qué mensaje técnico dejó el sistema.
- Qué eventos deberían generar una alerta.

## Tipos de evento previstos

Se propone normalizar los tipos de evento internos.

| Tipo | Uso |
|---|---|
| `login` | Inicios y cierres de sesión |
| `access` | Accesos a páginas del panel |
| `permission` | Accesos bloqueados por permisos |
| `backup` | Ejecución de backups |
| `service` | Acciones sobre servicios |
| `admin` | Gestión de usuarios y permisos |
| `system` | Eventos internos del sistema |
| `error` | Errores técnicos no clasificados |

## Severidad de eventos

Además del resultado `OK` o `ERROR`, conviene añadir una severidad.

Valores recomendados:

| Severidad | Uso |
|---|---|
| `info` | Evento normal |
| `warning` | Evento que requiere atención |
| `error` | Error operativo |
| `critical` | Error grave o posible impacto importante |

Ejemplos:

~~~text
info: usuario admin entra al panel
warning: usuario intenta acceder sin permisos
error: falla un backup
critical: no se puede conectar con la base de logs o backups
~~~

## Resultado del evento

El resultado debe mantenerse simple:

~~~text
OK
ERROR
~~~

Esto permite filtrar rápidamente acciones correctas y fallidas.

La severidad añade contexto, pero el resultado indica si la operación salió bien o mal.

## Campos recomendados

La tabla actual de eventos ya contiene campos importantes.

A futuro podría ampliarse con:

| Campo | Descripción |
|---|---|
| `id` | Identificador del evento |
| `fecha` | Fecha del evento |
| `origen` | Módulo o componente que genera el evento |
| `tipo` | Tipo de evento |
| `severidad` | Nivel de importancia |
| `usuario` | Usuario relacionado |
| `ip_origen` | IP desde la que se hizo la acción |
| `recurso` | Ruta, servicio, backup o elemento afectado |
| `resultado` | OK o ERROR |
| `detalle` | Mensaje resumido |
| `metadata` | Información adicional en formato JSON |

## Tabla de eventos mejorada

Modelo futuro propuesto:

~~~sql
CREATE TABLE IF NOT EXISTS eventos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    origen VARCHAR(40) NOT NULL,
    tipo VARCHAR(40) NOT NULL,
    severidad VARCHAR(20) DEFAULT 'info',
    usuario VARCHAR(60) DEFAULT NULL,
    ip_origen VARCHAR(45) DEFAULT NULL,
    recurso VARCHAR(120) DEFAULT NULL,
    resultado ENUM('OK','ERROR') NOT NULL,
    detalle VARCHAR(255) DEFAULT NULL,
    metadata JSON DEFAULT NULL
);
~~~

## Compatibilidad con la tabla actual

Para no romper el MVP, la mejora debe ser progresiva.

La tabla actual puede seguir funcionando con los campos existentes.

Los nuevos campos como `severidad` o `metadata` pueden añadirse más adelante mediante migración.

Decisión recomendada:

- Mantener tabla actual por compatibilidad.
- Documentar campos futuros.
- Mejorar primero la calidad de los mensajes.
- Añadir severidad cuando se haga una migración controlada.

## Eventos mínimos que deben registrarse

### Login

Debe registrarse:

- Login correcto.
- Login fallido.
- Logout.
- Acceso bloqueado por no autenticado.

Ejemplo:

~~~text
tipo: login
usuario: admin
resultado: OK
detalle: Inicio de sesión correcto
~~~

## Permisos

Debe registrarse:

- Usuario sin permisos intentando acceder.
- Usuario no autenticado intentando entrar a una ruta protegida.
- Acceso a administración por usuario no administrador.

Ejemplo:

~~~text
tipo: permission
usuario: daniel
resultado: ERROR
detalle: Acceso denegado a /admin/usuarios
~~~

## Backups

Debe registrarse:

- Backup iniciado.
- Backup finalizado correctamente.
- Backup fallido.
- Error de SSH.
- Error de MariaDB.
- Error de permisos o parámetros.

Ejemplo:

~~~text
tipo: backup
usuario: admin
resultado: OK
detalle: Backup full de employees creado correctamente
~~~

## Servicios

Debe registrarse:

- Servicio iniciado.
- Servicio detenido.
- Servicio reiniciado.
- Error al controlar servicio.
- Servicio no encontrado.

Ejemplo:

~~~text
tipo: service
usuario: admin
resultado: OK
detalle: Servicio cron.service reiniciado correctamente
~~~

## Administración

Debe registrarse:

- Usuario creado.
- Usuario eliminado.
- Intento de crear usuario duplicado.
- Cambio de permisos.
- Acción administrativa rechazada.

Ejemplo:

~~~text
tipo: admin
usuario: admin
resultado: OK
detalle: Usuario daniel creado con permisos logs y servicios
~~~

## Sistema

Debe registrarse:

- Arranque de la aplicación.
- Error de conexión con base de logs.
- Error de lectura de `users.json`.
- Error de configuración.
- Fallos internos no asociados a una ruta concreta.

Ejemplo:

~~~text
tipo: system
usuario: system
resultado: ERROR
detalle: No se pudo conectar con LOGS_DB_HOST
~~~

## Relación con R-009

El historial de backups no sustituye a los logs.

Cuando se ejecuta un backup, deben ocurrir dos registros:

1. Un evento en `eventos`.
2. Un registro en `backup_history`.

Ejemplo:

~~~text
eventos: el usuario admin ejecutó un backup con resultado OK
backup_history: backup full employees guardado en backup-20260522.sql.gz
~~~

## Relación con alertas

Los logs serán la base para futuras alertas.

Eventos que podrían generar alerta:

- Backup fallido.
- Error crítico de sistema.
- Servicio importante detenido.
- Acceso denegado repetido.
- Fallo de conexión con la base de datos.
- No existen backups recientes.

Esto conecta con el módulo de alertas de Telegram.

## Vista prevista en el panel

La vista de logs debería permitir:

- Ver eventos recientes.
- Filtrar por tipo.
- Filtrar por resultado.
- Filtrar por usuario.
- Buscar por texto.
- Diferenciar OK y ERROR visualmente.
- Ver detalles técnicos sin saturar la tabla.

Columnas recomendadas:

| Fecha | Tipo | Usuario | IP | Recurso | Resultado | Detalle |
|---|---|---|---|---|---|---|

Campos futuros:

- Severidad.
- Metadata.
- Acción relacionada.
- ID de backup asociado.

## Criterio de salida

R-011 se considerará completada cuando:

- Quede documentada la mejora de logs internos.
- Estén definidos los tipos de evento.
- Esté definida la severidad futura.
- Estén definidos los eventos mínimos por módulo.
- Esté clara la relación con historial de backups.
- Esté clara la relación con futuras alertas.
- Se mantenga compatibilidad con el sistema actual.
- Se prepare la mejora visual de logs para R-012.

## Decisión actual

Para mantener estabilidad, no se debe rehacer el sistema de logs de golpe.

Primero:

1. Mejorar documentación.
2. Normalizar nombres de tipos.
3. Mejorar mensajes de detalle.
4. Añadir filtros visuales.
5. Añadir severidad cuando exista migración.
6. Conectar alertas en fases posteriores.

## Estado

Estado actual: Pendiente de implementación.

Prioridad: Alta.

Dependencias:

- R-008 - Motor centralizado de backups.
- R-009 - Historial persistente de backups.
- R-010 - Programación automática de backups.

Bloque siguiente:

- R-012 - Limpieza de navegación y mensajes.
