# R-049V - Cierre reverse proxy Nginx para central-support

## Objetivo

Cerrar la validación del reverse proxy Nginx para el panel central DASC.

## Estado

Cerrada.

## Contexto

Antes de R-049V, el panel central DASC se accedía directamente por el puerto interno:

- http://IP_SERVIDOR:8010

Esto era válido para laboratorio, pero menos profesional para una base de producto.

R-049V prepara el acceso mediante Nginx, dejando el backend FastAPI en 8010 y exponiendo el panel central por HTTP estándar en el puerto 80.

## Arquitectura validada en laboratorio

En lab-pruebas se validó:

- Nginx en puerto 80.
- central-support en puerto 8010.
- Nginx reenvía tráfico hacia 127.0.0.1:8010.

Flujo validado:

- http://192.168.1.250/
- Nginx puerto 80
- proxy_pass hacia http://127.0.0.1:8010
- DASC Central Support

## Archivos añadidos

- deploy/central-support/install_nginx_central_support.sh
- deploy/central-support/uninstall_nginx_central_support.sh
- docs/validaciones/R-049V_reverse_proxy_nginx_central_support.md

## Commit funcional

- ebedee2 feat: añadir nginx reverse proxy central support

## Validación de instalación

Se ejecutó en lab-pruebas:

- sudo bash deploy/central-support/install_nginx_central_support.sh

Resultado:

- Nginx instalado correctamente.
- Configuración creada correctamente.
- Sitio default de Nginx desactivado.
- Sitio dasc-central-support activado.
- nginx -t correcto.
- nginx habilitado.
- nginx reiniciado correctamente.

## Servicios validados

Se comprobó:

- nginx active.
- nginx enabled.
- dasc-central-support active.
- dasc-central-support enabled.

## Puertos validados

Se comprobó:

- 0.0.0.0:80 escuchando con nginx.
- 0.0.0.0:8010 escuchando con central-support.
- 0.0.0.0:8000 escuchando con dasc-api local.

## Configuración Nginx validada

Se comprobó:

- /etc/nginx/sites-available/dasc-central-support existe.
- /etc/nginx/sites-enabled/dasc-central-support apunta al sitio disponible.
- nginx -t devuelve configuración correcta.

## Backend directo validado

Se comprobó:

- http://127.0.0.1:8010/health

Resultado:

- status: ok
- app: DASC Central Support
- db: /opt/dasc/central-support/data/central_support.db
- demo_client_id: cliente-demo-a

## Acceso por Nginx validado

Se comprobó:

- http://127.0.0.1/

Resultado:

- HTTP 303
- location: /login?msg=Sesion+requerida

Esto confirma que Nginx llega correctamente al panel central.

## Login por Nginx validado

Se realizó login por:

- http://127.0.0.1/login

Resultado:

- HTTP 303
- location: /
- cookie de sesión creada

## Dashboard por Nginx validado

Se accedió con cookie a:

- http://127.0.0.1/

Resultado:

- HTTP 200
- HTML del dashboard central cargado correctamente.

## Validación visual

En navegador se comprobó:

- http://192.168.1.250/

Resultado:

- Se muestra el login del panel central DASC sin usar :8010.

## Aclaración de arquitectura futura

En laboratorio, el panel central está en la misma VM lab-pruebas que también contiene el panel local.

En producto real, esta no debe ser la arquitectura final.

La arquitectura objetivo será:

- Panel local cliente: instalado en cada cliente.
- Panel central DASC: instalado solo en un servidor/VPS propio de DASC.
- Dominio público futuro: central.dasc.es o soporte.dasc.es.
- Nginx + HTTPS en el servidor central DASC.

## Criterio para panel local del cliente

Para clientes se adopta el modo recomendado:

- El instalador prepara Nginx local.
- El panel local queda accesible por IP.
- Si el cliente quiere nombre interno, su administrador configura DNS local.
- No se intenta modificar automáticamente el DNS de la empresa.

Ejemplos:

- http://192.168.1.50
- http://panel.empresa.lan
- http://dasc.empresa.lan

## Criterio para panel central DASC

El panel central será único y nuestro.

Ejemplo futuro:

- https://central.dasc.es

Los paneles locales de los clientes enviarán tickets a ese dominio mediante HTTPS y token de cliente.

## Resultado

R-049V queda validada correctamente.

El panel central DASC ya puede funcionar detrás de Nginx y queda preparado para una arquitectura más profesional con dominio y HTTPS en una fase posterior.

## Límites actuales

Esta tarea no incluye todavía:

- HTTPS real.
- Certbot.
- Dominio público.
- UFW activado.
- Restricción por IP.
- Ocultar 8010 mediante firewall.
- Cabeceras avanzadas de seguridad.
- Separación física en VPS real.

## Próximas tareas recomendadas

- R-049W - Panel visual de cola/sincronización.
- R-049X - Documentación global del soporte central.
- R-049Y - Preparación futura HTTPS/dominio.
- Futuro: VPS real para central.dasc.es.

## Conclusión

DASC Server Manager supera R-049V.

El panel central deja de depender directamente del puerto 8010 y pasa a estar servido mediante Nginx, manteniendo FastAPI como backend interno.
