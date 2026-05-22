# R-008 - Centralizar motor de backups

## Objetivo

El objetivo de esta tarea es centralizar la lógica de backups de DASC Server Manager en un único motor claro, mantenible y preparado para crecer.

Actualmente el proyecto ya permite ejecutar backups desde el panel web mediante FastAPI y un script Bash remoto. Esta solución funciona para el MVP, pero de cara a convertir el proyecto en producto es necesario ordenar mejor la lógica de copias.

La idea de R-008 no es cambiar toda la funcionalidad de golpe, sino definir una arquitectura más limpia para que los backups completos, incrementales, diferenciales, el historial, la restauración y la programación automática puedan apoyarse sobre una base común.

## Problema actual

En el MVP, la lógica de backups está repartida entre varias piezas:

- El formulario HTML del panel.
- Las rutas de FastAPI.
- El script `backups_api.sh`.
- La conexión SSH hacia el servidor de backups.
- La configuración de IPs y rutas.
- La salida textual del script.
- La redirección del resultado al panel.

Esto es válido para demostrar el funcionamiento, pero tiene limitaciones:

- Es más difícil mantener el sistema.
- Es más difícil añadir nuevos tipos de backup.
- Es más difícil registrar historial de forma estructurada.
- Es más difícil diferenciar entre backup completo, incremental y diferencial.
- Es más difícil reutilizar la lógica desde otros módulos.
- Es más difícil probar el sistema sin tocar la interfaz.

## Objetivo técnico

El sistema debería evolucionar hacia un motor central de backups que reciba una petición estructurada y devuelva un resultado también estructurado.

La idea sería pasar de una lógica basada únicamente en texto a una lógica más clara.

Ejemplo de petición:

~~~text
tipo: full
base_datos: employees
destino: /home/dasc/backups
nombre: backup-YYYYMMDD-HHMM.sql.gz
compresion: gzip
retencion: 30
origen: panel-web
usuario: admin
~~~

Ejemplo de resultado:

~~~text
estado: OK
tipo: full
archivo: /home/dasc/backups/backup-20260522-1830.sql.gz
fecha: 2026-05-22 18:30
mensaje: Backup completo creado correctamente
~~~

## Tipos de backup previstos

El motor debe estar preparado para soportar tres tipos de copia.

### 1. Backup completo

El backup completo copia toda la base de datos.

Es el tipo de backup más simple y el más importante para la base del sistema.

Uso previsto:

- Primera copia de seguridad.
- Copia manual antes de cambios importantes.
- Punto base para diferenciales e incrementales.

### 2. Backup incremental

El backup incremental debe guardar los cambios desde el último backup válido.

En una versión más madura, este tipo de copia debería apoyarse en binlogs de MariaDB/MySQL.

Uso previsto:

- Reducir espacio ocupado.
- Reducir tiempo de copia.
- Mantener una cadena de recuperación más eficiente.

### 3. Backup diferencial

El backup diferencial debe guardar los cambios desde el último backup completo.

Uso previsto:

- Recuperaciones más simples que con muchos incrementales.
- Mejor equilibrio entre espacio y facilidad de restauración.
- Escenario útil para PyMEs.

## Responsabilidades del motor de backups

El motor centralizado debería encargarse de:

- Validar los parámetros recibidos.
- Comprobar que el tipo de backup es válido.
- Construir el nombre final del archivo.
- Ejecutar el script correspondiente.
- Interpretar el resultado.
- Registrar el resultado en logs.
- Preparar datos para el historial.
- Devolver una respuesta clara al panel.
- Evitar que la interfaz dependa directamente de detalles internos del script.

## Separación propuesta

La arquitectura recomendada sería:

~~~text
Panel web
   ↓
Ruta FastAPI /backups/run
   ↓
Motor central de backups
   ↓
Ejecución local o remota
   ↓
Script backups_api.sh
   ↓
Resultado normalizado
   ↓
Logs + historial + respuesta al usuario
~~~

## Componentes previstos

### 1. Formulario web

El formulario seguirá siendo la entrada visual para el usuario.

Debe enviar:

- Tipo de backup.
- Base de datos.
- Destino.
- Nombre.
- Compresión.
- Retención.
- Referencia base.
- Notas.

### 2. FastAPI

FastAPI recibirá la petición y no debería contener toda la lógica de backup directamente.

Su papel debe ser:

- Recibir datos del formulario.
- Comprobar permisos.
- Llamar al motor de backups.
- Redirigir con el resultado.

### 3. Motor de backups

El motor debe concentrar la lógica principal.

En una primera versión puede seguir dentro de `main.py`, pero organizado en funciones claras.

En una versión posterior podría moverse a un archivo propio, por ejemplo:

~~~text
backup_engine.py
~~~

### 4. Script Bash

El script `backups_api.sh` seguirá siendo el encargado de ejecutar la operación real en el sistema.

Su papel debe ser:

- Ejecutar `mysqldump`.
- Aplicar compresión.
- Aplicar retención.
- Devolver un resultado claro.

### 5. Historial

El historial de backups no debería depender solo de listar archivos.

Debe prepararse para guardar información estructurada:

- ID del backup.
- Tipo.
- Base de datos.
- Archivo generado.
- Fecha.
- Usuario.
- Resultado.
- Tamaño.
- Referencia base.
- Notas.

Esta parte se desarrollará más en R-009.

## Primera versión del motor

Para no romper el MVP actual, la primera versión del motor puede mantener la ejecución actual por SSH, pero añadiendo una capa intermedia.

Funciones recomendadas:

~~~text
validate_backup_type()
build_backup_request()
run_backup()
parse_backup_result()
register_backup_event()
~~~

## Ejemplo de flujo interno

1. El usuario entra en `/backups`.
2. Selecciona tipo de backup.
3. Rellena base de datos, destino, nombre y retención.
4. Envía el formulario.
5. FastAPI recibe la petición.
6. Se crea una solicitud interna de backup.
7. El motor valida los datos.
8. El motor ejecuta el script remoto.
9. El motor interpreta si el resultado es OK o ERROR.
10. Se registra el evento.
11. El usuario vuelve al panel con mensaje claro.

## Criterio de salida

R-008 se considerará completada cuando:

- Quede documentado el motor central de backups.
- Se separen responsabilidades entre panel, API, motor y script.
- Se definan los tipos de backup soportados.
- Se defina el resultado esperado de una ejecución.
- Se prepare la base para R-009, R-010 y restauración futura.
- No se rompa la ejecución actual del MVP.

## Decisión actual

Para mantener estabilidad, no se modificará de golpe el sistema actual.

La evolución será progresiva:

1. Documentar el motor central.
2. Definir validaciones.
3. Preparar resultado estructurado.
4. Conectar historial persistente en R-009.
5. Conectar programación automática en R-010.
6. Mejorar incrementales y diferenciales en fases posteriores.

## Estado

Estado actual: Pendiente de implementación.

Prioridad: Alta.

Dependencias:

- R-006 - Configuración por perfiles.
- R-007 - Instalador base idempotente.

Bloques siguientes:

- R-009 - Historial persistente de backups.
- R-010 - Programación automática de backups.
