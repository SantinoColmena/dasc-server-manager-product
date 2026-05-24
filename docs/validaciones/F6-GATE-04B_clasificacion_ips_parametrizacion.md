# F6-GATE-04B - Clasificación de IPs fijas y plan de parametrización

## Objetivo

Clasificar las IPs fijas detectadas en F6-GATE-04A y decidir cuáles deben convertirse en variables reales de instalación.

## Estado

En curso.

## Fuente usada

~~~text
docs/auditoria/auditoria_ips_perfiles.md
~~~

## Resultado de auditoría

| Campo | Valor |
|---|---|
| Total referencias IP detectadas | 209 |
| Severidad ALTA | 8 |
| Severidad MEDIA | 36 |
| Severidad BAJA | 10 |
| Severidad INFO | 155 |

## Interpretación general

La mayoría de IPs detectadas están en documentación y validaciones históricas.

Estas referencias no bloquean el producto porque sirven como evidencia del laboratorio realizado.

Las referencias importantes son las que aparecen en instaladores, scripts de producto o valores por defecto que podrían afectar a una instalación real.

## Clasificación por severidad

### INFO - Documentación histórica

Las IPs en documentación, pilotos, validaciones y cierres de gates se mantienen.

Motivo:

- Documentan evidencias reales.
- Explican el laboratorio usado.
- No afectan a ejecución.
- No condicionan instalaciones futuras.

Acción:

~~~text
Mantener.
~~~

### BAJA - Ejemplos de configuración

Las IPs en `config.env.example` se aceptan de forma temporal como valores de ejemplo.

Motivo:

- No son secretos.
- No son configuración real.
- Ayudan a entender la arquitectura de laboratorio.

Acción futura recomendada:

~~~text
Sustituir gradualmente por placeholders comentados o valores más neutros.
~~~

Ejemplo futuro:

~~~env
LOGS_DB_HOST=IP_SERVIDOR_DB
BACKUP_DB_HOST=IP_SERVIDOR_DB
RESTORE_DB_HOST=IP_SERVIDOR_DB
BACKUPS_HOST=IP_SERVIDOR_BACKUPS
SERVICIOS_HOST=IP_SERVIDOR_SERVICIOS
~~~

### MEDIA - Código o recursos no críticos

Las IPs clasificadas como MEDIA deben revisarse una a una.

Criterio:

- Si son scripts antiguos, ejemplos o recursos no usados por instalación real, se documentan.
- Si afectan a ejecución real, se parametrizan.
- Si son referencias locales `127.0.0.1` para autocomprobación, pueden mantenerse justificadas.

Acción:

~~~text
Revisar antes del cierre completo de F6-GATE-04.
~~~

### ALTA - Instaladores

Las IPs de severidad ALTA son las prioritarias.

## Hallazgos ALTA

| Archivo | IP | Clasificación | Decisión |
|---|---|---|---|
| `deploy/api/install_dasc_api.sh` | `127.0.0.1` | Local aceptable | Mantener justificado |
| `deploy/api/install_dasc_api.sh` | `127.0.0.1` | Test local HTTP | Mantener justificado |
| `deploy/api/install_dasc_api.sh` | `127.0.0.1` | Mensaje URL local | Mantener justificado |
| `deploy/backup-services/install_backup_services.sh` | `192.168.60.20` | Valor por defecto de DB | Parametrizar |
| `deploy/db/install_db.sh` | `192.168.60.30` | Host permitido para backups | Parametrizar |
| `deploy/db/install_db.sh` | `192.168.60.10` | Host permitido para logs/API | Parametrizar |
| `deploy/proxy/install_reverse_proxy.sh` | `127.0.0.1` | Upstream local por defecto | Mantener justificado |
| `deploy/proxy/install_reverse_proxy.sh` | `127.0.0.1` | Test local HTTPS | Mantener justificado |

## Decisiones

### Mantener `127.0.0.1` cuando sea local

Se permite `127.0.0.1` en instaladores cuando representa:

