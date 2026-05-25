# F6-GATE-04F - Validación de instalación con perfiles e IPs explícitas

## Objetivo

Validar que DASC Server Manager puede funcionar usando un perfil de instalación con IPs explícitas, sin depender de valores rígidos de laboratorio dentro de los instaladores.

## Estado

En curso.

## Perfil validado

Se valida un perfil equivalente a Pro 3 servidores.

| Rol | Máquina | IP |
|---|---|---|
| API / panel | lab-pruebas | 192.168.60.10 |
| DB / logs | lab-db-gate02 | 192.168.60.20 |
| Backups / servicios | lab-backups-gate04d | 192.168.60.30 |

## Contexto

En F6-GATE-04C se parametrizó el instalador DB.

En F6-GATE-04D se parametrizó el instalador backup-services.

En F6-GATE-04E se adaptó `config.env.example` a placeholders por perfil.

F6-GATE-04F valida que el conjunto funciona como una instalación por perfil con IPs explícitas.

## Variables clave del perfil

### API / panel

~~~env
SERVICIOS_HOST=192.168.60.30
BACKUPS_HOST=192.168.60.30
TERMINAL_DATABASE_HOST=192.168.60.20
LOGS_DB_HOST=192.168.60.20
BACKUP_DB_HOST=192.168.60.20
RESTORE_DB_HOST=192.168.60.20
DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30
~~~

### DB / logs

~~~env
BACKUP_ALLOWED_HOST=192.168.60.30
LOGS_ALLOWED_HOST=192.168.60.10
~~~

### Backup-services

~~~env
DB_HOST=192.168.60.20
~~~

## Criterio de validación

F6-GATE-04F se considera preparada cuando:

- Las tres máquinas tienen IPs correctas.
- La API puede llegar a DB y backups.
- Backup-services puede llegar a DB.
- DB acepta usuarios desde API y backup-services.
- Se puede hacer dump desde backup-services.
- El panel/API sigue activo.
- El informe operativo sigue generándose.
- La instalación queda documentada como perfil explícito.

## Conclusión esperada

El producto queda validado como instalación de 3 servidores con IPs explícitas y sin dependencia rígida de valores internos del código.
