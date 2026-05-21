# R-006 - Validación de perfiles de instalación

## Objetivo

Este documento define cómo comprobar que los perfiles de instalación de DASC Server Manager tienen sentido antes de integrarlos dentro del instalador y del código principal.

La validación no consiste todavía en ejecutar una instalación automática completa, sino en revisar que cada perfil tiene una configuración coherente y que representa un escenario real.

## Perfiles disponibles

Los perfiles definidos son:

- `single`
- `dual`
- `distributed`

Cada perfil tiene un archivo de ejemplo dentro de:

~~~text
config/perfiles/
~~~

Archivos creados:

~~~text
config.single.env.example
config.dual.env.example
config.distributed.env.example
~~~

## Validación del perfil single

El perfil `single` representa una instalación en un único servidor.

Debe cumplir:

- `INSTALL_MODE=single`
- `SERVICIOS_HOST=127.0.0.1`
- `BACKUPS_HOST=127.0.0.1`
- `LOGS_DB_HOST=127.0.0.1`

Este perfil es válido si todos los servicios se ejecutan en la misma máquina.

Uso recomendado:

- Demos rápidas.
- Laboratorio local.
- Clientes pequeños.
- Instalaciones con bajo presupuesto.

Riesgo principal:

- Si falla el único servidor, falla todo el sistema.

## Validación del perfil dual

El perfil `dual` representa una instalación con dos servidores.

Debe cumplir:

- `INSTALL_MODE=dual`
- El servidor principal queda separado del nodo DASC.
- `BACKUPS_HOST` apunta al servidor encargado de copias.
- `LOGS_DB_HOST` puede apuntar al mismo servidor de DASC/backups.
- `SERVICIOS_HOST` apunta al servidor donde se gestionan los servicios reales.

Uso recomendado:

- PyMEs.
- Instalaciones con presupuesto moderado.
- Clientes que quieren algo más seguro que un único servidor.

Riesgo principal:

- Sigue existiendo concentración de varias funciones en el servidor DASC.

## Validación del perfil distributed

El perfil `distributed` representa una instalación completa y separada.

Debe cumplir:

- `INSTALL_MODE=distributed`
- El panel/API queda en una máquina.
- La base de datos queda en otra máquina.
- Las copias, servicios y logs quedan separados según la arquitectura definida.
- `BACKUPS_HOST` apunta al servidor de copias.
- `LOGS_DB_HOST` apunta al servidor donde esté la base de logs.

Uso recomendado:

- Entornos más profesionales.
- Clientes con datos importantes.
- Escenario más defendible a nivel técnico.

Riesgo principal:

- Mayor coste y más complejidad de instalación.

## Comprobaciones manuales

Antes de implementar esta lógica en el instalador, se deben revisar estos puntos:

### 1. Comprobar que existe INSTALL_MODE

Cada archivo debe incluir:

~~~env
INSTALL_MODE=single
~~~

o bien:

~~~env
INSTALL_MODE=dual
~~~

o bien:

~~~env
INSTALL_MODE=distributed
~~~

### 2. Comprobar hosts principales

Cada perfil debe definir:

~~~env
SERVICIOS_HOST=
BACKUPS_HOST=
LOGS_DB_HOST=
~~~

### 3. Comprobar variables de sesión y login

Cada perfil debe definir:

~~~env
SECRET_KEY=
ADMIN_USER=
ADMIN_PASSWORD=
~~~

### 4. Comprobar base de logs

Cada perfil debe definir:

~~~env
LOGS_DB_NAME=
LOGS_DB_USER=
LOGS_DB_PASS=
LOGS_ORIGIN=
~~~

### 5. Comprobar Cacti

Cada perfil debe definir:

~~~env
CACTI_URL=
~~~

## Decisión de compatibilidad

La implementación debe mantener compatibilidad con el MVP actual.

Esto significa que aunque exista `INSTALL_MODE`, el sistema no debe dejar de funcionar si las variables clásicas ya están configuradas manualmente.

Las variables actuales seguirán siendo válidas:

- `SERVICIOS_HOST`
- `BACKUPS_HOST`
- `LOGS_DB_HOST`
- `CACTI_URL`
- `SSH_USER`

## Resultado esperado

La tarea R-006 se considerará lista cuando existan:

- Documento de diseño de perfiles.
- Ejemplos `.env` por perfil.
- Documento de validación.
- Compatibilidad con el funcionamiento actual del MVP.

## Estado final de R-006

Con esta validación, R-006 queda preparada a nivel de documentación y estructura inicial.

El siguiente paso será R-007, donde el instalador deberá empezar a usar esta idea para preparar una instalación más limpia, reutilizable e idempotente.
