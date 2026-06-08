# R-009 - Historial persistente de backups

## Objetivo

El objetivo de esta tarea es definir un historial persistente para las copias de seguridad de Vigex.

Actualmente el sistema puede ejecutar backups desde el panel, pero para evolucionar hacia un producto real es necesario guardar información estructurada de cada copia realizada.

El historial persistente permitirá consultar qué backups existen, cuándo se hicieron, quién los lanzó, qué tipo de copia eran, si terminaron correctamente y qué archivo generaron.

## Problema actual

En el MVP, el resultado de una copia se muestra principalmente como un mensaje después de ejecutar el backup.

Esto permite comprobar si la acción ha funcionado, pero no es suficiente para un producto real porque:

- No queda un historial completo de backups.
- No se puede consultar fácilmente qué copias existen.
- No se puede saber qué usuario lanzó cada copia.
- No se puede preparar restauración de forma segura.
- No se puede relacionar un backup incremental o diferencial con su backup base.
- No se puede mostrar una tabla avanzada en el panel.
- No se puede auditar correctamente el ciclo de vida de las copias.

## Relación con R-008

R-008 define el motor centralizado de backups.

R-009 se apoya en ese motor para guardar cada ejecución en un historial persistente.

El flujo esperado sería:

~~~text
Usuario ejecuta backup
  ↓
FastAPI recibe la petición
  ↓
Motor central de backups valida y ejecuta
  ↓
Script backups_api.sh genera el archivo
  ↓
Motor interpreta el resultado
  ↓
Se registra en logs
  ↓
Se guarda en historial persistente
  ↓
El panel muestra el resultado
~~~

## Información que debe guardar el historial

Cada backup debe guardar como mínimo:

| Campo | Descripción |
|---|---|
| `id` | Identificador único del backup |
| `fecha` | Fecha y hora de creación |
| `tipo` | Tipo de backup: full, incremental o differential |
| `base_datos` | Base de datos copiada |
| `archivo` | Ruta o nombre del archivo generado |
| `destino` | Carpeta donde se guardó |
| `tamano_bytes` | Tamaño del archivo, si está disponible |
| `usuario` | Usuario que ejecutó la copia |
| `resultado` | OK o ERROR |
| `mensaje` | Mensaje técnico o resumen del resultado |
| `referencia_base` | Backup base usado para incremental/diferencial |
| `origen` | Origen de la ejecución: manual, programado o API |
| `notas` | Notas opcionales del usuario |

## Modelo de datos propuesto

La tabla propuesta para guardar el historial es:

~~~sql
CREATE TABLE IF NOT EXISTS backup_history (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo VARCHAR(30) NOT NULL,
    base_datos VARCHAR(120) NOT NULL,
    archivo VARCHAR(255) DEFAULT NULL,
    destino VARCHAR(255) DEFAULT NULL,
    tamano_bytes BIGINT DEFAULT NULL,
    usuario VARCHAR(80) DEFAULT NULL,
    resultado ENUM('OK','ERROR') NOT NULL,
    mensaje VARCHAR(255) DEFAULT NULL,
    referencia_base VARCHAR(255) DEFAULT NULL,
    origen VARCHAR(40) DEFAULT 'manual',
    notas VARCHAR(255) DEFAULT NULL
);
~~~

## Ubicación recomendada

Para mantener coherencia con el sistema actual de logs, el historial puede guardarse en la misma base de datos de auditoría:

~~~text
vigex_logs
~~~

Esto permite separar los datos funcionales del cliente de los datos de control de Vigex.

La base de datos principal del cliente no debe llenarse con información interna del panel.

## Diferencia entre logs e historial

Los logs y el historial no son exactamente lo mismo.

### Logs

Los logs responden a la pregunta:

~~~text
¿Qué acción ocurrió en el sistema?
~~~

Ejemplo:

~~~text
El usuario admin ejecutó POST /backups/run con resultado OK.
~~~

### Historial de backups

El historial responde a la pregunta:

~~~text
¿Qué copia de seguridad se creó y qué información tiene?
~~~

Ejemplo:

~~~text
Backup full de employees creado en /home/vigex/backups/backup-20260522.sql.gz.
~~~

Ambos sistemas se complementan.

## Estados posibles

El historial debe soportar como mínimo dos estados:

~~~text
OK
ERROR
~~~

En una versión posterior podrían añadirse estados adicionales:

~~~text
RUNNING
DELETED
RESTORED
FAILED
PARTIAL
~~~

Para la primera versión es suficiente con `OK` y `ERROR`.

## Origen de la ejecución

El campo `origen` permitirá distinguir de dónde viene el backup.

Valores previstos:

| Origen | Significado |
|---|---|
| `manual` | Backup lanzado desde el panel |
| `scheduled` | Backup lanzado por programación automática |
| `api` | Backup lanzado desde un endpoint o integración |
| `system` | Backup lanzado internamente por mantenimiento |

Esto será importante para R-010, donde se prepararán backups programados.

## Relación con restauración

El historial persistente será necesario para futuras funciones de restauración.

Antes de restaurar un backup, el sistema debería poder consultar:

- Qué archivo se va a restaurar.
- Qué tipo de backup es.
- A qué base de datos pertenece.
- Cuándo fue creado.
- Si fue generado correctamente.
- Si depende de un backup completo anterior.
- Si forma parte de una cadena incremental.

Por eso R-009 es una base necesaria antes de una restauración seria.

## Relación con eliminación de backups

El historial también permitirá controlar la eliminación.

Cuando se elimine una copia, el sistema podrá:

- Saber qué archivo corresponde.
- Registrar quién la eliminó.
- Marcar el backup como eliminado.
- Evitar eliminar copias base necesarias para incrementales o diferenciales.

En la primera versión no es obligatorio implementar todo esto, pero el modelo debe quedar preparado.

## Vista prevista en el panel

El panel debería mostrar una tabla de historial con columnas como:

| Fecha | Tipo | Base de datos | Archivo | Usuario | Resultado | Acciones |
|---|---|---|---|---|---|---|

Acciones futuras:

- Descargar.
- Restaurar.
- Eliminar.
- Ver detalle.

## Criterio de salida

R-009 se considerará completada cuando:

- Exista un diseño de historial persistente.
- Esté definido qué campos se guardan.
- Esté clara la diferencia entre logs e historial.
- Esté decidido dónde guardar el historial.
- Esté preparada la relación con restauración.
- Esté preparada la relación con backups programados.
- No se rompa el funcionamiento actual del MVP.

## Decisión actual

Para mantener estabilidad, la primera versión del historial debe ser sencilla.

Decisión recomendada:

- Guardar el historial en la base `vigex_logs`.
- Crear una tabla `backup_history`.
- Registrar backups manuales primero.
- Añadir backups programados después en R-010.
- Mantener logs de eventos separados del historial de copias.

## Estado

Estado actual: Pendiente de implementación.

Prioridad: Alta.

Dependencias:

- R-008 - Motor centralizado de backups.

Bloques siguientes:

- R-010 - Programación automática de backups.
- Restauración avanzada en fases posteriores.
