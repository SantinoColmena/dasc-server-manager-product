# Canales reales de soporte - Vigex

## Objetivo

Definir los canales mínimos por los que un cliente PyME puede contactar con el equipo Vigex sin usar GitHub.

## Principio

El cliente debe tener canales simples, claros y controlados.

GitHub queda reservado para gestión interna del equipo Vigex.

## Canales oficiales recomendados

| Canal | Uso principal | Estado |
|---|---|---|
| Email de soporte | Canal base para incidencias y consultas | Recomendado desde el inicio |
| Formulario de soporte | Canal estructurado para recoger datos mínimos | Recomendado |
| WhatsApp controlado | Canal rápido para incidencias urgentes o coordinación | Opcional |
| Teléfono controlado | Canal para casos urgentes o planes superiores | Opcional |
| Portal de cliente | Canal futuro para tickets e informes | Futuro |

## Email de soporte

### Uso

El email será el canal principal para clientes.

Sirve para:

- Reportar incidencias.
- Solicitar ayuda.
- Pedir cambios.
- Adjuntar capturas.
- Solicitar informes.
- Pedir revisión de backups o servicios.

### Ejemplo temporal

~~~text
soporte@vigex.local
~~~

En entorno real debe sustituirse por un dominio comercial.

### Ventajas

- Es familiar para clientes PyME.
- Permite adjuntar evidencias.
- Deja trazabilidad.
- No obliga al cliente a usar herramientas técnicas.

## Formulario de soporte

### Uso

El formulario ayuda a recoger la información mínima de forma ordenada.

### Campos mínimos

| Campo | Obligatorio | Descripción |
|---|---|---|
| Empresa | Sí | Nombre del cliente |
| Persona de contacto | Sí | Nombre de quien reporta |
| Email | Sí | Canal principal de respuesta |
| Teléfono | Opcional | Contacto rápido |
| Tipo de solicitud | Sí | Incidencia, consulta, cambio, restauración, informe |
| Prioridad percibida | Sí | Crítica, alta, media o baja |
| Servicio afectado | Sí | API, DB, backups, logs, alertas, informes u otro |
| Descripción | Sí | Explicación del problema |
| Fecha/hora aproximada | Opcional | Momento en que ocurrió |
| Captura o evidencia | Opcional | Imagen, texto o archivo |

## WhatsApp controlado

### Uso

WhatsApp puede usarse para planes con soporte cercano.

Debe limitarse a:

- Avisos urgentes.
- Confirmación rápida.
- Coordinación de intervención.
- Seguimiento de una incidencia ya registrada.

### Regla importante

WhatsApp no sustituye al ticket interno.

Toda solicitud recibida por WhatsApp debe registrarse después en el sistema interno.

## Teléfono controlado

### Uso

El teléfono se reserva para:

- Incidencias críticas.
- Caída de servicio importante.
- Restauraciones urgentes.
- Clientes con plan Pro o soporte prioritario.

### Regla importante

Toda llamada debe terminar en un registro interno.

## Portal de cliente futuro

### Uso previsto

A medio plazo, Vigex puede incorporar un portal de cliente.

Funciones futuras:

- Crear tickets.
- Consultar estado.
- Descargar informes.
- Ver historial.
- Solicitar restauración.
- Consultar mantenimientos.

## Datos mínimos para abrir soporte

Para poder actuar correctamente, el equipo Vigex debe intentar obtener como mínimo:

~~~text
Cliente
Persona de contacto
Canal de respuesta
Servicio afectado
Descripción
Prioridad percibida
Fecha/hora del problema
Evidencia si existe
~~~

## Qué se comunica al cliente

La respuesta al cliente debe ser clara y no excesivamente técnica.

Debe incluir:

- Confirmación de recepción.
- Prioridad asignada.
- Próximo paso.
- Tiempo estimado si aplica.
- Resultado final cuando se cierre.

## Qué se registra internamente

Internamente se debe registrar:

- Ticket.
- Diagnóstico técnico.
- Acciones realizadas.
- Evidencias.
- Cambios aplicados.
- Comunicación enviada.
- Resultado final.

## Conclusión

Vigex debe usar canales simples para el cliente y mantener la gestión técnica de soporte de forma interna.

El cliente no necesita GitHub para recibir soporte.
## Integración con herramientas gratuitas de ticketing

Los canales anteriores no obligan a gestionar todo manualmente.

Vigex puede conectar esos canales con una herramienta interna de ticketing.

Opciones contempladas:

| Herramienta | Uso | Decisión |
|---|---|---|
| Jira Service Management Free | Ticketing profesional inicial para equipo pequeño | Recomendada |
| Zammad self-hosted | Ticketing open source autogestionado | Alternativa |
| Freshdesk | Ticketing comercial con periodo gratuito limitado | Futura |
| GLPI | ITSM/inventario/ticketing | Descartada temporalmente |

El cliente seguirá usando canales simples.

~~~text
Email / Formulario / WhatsApp / Teléfono
~~~

El equipo Vigex podrá registrar o centralizar esas solicitudes en Jira o Zammad.

GitHub sigue siendo únicamente herramienta interna de desarrollo.