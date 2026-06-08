# R-007 - Instalador base idempotente

## Objetivo

El objetivo de esta tarea es preparar un instalador base más limpio, reutilizable e idempotente para Vigex.

Un instalador idempotente significa que se puede ejecutar más de una vez sin romper la instalación existente, sin duplicar configuraciones y sin dejar el sistema en un estado incoherente.

Esta mejora es importante porque Vigex debe poder instalarse en diferentes escenarios:

- Laboratorio académico.
- Demo interna.
- Cliente pequeño con un solo servidor.
- PyME con dos servidores.
- Arquitectura distribuida con varios nodos.

## Problema actual

El MVP ya dispone de instaladores funcionales, pero están muy orientados al entorno actual del proyecto.

Esto significa que muchas decisiones están pensadas para las máquinas del laboratorio y no todavía para un producto instalable de forma flexible.

El instalador actual cumple su función, pero debe evolucionar para:

- Evitar errores si se ejecuta varias veces.
- Detectar si una carpeta ya existe.
- Preservar configuración existente.
- Preguntar el perfil de instalación.
- Separar instalación, actualización y desinstalación.
- Mejorar los mensajes de salida.
- Dejar logs básicos de instalación.
- Preparar una futura instalación por perfiles.

## Relación con R-006

La tarea R-006 define los perfiles de instalación:

- `single`
- `dual`
- `distributed`

R-007 debe preparar el instalador para que en el futuro pueda usar esos perfiles.

En esta primera versión no es obligatorio que el instalador automatice toda la lógica de perfiles, pero sí debe quedar diseñado para soportarla.

## Requisitos del instalador

El instalador base debe cumplir los siguientes puntos:

### 1. Comprobación de permisos

El instalador debe comprobar que se ejecuta con permisos de administrador.

Si no se ejecuta con `sudo`, debe detenerse con un mensaje claro.

### 2. Comprobación de dependencias

Debe instalar o verificar las dependencias mínimas:

- `python3`
- `python3-venv`
- `python3-pip`
- `openssh-client`
- `curl`
- `sshpass`

### 3. Creación de estructura

Debe preparar la estructura estándar:

~~~text
/opt/vigex/
/opt/vigex/api/
/opt/vigex/api/venv/
~~~

### 4. Copia de archivos

Debe copiar el paquete de la API al directorio de instalación.

La copia debe hacerse de forma controlada, evitando borrar configuraciones importantes sin confirmación.

### 5. Preservación de config.env

Si ya existe un archivo:

~~~text
/opt/vigex/api/config.env
~~~

el instalador no debe sobrescribirlo directamente sin crear copia de seguridad.

Debe generar una copia como:

~~~text
config.env.bak
~~~

o mantener el archivo existente si el usuario así lo decide.

### 6. Creación del entorno virtual

Debe crear el entorno virtual solo si no existe.

Si ya existe, puede reutilizarlo y actualizar dependencias.

### 7. Instalación de dependencias Python

Debe instalar dependencias desde:

~~~text
requirements.txt
~~~

### 8. Creación del servicio systemd

Debe crear o actualizar el servicio:

~~~text
vigex-api.service
~~~

El servicio debe apuntar a:

~~~text
/opt/vigex/api
~~~

y ejecutar Uvicorn usando el entorno virtual.

### 9. Recarga y reinicio

Debe ejecutar:

~~~bash
systemctl daemon-reload
systemctl enable vigex-api
systemctl restart vigex-api
~~~

### 10. Validación final

Al terminar debe mostrar:

- Estado del servicio.
- Ruta de instalación.
- URL local.
- URL de red.
- Avisos si algo requiere revisión manual.

## Criterio de idempotencia

El instalador será considerado idempotente si:

- Se puede ejecutar dos veces seguidas sin romper la instalación.
- No duplica líneas en ficheros de configuración.
- No borra `config.env` sin copia.
- No falla si `/opt/vigex/api` ya existe.
- No falla si el entorno virtual ya existe.
- No falla si el servicio systemd ya existe.
- Actualiza el código de forma controlada.

## Estado esperado al terminar R-007

Al cerrar esta tarea debe existir:

- Documento técnico del instalador base.
- Diseño de comportamiento idempotente.
- Primer instalador revisado o preparado para refactor.
- Validación básica de instalación.
- Compatibilidad con R-006.

## Estado

Estado actual: Pendiente de implementación.

Prioridad: Alta.

Dependencias:

- R-006 - Configuración por perfiles.

Bloque siguiente:

- R-008 - Centralizar motor de backups.
