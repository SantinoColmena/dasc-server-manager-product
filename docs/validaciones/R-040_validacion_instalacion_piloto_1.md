# Validación R-040 - Instalación piloto 1 en perfil 2 servidores

## Objetivo de la validación

Confirmar que el primer piloto técnico de DASC Server Manager se ha ejecutado en un entorno limpio de 2 servidores, simulando una instalación tipo PyME.

## Arquitectura validada

| Servidor | Hostname | Función | Estado |
|---|---|---|---|
| Servidor cliente | piloto-cliente-db | Base de datos MariaDB y logs | Validado |
| Servidor DASC | piloto-dasc | Panel, backups, servicios, terminal y validación | Validado |

## Resultado general

El piloto 1 se ha ejecutado correctamente.

DASC Server Manager ha quedado instalado en una arquitectura de 2 servidores. Se ha validado el acceso al panel, la ejecución de backups, la escritura de logs, la gestión de servicios y el uso de terminal remoto hacia las máquinas del piloto.

## Comprobaciones

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Inventario técnico completado | OK | docs/pilotos/piloto_1/inventario_tecnico.md |
| Servidor cliente preparado | OK | MariaDB activo en piloto-cliente-db |
| Servidor DASC preparado | OK | Scripts y panel instalados en piloto-dasc |
| Panel DASC instalado | OK | Servicio dasc-api activo |
| Servicio dasc-api activo | OK | systemctl status dasc-api |
| Acceso web validado | OK | Panel accesible desde navegador |
| Usuario admin validado | OK | Login correcto como admin |
| Usuario limitado validado | OK | Módulo de permisos disponible |
| Backup completo ejecutado desde terminal | OK | piloto1-full-20260523-1157.sql.gz |
| Backup completo ejecutado desde panel | OK | dwadas.sql.gz |
| Archivo de backup localizado | OK | /home/dasc/backups |
| Logs registrados | OK | Tabla dasc_logs.eventos |
| Servicios validados | OK | Módulo Servicios funcional |
| Terminal Main validada | OK | hostname ejecutado como santino |
| Terminal Backup validada | OK | hostname ejecutado como dasc |
| Terminal Database validada | OK | Corregida clave SSH y known_hosts |
| Restauración o validación equivalente | Parcial | Backup generado y verificable; restauración completa queda como validación posterior |
| Alertas probadas o simuladas | Parcial | Módulo visible; validación completa posterior |
| Cacti | No validado | No incluido en este perfil limpio de 2 servidores |
| Incidencias anotadas | OK | docs/pilotos/piloto_1/incidencias.md |
| Feedback recogido | OK | Incidencias técnicas del piloto registradas |

## Evidencias técnicas obtenidas

### Base de datos

- MariaDB activo.
- Puerto 3306 escuchando.
- Base de datos employees creada.
- Base de datos dasc_logs creada.
- Tabla dasc_logs.eventos creada.
- Binlogs activos.
- Usuarios remotos creados para backups, restauración y logs.

### Backups

Backups localizados en:

    /home/dasc/backups

Archivos generados durante el piloto:

    piloto1-full-20260523-1157.sql.gz
    dwadas.sql.gz

### Panel

Panel accesible por navegador en el servidor DASC.

Servicio systemd:

    dasc-api

Puerto:

    8000

### Terminal remoto

Resultados validados:

| Terminal | Resultado |
|---|---|
| Main | OK |
| Backup | OK |
| Database | OK tras corregir known_hosts y clave SSH |

## Incidencias detectadas durante la validación

| Nº | Descripción | Gravedad | Estado | Solución |
|---|---|---|---|---|
| 1 | La documentación inicial indicaba instaladores en la raíz del repo | Media | Corregida | Se usaron rutas reales dentro de deploy |
| 2 | install_db.sh fallaba con dasc_logs por comillas invertidas sin escapar | Alta | Corregida | Se escaparon las comillas invertidas en el bloque SQL |
| 3 | LOGS_DB_PASS venía como CAMBIAR_PASSWORD_LOGS | Alta | Corregida | Se configuró dasc_logs_2026 en config.env |
| 4 | Terminal Database fallaba por known_hosts | Media | Corregida | Se registró la huella SSH de 192.168.60.20 |
| 5 | Terminal Database requería clave pública | Media | Corregida | Se copió la clave pública de la API al usuario dasc de la DB |
| 6 | Cacti no funciona/no se valida en este perfil | Baja | Documentada | Se deja como limitación del piloto de 2 servidores |

## Limitaciones aceptadas

Cacti no se valida en este piloto porque el perfil limpio de 2 servidores no incluye una instalación específica de Cacti.

La auditoría funcional se valida mediante la tabla dasc_logs.eventos y el módulo de Logs del panel.

La restauración completa queda como validación posterior, aunque el backup real queda generado correctamente y disponible en disco.

## Cierre

R-040 queda validada.

## Estado

Documentado: Sí  
Implementado: Sí  
Validado: Sí  
