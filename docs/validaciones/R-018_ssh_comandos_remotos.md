# Validación R-018 - Endurecimiento SSH y comandos remotos

## Objetivo

Mejorar la seguridad y mantenibilidad de las conexiones SSH usadas por DASC Server Manager para ejecutar scripts remotos en las máquinas de backups y servicios.

## Problema detectado

El backend del panel ya esperaba una clave dedicada en:

    /opt/dasc/api/.ssh/id_rsa_dasc

y un archivo known_hosts dedicado en:

    /opt/dasc/api/.ssh/known_hosts_dasc

Sin embargo, el instalador del API seguía generando la clave SSH en el home del usuario:

    ~/.ssh/id_rsa

Esto generaba una incoherencia entre el código y el despliegue real.

## Cambios realizados

- Se añaden variables de entorno específicas para SSH:
  - `DASC_SSH_KEY`
  - `DASC_SSH_KNOWN_HOSTS`
  - `DASC_SSH_TIMEOUT`
  - `DASC_SSH_CONNECT_TIMEOUT`
  - `DASC_SSH_STDIN_MAX_LENGTH`
  - `DASC_SSH_ALLOWED_HOSTS`
- Se centraliza la construcción del comando SSH en `build_ssh_base_command()`.
- Se valida que el host remoto esté permitido.
- Se valida que el script remoto esté permitido.
- Se limita el uso de comandos especiales como `cat`, `crontab` y `/bin/bash`.
- Se añade timeout a las llamadas SSH.
- Se mejora la gestión de errores por timeout.
- El instalador crea una clave dedicada en `/opt/dasc/api/.ssh/id_rsa_dasc`.
- El instalador crea un `known_hosts_dasc` dedicado.
- El instalador registra la huella del host remoto con `ssh-keyscan`.
- El instalador copia la clave pública usando `ssh-copy-id` con `StrictHostKeyChecking=yes`.
- El instalador escribe las variables SSH en `config.env`.

## Archivos modificados

- `deploy/api/package/main.py`
- `deploy/api/install_dasc_api.sh`
- `deploy/api/package/config.env.example`

## Criterio de seguridad

El panel no debe depender de la clave SSH global del usuario del sistema.

La API debe usar una clave propia del despliegue DASC y un archivo `known_hosts` propio, ubicados dentro de:

    /opt/dasc/api/.ssh/

## Pruebas pendientes en VM Ubuntu

| Prueba | Estado |
|---|---|
| Crear clave `/opt/dasc/api/.ssh/id_rsa_dasc` | Pendiente |
| Crear `known_hosts_dasc` | Pendiente |
| Copiar clave al servidor de backups | Pendiente |
| Validar `StrictHostKeyChecking=yes` | Pendiente |
| Ejecutar listado de servicios por SSH | Pendiente |
| Ejecutar backup por SSH | Pendiente |
| Probar timeout SSH | Pendiente |
| Validación completa en VM Ubuntu | Pendiente |

## Estado de cierre

R-018 queda implementado a nivel de código e instalador y pendiente de validación en VM Ubuntu.
