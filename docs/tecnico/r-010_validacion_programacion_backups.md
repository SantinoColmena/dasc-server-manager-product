# R-010 - Validación de la programación automática de backups

## Objetivo

Este documento define cómo validar la futura programación automática de backups de DASC Server Manager.

La validación busca comprobar que el sistema puede preparar tareas automáticas de copia sin romper el funcionamiento actual de los backups manuales.

## Qué se quiere validar

La programación automática debe permitir que una empresa no dependa de ejecutar backups manualmente desde el panel.

Debe poder responder a estas preguntas:

- Qué backup está programado.
- Cuándo se ejecuta.
- Qué tipo de backup realiza.
- Sobre qué base de datos trabaja.
- Si está activo o desactivado.
- Cuándo fue la última ejecución.
- Cuándo será la próxima ejecución.
- Qué resultado tuvo la última ejecución.
- Si el resultado quedó guardado en el historial.

## Relación con el motor de backups

La programación automática no debe crear una lógica separada.

Debe usar el mismo motor definido en R-008.

Flujo esperado:

~~~text
Tarea programada
  ↓
Motor centralizado de backups
  ↓
Script backups_api.sh
  ↓
Resultado normalizado
  ↓
backup_history
  ↓
eventos/logs
~~~

Esto evita tener dos formas distintas de ejecutar backups.

## Relación con el historial

Cada backup automático debe guardar un registro en `backup_history`.

El campo `origen` debe guardar:

~~~text
scheduled
~~~

Ejemplo:

~~~text
origen: scheduled
resultado: OK
tipo: full
base_datos: employees
~~~

Así se puede diferenciar un backup manual de un backup automático.

## Tabla esperada

La tabla propuesta para las programaciones es:

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

## Validación de frecuencias

El sistema debe aceptar como mínimo:

~~~text
daily
weekly
monthly
~~~

### daily

Debe ejecutar la tarea todos los días a una hora concreta.

Ejemplo:

~~~text
daily - 02:00
~~~

### weekly

Debe ejecutar la tarea una vez por semana.

Ejemplo:

~~~text
weekly - domingo - 03:00
~~~

### monthly

Debe ejecutar la tarea una vez al mes.

Ejemplo:

~~~text
monthly - día 1 - 04:00
~~~

## Validación de campos obligatorios

Antes de guardar una programación, se debe comprobar que existen:

- `nombre`
- `tipo_backup`
- `base_datos`
- `destino`
- `nombre_archivo`
- `frecuencia`
- `hora`

Si falta alguno, la tarea no debe guardarse.

## Validación de tipo de backup

Tipos válidos:

~~~text
full
incremental
differential
~~~

Resultado esperado:

- Si el tipo es válido, la programación se puede guardar.
- Si el tipo no es válido, se rechaza.
- No se debe crear una tarea con tipos desconocidos.

## Validación de hora

La hora debe tener formato claro.

Formato recomendado:

~~~text
HH:MM
~~~

Ejemplos válidos:

~~~text
02:00
14:30
23:45
~~~

Ejemplos inválidos:

~~~text
2
mañana
25:90
abc
~~~

## Validación de activación

Cada programación debe poder estar:

~~~text
activa
inactiva
~~~

Si `activo=1`, la tarea puede ejecutarse.

Si `activo=0`, la tarea queda guardada pero no se ejecuta.

Esto permite pausar programaciones sin eliminarlas.

## Validación de ejecución automática

Caso de prueba:

~~~text
nombre: Backup diario employees
tipo_backup: full
base_datos: employees
frecuencia: daily
hora: 02:00
activo: 1
~~~

Resultado esperado:

- La tarea queda guardada.
- El sistema calcula una próxima ejecución.
- Cuando se ejecuta, llama al motor de backups.
- El historial guarda el resultado con `origen=scheduled`.
- Los logs registran la acción.

## Validación de error

Si una tarea programada falla, el sistema debe:

- Guardar el intento en `backup_history`.
- Marcar resultado como `ERROR`.
- Guardar un mensaje claro.
- Registrar evento en logs.
- Preparar una futura alerta.

Ejemplo:

~~~text
resultado: ERROR
mensaje: No se pudo conectar con MariaDB
origen: scheduled
~~~

## Validación de compatibilidad

La programación automática no debe romper:

- Backups manuales.
- Ruta `/backups`.
- Script `backups_api.sh`.
- Historial persistente.
- Logs actuales.
- Instalador actual.
- Perfiles de instalación.

## Casos de prueba mínimos

### Caso 1 - Crear programación diaria

Entrada:

~~~text
frecuencia: daily
hora: 02:00
tipo_backup: full
base_datos: employees
~~~

Resultado esperado:

- Programación guardada correctamente.
- Estado activo.
- Próxima ejecución calculada.

### Caso 2 - Crear programación semanal

Entrada:

~~~text
frecuencia: weekly
dia_semana: domingo
hora: 03:00
tipo_backup: full
~~~

Resultado esperado:

- Programación guardada correctamente.
- Día semanal registrado.

### Caso 3 - Crear programación mensual

Entrada:

~~~text
frecuencia: monthly
dia_mes: 1
hora: 04:00
tipo_backup: full
~~~

Resultado esperado:

- Programación guardada correctamente.
- Día del mes registrado.

### Caso 4 - Desactivar programación

Entrada:

~~~text
activo: 0
~~~

Resultado esperado:

- La tarea queda guardada.
- No se ejecuta automáticamente.

### Caso 5 - Ejecución programada correcta

Resultado esperado:

- Se crea el backup.
- Se registra en historial.
- Se registra en logs.
- Se actualiza `ultima_ejecucion`.

### Caso 6 - Ejecución programada con error

Resultado esperado:

- Se guarda resultado ERROR.
- Se conserva mensaje técnico.
- No se oculta el fallo.

## Checklist de cierre

R-010 se considerará validada cuando se pueda marcar:

- [ ] Existe documento de diseño de programación automática.
- [ ] Existe documento de validación.
- [ ] Está definida la tabla `backup_schedules`.
- [ ] Están definidas las frecuencias mínimas.
- [ ] Está clara la relación con el motor de backups.
- [ ] Está clara la relación con `backup_history`.
- [ ] Está definido el origen `scheduled`.
- [ ] Está prevista la activación/desactivación de tareas.
- [ ] Está prevista la gestión de errores.
- [ ] No se rompe el backup manual actual.

## Estado

Estado actual: Diseño y validación documentados.

Prioridad: Alta.

Dependencias:

- R-008 - Motor centralizado de backups.
- R-009 - Historial persistente de backups.

Bloques siguientes:

- R-011 - Mejora de logs internos.
- R-012 - Limpieza de navegación y mensajes.
