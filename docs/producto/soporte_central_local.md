# Soporte central/local DASC Server Manager

## 1. Objetivo del módulo

El módulo de soporte central/local permite que DASC Server Manager funcione como un servicio gestionado para PYMES.

Su objetivo es separar claramente:

- Lo que ve el cliente.
- Lo que gestiona el técnico desde el panel local.
- Lo que gestiona el equipo DASC desde un panel central.
- La sincronización entre instalaciones locales y la central DASC.

Este módulo evita que el cliente tenga que usar GitHub, herramientas técnicas o canales complejos para abrir incidencias.

## 2. Idea general

Cada cliente tiene su propio panel local DASC instalado en su infraestructura.

El equipo DASC tiene un panel central propio donde recibe y gestiona solicitudes de todos los clientes.

El flujo general es:

- El cliente crea una solicitud desde su panel local.
- El panel local guarda el ticket en SQLite local.
- El panel local intenta enviarlo al panel central DASC.
- Si la central responde, se guarda la referencia central.
- Si la central no responde, el ticket queda localmente como pendiente/error.
- Un timer de systemd reintenta el envío automáticamente.
- El equipo DASC gestiona la incidencia desde el panel central.
- El panel local puede sincronizar el estado actualizado desde la central.
- El cliente puede ver una vista limpia del estado del ticket.

## 3. Separación de responsabilidades

### 3.1 Panel local del cliente

El panel local se instala en cada cliente.

Funciones principales:

- Formulario de soporte.
- Registro local de solicitudes.
- Vista limpia del estado del ticket para cliente.
- Cola de sincronización local-central.
- Reintentos automáticos si la central no está disponible.
- Vista técnica interna para el equipo DASC si está activada.

Ejemplos de rutas locales:

- /soporte
- /soporte/estado/{ticket_id}
- /soporte/tickets
- /soporte/tickets/{ticket_id}
- /soporte/sincronizacion

### 3.2 Panel central DASC

El panel central no se instala en cada cliente.

Debe estar en un servidor propio de DASC, idealmente un VPS o servidor cloud.

Funciones principales:

- Recibir tickets de varios clientes.
- Mostrar tickets centralizados.
- Gestionar estado y prioridad.
- Registrar historial central.
- Servir como herramienta interna del equipo DASC.
- Preparar una visión multi-cliente del soporte.

Ejemplos de rutas centrales:

- /
- /login
- /tickets/{central_ticket_id}
- /api/v1/support/tickets
- /api/v1/support/tickets/{central_ticket_id}

### 3.3 Cliente final

El cliente no debe ver herramientas internas.

El cliente debe poder:

- Crear una solicitud.
- Ver su referencia.
- Consultar el estado.
- Ver la información básica de su solicitud.
- Saber si está registrada, en revisión, pendiente de información, resuelta o cerrada.

El cliente no debe ver:

- Resumen Jira/Zammad.
- Plantillas internas.
- Botones de sincronización central.
- Diagnóstico técnico.
- Errores internos.
- Tokens.
- Configuración.
- Gestión interna del equipo DASC.

## 4. Rutas principales

## 4.1 Rutas visibles para cliente

### /soporte

Formulario principal para crear solicitudes.

Permite registrar:

- Empresa.
- Persona de contacto.
- Email.
- Teléfono.
- Tipo de solicitud.
- Prioridad percibida.
- Servicio afectado.
- Descripción.
- Evidencia opcional.

Después de crear el ticket, muestra la referencia local y enlace a la vista de estado.

### /soporte/estado/{ticket_id}

Vista limpia de seguimiento para el cliente.

Muestra:

- ID del ticket.
- Estado actual.
- Prioridad.
- Tipo.
- Progreso visual.
- Datos básicos.
- Descripción enviada.
- Evidencia aportada.
- Seguimiento básico.
- Información para el cliente.

No permite modificar el ticket.

No muestra herramientas internas.

## 4.2 Rutas técnicas locales

### /soporte/tickets

Vista interna de tickets locales.

Uso recomendado:

- Equipo DASC.
- Técnico autorizado.
- Validaciones internas.
- Diagnóstico del soporte local.

Muestra:

- Total de tickets.
- Abiertos.
- Cerrados.
- Pendientes central.
- Tabla de tickets.
- Referencia central si existe.
- Estado local.
- Prioridad.
- Servicio.
- Enlace a vista técnica.

### /soporte/tickets/{ticket_id}

Vista técnica interna del ticket local.

Permite:

- Actualizar estado y prioridad.
- Generar resumen técnico.
- Usar plantillas de respuesta.
- Ver historial interno.
- Ver sincronización central.
- Sincronizar estado desde central.
- Diagnosticar problemas de integración.

Esta vista no debe ser usada como vista de cliente.

### /soporte/sincronizacion

Vista técnica interna de cola local-central.

Muestra:

