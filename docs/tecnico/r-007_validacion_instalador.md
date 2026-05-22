# R-007 - Validación del instalador base idempotente

## Objetivo

Este documento define cómo validar que el instalador base de DASC Server Manager cumple el criterio de idempotencia.

La validación busca comprobar que el instalador puede ejecutarse varias veces sin romper la instalación, sin duplicar configuraciones y sin perder archivos importantes.

## Qué significa idempotente

En este proyecto, un instalador idempotente es aquel que puede ejecutarse más de una vez y deja el sistema en un estado correcto.

Esto es importante porque en una instalación real pueden ocurrir situaciones como:

- Repetir una instalación por error.
- Reinstalar después de una actualización.
- Reparar una instalación incompleta.
- Ejecutar el instalador en una máquina donde ya existía parte del sistema.
- Cambiar de versión sin borrar toda la configuración anterior.

## Elementos que se deben validar

### 1. Permisos de ejecución

El instalador debe detectar si no se ejecuta con permisos de administrador.

Comprobación esperada:

~~~bash
./install_dasc_api.sh
~~~

Resultado esperado:

~~~text
ERROR: ejecuta este script con sudo.
~~~

### 2. Ejecución con sudo

El instalador debe poder ejecutarse correctamente con:

~~~bash
sudo ./install_dasc_api.sh
~~~

Resultado esperado:

- Instala dependencias.
- Crea la estructura en `/opt/dasc/api`.
- Crea entorno virtual.
- Instala dependencias Python.
- Crea el servicio `dasc-api`.
- Reinicia el servicio.
- Muestra estado final.

### 3. Reejecución del instalador

Después de una primera instalación correcta, se debe ejecutar otra vez:

~~~bash
sudo ./install_dasc_api.sh
~~~

Resultado esperado:

- No debe romper la instalación.
- No debe borrar configuración sin copia.
- No debe fallar porque `/opt/dasc/api` ya existe.
- No debe fallar porque el entorno virtual ya existe.
- No debe fallar porque el servicio systemd ya existe.

### 4. Preservación de config.env

Si existe:

~~~text
/opt/dasc/api/config.env
~~~

el instalador debe conservarlo o crear una copia de seguridad antes de sobrescribirlo.

Resultado esperado:

~~~text
config.env
config.env.bak
~~~

o un comportamiento equivalente documentado.

### 5. Validación del servicio systemd

Después de instalar, se debe comprobar:

~~~bash
systemctl status dasc-api --no-pager
~~~

Resultado esperado:

- El servicio existe.
- El servicio está activo o al menos intenta arrancar correctamente.
- El `WorkingDirectory` apunta a `/opt/dasc/api`.
- El `ExecStart` usa el entorno virtual del proyecto.

### 6. Validación de puerto

Se debe comprobar que el panel responde localmente:

~~~bash
curl -I http://127.0.0.1:8000
~~~

Resultado esperado:

- Respuesta HTTP.
- El panel no debe quedar inaccesible por error del instalador.

### 7. Validación de estructura

Se debe comprobar que existen las rutas principales:

~~~bash
ls -ld /opt/dasc
ls -ld /opt/dasc/api
ls -ld /opt/dasc/api/venv
ls -l /opt/dasc/api/main.py
ls -l /opt/dasc/api/requirements.txt
ls -l /opt/dasc/api/config.env
~~~

Resultado esperado:

- Las rutas existen.
- Los archivos principales están presentes.
- Los permisos son coherentes con el usuario de ejecución.

### 8. Validación de logs de instalación

En una versión más madura, el instalador debería dejar un registro básico del proceso.

Ruta propuesta:

~~~text
/var/log/dasc-install.log
~~~

En esta fase no es obligatorio que el log exista, pero queda marcado como mejora recomendable.

## Casos de prueba mínimos

### Caso 1 - Instalación limpia

Máquina sin instalación previa.

Resultado esperado:

- Instalación completada.
- Servicio creado.
- Panel accesible.

### Caso 2 - Instalación repetida

Máquina con DASC ya instalado.

Resultado esperado:

- Instalación no se rompe.
- Servicio sigue existiendo.
- Configuración no se pierde.

### Caso 3 - Instalación incompleta

Máquina donde existe `/opt/dasc/api`, pero falta el entorno virtual o el servicio.

Resultado esperado:

- El instalador completa lo que falta.
- No obliga a borrar manualmente todo.

### Caso 4 - Servicio existente

Máquina donde ya existe `/etc/systemd/system/dasc-api.service`.

Resultado esperado:

- El instalador actualiza o conserva el servicio de forma controlada.
- Ejecuta `systemctl daemon-reload`.
- Reinicia el servicio.

### Caso 5 - Configuración existente

Máquina donde ya existe `config.env`.

Resultado esperado:

- No se pierde la configuración.
- Se crea copia o se conserva el archivo existente.

## Checklist de cierre

R-007 se considerará validado cuando se pueda marcar:

- [ ] El instalador detecta si no se ejecuta con sudo.
- [ ] El instalador instala dependencias mínimas.
- [ ] El instalador crea `/opt/dasc/api`.
- [ ] El instalador crea o reutiliza el entorno virtual.
- [ ] El instalador instala dependencias Python.
- [ ] El instalador crea o actualiza `dasc-api.service`.
- [ ] El instalador preserva `config.env`.
- [ ] El instalador puede ejecutarse dos veces sin romper nada.
- [ ] El panel responde después de la instalación.
- [ ] El comportamiento queda documentado.

## Estado

Estado actual: Pendiente de implementación práctica.

Prioridad: Alta.

Dependencias:

- R-006 - Configuración por perfiles.
- R-007 - Diseño del instalador base idempotente.

Bloque siguiente:

- Revisión del script `install_dasc_api.sh`.
