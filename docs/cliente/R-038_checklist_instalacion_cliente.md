# R-038 - Checklist de instalación en cliente

## Objetivo

Definir una lista de comprobación para instalar DASC Server Manager en un entorno de cliente de forma ordenada, segura y repetible.

Este checklist sirve como guía previa, durante y posterior a la instalación.

## Alcance

Este checklist está pensado para instalaciones tipo:

- DASC Lite: 1 servidor + copia externa obligatoria.
- DASC PyME: 2 servidores.
- DASC Pro: 3 servidores separados.

La arquitectura recomendada para una PyME es la instalación con 2 servidores:

- Servidor principal del cliente.
- Servidor DASC/backups/logs o nodo de copias separado.

## 1. Información previa del cliente

Antes de instalar, recopilar:

| Elemento | Estado |
|---|---|
| Nombre de la empresa | Pendiente |
| Persona de contacto | Pendiente |
| Teléfono o correo de contacto | Pendiente |
| Horario recomendado para instalación | Pendiente |
| Tipo de instalación: Lite, PyME o Pro | Pendiente |
| Responsable que autoriza cambios | Pendiente |

## 2. Información técnica previa

Recopilar:

| Elemento | Estado |
|---|---|
| IP del servidor principal | Pendiente |
| IP del servidor de backups | Pendiente |
| IP del servidor de base de datos | Pendiente |
| Sistema operativo | Pendiente |
| Versión de Ubuntu/Debian | Pendiente |
| Motor de base de datos | Pendiente |
| Nombre de base de datos a proteger | Pendiente |
| Puerto de base de datos | Pendiente |
| Usuario de backup | Pendiente |
| Ruta de destino de backups | Pendiente |

## 3. Requisitos mínimos

Comprobar:

| Requisito | Estado |
|---|---|
| Servidor con Linux actualizado | Pendiente |
| Acceso SSH disponible | Pendiente |
| Usuario con permisos sudo | Pendiente |
| Espacio suficiente para backups | Pendiente |
| Conectividad entre servidores | Pendiente |
| Puerto 8000 disponible para el panel | Pendiente |
| Puerto 3306 accesible solo desde hosts permitidos | Pendiente |
| Hora del sistema sincronizada | Pendiente |

## 4. Comprobaciones de seguridad previas

Antes de instalar:

| Comprobación | Estado |
|---|---|
| No usar contraseñas por defecto | Pendiente |
| No exponer MySQL a Internet | Pendiente |
| No publicar tokens en repositorios | Pendiente |
| No usar claves SSH privadas compartidas | Pendiente |
| Limitar usuarios con permisos de administración | Pendiente |
| Confirmar que los backups no contienen datos innecesarios | Pendiente |
| Confirmar ubicación segura para copias externas | Pendiente |

## 5. Instalación de la base de datos

Comprobar:

| Paso | Estado |
|---|---|
| Instalar MariaDB/MySQL | Pendiente |
| Crear base de datos de prueba o proteger base existente | Pendiente |
| Crear usuario específico de backup | Pendiente |
| Limitar usuario de backup por IP | Pendiente |
| Validar conexión remota desde servidor de backups | Pendiente |
| Validar mysqldump | Pendiente |
| Confirmar que el puerto 3306 no está expuesto públicamente | Pendiente |

## 6. Instalación del servidor de backups y servicios

Comprobar:

| Paso | Estado |
|---|---|
| Crear usuario de servicio dasc | Pendiente |
| Instalar openssh-server | Pendiente |
| Instalar cliente MariaDB/MySQL | Pendiente |
| Instalar script backups_api.sh | Pendiente |
| Instalar script servicios_api.sh | Pendiente |
| Crear carpeta de backups | Pendiente |
| Configurar .my.cnf del usuario de backup | Pendiente |
| Configurar permisos sudo controlados | Pendiente |
| Validar ejecución manual de backup | Pendiente |
| Validar listado de servicios | Pendiente |

## 7. Instalación del panel DASC

Comprobar:

| Paso | Estado |
|---|---|
| Copiar paquete de instalación | Pendiente |
| Ejecutar install_dasc_api.sh | Pendiente |
| Crear entorno virtual Python | Pendiente |
| Instalar requirements.txt | Pendiente |
| Crear servicio systemd dasc-api | Pendiente |
| Configurar config.env | Pendiente |
| Configurar clave SSH hacia servidor de backups | Pendiente |
| Validar arranque del servicio | Pendiente |
| Acceder al panel desde navegador | Pendiente |

## 8. Configuración inicial del panel

Comprobar:

| Paso | Estado |
|---|---|
| Cambiar contraseña de administrador | Pendiente |
| Crear usuario cliente limitado | Pendiente |
| Crear usuario técnico si aplica | Pendiente |
| Revisar permisos por usuario | Pendiente |
| Comprobar acceso al dashboard | Pendiente |
| Comprobar acceso a backups | Pendiente |
| Comprobar acceso a logs | Pendiente |
| Comprobar acceso a servicios | Pendiente |
| Comprobar que usuario no admin no ve administración | Pendiente |

## 9. Validación funcional

Realizar pruebas:

| Prueba | Estado |
|---|---|
| Login correcto | Pendiente |
| Login incorrecto registrado | Pendiente |
| Crear backup completo | Pendiente |
| Crear backup incremental | Pendiente |
| Crear backup diferencial | Pendiente |
| Ver backup generado en carpeta destino | Pendiente |
| Ver evento en logs | Pendiente |
| Probar botón o flujo de servicios | Pendiente |
| Probar alerta si está configurada | Pendiente |
| Probar restauración en entorno seguro | Pendiente |

## 10. Validación de copias externas

Si el cliente tiene copia externa:

| Prueba | Estado |
|---|---|
| Destino externo configurado | Pendiente |
| Copia externa ejecutada | Pendiente |
| Cifrado aplicado si corresponde | Pendiente |
| Descifrado de prueba realizado | Pendiente |
| Archivo recuperable desde destino externo | Pendiente |
| Evidencia guardada | Pendiente |

## 11. Evidencias a guardar

Guardar evidencias en la documentación del cliente o en carpeta de validación:

- Captura del panel funcionando.
- Captura de backup ejecutado.
- Captura de archivo generado.
- Captura de logs.
- Captura de servicio dasc-api activo.
- Captura de conexión SSH validada.
- Captura de prueba de restauración.
- Captura de copia externa, si aplica.

## 12. Entrega al cliente

Al finalizar, entregar:

| Elemento | Estado |
|---|---|
| URL de acceso al panel | Pendiente |
| Usuario inicial del cliente | Pendiente |
| Manual rápido | Pendiente |
| Explicación de backups | Pendiente |
| Explicación de logs | Pendiente |
| Explicación de alertas | Pendiente |
| Canal de soporte | Pendiente |
| Límites del soporte | Pendiente |
| Recomendaciones de uso | Pendiente |

## 13. Cierre de instalación

La instalación se considera cerrada cuando:

- El panel está accesible.
- Los backups funcionan.
- Los logs registran eventos.
- Los permisos de usuario están configurados.
- Existe al menos una copia válida.
- Existe una prueba de restauración o validación equivalente.
- El cliente sabe cómo acceder y qué hacer ante errores.
- Se han guardado evidencias.

## Resultado esperado

DASC Server Manager queda instalado de forma controlada, con backups funcionales, logs activos, permisos definidos y documentación básica entregada al cliente.