- Total local.
- Enviados.
- Pendientes/error.
- Desactivados.
- Sin central.
- Ticket local.
- Cliente.
- Estado central.
- Ticket central.
- Última sincronización.
- Detalle del último intento.

Permite reintentar pendientes si existen.

## 4.3 Rutas centrales

### /

Dashboard central del equipo DASC.

Muestra:

- Total de tickets centralizados.
- Nuevos.
- En gestión.
- Críticos.
- Cerrados/resueltos.
- Filtros por estado.
- Filtros por prioridad.
- Búsqueda.
- Tabla centralizada multi-cliente.

### /tickets/{central_ticket_id}

Vista interna central del ticket.

Permite:

- Consultar datos recibidos desde el cliente.
- Cambiar estado central.
- Cambiar prioridad.
- Registrar historial central.
- Preparar la gestión interna del equipo DASC.

### /api/v1/support/tickets

Endpoint usado por paneles locales para enviar tickets al panel central.

Requiere token de cliente.

### /api/v1/support/tickets/{central_ticket_id}

Endpoint usado por paneles locales para consultar estado actualizado desde central.

## 5. Flujo completo de alta de ticket

El flujo de alta es:

1. El usuario entra al panel local.
2. Abre /soporte.
3. Rellena el formulario.
4. El panel local crea un ticket local tipo DASC-YYYY-NNN.
5. El ticket se guarda en SQLite local.
6. El panel local intenta enviarlo al panel central.
7. Si el envío funciona:
   - La central crea un ticket CENTRAL-YYYY-NNN.
   - El panel local guarda central_ticket_id.
   - central_sync_status pasa a sent.
   - central_sync_detail registra el resultado.
8. Si el envío falla:
   - El ticket local queda guardado.
   - central_sync_status pasa a error.
   - central_sync_detail registra el error.
   - El ticket queda pendiente de reintento.
9. El usuario ve la referencia local.
10. El usuario puede consultar /soporte/estado/{ticket_id}.

## 6. Flujo de reintento offline

Si el panel central no responde, el panel local no pierde la solicitud.

El comportamiento esperado es:

- El ticket se queda guardado localmente.
- Se marca como error de sincronización.
- Se muestra como pendiente/error en /soporte/sincronizacion.
- El botón de reintento manual puede reenviarlo.
- El timer systemd dasc-central-retry.timer intenta reenviarlo periódicamente.
- Cuando la central vuelve a estar disponible, el ticket se envía.
- Se guarda la referencia central.
- El estado pasa a sent.

Esto permite tolerar caídas temporales del servidor central.

## 7. Flujo de sincronización central hacia local

Una vez que el equipo DASC gestiona el ticket en el panel central, el panel local puede consultar el estado actualizado.

El flujo es:

1. El técnico cambia estado/prioridad en el panel central.
2. El panel central guarda el cambio.
3. El panel local tiene central_ticket_id asociado.
4. Desde la vista técnica local se pulsa sincronizar estado desde central.
5. El panel local consulta la API central.
6. El estado/prioridad local se actualizan.
7. El cliente puede ver el estado actualizado en /soporte/estado/{ticket_id}.

## 8. Estados del ticket

Estados habituales:

- Abierto.
- En análisis.
- En curso.
- Pendiente cliente.
- Resuelto.
- Cerrado.

Interpretación para cliente:

- Abierto: solicitud registrada.
- En análisis: el equipo DASC está revisando el caso.
- En curso: el equipo DASC está trabajando en la incidencia.
- Pendiente cliente: se necesita información adicional.
- Resuelto: el caso está solucionado.
- Cerrado: el caso se da por finalizado.

## 9. Prioridades

Prioridades habituales:

- Baja.
- Media.
- Alta.
- Crítica.

La prioridad del cliente se registra como prioridad percibida.

El equipo DASC puede ajustar la prioridad real durante la gestión interna.

## 10. Seguridad aplicada

Medidas actuales:

- Separación de vista cliente y vista técnica.
- Vista técnica local protegida por usuario administrador.
- Activación explícita mediante DASC_LOCAL_INTERNAL_SUPPORT_ENABLED.
- Panel central con login propio.
- Credenciales centrales gestionadas mediante variables de entorno.
- Bloqueo de credenciales de laboratorio si DASC_CENTRAL_LAB_MODE=false.
- config.env del panel central protegido como root:root 600.
- Panel central servido mediante Nginx.
- Tokens para comunicación local-central.

## 11. Seguridad pendiente o futura

Mejoras futuras recomendadas:

- HTTPS real con dominio.
- Certbot o certificados gestionados.
- UFW/firewall.
- Restringir puerto 8010 al acceso local.
- Bloqueo por intentos fallidos.
- Auditoría completa de login central.
- Usuarios centrales en base de datos.
- Contraseñas hasheadas.
- 2FA.
- Rotación de tokens por cliente.
- Panel de gestión de clientes y tokens.
- Logs de seguridad centralizados.

## 12. Nginx y despliegue central

En laboratorio, el panel central se validó así:

