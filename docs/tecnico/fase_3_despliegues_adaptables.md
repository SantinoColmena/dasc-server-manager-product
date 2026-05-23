# Fase 3 - Despliegues adaptables

## Estado inicial

La Fase 3 parte de la Fase 2 ya cerrada, implementada, documentada y validada en laboratorio real con tres máquinas Ubuntu.

El objetivo de esta fase no es añadir funciones visuales nuevas al panel, sino adaptar DASC Server Manager para poder instalarse de forma flexible según el tamaño y presupuesto del cliente.

## Tareas incluidas

| ID | Tarea | Objetivo |
|---|---|---|
| R-025 | Perfil 1 servidor + copia externa | Crear una instalación Lite para clientes pequeños |
| R-026 | Perfil estándar de 2 servidores | Definir la arquitectura recomendada para PyMEs |
| R-027 | Perfil Pro de 3 servidores | Mantener la arquitectura distribuida validada |
| R-028 | Soporte NAS/SFTP | Permitir destinos externos de backup |
| R-029 | Copia externa cifrada | Preparar cifrado opcional para copias externas |
| R-030 | Asistente de instalación por perfil | Guiar la instalación según el modo elegido |
| R-031 | Documentación de arquitecturas | Explicar Lite, PyME y Pro de forma clara |

## Perfiles definidos

### 1. DASC Lite - 1 servidor

Este perfil concentra panel, base de datos, logs y backups en una misma máquina.

No es la opción más segura, pero permite ofrecer una entrada económica para microempresas o pruebas piloto.

Condición obligatoria: debe existir una copia externa. Puede ser NAS, disco externo, SFTP, otro equipo o almacenamiento externo cifrado.

Uso recomendado:

- Microempresas.
- Pilotos.
- Clientes con presupuesto bajo.
- Entornos donde todavía no se justifica un segundo servidor.

Riesgo principal:

Si el servidor falla completamente, se pierden el sistema y las copias locales. Por eso la copia externa es obligatoria.

### 2. DASC PyME - 2 servidores

Este perfil es el estándar recomendado para clientes reales.

Distribución:

- Servidor principal: base de datos o aplicación del cliente.
- Servidor DASC: panel, backups, logs, alertas y restauración.

Ventajas:

- Separa las copias del servidor principal.
- Reduce el riesgo de pérdida total.
- Mantiene un coste razonable.
- Es más sencillo que una arquitectura de 3 servidores.

Uso recomendado:

- Gestorías.
- Academias.
- Talleres.
- Clínicas pequeñas.
- Comercios con base de datos local.
- Empresas de 5 a 30 empleados.

### 3. DASC Pro - 3 servidores

Este perfil mantiene la arquitectura distribuida validada en laboratorio.

Distribución:

- Servidor API / Panel.
- Servidor DB / Logs.
- Servidor Backups / Servicios.

Ventajas:

- Mayor separación de responsabilidades.
- Mejor aislamiento.
- Más parecido a un entorno profesional.
- Útil para clientes con datos más críticos.

Inconvenientes:

- Mayor coste.
- Más mantenimiento.
- Más puntos de configuración.

## Decisión de producto

La arquitectura de 2 servidores será considerada el estándar comercial recomendado para PyMEs.

La arquitectura de 1 servidor queda como entrada económica, siempre con copia externa obligatoria.

La arquitectura de 3 servidores queda como opción Pro o como laboratorio de validación avanzada.

## Variables comunes de perfil

Los perfiles se definen mediante archivos de ejemplo en:

- config/perfiles/config.single.env.example
- config/perfiles/config.dual.env.example
- config/perfiles/config.distributed.env.example

Variables principales:

| Variable | Uso |
|---|---|
| INSTALL_MODE | Define single, dual o distributed |
| SERVICIOS_HOST | Servidor donde se gestionan servicios |
| BACKUPS_HOST | Servidor donde se ejecutan backups |
| LOGS_DB_HOST | Servidor donde viven los logs |
| DB_HOST | Servidor de base de datos principal |
| EXTERNAL_BACKUP_REQUIRED | Indica si la copia externa es obligatoria o recomendada |
| EXTERNAL_BACKUP_ENABLED | Activa o desactiva copia externa |
| EXTERNAL_BACKUP_TYPE | Tipo de destino externo: none, local, nas o sftp |
| EXTERNAL_BACKUP_ENCRYPTION | Cifrado futuro: none, gpg o restic |

## Criterios de cierre de la Fase 3

La Fase 3 se podrá cerrar cuando:

- Existan perfiles single, dual y distributed documentados.
- El perfil single esté probado con copia externa.
- El perfil dual esté validado de punta a punta.
- El perfil distributed siga funcionando después de los cambios.
- El instalador permita seleccionar perfil o usar plantillas claras.
- Exista documentación entendible para explicar Lite, PyME y Pro.
- Existan evidencias en docs/validaciones.

## Estado actual

- R-025: iniciada.
- R-026: iniciada.
- R-027: iniciada.
- R-028: implementada y validada en modo local. NAS/SFTP queda preparado para validación futura.
- R-029: implementada y validada con cifrado GPG simétrico en destino local.
- R-030: implementada primera versión del asistente scripts/generar_config_perfil.sh. Pendiente integración final en instaladores.
- R-031: iniciada con este documento.
