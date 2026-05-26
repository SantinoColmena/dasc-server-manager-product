# R-049X - Cierre documentación global soporte central/local

## Objetivo

Cerrar la documentación global del módulo de soporte central/local de DASC Server Manager.

## Estado

Cerrada.

## Contexto

Después de completar las tareas R-049L a R-049W, el módulo de soporte dejó de ser una funcionalidad aislada y pasó a convertirse en una parte importante de la evolución de DASC Server Manager hacia producto-servicio.

El módulo ya incluye:

- Formulario local de soporte.
- Vista cliente limpia.
- Vista técnica local.
- Cola offline.
- Reintentos manuales.
- Reintentos automáticos con systemd timer.
- Sincronización central-local.
- Panel central DASC.
- Login central.
- Nginx reverse proxy.
- Endurecimiento básico de credenciales.
- Separación entre cliente, técnico local y central DASC.

## Documentos creados

Se crearon los siguientes documentos:

- docs/producto/soporte_central_local.md
- docs/arquitectura/soporte_central_local_arquitectura.md
- docs/validaciones/R-049X_documentacion_global_soporte_central_local.md

## Documento de producto

El documento docs/producto/soporte_central_local.md recoge la visión funcional completa del módulo.

Incluye:

- Objetivo del módulo.
- Idea general.
- Separación de responsabilidades.
- Rutas principales.
- Flujo completo de alta de ticket.
- Flujo de reintento offline.
- Flujo de sincronización central hacia local.
- Estados del ticket.
- Prioridades.
- Seguridad aplicada.
- Seguridad futura.
- Nginx y despliegue central.
- DNS y acceso en clientes.
- Arquitectura objetivo futura.
- Variables relevantes.
- Bases de datos.
- Evidencias validadas.
- Limitaciones actuales.

## Documento de arquitectura

El documento docs/arquitectura/soporte_central_local_arquitectura.md resume la arquitectura en tres capas:

- Cliente.
- Panel local DASC.
- Panel central DASC.

También documenta:

- Separación de vistas.
- Despliegue de laboratorio.
- Despliegue objetivo.
- Decisión sobre DNS local.
- Diferencia entre acceso por IP y acceso por DNS local.

## Criterios de producto documentados

Queda documentado que:

- El panel local se instala en cada cliente.
- El panel central no se instala en cada cliente.
- El panel central debe vivir en un servidor/VPS propio de DASC.
- El cliente puede acceder por IP local.
- El DNS local lo configura el administrador de red del cliente si lo desea.
- DASC puede preparar Nginx, pero no debe asumir control automático del DNS de la empresa.
- El dominio público central futuro sería algo tipo central.dasc.es o soporte.dasc.es.

## Separación de vistas documentada

Queda documentada la separación entre:

### Cliente

- /soporte
- /soporte/estado/{ticket_id}

### Técnico local DASC

- /soporte/tickets
- /soporte/tickets/{ticket_id}
- /soporte/sincronizacion

### Equipo central DASC

- /
- /tickets/{central_ticket_id}

## Resultado

R-049X queda validada correctamente.

El módulo de soporte central/local queda documentado como una pieza completa de producto, no solo como una función técnica aislada.

## Límites actuales

La documentación también deja claros los límites actuales:

- No hay comentarios bidireccionales cliente-DASC.
- No hay adjuntos reales por ticket.
- No hay portal público por código seguro.
- No hay email automático.
- No hay SLA visual.
- No hay panel de clientes completo.
- No hay gestión de tokens desde interfaz.
- No hay HTTPS real todavía.
- No hay VPS real todavía.

## Conclusión

DASC Server Manager supera R-049X.

El proyecto ya cuenta con una documentación global sólida para explicar el soporte central/local como parte de la transición de MVP académico a base de producto-servicio.
