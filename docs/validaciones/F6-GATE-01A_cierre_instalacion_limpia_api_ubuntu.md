# F6-GATE-01A - Cierre instalación limpia API en Ubuntu

## Objetivo

Validar que el paquete API de DASC Server Manager puede instalarse correctamente en una máquina Ubuntu limpia y quedar operativo en `/opt/dasc/api`.

## Estado

Cerrada.

## Entorno usado

| Campo | Valor |
|---|---|
| Máquina | lab-pruebas |
| Sistema | Ubuntu 22.04 |
| Tipo de prueba | Instalación limpia API |
| Fecha | 2026-05-23 |
| Ruta de instalación | `/opt/dasc/api` |
| Servicio | `dasc-api` |

## Resultado de instalación

La instalación API se completó correctamente después de corregir el comportamiento bloqueante de SSH hacia hosts remotos no disponibles.

Durante la instalación se comprobó que:

- El instalador creó `/opt/dasc/api`.
- Se creó `config.env`.
- Se conservó `config.env.example`.
- Se creó el entorno virtual Python.
- Se instalaron dependencias.
- Se creó el servicio systemd `dasc-api`.
- El servicio quedó activo.
- El panel respondió localmente en `http://127.0.0.1:8000`.
- Se crearon las carpetas runtime `data`, `reports` y `tools`.

## Corrección aplicada durante la prueba

Durante la primera ejecución se detectó que el instalador intentaba registrar la huella SSH de hosts remotos como `192.168.60.30` y `192.168.60.20`.

En una validación de 1 servidor, esos hosts no tienen por qué existir.

Se corrigió el instalador para que:

- Avise si no puede obtener la huella SSH.
- Omita la preparación SSH de ese host.
- Continúe la instalación API.
- Deje la validación SSH/backups para una puerta posterior de 2 servidores.

## Validación post-instalación

Se ejecutó:

~~~bash
cd /opt/dasc/api
sudo ./tools/check_api_installation.sh "DASC validacion" "2026-05"
~~~

Resultado:

| Campo | Valor |
|---|---|
| Correctas | 17 |
| Fallidas | 0 |
| Resultado | OK |

Comprobaciones superadas:

- Directorio de instalación.
- `main.py`.
- `requirements.txt`.
- `config.env`.
- `config.env.example`.
- Directorio `data`.
- Directorio `reports`.
- Directorio `tools`.
- Entorno virtual.
- Python del entorno virtual.
- Generador de informe operativo.
- Wrapper de informe operativo.
- Validador post-instalación.
- Servicio systemd existente.
- Servicio systemd activo.
- Puerto local API respondiendo.
- Generación de informe operativo.

## Informe operativo

Se ejecutó:

~~~bash
cd /opt/dasc/api
sudo ./tools/generate_operational_report.sh "DASC validacion" "2026-05"
~~~

Resultado:

- El informe operativo se generó correctamente.
- Leyó `/opt/dasc/api/config.env`.
- Detectó modo de configuración real.
- Enmascaró variables sensibles.
- Detectó `data`, `reports`, `users.json` y `alerts.db`.

El informe operativo quedó como:

~~~text
Resultado: OPERATIVO PARCIAL.
~~~

Motivo:

~~~text
No se pudo conectar con MySQL en 192.168.60.20.
~~~

Esto se considera aceptable en F6-GATE-01A porque esta puerta valida solo la instalación API en 1 servidor.

La validación de logs remotos y base de datos separada se hará en una puerta posterior.

## Criterio de cierre

F6-GATE-01A se considera cerrada porque:

- El API se instala en Ubuntu.
- El servicio systemd queda activo.
- El panel responde.
- La estructura runtime existe.
- Los scripts de informe y validación están instalados.
- La validación post-instalación da 0 fallos.
- El informe operativo se genera desde la instalación real.

## Límites

Esta puerta no valida todavía:

- Backups remotos.
- SSH real contra nodo de backups.
- Base de datos remota de logs.
- Restauraciones.
- Arquitectura PyME de 2 servidores.
- Arquitectura Pro de 3 servidores.
- Informe final de cliente.

## Próxima puerta recomendada

Después de esta validación, la siguiente puerta lógica es:

~~~text
F6-GATE-01B - Reinstalación / actualización sobre entorno existente
~~~

Después:

~~~text
F6-GATE-02 - Validación PyME de 2 servidores
~~~

## Conclusión

La instalación limpia del API en Ubuntu queda validada.

DASC Server Manager supera la primera puerta técnica real de instalación API antes de avanzar hacia ventas o clientes.
