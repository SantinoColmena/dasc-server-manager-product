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
| IP interna DASC | 192.168.60.40 |
| IP de acceso desde navegador | 192.168.1.248 |
| Sistema operativo | Ubuntu 22.04 |
| Motor de base de datos | MariaDB |
| Base de datos protegida | employees |
| Panel instalado | Sí |
| Ruta instalación API | /opt/dasc/api |
| Servicio systemd | dasc-api |
| Ruta backups locales | /home/dasc/backups |
| Ruta copia externa simulada | /home/dasc/external-backups |
| Logs configurados | Sí |

## Componentes instalados

| Componente | Estado |
|---|---|
| MariaDB | Activo |
| SSH | Activo |
| Cron | Activo |
| Scripts de backup | Instalados |
| Scripts de servicios | Instalados |
| API FastAPI | Activa |
| Panel web | Accesible |
| Logs | Operativos |
| Copia externa simulada | Operativa |

## Evidencias obtenidas

| Evidencia | Estado |
|---|---|
| Captura del panel accesible | Realizada |
| Captura de login correcto | Realizada |
| Captura de backup ejecutado | Realizada |
| Captura de archivo local generado | Realizada |
| Captura de copia externa simulada | Validada por comando |
| Captura de logs | Realizada |
| Captura de terminal Main | Realizada |
| Captura de terminal Backup | Realizada |
| Captura de terminal Database | Realizada |
| Captura de servicios | Realizada |

## Riesgos controlados

| Riesgo | Medida |
|---|---|
| Pérdida del único servidor | Exigir copia externa obligatoria |
| Menor separación de responsabilidades | Documentar como perfil Lite |
| Confusión con perfil PyME | Comparar contra piloto 1 |
| Uso de datos reales | Usar base de datos de prueba |