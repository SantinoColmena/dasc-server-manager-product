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
| Copia externa | Carpeta externa simulada |

## Máquina esperada

- Hostname: piloto-lite.
- IP propuesta: 192.168.60.40.
- Sistema operativo: Ubuntu Server.
- Base de datos: employees.
- Ruta backups locales: /home/dasc/backups.
- Ruta copia externa simulada: /home/dasc/external-backups.

## Orden de ejecución

1. Preparar VM limpia.
2. Configurar hostname e IP.
3. Clonar repositorio.
4. Instalar base de datos local.
5. Instalar backups y servicios apuntando a la propia máquina.
6. Instalar panel DASC.
7. Configurar logs contra la propia máquina.
8. Ejecutar backup local.
9. Simular copia externa.
10. Validar panel, logs, servicios y terminal.
11. Registrar incidencias.
12. Cerrar R-043.

## Comandos previstos

Preparación inicial:

    sudo apt update
    sudo apt install -y git
    git clone https://github.com/SantinoColmena/dasc-server-manager-product.git
    cd dasc-server-manager-product

Instalación de base de datos local:

    sudo BACKUP_ALLOWED_HOST=192.168.60.40 LOGS_ALLOWED_HOST=192.168.60.40 bash deploy/db/install_db.sh

Instalación de backups y servicios:

    sudo DB_HOST=192.168.60.40 bash deploy/backup-services/install_backup_services.sh

Instalación del panel:

    sudo bash deploy/api/install_dasc_api.sh

Creación de carpeta externa simulada:

    sudo mkdir -p /home/dasc/external-backups
    sudo chown -R dasc:dasc /home/dasc/external-backups

Validación de copia externa simulada:

    sudo -u dasc cp /home/dasc/backups/*.sql.gz /home/dasc/external-backups/
    ls -lh /home/dasc/external-backups

## Validaciones mínimas

| Prueba | Resultado esperado |
|---|---|
| MariaDB | active |
| dasc-api | active |
| Puerto 8000 | escuchando |
| Backup local | archivo .sql.gz generado |
| Copia externa simulada | archivo duplicado en external-backups |
| Logs | eventos visibles |
| Terminal | hostname ejecutado correctamente |
| Panel | login correcto |

## Limitaciones del perfil Lite

- Menor separación entre datos, panel y backups.
- Si el servidor se pierde, también se pierden los backups locales.
- La copia externa es obligatoria para que el perfil tenga sentido.
- No sustituye al perfil PyME de 2 servidores cuando el cliente tiene datos críticos.

## Criterio de cierre

El piloto 2 se considera válido si el sistema funciona en una sola máquina y se demuestra una copia externa simulada o equivalente.

## Estado

Documentado: Sí  
Implementado: Pendiente  
Validado: Pendiente  