- Nginx escucha en puerto 80.
- central-support escucha en puerto 8010.
- Nginx reenvía tráfico hacia 127.0.0.1:8010.

Flujo:

- http://192.168.1.250/
- Nginx
- http://127.0.0.1:8010
- DASC Central Support

En producción, el objetivo sería:

- https://central.dasc.es
- Nginx con HTTPS
- Backend central-support en 127.0.0.1:8010
- Firewall evitando exponer 8010 directamente

## 13. DNS y acceso en clientes

El panel local del cliente puede funcionar por IP.

Ejemplo:

- http://192.168.1.50

Modo recomendado:

- El instalador prepara Nginx en el servidor local.
- El panel local queda accesible por IP.
- Si el cliente quiere nombre interno, su administrador configura DNS local.

Ejemplos:

- http://panel.empresa.lan
- http://dasc.empresa.lan
- http://soporte.empresa.lan

DASC no debe modificar automáticamente el DNS de la empresa salvo que tenga autorización y acceso al sistema DNS del cliente.

## 14. Arquitectura objetivo futura

En producto real:

- Cada cliente tiene su panel local.
- DASC tiene un panel central único.
- Los paneles locales envían tickets al panel central.
- El panel central se aloja en un VPS o cloud propio de DASC.
- El acceso central se hace por dominio público y HTTPS.
- El cliente solo consulta su panel local.
- El equipo DASC gestiona todo desde el panel central.

Flujo objetivo:

- Cliente A local -> central.dasc.es
- Cliente B local -> central.dasc.es
- Cliente C local -> central.dasc.es
- Equipo DASC -> central.dasc.es

## 15. Variables relevantes

Variables locales habituales:

- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED
- DASC_CENTRAL_SUPPORT_ENABLED
- DASC_CENTRAL_SUPPORT_URL
- DASC_CENTRAL_SUPPORT_TOKEN
- DASC_CLIENT_ID
- DASC_CLIENT_NAME
- DASC_LOCAL_PANEL_VERSION

Variables centrales habituales:

- DASC_CENTRAL_AUTH_ENABLED
- DASC_CENTRAL_LAB_MODE
- DASC_CENTRAL_SECRET_KEY
- DASC_CENTRAL_ADMIN_USER
- DASC_CENTRAL_ADMIN_PASSWORD
- DASC_CENTRAL_TECH_USER
- DASC_CENTRAL_TECH_PASSWORD
- DASC_CENTRAL_DEMO_CLIENT_ID
- DASC_CENTRAL_DEMO_CLIENT_NAME
- DASC_CENTRAL_DEMO_TOKEN

## 16. Base de datos local de soporte

La base local de soporte usa SQLite.

Ruta habitual:

- /opt/dasc/api/data/support_tickets.db

Contiene tickets locales y campos de sincronización central.

Campos importantes:

- id
- cliente
- contacto
- email
- telefono
- tipo
- prioridad
- servicio
- estado
- descripcion
- evidencia
- fecha_apertura
- fecha_actualizacion
- central_ticket_id
- central_sync_status
- central_sync_detail
- central_sync_at

## 17. Base de datos central de soporte

La base central usa SQLite en la validación actual.

Ruta habitual:

- /opt/dasc/central-support/data/central_support.db

Contiene:

- Tickets centralizados.
- Estado central.
- Prioridad central.
- Cliente origen.
- Ticket local asociado.
- Historial interno central.

En una evolución de producto, esta base podría migrarse a PostgreSQL o MariaDB si aumenta el número de clientes.

## 18. Evidencias validadas

Durante las tareas R-049L a R-049W se validó:

- Creación local de tickets.
- Envío a central.
- Guardado de central_ticket_id.
- Simulación de central apagado.
- Cola offline.
- Reintento manual.
- Reintento automático con systemd timer.
- Sincronización desde central.
- Login del panel central.
- Instalador systemd de central-support.
- Nginx reverse proxy.
- Endurecimiento de credenciales.
- Vista técnica de sincronización.
- Vista cliente limpia.

## 19. Limitaciones actuales

El módulo aún no incluye:

- Comentarios bidireccionales cliente-DASC.
- Adjuntos reales subidos por formulario.
- Portal público sin login por código seguro.
- Notificaciones automáticas por email.
- SLA visual.
- Exportación CSV.
- Panel de clientes centralizado.
- Gestión de tokens desde interfaz.
- Alta/baja de clientes desde central.
- Multiusuario avanzado en central.
- Hash de contraseñas.
- 2FA.
- HTTPS real.
- VPS real.

## 20. Conclusión

El módulo de soporte central/local convierte DASC Server Manager en una base más cercana a producto-servicio.

Permite que cada cliente tenga un canal simple para comunicar incidencias y que el equipo DASC tenga herramientas internas para gestionarlas, sincronizarlas y centralizarlas.

La separación entre vista cliente, vista técnica local y panel central evita mezclar experiencia de usuario con herramientas internas.
