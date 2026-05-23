# F6-GATE-01B - Cierre reinstalación sobre entorno existente

## Objetivo

Validar que DASC Server Manager puede reinstalarse o actualizarse sobre una instalación API existente sin romper configuración, datos runtime, servicio ni herramientas operativas.

## Estado

Cerrada.

## Entorno usado

| Campo | Valor |
|---|---|
| Máquina | lab-pruebas |
| Sistema | Ubuntu 22.04 |
| Tipo de prueba | Reinstalación sobre entorno existente |
| Fecha | 2026-05-23 |
| Ruta de instalación | `/opt/dasc/api` |
| Servicio | `dasc-api` |

## Situación inicial

Antes de reinstalar se comprobó que:

- El servicio `dasc-api` estaba activo.
- El panel respondía localmente en `http://127.0.0.1:8000`.
- Existía `/opt/dasc/api/config.env`.
- Existían los directorios `data` y `reports`.

También se crearon marcadores runtime:

~~~text
/opt/dasc/api/data/F6_GATE_01B_data_marker.txt
/opt/dasc/api/reports/F6_GATE_01B_report_marker.txt
~~~

## Control de configuración

Antes de reinstalar se calcularon hashes de:

- `config.env`.
- Línea `SECRET_KEY`.
- Línea `ADMIN_PASSWORD`.

Después de reinstalar se volvieron a calcular los mismos hashes.

Resultado:

| Elemento | Resultado |
|---|---|
| `config.env` | Conservado |
| `SECRET_KEY` | Conservada |
| `ADMIN_PASSWORD` | Conservada |
| Marcador en `data/` | Conservado |
| Marcador en `reports/` | Conservado |

## Resultado de reinstalación

La reinstalación se completó correctamente.

Durante la reinstalación:

- El instalador detectó `config.env` existente y lo conservó.
- Conservó `SECRET_KEY`.
- Conservó `ADMIN_PASSWORD`.
- Reutilizó el entorno virtual existente.
- Reinstaló/verificó dependencias.
- Recreó/actualizó el servicio systemd.
- Reinició `dasc-api`.
- Continuó aunque los hosts SSH remotos no estaban disponibles.
- El servicio quedó activo.
- El panel siguió respondiendo en `/login`.

## Validación post-instalación

Se ejecutó:

~~~bash
cd /opt/dasc/api
sudo ./tools/check_api_installation.sh "DASC validacion reinstalacion" "2026-05"
~~~

Resultado:

| Campo | Valor |
|---|---|
| Correctas | 17 |
| Fallidas | 0 |
| Resultado | OK |

## Informe operativo

Se ejecutó:

~~~bash
cd /opt/dasc/api
sudo ./tools/generate_operational_report.sh "DASC validacion reinstalacion" "2026-05"
~~~

Resultado:

- El informe se generó correctamente.
- Leyó `/opt/dasc/api/config.env`.
- Detectó modo de configuración real.
- Enmascaró variables sensibles.
- Detectó runtime `data` y `reports`.

El informe quedó como:

~~~text
Resultado: OPERATIVO PARCIAL.
~~~

Motivo:

~~~text
No se pudo conectar con MySQL en 192.168.60.20.
~~~

Esto es aceptable en F6-GATE-01B porque esta puerta valida la reinstalación API en un servidor, no la arquitectura PyME con base de datos remota.

## Corrección adicional de calidad

Durante la prueba se detectó que el mensaje final del instalador podía resultar confuso, porque decía que SSH automático estaba configurado aunque los hosts remotos se hubieran omitido por no estar disponibles.

Se ajustó el mensaje para reflejar que SSH remoto queda en modo no bloqueante y que la validación completa se hará en una puerta posterior de 2 servidores.

## Criterio de cierre

F6-GATE-01B se considera cerrada porque:

- La reinstalación no rompió `config.env`.
- La reinstalación no cambió `SECRET_KEY`.
- La reinstalación no cambió `ADMIN_PASSWORD`.
- No se perdieron datos runtime en `data`.
- No se perdieron datos runtime en `reports`.
- El servicio quedó activo.
- El panel respondió.
- La validación post-instalación dio 0 fallos.
- El informe operativo volvió a generarse.

## Límites

Esta puerta no valida todavía:

- SSH real contra nodo de backups.
- Base de datos remota de logs.
- Backups reales.
- Restauraciones.
- Arquitectura PyME de 2 servidores.
- Arquitectura Pro de 3 servidores.

## Próxima puerta recomendada

La siguiente puerta lógica es:

~~~text
F6-GATE-02 - Validación PyME de 2 servidores
~~~

## Conclusión

La reinstalación sobre entorno existente queda validada.

DASC Server Manager supera la segunda puerta técnica de instalación API antes de avanzar hacia validaciones PyME o clientes reales.
