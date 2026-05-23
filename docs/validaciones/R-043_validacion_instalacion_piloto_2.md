# Validación R-043 - Instalación piloto 2 en perfil 1 servidor + externo

## Objetivo

Validar la ejecución del piloto 2 en perfil Lite de 1 servidor más copia externa.

## Resultado general

R-043 se considera validada.

DASC Server Manager funciona correctamente en una única máquina, con backups locales, logs, servicios, terminal remota y copia externa simulada.

## Comprobaciones

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Inventario técnico completado | OK | docs/pilotos/piloto_2/inventario_tecnico.md |
| Servidor único preparado | OK | piloto-lite |
| MariaDB local instalada | OK | Servicio activo y puerto 3306 escuchando |
| Base employees creada | OK | MariaDB |
| Base dasc_logs creada | OK | MariaDB |
| Tabla eventos creada | OK | dasc_logs.eventos |
| Panel DASC instalado | OK | /opt/dasc/api |
| Servicio dasc-api activo | OK | systemctl status dasc-api |
| Acceso web validado | OK | http://192.168.1.248:8000 |
| Login admin validado | OK | Panel principal |
| Backup local ejecutado | OK | /home/dasc/backups |
| Backup desde panel ejecutado | OK | dwdafsdac.sql.gz |
| Copia externa simulada | OK | /home/dasc/external-backups |
| Logs registrados | OK | dasc_logs.eventos |
| Terminal Main validada | OK | hostname && whoami && date |
| Terminal Backup validada | OK | hostname && whoami && date |
| Terminal Database validada | OK | hostname && whoami && date |
| Servicios validados | OK | Listado de servicios cargado |
| Incidencias anotadas | OK | docs/pilotos/piloto_2/incidencias.md |

## Evidencias técnicas

### Backups locales

Archivos encontrados:

    /home/dasc/backups/piloto2-lite-full-20260523-1315.sql.gz
    /home/dasc/backups/dwdafsdac.sql.gz

### Copia externa simulada

Archivo encontrado:

    /home/dasc/external-backups/piloto2-lite-full-20260523-1315.sql.gz

### Logs

Últimos eventos validados:

- POST /backups/run con resultado OK.
- GET /servicios con resultado OK.
- POST /servicios/accion con resultado OK.
- POST /api/terminal/run/database con resultado OK.
- POST /api/terminal/run/backup con resultado OK.
- POST /api/terminal/run/main con resultado OK.

### Servicios

El panel muestra servicios del sistema:

- Servicios totales: 143.
- Activos: 65.
- No activos: 78.

## Incidencias corregidas

| Incidencia | Estado |
|---|---|
| Sustitución de MariaDB por paquetes MySQL durante backup-services | Corregida |
| Host SSH no permitido 192.168.60.40 | Corregida |
| Backup vacío inicial | Corregido |
| Copia externa inicial sin .sql.gz | Corregida |

## Limitaciones aceptadas

Cacti no se valida como parte obligatoria de este perfil Lite.

La copia externa se valida como simulación local en este piloto. En un entorno real debería usarse un destino externo real, como otro servidor, NAS, SFTP o almacenamiento externo.

## Criterio de cierre

R-043 se cierra porque:

- El panel funciona.
- La base de datos local funciona.
- Los backups locales funcionan.
- La copia externa simulada funciona.
- Los logs funcionan.
- Servicios funciona.
- Terminal funciona.
- Las incidencias principales han sido corregidas.
- Las limitaciones quedan documentadas.

## Estado

Documentado: Sí  
Implementado: Sí  
Validado: Sí  