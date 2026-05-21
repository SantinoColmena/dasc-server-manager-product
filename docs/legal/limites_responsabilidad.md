# Límites de responsabilidad del servicio - DASC Server Manager

## 1. Objetivo del documento

Este documento define los límites de responsabilidad del servicio DASC Server Manager.

El objetivo es dejar claro qué cubre el producto, qué cubre el servicio de instalación o mantenimiento, qué responsabilidades corresponden al cliente y qué situaciones quedan fuera del alcance.

Este documento es importante porque DASC Server Manager trabaja con copias de seguridad, logs, servicios y datos empresariales. Por tanto, antes de ofrecerlo como producto real, es necesario evitar promesas poco realistas y definir un marco claro de uso.

---

## 2. Alcance general de DASC Server Manager

DASC Server Manager es una herramienta local orientada a facilitar la gestión de copias de seguridad, servicios, logs y alertas básicas desde un panel web.

El producto está pensado para ayudar a pequeñas y medianas empresas a mejorar el control sobre sus datos y operaciones del servidor.

DASC Server Manager puede ayudar en tareas como:

- Ejecutar copias de seguridad.
- Consultar historial de acciones.
- Revisar logs del panel.
- Controlar servicios básicos.
- Recibir alertas.
- Centralizar tareas administrativas sencillas.
- Reducir dependencia de procesos manuales.

DASC Server Manager no debe presentarse como una garantía absoluta de seguridad, continuidad o recuperación de datos.

---

## 3. Qué cubre DASC

Dependiendo del paquete contratado, DASC puede cubrir:

- Instalación inicial del panel.
- Configuración básica del entorno.
- Configuración de acceso a la base de datos.
- Configuración del servidor de backups.
- Configuración de logs.
- Configuración de usuarios iniciales.
- Configuración básica de permisos.
- Configuración de alertas si están incluidas.
- Configuración de Cacti si está incluido en el paquete.
- Prueba inicial de backup.
- Prueba inicial de restauración si está incluida.
- Documentación básica de uso.
- Soporte inicial durante el arranque.
- Corrección de errores propios del software DASC.
- Revisión del funcionamiento según el plan contratado.

---

## 4. Qué no cubre DASC por defecto

Salvo contratación específica, DASC no cubre:

- Reparación de hardware del cliente.
- Sustitución de discos dañados.
- Administración completa de todos los servidores del cliente.
- Gestión completa de la red interna del cliente.
- Configuración avanzada de firewall no relacionada con DASC.
- Auditoría completa de ciberseguridad.
- Protección absoluta frente a ataques externos.
- Recuperación garantizada de datos si no existen backups válidos.
- Soporte 24/7.
- Monitorización permanente si no se contrata mantenimiento.
- Desarrollo a medida ilimitado.
- Migraciones complejas no acordadas previamente.
- Formación avanzada de administradores.
- Gestión de sistemas ajenos al alcance contratado.
- Responsabilidad sobre cambios realizados manualmente por terceros.
- Responsabilidad sobre credenciales entregadas de forma incorrecta.

---

## 5. Responsabilidad sobre copias de seguridad

DASC Server Manager facilita la creación, gestión y revisión de copias de seguridad, pero el cliente sigue teniendo responsabilidades importantes.

### DASC puede responsabilizarse de:

- Configurar el sistema de backups según el paquete contratado.
- Validar que el sistema puede ejecutar una copia inicial.
- Documentar la ubicación de las copias.
- Configurar la retención básica.
- Mostrar el estado de las copias desde el panel.
- Avisar de errores si el sistema de alertas está configurado.
- Realizar pruebas de restauración si están incluidas en el servicio.

### El cliente debe responsabilizarse de:

- Mantener encendidos y accesibles los servidores necesarios.
- Garantizar espacio suficiente en disco.
- No eliminar manualmente copias de seguridad necesarias.
- No modificar rutas, usuarios o permisos sin avisar.
- Conservar las credenciales de forma segura.
- Revisar periódicamente que el sistema funciona.
- Solicitar pruebas de restauración si necesita garantías adicionales.
- Informar de cambios en la infraestructura.

