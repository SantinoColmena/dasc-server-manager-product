# Perfiles de despliegue Vigex

## Objetivo

Definir los perfiles de despliegue previstos para Vigex como base de producto.

Los perfiles permiten adaptar la instalación a diferentes tamaños de cliente, presupuesto y nivel de separación técnica.

## Principio general

Vigex debe poder instalarse en varios escenarios sin depender de IPs fijas de laboratorio.

Cada perfil debe definir:

- Número de servidores.
- Servicios instalados.
- Variables necesarias.
- Nivel de resiliencia.
- Complejidad de mantenimiento.
- Uso recomendado.

## Perfil Lite

### Objetivo

Perfil pensado para clientes pequeños o primeras implantaciones controladas.

### Número de servidores

1 servidor.

### Componentes

En el mismo servidor:

- Panel/API local.
- Nginx local.
- Scripts de backup.
- Base de datos local si aplica.
- Logs locales.
- Soporte local.

### Ventajas

- Instalación simple.
- Menor coste.
- Menos infraestructura.
- Adecuado para cliente pequeño.

### Inconvenientes

- Menor separación de responsabilidades.
- Si cae el servidor, cae todo.
- Requiere copia externa obligatoria para tener sentido como servicio.

### Variables principales

- VIGEX_PROFILE=lite
- LOCAL_PANEL_HOST=127.0.0.1
- LOCAL_PANEL_PORT=8000
- NGINX_PUBLIC_PORT=80
- DB_HOST=127.0.0.1
- BACKUPS_HOST=127.0.0.1
- SERVICIOS_HOST=127.0.0.1
- LOGS_DB_HOST=127.0.0.1
- CENTRAL_SUPPORT_ENABLED=true/false
- CENTRAL_SUPPORT_URL
- CENTRAL_SUPPORT_CLIENT_ID
- CENTRAL_SUPPORT_CLIENT_NAME

### Uso recomendado

- Microempresa.
- Demo avanzada.
- Cliente con presupuesto bajo.
- Piloto controlado.

## Perfil Standard

### Objetivo

Perfil recomendado para una PyME real.

### Número de servidores

2 servidores.

### Distribución recomendada

Servidor 1:

- Panel/API local.
- Nginx local.
- Soporte local.
- Terminal controlada.
- Conexión SSH hacia servidor 2.

Servidor 2:

- Base de datos.
- Backups.
- Scripts de backup/restauración.
- Logs.

### Ventajas

- Mejor separación que Lite.
- Coste razonable.
- Menos complejidad que Pro.
- Buen equilibrio para PyME.

### Inconvenientes

- DB y backups siguen compartiendo servidor.
- Requiere validar bien permisos y copias externas.

### Variables principales

- VIGEX_PROFILE=standard
- API_HOST=<IP_SERVIDOR_API>
- DB_HOST=<IP_SERVIDOR_DB_BACKUPS>
- BACKUPS_HOST=<IP_SERVIDOR_DB_BACKUPS>
- SERVICIOS_HOST=<IP_SERVIDOR_DB_BACKUPS>
- LOGS_DB_HOST=<IP_SERVIDOR_DB_BACKUPS>
- BACKUP_ALLOWED_HOST=<IP_SERVIDOR_DB_BACKUPS_O_API_SEGUN_FLUJO>
- LOGS_ALLOWED_HOST=<IP_SERVIDOR_API>
- NGINX_PUBLIC_PORT=80
- CENTRAL_SUPPORT_ENABLED=true
- CENTRAL_SUPPORT_URL
- CENTRAL_SUPPORT_CLIENT_ID
- CENTRAL_SUPPORT_CLIENT_NAME

### Uso recomendado

- PyME estándar.
- Cliente que requiere separación mínima.
- Servicio gestionado Vigex con coste moderado.

## Perfil Pro

### Objetivo

Perfil para cliente más exigente o entorno donde se quiere separación clara de responsabilidades.

