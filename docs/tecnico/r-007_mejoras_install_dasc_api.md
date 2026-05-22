# R-007 - Mejoras previstas sobre install_dasc_api.sh

## Objetivo

Este documento aterriza la tarea R-007 sobre el instalador real del proyecto.

El objetivo no es cambiar todavía toda la instalación de golpe, sino dejar claro qué partes del script `install_dasc_api.sh` deben mejorarse para convertirlo en un instalador base idempotente, reutilizable y preparado para perfiles de instalación.

## Situación actual

El instalador actual de la API cumple su función dentro del entorno del MVP.

Actualmente permite:

- Instalar dependencias del sistema.
- Copiar el paquete de la API a `/opt/dasc/api`.
- Crear un entorno virtual de Python.
- Instalar dependencias desde `requirements.txt`.
- Crear el servicio systemd `dasc-api`.
- Reiniciar el servicio.
- Preparar clave SSH para la comunicación con el servidor de backups.
- Exportar la clave pública como `api_panel.pub`.
- Copiar la clave al servidor de backups usando `sshpass`.

Esto hace que el instalador sea útil para el laboratorio actual, pero todavía necesita mejoras para ser usado como base de producto.

## Problemas detectados

### 1. Riesgo de sobrescribir configuración

El instalador copia el contenido del paquete directamente sobre:

~~~text
/opt/dasc/api
~~~

Esto puede afectar a archivos ya configurados, especialmente:

~~~text
config.env
~~~

En una instalación real, `config.env` puede contener IPs, credenciales, perfil de instalación y datos específicos del cliente.

Por tanto, no debería sobrescribirse sin copia o confirmación.

## 2. Falta de selección de perfil

Después de R-006, el proyecto ya contempla varios perfiles:

- `single`
- `dual`
- `distributed`

El instalador todavía no pregunta cuál se quiere usar.

En una versión mejorada, el instalador debería preguntar:

~~~text
Selecciona perfil de instalación:
1) single
2) dual
3) distributed
~~~

Y a partir de esa respuesta preparar un `config.env` inicial coherente.

## 3. Reejecución poco controlada

El instalador debe poder ejecutarse más de una vez.

Para ello debe comprobar antes de crear o copiar:

- Si `/opt/dasc/api` ya existe.
- Si el entorno virtual ya existe.
- Si el servicio systemd ya existe.
- Si `config.env` ya existe.
- Si la clave SSH ya existe.

Si algo ya existe, debe reutilizarse o actualizarse de forma controlada.

## 4. Logs de instalación

Actualmente el instalador muestra mensajes por pantalla, pero no queda un registro claro de instalación.

Sería recomendable guardar un log en:

~~~text
/var/log/dasc-install.log
~~~

Esto ayudaría en soporte técnico y en resolución de errores.

## 5. Validación final limitada

El instalador comprueba el estado del servicio y hace un `curl` local, pero podría mostrar una validación más ordenada.

Al terminar debería mostrar:

- Estado del servicio.
- Ruta de instalación.
- Usuario de ejecución.
- Perfil usado.
- URL local.
- URL de red.
- Estado de SSH contra backups.
- Avisos pendientes.

## 6. Dependencia directa de sshpass

El instalador usa `sshpass` para copiar la clave SSH al servidor de backups.

Esto es cómodo para el MVP, pero en un producto más maduro debería poder funcionar en dos modos:

- Modo automático con contraseña temporal.
- Modo manual copiando `api_panel.pub`.

De esta manera se evita depender siempre de contraseña SSH.

## 7. Falta de modo no interactivo

Para instalaciones automatizadas sería útil permitir variables previas como:

~~~bash
INSTALL_MODE=dual
ADMIN_PASSWORD=...
DASC_PASS=...
sudo ./install_dasc_api.sh
~~~

Esto permitiría instalar DASC desde scripts, documentación o procesos semiautomáticos.

## Mejoras propuestas

### Mejora 1 - Preservar config.env

Antes de copiar archivos, el instalador debe comprobar si existe:

~~~text
/opt/dasc/api/config.env
~~~

Si existe, debe hacer:

~~~text
/opt/dasc/api/config.env.bak
~~~

o conservar el archivo actual.

### Mejora 2 - Añadir INSTALL_MODE

El instalador debe permitir definir:

~~~env
INSTALL_MODE=single
~~~

o:

~~~env
INSTALL_MODE=dual
~~~

o:

~~~env
INSTALL_MODE=distributed
~~~

Esta variable será la base de la configuración por perfiles.

### Mejora 3 - Reutilizar entorno virtual

Si ya existe:

~~~text
/opt/dasc/api/venv
~~~

no debe fallar.

Puede reutilizarlo y ejecutar:

~~~bash
pip install --upgrade pip
pip install -r requirements.txt
~~~

### Mejora 4 - Actualizar systemd de forma segura

El instalador puede regenerar el servicio `dasc-api.service`, pero siempre debe ejecutar:

~~~bash
systemctl daemon-reload
systemctl enable dasc-api
systemctl restart dasc-api
~~~

Después debe mostrar el estado.

### Mejora 5 - Mejorar mensajes finales

El final del instalador debería mostrar algo similar a:

~~~text
Instalación completada
Perfil usado: dual
Panel instalado en: /opt/dasc/api
Servicio: dasc-api
URL local: http://127.0.0.1:8000
URL red: http://<IP_DEL_SERVIDOR>:8000
SSH backups: configurado / pendiente de revisión
~~~

### Mejora 6 - Preparar modo producto

El instalador debe estar preparado para crecer sin rehacerse desde cero.

Por eso se recomienda separar internamente funciones como:

~~~bash
check_root
install_dependencies
prepare_directories
preserve_config
copy_package
create_venv
install_python_requirements
create_systemd_service
prepare_ssh
validate_installation
~~~

Aunque el script siga siendo Bash, organizarlo mentalmente en bloques facilita mantenimiento y soporte.

## Criterio de salida

Esta parte de R-007 se considerará completada cuando:

- Queden documentadas las mejoras necesarias del instalador.
- Esté claro cómo preservar `config.env`.
- Esté claro cómo añadir `INSTALL_MODE`.
- Esté claro cómo validar la reejecución del instalador.
- Esté claro qué debe comprobar el instalador al finalizar.
- El script actual pueda refactorizarse siguiendo este documento.

## Decisión actual

Para no romper el MVP entregado, no se modificará directamente el instalador actual sin una prueba previa.

Primero se documenta la mejora.

Después se podrá crear una versión revisada o experimental del instalador y validarla en laboratorio.

## Estado

Estado actual: Diseño práctico completado.

Prioridad: Alta.

Dependencias:

- R-006 - Configuración por perfiles.
- R-007 - Documento base del instalador idempotente.
- R-007 - Validación del instalador idempotente.

Bloque siguiente:

- R-008 - Centralizar motor de backups.