---

## 6. Situaciones en las que no se puede garantizar recuperación de datos

DASC no puede garantizar la recuperación de datos en situaciones como:

- El cliente ha eliminado manualmente los backups.
- El disco donde estaban las copias se ha dañado.
- Las copias estaban incompletas por falta de espacio.
- Las credenciales de base de datos eran incorrectas.
- El servidor de backups estaba apagado o inaccesible.
- Se modificó la configuración sin avisar.
- La base de datos original estaba corrupta antes de la copia.
- El cliente no contrató pruebas de restauración.
- Las copias fueron cifradas, borradas o alteradas por un ataque externo.
- Las copias se almacenaban en el mismo servidor que falló físicamente.
- El cliente no aplicó las recomendaciones mínimas de separación de servidores.

---

## 7. Responsabilidad sobre seguridad

DASC Server Manager mejora la trazabilidad y el control operativo, pero no sustituye una auditoría completa de ciberseguridad.

### DASC puede aportar:

- Control de acceso al panel.
- Gestión básica de usuarios.
- Registro de acciones.
- Logs de actividad.
- Separación de permisos por módulo.
- Recomendaciones de despliegue.
- Configuración básica segura según el paquete.

### DASC no garantiza:

- Protección total frente a ciberataques.
- Eliminación de todos los riesgos.
- Seguridad absoluta del servidor del cliente.
- Protección frente a malas prácticas externas.
- Seguridad de sistemas no gestionados por DASC.
- Cumplimiento legal completo sin revisión especializada.
- Seguridad de contraseñas compartidas indebidamente por el cliente.

---

## 8. Responsabilidad sobre usuarios y credenciales

El cliente es responsable de gestionar correctamente sus usuarios y credenciales.

DASC recomienda:

- Usar contraseñas seguras.
- No compartir usuarios entre varias personas.
- Eliminar usuarios que ya no trabajen en la empresa.
- Revisar permisos periódicamente.
- Cambiar contraseñas ante sospechas de acceso indebido.
- Guardar tokens y claves fuera del repositorio.
- No publicar archivos config.env reales.

DASC no se responsabiliza de accesos indebidos provocados por:

- Contraseñas débiles.
- Contraseñas compartidas.
- Usuarios antiguos no eliminados.
- Credenciales publicadas por error.
- Tokens enviados por canales inseguros.
- Accesos físicos no controlados al servidor.

---

## 9. Responsabilidad sobre infraestructura del cliente

DASC Server Manager depende de la infraestructura donde se instala.

El cliente debe asegurar:

- Servidores encendidos.
- Conectividad de red.
- Almacenamiento suficiente.
- Sistema operativo actualizado.
- Acceso SSH funcional si se usa arquitectura multi-servidor.
- Base de datos accesible.
- Permisos correctos.
- Copias externas si el nivel de criticidad lo requiere.

DASC no se responsabiliza de fallos causados por:

- Cortes eléctricos.
- Fallos de hardware.
- Problemas de red ajenos al producto.
- Cambios manuales del cliente.
- Eliminación de usuarios del sistema.
- Cambios en firewall.
- Cambios en IPs.
- Cambios en contraseñas sin actualizar la configuración.
- Sistemas operativos sin mantenimiento.

---

## 10. Responsabilidad sobre servicios controlados desde el panel

El módulo de servicios permite iniciar, detener o reiniciar servicios del sistema.

Esta función debe usarse con cuidado.

DASC puede configurar el acceso a servicios concretos, pero no debe permitir por defecto el control libre de cualquier servicio crítico.

El cliente debe entender que detener servicios importantes puede provocar:

- Caída de aplicaciones.
- Interrupción de bases de datos.
- Pérdida temporal de acceso.
- Errores en procesos activos.
- Interrupción de usuarios conectados.

