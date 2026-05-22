# Validación adicional R-021 - Retención segura en laboratorio real

## Objetivo

Validar de forma específica la retención segura de backups en el laboratorio real Ubuntu.

## Prueba 1 - Purgado seguro de backup antiguo

Se creó un backup completo temporal con retención desactivada.

Después se modificó su fecha en `history.tsv` para simular que era antiguo.

Al ejecutar un nuevo backup con retención activa, el sistema:

- Marcó el backup antiguo como `PRUNED`.
- Añadió marca `pruned_at`.
- Eliminó el fichero físico.
- Eliminó el checksum asociado.
- Registró la operación en `audit.log` como `backup.prune`.

Resultado:

    FICHERO_PURGADO_OK
    CHECKSUM_PURGADO_OK
    action=backup.prune result=OK

## Prueba 2 - Conservación de base referenciada

Se creó un backup completo base.

Después se creó un backup incremental que referenciaba esa base.

La fecha de la base se modificó para simular que era antigua.

Al ejecutar la retención, el sistema conservó la base porque seguía referenciada por un incremental activo.

Resultado:

    BASE_REFERENCIADA_CONSERVADA_OK
    CHECKSUM_BASE_CONSERVADO_OK

## Conclusión

R-021 queda validado en laboratorio real.

La retención segura elimina backups antiguos no referenciados y conserva copias base necesarias para cadenas activas.
