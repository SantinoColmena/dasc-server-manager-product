# R-006 - Configuración por perfiles

## Objetivo

El objetivo de esta tarea es preparar Vigex para poder funcionar en diferentes arquitecturas sin tener que modificar el código fuente en cada instalación.

Actualmente el proyecto funciona con variables concretas en `config.env`, como las IPs de servicios, backups, logs y Cacti. Esto es válido para el entorno académico y para el MVP, pero no es suficiente para convertir el proyecto en un producto adaptable a diferentes clientes.

Con esta mejora, Vigex podrá arrancar usando un modo de instalación definido mediante la variable `INSTALL_MODE`.

## Perfiles previstos

### 1. Perfil single

El perfil `single` representa una instalación mínima en un único servidor.

Este modo está pensado para clientes pequeños, pruebas internas o demostraciones sencillas.

En este escenario, el panel, la base de datos, los backups, los logs y los servicios gestionados pueden convivir en la misma máquina.

Ejemplo:

~~~env
INSTALL_MODE=single
SERVICIOS_HOST=127.0.0.1
BACKUPS_HOST=127.0.0.1
LOGS_DB_HOST=127.0.0.1
CACTI_URL=/cacti/
~~~

Ventajas:

- Menor coste inicial.
- Instalación más sencilla.
- Útil para demos y clientes muy pequeños.

Limitaciones:

- Menor separación de responsabilidades.
- Si falla el servidor principal, afecta a todo el sistema.
- Menos recomendable para entornos críticos.

## 2. Perfil dual

El perfil `dual` representa una instalación equilibrada con dos servidores.

Este modo será el perfil estándar recomendado para una PyME.

La idea es separar el servidor principal del cliente del nodo Vigex, donde estarían el panel, los backups, logs y tareas de mantenimiento.

Ejemplo:

~~~env
INSTALL_MODE=dual
SERVICIOS_HOST=192.168.60.20
BACKUPS_HOST=192.168.60.30
LOGS_DB_HOST=192.168.60.30
CACTI_URL=/cacti/
~~~

Ventajas:

- Mejor equilibrio entre coste y seguridad.
- Separación básica entre datos y copias.
- Más vendible para una PyME real.

Limitaciones:

- Requiere un segundo servidor, miniPC, NAS o VM.
- Hay que configurar SSH y acceso remoto correctamente.

## 3. Perfil distributed

El perfil `distributed` representa la arquitectura más completa.

Este modo separa las responsabilidades principales en tres servidores:

- Servidor Panel/API.
- Servidor Base de Datos.
- Servidor Backups/Servicios/Logs.

Ejemplo:

~~~env
INSTALL_MODE=distributed
SERVICIOS_HOST=192.168.60.30
BACKUPS_HOST=192.168.60.30
LOGS_DB_HOST=192.168.60.20
CACTI_URL=/cacti/
~~~

Ventajas:

- Mejor separación técnica.
- Más seguridad.
- Arquitectura más profesional.
- Más fácil de defender ante clientes con datos críticos.

Limitaciones:

- Mayor coste.
- Más complejidad de instalación.
- Más mantenimiento.

## Variables principales

Las variables mínimas que debe manejar Vigex son:

| Variable | Función |
|---|---|
| `INSTALL_MODE` | Define el perfil usado: `single`, `dual` o `distributed` |
| `SSH_USER` | Usuario usado para conexiones SSH |
| `SERVICIOS_HOST` | Máquina donde se gestionan servicios |
| `BACKUPS_HOST` | Máquina donde se ejecutan y guardan backups |
| `LOGS_DB_HOST` | Máquina donde se guarda la base de logs |
| `LOGS_DB_NAME` | Nombre de la base de datos de logs |
| `LOGS_DB_USER` | Usuario de la base de logs |
| `LOGS_DB_PASS` | Contraseña de la base de logs |
| `CACTI_URL` | URL de acceso a Cacti |
| `SECRET_KEY` | Clave interna de sesión |
| `ADMIN_USER` | Usuario administrador inicial |
| `ADMIN_PASSWORD` | Contraseña inicial del administrador |

## Criterio de salida

Esta tarea se considerará completada cuando:

- Exista una variable `INSTALL_MODE`.
- El proyecto tenga definidos los perfiles `single`, `dual` y `distributed`.
- El sistema pueda arrancar con una configuración clara por perfil.
- El instalador pueda preparar un `config.env` coherente según el perfil elegido.
- La documentación explique cuándo usar cada perfil.
- No se rompa el funcionamiento actual del MVP.

## Decisión inicial

Para no romper el estado actual del proyecto, la primera versión mantendrá compatibilidad con las variables existentes.

Es decir, aunque se añada `INSTALL_MODE`, las variables actuales como `SERVICIOS_HOST`, `BACKUPS_HOST` y `LOGS_DB_HOST` seguirán funcionando.

La mejora se hará de forma progresiva:

1. Documentar perfiles.
2. Añadir `INSTALL_MODE` a `config.env`.
3. Adaptar `main.py` para leer el perfil.
4. Adaptar instaladores para preguntar el perfil.
5. Probar los tres modos en laboratorio.

## Estado

Estado actual: Pendiente de implementación.

Prioridad: Crítica.

Dependencias: R-004.

Bloque siguiente: R-007 - Instalador base idempotente.
