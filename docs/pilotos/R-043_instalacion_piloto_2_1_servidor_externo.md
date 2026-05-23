# R-043 - Instalación piloto 2 en perfil 1 servidor + externo

## Objetivo

Ejecutar el segundo piloto técnico de DASC Server Manager usando el perfil Lite de 1 servidor más copia externa.

La finalidad es comprobar si DASC puede funcionar en una arquitectura más económica y sencilla que el perfil PyME de 2 servidores, pensada para microempresas o entornos con menos presupuesto.

## Tipo de piloto

Piloto técnico controlado.

## Arquitectura validada

Perfil: DASC Lite - 1 servidor + copia externa.

| Componente | Ubicación | Estado |
|---|---|---|
| Panel DASC | piloto-lite | Validado |
| Base de datos MariaDB | piloto-lite | Validado |
| Backups locales | piloto-lite | Validado |
| Logs | piloto-lite | Validado |
| Servicios | piloto-lite | Validado |
| Terminal remota | piloto-lite | Validado |
| Copia externa | /home/dasc/external-backups | Validada como simulación |

## Máquina usada

| Campo | Valor |
|---|---|
| Hostname | piloto-lite |
| IP de gestión interna | 192.168.60.40 |
| IP de acceso desde navegador | 192.168.1.248 |
| Sistema operativo | Ubuntu 22.04 |
| Perfil | 1 servidor + externo |
| Base de datos protegida | employees |
| Ruta backups locales | /home/dasc/backups |
| Ruta copia externa simulada | /home/dasc/external-backups |
| Servicio panel | dasc-api |
| Puerto panel | 8000 |

## Resultado general

El piloto 2 se ha ejecutado correctamente.

DASC Server Manager ha quedado instalado en una arquitectura Lite de 1 servidor. Se ha validado el acceso al panel, la ejecución de backups, la escritura de logs, la gestión de servicios, la terminal remota y una copia externa simulada.

## Evidencias funcionales

### Panel

El panel queda accesible desde navegador mediante:

    http://192.168.1.248:8000

El login con usuario administrador funciona correctamente.

### Backups

Se validan backups locales desde terminal y desde panel.

Archivos generados:

    /home/dasc/backups/piloto2-lite-full-20260523-1315.sql.gz
    /home/dasc/backups/dwdafsdac.sql.gz

### Copia externa simulada

Se valida copia externa simulada en:

    /home/dasc/external-backups/piloto2-lite-full-20260523-1315.sql.gz

### Logs

Se validan eventos en la base:

    dasc_logs.eventos

Eventos confirmados:

- Accesos al panel.
- Ejecución de backup desde panel.
- Acceso a servicios.
- Acción sobre servicios.
- Terminal Main.
- Terminal Backup.
- Terminal Database.

### Servicios

El módulo Servicios carga correctamente el listado del sistema.

Resultado observado:

- Servicios totales: 143.
- Activos: 65.
- No activos: 78.

### Terminal

Se valida el comando:

    hostname && whoami && date

Resultados:

| Terminal | Host | Usuario | Estado |
|---|---|---|---|
| Main | piloto-lite | santino | OK |
| Backup | piloto-lite | dasc | OK |
| Database | piloto-lite | dasc | OK |

## Incidencias detectadas

Durante el piloto se detectaron dos incidencias relevantes:

| Nº | Incidencia | Gravedad | Estado |
|---|---|---|---|
| 1 | install_backup_services.sh sustituyó MariaDB por paquetes MySQL al instalar dependencias | Alta | Corregida |
| 2 | 192.168.60.40 no estaba permitido en DASC_SSH_ALLOWED_HOSTS | Media | Corregida |

## Limitaciones del perfil Lite

Este perfil funciona, pero tiene limitaciones frente al perfil PyME de 2 servidores:

- Panel, base de datos y backups locales comparten la misma máquina.
- Si el servidor se pierde, los backups locales también se pierden.
- La copia externa es obligatoria para que el perfil tenga sentido.
- Es una opción económica, no la arquitectura recomendada para datos críticos.

## Conclusión

R-043 queda completada.

El perfil Lite de 1 servidor + copia externa es viable para entornos pequeños, siempre que se mantenga una copia externa real y se documente que la separación de responsabilidades es menor que en el perfil de 2 servidores.

## Estado

Documentado: Sí  
Implementado: Sí  
Validado: Sí  