- Comprobación local del servicio.
- URL local informativa.
- Upstream local de reverse proxy.
- Lista de hosts locales permitidos.

No se considera dependencia de laboratorio.

### Parametrizar IPs de laboratorio

Se deben parametrizar las IPs:

~~~text
192.168.60.10
192.168.60.20
192.168.60.30
192.168.60.40
~~~

cuando aparezcan como:

- Host de DB.
- Host de backups.
- Host permitido para logs.
- Host permitido para API.
- Host SSH remoto.
- Host de servicios.

## Variables objetivo

### Para API

Variables principales:

~~~env
SERVICIOS_HOST=
BACKUPS_HOST=
TERMINAL_DATABASE_HOST=
LOGS_DB_HOST=
BACKUP_DB_HOST=
RESTORE_DB_HOST=
DASC_SSH_ALLOWED_HOSTS=
~~~

### Para DB

Variables principales:

~~~env
BACKUP_ALLOWED_HOST=
LOGS_ALLOWED_HOST=
DB_BIND_ADDRESS=
~~~

### Para backup-services

Variables principales:

~~~env
DB_HOST=
BACKUP_OUTPUT_DIR=
BACKUP_RETENTION_KEEP=
~~~

### Para proxy

Variables principales:

~~~env
UPSTREAM_HOST=
UPSTREAM_PORT=
PUBLIC_HOSTNAME=
ENABLE_HTTPS=
~~~

## Perfiles objetivo

### Perfil Lite

Un solo servidor principal.

Uso previsto:

- API y DB en el mismo servidor o red local mínima.
- Backups locales con copia externa obligatoria.
- `127.0.0.1` permitido para servicios locales.
- Requiere configuración clara de copia externa.

### Perfil PyME 2 servidores

Arquitectura estándar recomendada.

Uso previsto:

- Servidor 1: API / panel / backups.
- Servidor 2: DB / logs / datos.
- Variables DB apuntan al servidor 2.
- Backups se ejecutan desde servidor 1 contra servidor 2.

### Perfil Pro 3 servidores

Arquitectura separada.

Uso previsto:

- Servidor 1: API / panel.
- Servidor 2: DB / logs.
- Servidor 3: backups / almacenamiento.
- Permite separar responsabilidades y endurecer permisos.

## Plan de parametrización

### F6-GATE-04C

Parametrizar `deploy/db/install_db.sh`.

Objetivo:

- Eliminar dependencia real de `192.168.60.30`.
- Eliminar dependencia real de `192.168.60.10`.
- Pedir o recibir por variable:
  - `BACKUP_ALLOWED_HOST`
  - `LOGS_ALLOWED_HOST`

### F6-GATE-04D

Parametrizar `deploy/backup-services/install_backup_services.sh`.

Objetivo:

- Eliminar dependencia real de `192.168.60.20`.
- Pedir o recibir por variable:
  - `DB_HOST`

### F6-GATE-04E

Revisar `config.env.example`.

Objetivo:

- Mantener utilidad didáctica.
- Evitar que parezca configuración obligatoria.
- Añadir comentarios claros o placeholders.

### F6-GATE-04F

Validar instalación con IPs distintas al laboratorio.

Objetivo:

- Instalar con IPs diferentes a `192.168.60.x`.
- Confirmar que API, DB, backups e informe siguen funcionando.

## Criterio de cierre de F6-GATE-04B

F6-GATE-04B se considera cerrada cuando:

- Las IPs fijas están clasificadas.
- Se separan IPs aceptables de IPs a parametrizar.
- Se define qué instaladores hay que modificar.
- Se define el orden de actuación.
- Se documentan los perfiles Lite, PyME 2 servidores y Pro 3 servidores.

## Conclusión

F6-GATE-04B establece que no todas las IPs fijas son un problema.

Las IPs de documentación se mantienen como evidencia.

Las IPs locales `127.0.0.1` se aceptan cuando son comprobaciones internas.

Las IPs de laboratorio usadas como valores por defecto en instaladores deben parametrizarse antes de considerar el producto instalable en entornos reales.
