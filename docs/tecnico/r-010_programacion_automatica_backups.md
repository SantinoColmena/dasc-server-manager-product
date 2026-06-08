# R-010 - Programación automática de backups

## Objetivo

El objetivo de esta tarea es definir el sistema de programación automática de backups de Vigex.

Hasta ahora, el sistema permite ejecutar backups manuales desde el panel. Esto es útil, pero para un producto real no es suficiente. Una empresa necesita que las copias se ejecuten de forma automática, con una planificación clara y sin depender de que un usuario recuerde pulsar un botón.

R-010 define cómo debe funcionar la programación automática de backups y cómo se relaciona con el motor centralizado de backups y el historial persistente.

## Problema actual

En el MVP, la ejecución de backups depende principalmente de una acción manual desde el panel.

Esto tiene varias limitaciones:

- El usuario puede olvidarse de hacer copias.
- No existe una planificación recurrente.
- No se puede garantizar una política de copias diaria o semanal.
- No se puede demostrar una estrategia de mantenimiento continua.
- No se puede ofrecer fácilmente como servicio gestionado.
- No se puede diferenciar entre backup manual y backup automático.

Para convertir Vigex en un producto más serio, debe existir una capa de programación automática.

## Relación con R-008 y R-009

R-008 define el motor centralizado de backups.

R-009 define el historial persistente.

R-010 debe apoyarse en ambos.

El flujo esperado es:

~~~text
Programación automática
  ↓
Ejecuta tarea en fecha/hora definida
  ↓
Llama al motor central de backups
  ↓
El motor ejecuta backups_api.sh
  ↓
Se guarda resultado en backup_history
  ↓
Se registra evento en logs
  ↓
Se notifica el resultado si existen alertas
~~~

## Tipos de programación previstos

El sistema debe estar preparado para soportar varios tipos de programación.

### 1. Backup diario

Ejecuta una copia cada día a una hora concreta.

Ejemplo:

~~~text
Todos los días a las 02:00
~~~

Uso recomendado:

- Bases de datos pequeñas o medianas.
- Clientes que necesitan una copia diaria.
- Entornos con cambios frecuentes.

### 2. Backup semanal

Ejecuta una copia un día concreto de la semana.

Ejemplo:

~~~text
Todos los domingos a las 03:00
~~~

Uso recomendado:

- Copias completas semanales.
- Entornos con menos cambios.
- Estrategia combinada con incrementales diarios.

### 3. Backup mensual

Ejecuta una copia una vez al mes.

Ejemplo:

~~~text
Día 1 de cada mes a las 04:00
~~~

Uso recomendado:

- Copias de archivo.
- Retención larga.
- Puntos de recuperación mensuales.

### 4. Programación combinada

En una versión más avanzada se podrá combinar:

- Full semanal.
- Incremental diario.
- Diferencial cada varios días.

Ejemplo:

~~~text
Domingo: backup completo
Lunes a sábado: backup incremental
~~~

## Datos que debe guardar una programación

Cada tarea programada debe guardar como mínimo:

| Campo | Descripción |
|---|---|
| `id` | Identificador único |
| `nombre` | Nombre visible de la tarea |
| `activo` | Indica si la tarea está activada |
| `tipo_backup` | full, incremental o differential |
| `base_datos` | Base de datos que se copiará |
| `destino` | Carpeta de destino |
| `nombre_archivo` | Plantilla de nombre del archivo |
| `compresion` | gzip o none |
| `retencion` | Días de conservación |
| `frecuencia` | daily, weekly o monthly |
| `hora` | Hora de ejecución |
| `dia_semana` | Día de la semana si aplica |
| `dia_mes` | Día del mes si aplica |
| `ultima_ejecucion` | Fecha de última ejecución |
| `proxima_ejecucion` | Fecha calculada de próxima ejecución |
| `notas` | Notas opcionales |

## Modelo de datos propuesto

Tabla propuesta:

