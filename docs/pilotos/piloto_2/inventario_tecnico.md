# Inventario técnico - Piloto 2

## Datos generales

| Campo | Valor |
|---|---|
| Nombre del piloto | Piloto 2 - Perfil Lite 1 servidor + externo |
| Fecha de inicio | 23/05/2026 |
| Responsable técnico | Equipo DASC |
| Tipo de entorno | Piloto técnico controlado |
| Cliente / entorno | Entorno controlado propio |
| Autorización recibida | No aplica en entorno propio |

## Objetivo del piloto

Validar DASC Server Manager en una arquitectura Lite de 1 servidor más copia externa.

Este perfil representa una opción de entrada para microempresas o entornos donde no es viable mantener dos servidores separados.

## Servidor único

| Campo | Valor |
|---|---|
| Hostname | piloto-lite |
| IP | 192.168.60.40 |
| Sistema operativo | Ubuntu Server |
| Motor de base de datos | MariaDB |
| Base de datos protegida | employees |
| Panel instalado | Pendiente |
| Ruta instalación API | /opt/dasc/api |
| Servicio systemd | dasc-api |
| Ruta backups locales | /home/dasc/backups |
| Ruta copia externa simulada | /home/dasc/external-backups |
| Logs configurados | Pendiente |

## Evidencias previstas

| Evidencia | Estado |
|---|---|
| Captura del panel accesible | Pendiente |
| Captura de login correcto | Pendiente |
| Captura de backup ejecutado | Pendiente |
| Captura de archivo local generado | Pendiente |
| Captura de copia externa simulada | Pendiente |
| Captura de logs | Pendiente |
| Captura de terminal local | Pendiente |
| Comandos principales usados | Pendiente |

## Riesgos controlados

| Riesgo | Medida |
|---|---|
| Pérdida del único servidor | Exigir copia externa obligatoria |
| Menor separación de responsabilidades | Documentar como perfil Lite |
| Confusión con perfil PyME | Comparar contra piloto 1 |
| Uso de datos reales | Usar base de datos de prueba |
