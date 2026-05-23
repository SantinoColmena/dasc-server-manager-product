# Plan de ejecución - Piloto 2

## Objetivo

Ejecutar el segundo piloto técnico de DASC Server Manager usando el perfil Lite de 1 servidor más copia externa.

## Arquitectura usada

| Componente | Ubicación |
|---|---|
| Panel DASC | piloto-lite |
| MariaDB | piloto-lite |
| Backups locales | piloto-lite |
| Logs | piloto-lite |
| Copia externa | /home/dasc/external-backups |

## Máquina usada

- Hostname: piloto-lite.
- IP interna DASC: 192.168.60.40.
- IP de acceso desde navegador: 192.168.1.248.
- Sistema operativo: Ubuntu 22.04.
- Base de datos: employees.
- Ruta backups locales: /home/dasc/backups.
- Ruta copia externa simulada: /home/dasc/external-backups.

## Orden ejecutado

1. Preparación de VM limpia.
2. Configuración de hostname.
3. Configuración de red.
4. Clonado del repositorio.
5. Instalación de base de datos local.
6. Instalación de backups y servicios.
7. Corrección de incidencia con paquetes MySQL/MariaDB.
8. Ejecución de backup local.
9. Creación de copia externa simulada.
10. Preparación de config.env.example para perfil Lite.
11. Instalación del panel DASC.
12. Corrección de hosts SSH permitidos.
13. Validación desde panel.
14. Validación por terminal.
15. Registro de incidencias.

## Comandos principales usados

Preparación inicial:

    sudo apt update
    sudo apt install -y git
    git clone https://github.com/SantinoColmena/dasc-server-manager-product.git
    cd dasc-server-manager-product

Instalación de base de datos local:

    sudo BACKUP_ALLOWED_HOST=192.168.60.40 LOGS_ALLOWED_HOST=192.168.60.40 bash deploy/db/install_db.sh

Instalación de backups y servicios:

    sudo DB_HOST=192.168.60.40 bash deploy/backup-services/install_backup_services.sh

Reparación de MariaDB tras incidencia:

    sudo apt install -y mariadb-server mariadb-client
    sudo systemctl enable --now mariadb
    sudo systemctl restart mariadb

Backup local:

    sudo -u dasc /usr/local/bin/backups_api.sh full employees /home/dasc/backups piloto2-lite-full-YYYYMMDD-HHMM.sql gzip 30 manual "prueba piloto 2 lite"

Copia externa simulada:

    sudo mkdir -p /home/dasc/external-backups
    sudo chown -R dasc:dasc /home/dasc/external-backups
    sudo -u dasc cp /home/dasc/backups/*.sql.gz /home/dasc/external-backups/

Instalación del panel:

    sudo bash deploy/api/install_dasc_api.sh

Corrección de hosts SSH permitidos:

    DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40

## Validaciones realizadas

| Prueba | Resultado |
|---|---|
| MariaDB | OK |
| dasc-api | OK |
| Puerto 8000 | OK |
| Backup local | OK |
| Copia externa simulada | OK |
| Logs | OK |
| Terminal Main | OK |
| Terminal Backup | OK |
| Terminal Database | OK |
| Servicios | OK |
| Panel | OK |

## Limitaciones del perfil Lite

- Menor separación entre datos, panel y backups.
- Si el servidor se pierde, también se pierden los backups locales.
- La copia externa es obligatoria para que el perfil tenga sentido.
- No sustituye al perfil PyME de 2 servidores cuando el cliente tiene datos críticos.

## Criterio de cierre

El piloto 2 se considera válido porque el sistema funciona en una sola máquina y se demuestra una copia externa simulada.

## Estado

Documentado: Sí  
Implementado: Sí  
Validado: Sí  