~~~sql
CREATE TABLE IF NOT EXISTS backup_schedules (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    tipo_backup VARCHAR(30) NOT NULL,
    base_datos VARCHAR(120) NOT NULL,
    destino VARCHAR(255) NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    compresion VARCHAR(20) DEFAULT 'gzip',
    retencion INT DEFAULT 30,
    frecuencia VARCHAR(30) NOT NULL,
    hora VARCHAR(10) NOT NULL,
    dia_semana VARCHAR(20) DEFAULT NULL,
    dia_mes INT DEFAULT NULL,
    ultima_ejecucion DATETIME DEFAULT NULL,
    proxima_ejecucion DATETIME DEFAULT NULL,
    notas VARCHAR(255) DEFAULT NULL,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
~~~

## Ubicación recomendada

La tabla de programaciones puede guardarse en la misma base de control del sistema:

~~~text
vigex_logs
~~~

Aunque el nombre sea `vigex_logs`, esta base ya actúa como base interna de control de Vigex.

Puede contener:

- Eventos.
- Historial de backups.
- Programaciones de backups.
- Futuras alertas o auditoría.

## Opciones técnicas de implementación

Existen varias formas de ejecutar backups programados.

### Opción 1 - Cron del sistema

La opción más simple es usar `cron`.

Ventajas:

- Muy estable.
- Disponible en Linux.
- Fácil de entender.
- Adecuado para el MVP extendido.

Limitaciones:

- Menos flexible desde el panel.
- Hay que escribir o actualizar entradas en crontab.
- Puede ser menos cómodo para gestionar desde la interfaz web.

### Opción 2 - systemd timers

Otra opción es usar timers de systemd.

Ventajas:

- Integración moderna con Linux.
- Mejor control de servicios.
- Logs mediante journalctl.
- Más profesional.

Limitaciones:

- Algo más complejo que cron.
- Requiere generar unidades systemd.

### Opción 3 - Scheduler interno en Python

Otra opción es que la propia API tenga un proceso interno que revise tareas pendientes.

Ventajas:

- Más integrado con FastAPI.
- Más fácil de mostrar en panel.
- Permite guardar todo en base de datos.

Limitaciones:

- Hay que controlar bien reinicios.
- Si la API cae, no se ejecutan tareas.
- Requiere más cuidado para evitar ejecuciones duplicadas.

## Decisión recomendada inicial

Para una primera versión estable, la opción recomendada es:

~~~text
cron o systemd timer para ejecución real
base de datos para guardar la programación
motor centralizado para ejecutar el backup
~~~

De esta forma:

- La programación queda registrada.
- La ejecución se apoya en herramientas fiables del sistema.
- El backup pasa por el mismo motor que los backups manuales.
- El historial puede marcar el origen como `scheduled`.

## Origen scheduled

Cuando un backup sea ejecutado automáticamente, el historial debe guardar:

~~~text
origen: scheduled
~~~

Esto permitirá diferenciarlo de una copia manual.

Ejemplo:

~~~text
Backup full de employees creado automáticamente por tarea nocturna.
~~~

## Vista prevista en el panel

El panel debería tener una sección de programación con una tabla como:

| Nombre | Tipo | Base de datos | Frecuencia | Hora | Estado | Última ejecución | Acciones |
|---|---|---|---|---|---|---|---|

Acciones previstas:

- Crear programación.
- Activar.
- Desactivar.
- Editar.
- Eliminar.
- Ejecutar ahora.
- Ver historial asociado.

## Reglas mínimas de validación

Antes de guardar una programación, el sistema debe comprobar:

- El nombre no está vacío.
- El tipo de backup es válido.
- La base de datos no está vacía.
- La frecuencia es válida.
- La hora tiene formato correcto.
- La retención es un número válido.
- El destino no está vacío.
- El nombre de archivo no está vacío.

## Relación con alertas

En una versión posterior, cada backup programado podrá generar alertas.

Ejemplos:

- Avisar si el backup programado termina correctamente.
- Avisar si el backup programado falla.
- Avisar si una tarea lleva demasiado tiempo sin ejecutarse.
- Avisar si no existe ningún backup reciente.

Esto conecta con la parte de alertas de Telegram.

## Criterio de salida

R-010 se considerará completada cuando:

- Exista diseño de programación automática.
- Esté definida la tabla `backup_schedules`.
- Esté clara la relación con `backup_history`.
- Esté definido el origen `scheduled`.
- Estén claras las opciones cron, systemd timer y scheduler interno.
- Esté elegida una estrategia inicial.
- No se rompa el funcionamiento actual de backups manuales.

## Decisión actual

La decisión recomendada es no sustituir todavía el backup manual.

La programación automática debe añadirse como capa adicional.

Primero:

1. Guardar programaciones en base de datos.
2. Ejecutar tareas usando cron o systemd timer.
3. Pasar siempre por el motor centralizado.
4. Guardar resultados en `backup_history`.
5. Registrar eventos en logs.

## Estado

Estado actual: Pendiente de implementación.

Prioridad: Alta.

Dependencias:

- R-008 - Motor centralizado de backups.
- R-009 - Historial persistente de backups.

Bloques siguientes:

- R-011 - Mejora de logs internos.
- R-012 - Limpieza de navegación y mensajes.
