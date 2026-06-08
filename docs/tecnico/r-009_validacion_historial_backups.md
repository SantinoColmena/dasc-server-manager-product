# R-009 - Validación del historial persistente de backups

## Objetivo

Este documento define cómo validar el historial persistente de backups de Vigex.

La validación busca comprobar que cada copia de seguridad queda registrada de forma estructurada y que el sistema no depende únicamente de mensajes temporales o de listar archivos en una carpeta.

## Qué se quiere validar

El historial persistente debe permitir responder a estas preguntas:

- Qué backup se creó.
- Cuándo se creó.
- Qué usuario lo ejecutó.
- Qué tipo de copia era.
- Qué base de datos se copió.
- Qué archivo se generó.
- Dónde se guardó.
- Si terminó correctamente o con error.
- Qué mensaje técnico dejó el sistema.
- Si depende de otro backup base.

## Diferencia entre log e historial

La validación debe comprobar que el sistema diferencia entre logs e historial.

### Log

El log registra una acción del sistema.

Ejemplo:

~~~text
El usuario admin ejecutó POST /backups/run con resultado OK.
~~~

### Historial

El historial registra una copia concreta.

Ejemplo:

~~~text
Backup full de employees creado en /home/vigex/backups/backup-20260522.sql.gz.
~~~

Ambos datos son útiles, pero no sustituyen uno al otro.

## Tabla esperada

La tabla propuesta es:

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

## Validación de campos obligatorios

Cada registro debe tener como mínimo:

- `fecha`
- `tipo`
- `base_datos`
- `resultado`
- `origen`

Además, si el backup termina correctamente, debería guardar:

- `archivo`
- `destino`
- `usuario`
- `mensaje`

## Validación de tipos de backup

El historial debe aceptar los tipos previstos:

~~~text
full
incremental
differential
~~~

Resultado esperado:

- `full` se guarda correctamente.
- `incremental` se guarda correctamente.
- `differential` se guarda correctamente.
- Un tipo no válido debe ser rechazado antes de guardar.

## Validación de resultado OK

Caso de prueba:

~~~text
tipo: full
base_datos: employees
archivo: /home/vigex/backups/backup-20260522.sql.gz
resultado: OK
usuario: admin
origen: manual
~~~

Resultado esperado:

- Se crea el archivo de backup.
- Se inserta un registro en `backup_history`.
- El registro queda marcado como `OK`.
- El panel puede mostrarlo en el historial.

## Validación de resultado ERROR

Caso de prueba:

~~~text
tipo: full
base_datos: employees
archivo: -
resultado: ERROR
usuario: admin
origen: manual
mensaje: No se pudo conectar con MariaDB
~~~

Resultado esperado:

- No se oculta el error.
- Se guarda el intento fallido.
- El historial permite saber que hubo un fallo.
- El log también registra el evento como ERROR.

## Validación de origen

El campo `origen` debe permitir distinguir cómo se lanzó el backup.

Valores previstos:

| Valor | Uso |
|---|---|
| `manual` | Backup ejecutado desde el panel |
| `scheduled` | Backup ejecutado automáticamente |
| `api` | Backup ejecutado desde integración o endpoint |
| `system` | Backup ejecutado internamente |

En R-009 debe quedar preparado `manual`.

En R-010 se añadirá `scheduled`.

## Validación de referencia base

Para backups incrementales y diferenciales debe existir el campo:

~~~text
referencia_base
~~~

En la primera versión puede estar vacío, pero debe estar preparado para guardar:

- Último backup completo.
- Último backup incremental.
- Cadena de restauración.
- Punto base de recuperación.

## Validación de vista en el panel

La futura vista de historial debe poder mostrar como mínimo:

| Fecha | Tipo | Base de datos | Archivo | Usuario | Resultado |
|---|---|---|---|---|---|

Acciones futuras previstas:

- Ver detalle.
- Descargar.
- Restaurar.
- Eliminar.

En esta fase no es obligatorio implementar todas las acciones, pero el historial debe prepararlas.

## Casos de prueba mínimos

### Caso 1 - Backup completo correcto

Entrada:

~~~text
tipo: full
base_datos: employees
resultado: OK
origen: manual
~~~

Resultado esperado:

- Registro insertado en `backup_history`.
- Resultado visible como OK.
- Archivo asociado guardado.

### Caso 2 - Backup con error

Entrada:

~~~text
tipo: full
base_datos: employees
resultado: ERROR
mensaje: Error de conexión
origen: manual
~~~

Resultado esperado:

- Registro insertado igualmente.
- Resultado visible como ERROR.
- Mensaje de error conservado.

### Caso 3 - Backup incremental

Entrada:

~~~text
tipo: incremental
base_datos: employees
referencia_base: backup-full-001
resultado: OK
~~~

Resultado esperado:

- Registro insertado.
- Se conserva la referencia base.

### Caso 4 - Backup diferencial

Entrada:

~~~text
tipo: differential
base_datos: employees
referencia_base: backup-full-001
resultado: OK
~~~

Resultado esperado:

- Registro insertado.
- Se conserva la referencia al último completo.

### Caso 5 - Consulta de historial

Consulta esperada:

~~~sql
SELECT id, fecha, tipo, base_datos, archivo, usuario, resultado
FROM backup_history
ORDER BY fecha DESC
LIMIT 100;
~~~

Resultado esperado:

- Devuelve los últimos backups.
- Ordena del más reciente al más antiguo.
- Permite alimentar la tabla del panel.

## Validación de compatibilidad

La incorporación del historial no debe romper:

- La ejecución manual actual.
- La ruta `/backups`.
- El script `backups_api.sh`.
- Los logs existentes.
- Los mensajes de éxito o error.
- La futura programación automática.

## Checklist de cierre

R-009 se considerará validada cuando se pueda marcar:

- [ ] Existe documento de diseño del historial persistente.
- [ ] Existe documento de validación del historial.
- [ ] Está definida la tabla `backup_history`.
- [ ] Está clara la diferencia entre logs e historial.
- [ ] Están definidos los campos mínimos.
- [ ] Está definido cómo guardar resultados OK y ERROR.
- [ ] Está preparado el campo `origen`.
- [ ] Está preparado el campo `referencia_base`.
- [ ] Está preparada la relación con R-010.
- [ ] Está preparada la relación con restauración futura.

## Estado

Estado actual: Diseño y validación documentados.

Prioridad: Alta.

Dependencias:

- R-008 - Motor centralizado de backups.

Bloque siguiente:

- R-010 - Programación automática de backups.