DASC no se responsabiliza de interrupciones provocadas por acciones realizadas manualmente desde el panel por usuarios autorizados del cliente.

---

## 11. Responsabilidad sobre alertas

Las alertas ayudan a detectar errores, pero no garantizan que todos los problemas sean detectados a tiempo.

DASC puede configurar alertas para:

- Backups correctos.
- Backups fallidos.
- Errores de servicios.
- Errores generales del panel.
- Eventos relevantes del sistema.

DASC no puede garantizar la entrega de alertas si:

- Telegram u otro proveedor externo falla.
- El bot ha sido eliminado.
- El token es incorrecto.
- El chat destino ha cambiado.
- El servidor no tiene conexión a Internet.
- El cliente no revisa los avisos.
- La alerta fue desactivada por el usuario.

---

## 12. Responsabilidad sobre Cacti y monitorización

Cacti puede incluirse como complemento de monitorización, especialmente en el paquete Pro.

DASC puede instalar y configurar una monitorización básica, pero no garantiza por defecto una supervisión completa de toda la infraestructura del cliente.

Queda fuera del alcance por defecto:

- Monitorización avanzada de todos los dispositivos.
- Creación de dashboards complejos.
- Integración con todos los sistemas internos.
- Monitorización 24/7.
- Respuesta automática ante incidentes.
- Informes avanzados personalizados.

---

## 13. Responsabilidad sobre mantenimiento

DASC Server Manager puede instalarse como producto de pago único o como producto acompañado de mantenimiento.

Si el cliente no contrata mantenimiento, DASC no se responsabiliza de:

- Revisiones periódicas.
- Actualizaciones futuras.
- Comprobación continua de backups.
- Pruebas regulares de restauración.
- Revisión de logs.
- Cambios en la infraestructura.
- Soporte fuera de la instalación inicial.

Si el cliente contrata mantenimiento, el alcance deberá definirse en un acuerdo separado.

---

## 14. Buenas prácticas recomendadas al cliente

Para reducir riesgos, se recomienda al cliente:

- Separar el servidor de backups del servidor principal siempre que sea posible.
- Realizar pruebas de restauración periódicas.
- Mantener los sistemas actualizados.
- Revisar logs de forma regular.
- Usar contraseñas seguras.
- Guardar credenciales en un lugar seguro.
- No modificar archivos de configuración sin aviso.
- No eliminar backups manualmente.
- Revisar el espacio disponible en disco.
- Mantener una copia externa adicional para datos críticos.
- Documentar cambios importantes de infraestructura.

---

## 15. Condiciones mínimas antes de un piloto real

Antes de usar DASC Server Manager en un entorno real, se recomienda realizar una instalación piloto.

La instalación piloto debería validar:

- Acceso al panel.
- Creación de usuarios.
- Conexión con la base de datos.
- Creación de backup completo.
- Creación de backup incremental si está incluida.
- Creación de backup diferencial si está incluida.
- Consulta de logs.
- Control de servicios permitidos.
- Envío de alertas si están activadas.
- Restauración de prueba.
- Revisión de permisos.
- Espacio disponible.
- Documentación entregada al cliente.

---

## 16. Frase legal simplificada

DASC Server Manager es una herramienta de apoyo para la gestión de backups, logs, servicios y alertas. Su uso mejora el control operativo, pero no garantiza por sí solo la seguridad absoluta, la continuidad total del servicio ni la recuperación de datos en cualquier circunstancia.

---

## 17. Conclusión

Definir límites de responsabilidad es imprescindible antes de convertir DASC Server Manager en un producto real.

El producto puede aportar mucho valor a pequeñas y medianas empresas, pero debe venderse con un alcance claro, evitando prometer garantías absolutas.

La responsabilidad debe repartirse correctamente entre el software, el proveedor del servicio y el cliente. De esta forma se reduce el riesgo comercial, técnico y legal del proyecto.
