# Fase 3 - Cierre de despliegues adaptables

## Objetivo de la fase

La Fase 3 tenía como objetivo adaptar DASC Server Manager para que no dependiera únicamente de una arquitectura fija de laboratorio, sino que pudiera plantearse como un producto instalable en diferentes escenarios.

Los perfiles definidos son:

- DASC Lite: 1 servidor con copia externa obligatoria.
- DASC PyME: 2 servidores como arquitectura estándar recomendada.
- DASC Pro: 3 servidores con separación completa de responsabilidades.

## Arquitectura real utilizada para validación

La validación real se ha realizado sobre la arquitectura distribuida de tres servidores del laboratorio:

| Rol | Servidor | Función |
|---|---|---|
| API / Panel | 192.168.60.10 | Panel FastAPI, asistente de perfiles y punto de control |
| DB / Logs | 192.168.60.20 | Base de datos principal y base de datos de logs |
| Backups / Servicios | 192.168.60.30 | Ejecución de backups, servicios y copia externa |

## Tareas de la fase

| ID | Tarea | Estado |
|---|---|---|
| R-025 | Perfil 1 servidor + copia externa | Documentado |
| R-026 | Perfil estándar de 2 servidores | Documentado como estándar PyME |
| R-027 | Perfil Pro de 3 servidores | Documentado y validado parcialmente |
| R-028 | Soporte NAS/SFTP | Implementado y validado en modo local |
| R-029 | Copia externa cifrada | Implementada y validada con GPG |
| R-030 | Asistente de instalación por perfil | Implementado, corregido y validado |
| R-031 | Documentación de arquitecturas | Implementada como documentación base |

## R-025 - Perfil 1 servidor / Lite

El perfil `single` queda definido para instalaciones mínimas.

Características:

- Panel, base de datos, logs y backups en la misma máquina.
- Menor coste de entrada.
- Pensado para pruebas piloto o microempresas.
- Requiere copia externa obligatoria.

Archivo relacionado:

~~~text
config/perfiles/config.single.env.example
~~~

Estado: documentado.

No se ha validado en máquina real durante esta fase porque el laboratorio actual está basado en tres servidores.

## R-026 - Perfil 2 servidores / PyME

El perfil `dual` queda definido como arquitectura comercial recomendada para pequeñas empresas.

Distribución recomendada:

- Servidor principal: datos, base de datos o aplicación del cliente.
- Servidor DASC: panel, backups, logs, alertas y restauración.

Archivo relacionado:

~~~text
config/perfiles/config.dual.env.example
~~~

Estado: documentado.

No se ha validado físicamente como dos servidores independientes, pero queda definido como opción estándar de producto.

## R-027 - Perfil 3 servidores / Pro

El perfil `distributed` representa la arquitectura real del laboratorio.

Distribución:

- API / Panel: 192.168.60.10.
- DB / Logs: 192.168.60.20.
- Backups / Servicios: 192.168.60.30.

Archivo relacionado:

~~~text
config/perfiles/config.distributed.env.example
~~~

Estado: validado a nivel de generación de configuración y coherencia con la arquitectura real.

## R-028 - Copia externa NAS/SFTP

Se implementó el script:

~~~text
deploy/backup-services/package/sync_external_backup.sh
~~~

Este script permite sincronizar backups hacia:

- destino local,
- carpeta NAS montada,
- servidor SFTP mediante rsync sobre SSH.

Validación realizada:

- Origen: /tmp/dasc-backups-test
- Destino externo local: /tmp/dasc-external-test
- Servidor: Backups / Servicios 192.168.60.30

Resultado:

- El archivo `backup-demo.sql` se sincronizó correctamente.
- El contenido fue verificado después de la copia.

Estado: validado en modo local.

Pendiente futuro:

- Validar con NAS real.
- Validar con servidor SFTP real.

## R-029 - Copia externa cifrada

Se añadió cifrado opcional con GPG simétrico al script de copia externa.

Variables principales:

~~~text
EXTERNAL_BACKUP_ENCRYPTION=gpg
EXTERNAL_GPG_PASSPHRASE=
~~~

Validación realizada:

- Se generó un archivo `.gpg`.
- Se sincronizó al destino externo local.
- Se descifró correctamente.
- Se verificó que el contenido recuperado coincidía con el original.

Resultado validado:

~~~text
backup cifrado de prueba R-029
~~~

Estado: validado con GPG en modo local.

## R-030 - Asistente de instalación por perfil

Se creó el script:

~~~text
scripts/generar_config_perfil.sh
~~~

Función:

- Permite seleccionar perfil `single`, `dual` o `distributed`.
- Genera un `config.env` base desde la plantilla correspondiente.
- Crea backup del `config.env` anterior si ya existe.

Validaciones realizadas:

- Ejecución con Bash.
- Ejecución directa con `./scripts/generar_config_perfil.sh`.
- Validación de ausencia de BOM.
- Validación del perfil `distributed` en el servidor API / Panel.

Resultado comprobado:

~~~text
INSTALL_MODE=distributed
DASC_PROFILE_NAME=DASC Pro
SERVICIOS_HOST=192.168.60.30
BACKUPS_HOST=192.168.60.30
LOGS_DB_HOST=192.168.60.20
DB_HOST=192.168.60.20
EXTERNAL_BACKUP_REQUIRED=recommended
~~~

Estado: validado.

## R-031 - Documentación de arquitecturas

Se creó documentación técnica de la fase en:

~~~text
docs/tecnico/fase_3_despliegues_adaptables.md
docs/tecnico/R-028_R-029_copia_externa_cifrado.md
~~~

También se generaron evidencias específicas en:

~~~text
docs/validaciones/R-025_R-026_R-027_validacion_inicial_perfiles.md
docs/validaciones/R-030_asistente_perfiles.md
docs/validaciones/R-030_validacion_distributed_3_servidores.md
docs/validaciones/R-030_correccion_bom_script_perfiles.md
docs/validaciones/R-030_validacion_final_sin_bom.md
docs/validaciones/R-028_validacion_copia_externa_local.md
docs/validaciones/R-029_validacion_copia_externa_cifrada_gpg.md
~~~

Estado: documentado.

## Decisiones de producto tomadas

### Arquitectura Lite

Se acepta como entrada económica, pero solo con copia externa obligatoria.

### Arquitectura PyME

Se define como la arquitectura estándar comercial recomendada.

Motivo:

- Mejor equilibrio entre coste y seguridad.
- Separa el servidor de datos del servidor de backups.
- Es más realista para pequeñas empresas que exigir tres servidores.

### Arquitectura Pro

Se mantiene como opción avanzada y como arquitectura de laboratorio validada.

### Copia externa

Se considera necesaria para que DASC tenga sentido como producto real.

En especial:

- Obligatoria en modo Lite.
- Recomendada en modo PyME.
- Recomendable como capa extra en modo Pro.

### Cifrado

Se implementa como opcional para evitar introducir secretos reales en el repositorio.

En entornos reales, la contraseña de cifrado no debe guardarse en documentación pública ni en GitHub.

## Limitaciones asumidas

- No se ha probado con NAS real.
- No se ha probado con servidor SFTP real.
- No se ha desplegado físicamente el perfil single.
- No se ha desplegado físicamente el perfil dual.
- El cifrado se ha validado con GPG simétrico y contraseña de prueba.
- La integración automática completa con el instalador queda preparada, pero puede seguir mejorándose.

## Conclusión

La Fase 3 queda cerrada a nivel de implementación base, documentación y validación principal.

Se ha conseguido que DASC Server Manager pueda plantearse como una solución adaptable a varios perfiles:

- Lite para entrada económica.
- PyME como estándar recomendado.
- Pro como arquitectura distribuida avanzada.

Además, se ha añadido una base funcional para copia externa y cifrado opcional, dos elementos importantes para convertir el MVP académico en un producto más realista orientado a PYMES.

Estado final: Fase 3 cerrada con pendientes futuros controlados.
