# R-052F-FIX1 - Robustecer validación health central-support

## Objetivo

Corregir la validación del hardening de central-support para evitar falsos negativos.

## Estado

En curso.

## Problemas detectados

Durante R-052F se aplicó correctamente el hardening:

- central-support pasó a escuchar en 127.0.0.1:8010.
- systemd quedó usando --host 127.0.0.1.
- Nginx siguió funcionando por puerto 80.
- config.env central siguió protegido.

Pero aparecieron dos incidencias de validación:

### 1. Health demasiado rápido

El script consultó /health justo después de arrancar el servicio.

Resultado:

- Expecting value: line 1 column 1

La validación posterior confirmó que /health respondía correctamente, así que era un problema de espera, no del servicio.

### 2. Falso positivo en grep de 0.0.0.0

La validación usó:

- grep ':8010' | grep '0.0.0.0'

Pero en la salida de ss aparece:

- 127.0.0.1:8010 0.0.0.0:*

El 0.0.0.0:* pertenece a la columna de destino, no a la dirección local de escucha.

## Solución aplicada

Se modifica:

- deploy/central-support/harden_central_support_security.sh

para esperar hasta 30 segundos a que /health responda correctamente.

## Validación correcta

La validación correcta debe mirar la dirección local de escucha.

Resultado esperado:

- 127.0.0.1:8010

No debe aparecer como dirección local:

- 0.0.0.0:8010

## Criterio de cierre

R-052F-FIX1 queda cerrado cuando:

- El script mantiene sintaxis Bash válida.
- /health responde tras espera controlada.
- ss confirma 127.0.0.1:8010 como dirección local.
- No aparece 0.0.0.0:8010 como dirección local.
- Panel central por Nginx sigue funcionando.
- Panel local por Nginx sigue funcionando.
