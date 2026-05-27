# R-052F - Cierre endurecimiento central-support como backend interno

## Objetivo

Cerrar la validación del endurecimiento de `central-support` para que funcione como backend interno detrás de Nginx.

## Estado

Cerrada.

## Contexto

Durante R-052C y R-052E se detectó que:

- dasc-api ya escuchaba internamente en 127.0.0.1:8000.
- central-support seguía escuchando en 0.0.0.0:8010.
- Nginx ya publicaba el panel central por el puerto 80.

El objetivo de R-052F era dejar central-support igual que el panel local: accesible públicamente solo a través de Nginx.

## Cambio aplicado

Se creó y ejecutó:

- deploy/central-support/harden_central_support_security.sh

También se ajustó:

- deploy/central-support/install_nginx_central_support.sh

## Commits funcionales

- e662c66 feat: endurecer central support interno
- 5ec9940 fix: robustecer health central support

## Estado antes

central-support escuchaba como:

- 0.0.0.0:8010

Esto exponía directamente el backend central.

## Estado después

central-support escucha como:

- 127.0.0.1:8010

El panel central se accede mediante:

- http://192.168.1.250/

Flujo:

- Nginx puerto 80
- 127.0.0.1:8010
- central-support

## Unidad systemd validada

La unidad quedó con:

- User=dasc
- Group=dasc
- WorkingDirectory=/opt/dasc/central-support
- EnvironmentFile=/opt/dasc/central-support/config.env
- ExecStart=/opt/dasc/central-support/venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8010

## Config central

Se mantiene protegido:

- /opt/dasc/central-support/config.env
- root:root
- 600

Validación:

- usuario normal no puede leer config.env central.

## R-052F-FIX1

Durante la primera validación apareció un falso negativo por dos motivos:

### Health demasiado rápido

El script consultaba `/health` justo después de arrancar el servicio.

Se corrigió añadiendo espera controlada de hasta 30 segundos.

### Validación incorrecta de 0.0.0.0

La comprobación inicial buscaba `0.0.0.0` en toda la línea de `ss`.

Eso generaba falso positivo porque `ss` muestra:

- 127.0.0.1:8010 0.0.0.0:*

El segundo campo pertenece a destino, no a la dirección local de escucha.

La validación correcta revisa solo la dirección local.

## Validación final

Se validó:

- dasc-central-support active.
- dasc-api active.
- nginx active.
- systemd central usa --host 127.0.0.1.
- 8010 escucha en 127.0.0.1:8010.
- 8010 no escucha como 0.0.0.0:8010.
- /health responde correctamente.
- Panel central por Nginx responde.
- Panel local por Nginx responde.
- API local backend interno responde.
- config.env central sigue protegido.
- usuario normal no puede leer config.env central.
- repo limpio.

## Resultado

R-052F queda cerrada correctamente.

Tanto el panel local como el panel central quedan detrás de Nginx, con sus backends escuchando solo en localhost:

- dasc-api: 127.0.0.1:8000
- central-support: 127.0.0.1:8010

## Próximo paso

Continuar con:

- R-052G - Validación global final de seguridad