### Número de servidores

3 servidores.

### Distribución recomendada

Servidor 1:

- Panel/API local.
- Nginx local.
- Soporte local.
- Terminal controlada.

Servidor 2:

- Base de datos.
- Logs.
- MariaDB/MySQL.
- Binlogs.

Servidor 3:

- Backups.
- Restauración.
- Copia externa.
- Scripts de backup.
- Validaciones de restore.

### Ventajas

- Separación clara.
- Mejor seguridad.
- Mejor trazabilidad.
- Mejor base para restauraciones.
- Más cercano a arquitectura profesional.

### Inconvenientes

- Mayor coste.
- Mayor complejidad.
- Más puntos de configuración.
- Requiere checklist de validación más estricto.

### Variables principales

- VIGEX_PROFILE=pro
- API_HOST=<IP_SERVIDOR_API>
- DB_HOST=<IP_SERVIDOR_DB>
- BACKUPS_HOST=<IP_SERVIDOR_BACKUPS>
- SERVICIOS_HOST=<IP_SERVIDOR_BACKUPS_O_DB>
- LOGS_DB_HOST=<IP_SERVIDOR_DB>
- BACKUP_ALLOWED_HOST=<IP_SERVIDOR_BACKUPS>
- LOGS_ALLOWED_HOST=<IP_SERVIDOR_API>
- DB_BIND_ADDRESS=0.0.0.0
- DB_SERVER_ID=<ID_UNICO>
- NGINX_PUBLIC_PORT=80
- CENTRAL_SUPPORT_ENABLED=true
- CENTRAL_SUPPORT_URL
- CENTRAL_SUPPORT_CLIENT_ID
- CENTRAL_SUPPORT_CLIENT_NAME

### Uso recomendado

- Cliente con mayor criticidad.
- PyME con datos importantes.
- Entorno donde la restauración y continuidad importan más.

## Perfil Central Vigex

### Objetivo

Servidor propio del equipo Vigex para soporte multi-cliente.

### Número de servidores

1 servidor o VPS propio de Vigex.

### Componentes

- central-support.
- Nginx central.
- Base SQLite central en fase actual.
- Futuro PostgreSQL/MariaDB si escala.
- Login central.
- Recepción de tickets locales.
- Gestión multi-cliente.

### Variables principales

- Vigex_CENTRAL_AUTH_ENABLED=true
- Vigex_CENTRAL_LAB_MODE=false
- Vigex_CENTRAL_SECRET_KEY
- Vigex_CENTRAL_ADMIN_USER
- Vigex_CENTRAL_ADMIN_PASSWORD
- Vigex_CENTRAL_TECH_USER
- Vigex_CENTRAL_TECH_PASSWORD
- Vigex_CENTRAL_DEMO_CLIENT_ID o futuro Vigex_CENTRAL_INITIAL_CLIENT_ID
- Vigex_CENTRAL_DEMO_CLIENT_NAME o futuro Vigex_CENTRAL_INITIAL_CLIENT_NAME
- Vigex_CENTRAL_DEMO_TOKEN o futuro token por cliente

### Uso recomendado

- Servicio interno Vigex.
- Gestión centralizada de tickets.
- Futuro portal multi-cliente.

## Comparativa rápida

| Perfil | Servidores | Coste | Separación | Uso |
|---|---:|---:|---:|---|
| Lite | 1 | Bajo | Baja | Piloto o microcliente |
| Standard | 2 | Medio | Media | PyME recomendada |
| Pro | 3 | Alto | Alta | Cliente exigente |
| Central Vigex | 1 VPS | Medio | Interna Vigex | Soporte multi-cliente |

## Decisión actual

El perfil recomendado para venta futura a PyME será Standard.

Lite queda como opción de entrada, pero solo con copia externa obligatoria.

Pro queda como opción avanzada.

Central Vigex no se instala en clientes; pertenece al equipo Vigex.
