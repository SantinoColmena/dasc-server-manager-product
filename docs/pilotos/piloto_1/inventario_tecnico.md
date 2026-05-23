# Inventario técnico - Piloto 1

## Datos generales

| Campo | Valor |
|---|---|
| Nombre del piloto | Piloto 1 - Perfil PyME 2 servidores |
| Fecha de inicio | 23/05/2026 |
| Responsable técnico | Equipo DASC |
| Tipo de entorno | Piloto técnico controlado |
| Cliente / entorno | Entorno controlado propio |
| Autorización recibida | No aplica en entorno propio |

## Objetivo del piloto

Validar DASC Server Manager en una arquitectura de 2 servidores, simulando un caso real de PyME.

Este piloto no se considera una venta ni una instalación definitiva en cliente, sino una prueba técnica controlada para comprobar instalación, backups, logs, permisos, alertas y restauración.

## Arquitectura del piloto

| Servidor | Función | IP propuesta | Estado |
|---|---|---|---|
| Servidor cliente | Base de datos protegida | 192.168.60.20 | Pendiente |
| Servidor DASC | Panel, backups, servicios, logs y validación | 192.168.60.30 | Pendiente |

## Servidor cliente

| Campo | Valor |
|---|---|
| Hostname | piloto-cliente-db |
| IP | 192.168.60.20 |
| Sistema operativo | Ubuntu Server |
| Motor de base de datos | MariaDB |
| Base de datos protegida | employees |
| Puerto DB | 3306 |
| Usuario de backup | dasc_backup |
| Exposición a Internet | No |

## Servidor DASC

| Campo | Valor |
|---|---|
| Hostname | piloto-dasc |
| IP | 192.168.60.30 |
| Sistema operativo | Ubuntu Server |
| Panel instalado | Pendiente |
| Ruta instalación | /opt/dasc/api |
| Servicio systemd | dasc-api |
| Ruta backups | /home/dasc/backups |
| Logs configurados | Pendiente |
| Acceso SSH al servidor cliente | Pendiente |

## Evidencias previstas

| Evidencia | Estado |
|---|---|
| Captura del panel accesible | Pendiente |
| Captura de login correcto | Pendiente |
| Captura de usuario limitado | Pendiente |
| Captura de backup ejecutado | Pendiente |
| Captura de archivo generado | Pendiente |
| Captura de logs | Pendiente |
| Captura de restauración o validación equivalente | Pendiente |
| Captura de alerta o simulación | Pendiente |
| Comandos principales usados | Pendiente |

## Riesgos controlados

| Riesgo | Medida |
|---|---|
| Uso de datos reales | Se usará base de datos de prueba |
| Pérdida de datos | Restauración solo en entorno seguro |
| Exposición de MySQL | No se abrirá a Internet |
| Contraseñas por defecto | Se revisarán durante la instalación |
| Falta de evidencias | Se guardarán capturas y comandos |
