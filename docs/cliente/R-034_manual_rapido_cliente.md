# R-034 - Manual rápido para cliente

## Objetivo

Crear un manual sencillo para que un cliente pueda entender cómo usar Vigex sin conocimientos técnicos avanzados.

Este documento está pensado para una PyME o usuario final que necesita realizar acciones básicas como consultar el estado del sistema, revisar copias de seguridad, comprobar logs y entender cuándo debe contactar con soporte.

## ¿Qué es Vigex?

Vigex es un panel web pensado para ayudar a pequeñas y medianas empresas a controlar copias de seguridad, logs, servicios y alertas desde una interfaz sencilla.

El objetivo principal no es que el cliente tenga que administrar servidores complejos, sino que pueda comprobar de forma rápida si sus datos están protegidos y si el sistema está funcionando correctamente.

## Acceso al panel

Para acceder al panel:

1. Abrir el navegador.
2. Entrar en la URL indicada por el proveedor o técnico.
3. Introducir usuario y contraseña.
4. Pulsar en Entrar.

Ejemplo de URL interna:

http://IP_DEL_SERVIDOR:8000

En una instalación real, esta dirección puede cambiar según la red del cliente.

## Pantalla principal

La pantalla principal muestra los accesos disponibles según los permisos del usuario.

Desde el panel se puede acceder a:

- Copias de seguridad.
- Logs del sistema.
- Servicios.
- Administración de usuarios, solo si el usuario es administrador.

Cada usuario puede ver únicamente las secciones que tenga permitidas.

## Copias de seguridad

La sección de copias permite ejecutar o revisar backups de la base de datos.

### Tipos de copia

Vigex puede trabajar con tres tipos de copias:

- Copia completa: guarda todos los datos.
- Copia incremental: guarda cambios desde la última copia realizada.
- Copia diferencial: guarda cambios desde la última copia completa.

### Cómo lanzar una copia manual

1. Entrar en la sección Copias.
2. Seleccionar el tipo de copia.
3. Indicar la base de datos.
4. Elegir el nombre del archivo.
5. Seleccionar compresión y retención.
6. Pulsar Ejecutar backup.
7. Comprobar el mensaje de resultado.

## Historial de backups

El historial permite revisar qué copias se han realizado.

Se recomienda comprobar:

- Fecha de la copia.
- Tipo de copia.
- Resultado.
- Ubicación.
- Tamaño, si está disponible.
- Usuario que la ejecutó, si aparece registrado.

## Restauración de copias

La restauración de backups debe tratarse como una acción delicada.

Antes de restaurar una copia se recomienda:

1. Confirmar que la copia seleccionada es la correcta.
2. Verificar la fecha del backup.
3. Confirmar que se entiende que la restauración puede sobrescribir datos.
4. Avisar al responsable técnico o proveedor.
5. Guardar una copia previa antes de restaurar.

En un cliente real, las restauraciones críticas deben validarse con soporte técnico.

## Logs del sistema

La sección de logs muestra eventos registrados por Vigex.

Los logs ayudan a saber:

- Quién ha accedido al panel.
- Qué acciones se han realizado.
- Cuándo se ha ejecutado una copia.
- Si una acción ha terminado correctamente o con error.
- Desde qué origen o IP se ha producido una acción.

## Servicios

La sección de servicios permite comprobar el estado de servicios del sistema.

Según los permisos del usuario, puede permitir:

- Ver servicios activos.
- Ver servicios inactivos.
- Reiniciar servicios.
- Detener servicios.
- Arrancar servicios.

No se recomienda detener servicios si no se sabe exactamente qué función cumplen.

## Alertas

El sistema puede enviar alertas cuando se detectan eventos importantes.

Ejemplos de alertas:

- Backup correcto.
- Error en backup.
- Error de servicio.
- Error de API.
- Incidencia crítica.

Las alertas pueden configurarse para canales como Telegram u otros sistemas futuros.

## Usuarios y permisos

La administración de usuarios solo debe estar disponible para responsables autorizados.

Un usuario administrador puede:

- Crear usuarios.
- Asignar permisos.
- Eliminar usuarios.
- Dar acceso solo a las secciones necesarias.

Se recomienda aplicar el principio de mínimo privilegio: cada usuario debe tener solo los permisos que necesita.

## Buenas prácticas para el cliente

Se recomienda:

- No compartir contraseñas.
- No usar usuarios genéricos para varias personas.
- Revisar los logs de forma periódica.
- Comprobar que existen backups recientes.
- Verificar restauraciones de prueba periódicamente.
- Avisar al soporte si aparece un error repetido.
- No borrar copias antiguas sin confirmar que existen copias recientes válidas.
- No modificar ficheros internos del sistema.

## Qué hacer si aparece un error

Si aparece un error en el panel:

1. Anotar la hora del error.
2. Hacer captura de pantalla.
3. Revisar si aparece en la sección Logs.
4. No repetir muchas veces la misma acción si sigue fallando.
5. Contactar con soporte e indicar:
   - Usuario.
   - Acción realizada.
   - Hora aproximada.
   - Mensaje de error.
   - Captura, si existe.

## Responsabilidad del proveedor

En una instalación gestionada, el proveedor o responsable técnico debe encargarse de:

- Instalación inicial.
- Configuración de backups.
- Revisión de alertas.
- Pruebas de restauración.
- Actualizaciones.
- Resolución de incidencias.
- Revisión periódica del estado del sistema.

## Responsabilidad del cliente

El cliente debe encargarse de:

- Usar credenciales de forma segura.
- Avisar si detecta errores.
- No compartir accesos.
- No manipular archivos internos.
- No borrar copias sin confirmación.
- Informar de cambios importantes en la infraestructura.

## Resumen rápido

Vigex permite controlar desde un panel:

- Copias de seguridad.
- Restauraciones.
- Logs.
- Servicios.
- Alertas.
- Usuarios y permisos.

Su finalidad principal es dar tranquilidad al cliente, facilitando que pueda comprobar si sus datos están protegidos y si el sistema funciona correctamente.
