# R-008 - Validación del motor centralizado de backups

## Objetivo

Este documento define cómo validar que la futura centralización del motor de backups de DASC Server Manager tiene sentido y no rompe el funcionamiento actual del MVP.

La validación se centra en comprobar que la lógica de backups queda mejor organizada, que los datos necesarios están claros y que el sistema queda preparado para historial, programación automática y restauración futura.

## Qué se quiere validar

La tarea R-008 no consiste únicamente en que el botón de backup funcione.

El objetivo real es comprobar que el sistema queda preparado para crecer.

Por tanto, se debe validar que existe una separación clara entre:

- Interfaz web.
- Ruta FastAPI.
- Motor de backups.
- Script de ejecución.
- Registro de logs.
- Futuro historial persistente.

## Flujo esperado

El flujo correcto debe ser:

~~~text
Usuario
  ↓
Panel web /backups
  ↓
FastAPI
  ↓
Motor central de backups
  ↓
Script backups_api.sh
  ↓
Resultado normalizado
  ↓
Logs e historial
  ↓
Respuesta al usuario
~~~

## Validación del formulario web

El formulario de backups debe recoger como mínimo:

- Tipo de backup.
- Base de datos.
- Carpeta destino.
- Nombre del archivo.
- Compresión.
- Retención.
- Referencia base.
- Notas.

Comprobación esperada:

- El usuario puede lanzar una copia desde el panel.
- El formulario no debe depender de valores ocultos imposibles de modificar.
- El tipo de backup debe enviarse correctamente.
- La base de datos debe llegar al backend.
- La respuesta debe mostrarse de forma clara.

## Validación de FastAPI

FastAPI debe actuar como punto de entrada, pero no debería acumular toda la lógica de backup.

Debe encargarse de:

- Comprobar permisos.
- Recibir datos del formulario.
- Preparar la solicitud.
- Llamar al motor de backups.
- Devolver una respuesta al usuario.

FastAPI no debería convertirse en un bloque gigante donde se mezclan validaciones, SSH, parseo, historial y mensajes.

## Validación del motor de backups

El motor central debe encargarse de la lógica principal.

Debe validar:

- Que el tipo de backup sea válido.
- Que la base de datos no esté vacía.
- Que el destino sea correcto.
- Que el nombre de archivo sea aceptable.
- Que la retención tenga sentido.
- Que la compresión sea válida.

Tipos permitidos:

~~~text
full
incremental
differential
~~~

## Validación del script backups_api.sh

El script debe seguir siendo el encargado de ejecutar la operación real.

Debe comprobarse que puede recibir parámetros como:

~~~bash
backups_api.sh full employees /home/dasc/backups backup-YYYYMMDD-HHMM.sql gzip 30 manual prueba
~~~

Resultado esperado:

- Si funciona, devuelve un mensaje que empiece por `OK`.
- Si falla, devuelve un mensaje claro que empiece por `ERROR`.
- No debe dejar salidas ambiguas difíciles de interpretar.

## Resultado normalizado

El motor debe transformar la salida del script en un resultado claro.

Ejemplo de resultado correcto:

~~~text
estado: OK
tipo: full
base_datos: employees
archivo: /home/dasc/backups/backup-20260522-1830.sql.gz
mensaje: Backup creado correctamente
~~~

Ejemplo de resultado con error:

~~~text
estado: ERROR
tipo: full
base_datos: employees
archivo: -
mensaje: No se pudo conectar con MariaDB
~~~

## Validación de logs

Cada ejecución de backup debe generar un evento.

El evento debe incluir:

- Usuario.
- Tipo de acción.
- Resultado.
- Recurso afectado.
- Detalle del error o éxito.

Ejemplo:

~~~text
tipo: backup
usuario: admin
recurso: POST /backups/run
resultado: OK
detalle: Backup full de employees creado correctamente
~~~

## Validación de compatibilidad

La centralización del motor de backups no debe romper el MVP actual.

Debe seguir funcionando:

- La ruta `/backups`.
- El formulario de creación de copias.
- La ejecución por SSH.
- El script `backups_api.sh`.
- Los mensajes de éxito o error.
- El sistema de logs existente.

## Casos de prueba mínimos

### Caso 1 - Backup completo correcto

Entrada:

~~~text
tipo: full
base_datos: employees
destino: /home/dasc/backups
nombre: backup-YYYYMMDD-HHMM.sql
compresion: gzip
retencion: 30
~~~

Resultado esperado:

- Se crea el backup.
- Se muestra mensaje OK.
- Se registra evento en logs.

### Caso 2 - Tipo de backup no válido

Entrada:

~~~text
tipo: prueba
~~~

Resultado esperado:

- El sistema rechaza la solicitud.
- No ejecuta el script.
- Muestra error claro.

### Caso 3 - Base de datos vacía

Entrada:

~~~text
base_datos:
~~~

Resultado esperado:

- El sistema rechaza la solicitud.
- No ejecuta backup.
- Muestra mensaje de validación.

### Caso 4 - Error de SSH

Situación:

- El servidor de backups no responde.
- La clave SSH no está configurada.
- El usuario remoto no existe.

Resultado esperado:

- El panel no se queda bloqueado.
- Se muestra error.
- Se registra evento con resultado ERROR.

### Caso 5 - Error de MariaDB

Situación:

- La base de datos no responde.
- El usuario de backup no tiene permisos.
- La base indicada no existe.

Resultado esperado:

- El script devuelve ERROR.
- El motor interpreta el fallo.
- El panel muestra mensaje entendible.

## Checklist de cierre

R-008 se considerará validada cuando se pueda marcar:

- [ ] Existe documento del motor centralizado.
- [ ] Está definido el flujo Panel → FastAPI → Motor → Script.
- [ ] Están definidos los tipos de backup.
- [ ] Están definidas las validaciones mínimas.
- [ ] Está definido el resultado esperado.
- [ ] Está definido cómo registrar logs.
- [ ] Se mantiene compatibilidad con el MVP actual.
- [ ] Queda preparada la conexión con R-009.
- [ ] Queda preparada la conexión con R-010.

## Estado

Estado actual: Diseño y validación documentados.

Prioridad: Alta.

Dependencias:

- R-006 - Configuración por perfiles.
- R-007 - Instalador base idempotente.

Bloques siguientes:

- R-009 - Historial persistente de backups.
- R-010 - Programación automática de backups.
