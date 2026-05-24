# F6-GATE-03E - Validación de backups en informe operativo

## Objetivo

Integrar el estado de backups completos dentro del informe operativo de DASC Server Manager.

## Estado

En curso.

## Contexto

En F6-GATE-03D se validó que el producto puede generar backups completos mediante:

~~~text
/opt/dasc/api/tools/run_full_db_backup.sh
~~~

Ese proceso genera:

~~~text
.sql
.sql.sha256
.sql.meta.json
~~~

F6-GATE-03E busca que el informe operativo lea esa información y la muestre.

## Cambios aplicados

Se actualiza:

~~~text
deploy/api/package/tools/generate_operational_report.py
~~~

## Nueva sección del informe

El informe debe incluir:

~~~text
## 7. Backups completos
~~~

Esta sección debe mostrar:

- Estado de backups.
- Directorio de backups.
- Último backup detectado.
- Fecha de generación.
- Base de datos.
- Host origen.
- Usuario de backup.
- Tamaño.
- SHA256.
- Existencia del archivo `.sql`.
- Existencia del archivo `.sha256`.
- Validación de `CREATE TABLE`.
- Validación de `INSERT INTO`.
- Binario usado para el dump.
- Etiqueta.

## Resultado esperado en Ubuntu real

Al ejecutar:

~~~bash
cd /opt/dasc/api
sudo ./tools/generate_operational_report.sh "DASC validacion backup informe" "2026-05"
~~~

El informe debe concluir:

~~~text
Resultado: BASE OPERATIVA OK CON BACKUP.
~~~

## Límites

Esta puerta todavía no valida:

- Restauración automática en informe.
- Retención.
- Cifrado.
- Copia externa.
- Exportación PDF.
- Envío al cliente.

## Conclusión

F6-GATE-03E prepara el informe operativo para mostrar evidencias reales de backup completo.
