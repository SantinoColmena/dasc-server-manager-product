# R-050 - Cierre preparación de despliegue cliente/panel local con Nginx

## Objetivo

Cerrar la validación de Nginx como reverse proxy para el panel local DASC del cliente.

## Estado

Cerrada.

## Contexto

Antes de R-050, el panel local se accedía directamente por el puerto interno de FastAPI/Uvicorn:

- http://IP_CLIENTE:8000

Esto funciona en laboratorio, pero no es el acceso más profesional para una PyME.

R-050 prepara el panel local para poder acceder mediante Nginx.

## Arquitectura objetivo en cliente real

En un cliente real, la arquitectura recomendada es:

- Nginx escucha en puerto 80.
- dasc-api escucha internamente en 127.0.0.1:8000.
- El usuario entra por http://IP_CLIENTE/ o por un nombre DNS local si el cliente lo configura.
- Nginx reenvía internamente hacia FastAPI/Uvicorn.

Flujo:

- http://IP_CLIENTE/
- Nginx puerto 80
- http://127.0.0.1:8000
- DASC API / panel local

## Arquitectura validada en laboratorio

En lab-pruebas ya existía el panel central usando Nginx en el puerto 80.

Por tanto, para no romper el panel central, R-050 se validó usando puerto 8080 para el panel local.

Flujo validado:

- http://192.168.1.250:8080/
- Nginx puerto 8080
- http://127.0.0.1:8000
- DASC API / panel local

El panel central se mantuvo en:

- http://192.168.1.250/
- Nginx puerto 80
- http://127.0.0.1:8010
- DASC Central Support

## Archivos añadidos

- deploy/api/install_nginx_dasc_api.sh
- deploy/api/uninstall_nginx_dasc_api.sh
- docs/validaciones/R-050_nginx_panel_local_cliente.md

## Archivos modificados por FIX1

- deploy/api/install_nginx_dasc_api.sh
- docs/validaciones/R-050_FIX1_nginx_host_puerto_panel_local.md

## Commits relacionados

- 19006c9 feat: añadir nginx para panel local cliente
- cf4a332 fix: conservar host puerto nginx panel local
- 555173f fix: aplicar host puerto nginx panel local

## Validación inicial

Se ejecutó en lab-pruebas:

- sudo env PUBLIC_PORT=8080 SERVER_NAME="_" NGINX_SITE_NAME="dasc-api-local" bash deploy/api/install_nginx_dasc_api.sh

Resultado:

- Nginx instalado o reutilizado correctamente.
- Servicio dasc-api activo.
- Sitio dasc-api-local creado.
- nginx -t correcto.
- Nginx recargado.
- Proxy local en 8080 responde.

## Problema detectado

Durante la validación visual, el panel local por:

- http://192.168.1.250:8080

cargaba el HTML, pero se veía sin estilos.

Se comprobó que no era un problema de Nginx sirviendo estáticos, porque:

- /static/css/estilo.css por 8000 devolvía 200 OK.
- /static/css/estilo.css por 8080 devolvía 200 OK.

El problema real era que el HTML autenticado generaba rutas absolutas sin conservar el puerto 8080:

- http://192.168.1.250/static/css/estilo.css

en lugar de:

- http://192.168.1.250:8080/static/css/estilo.css

## Solución aplicada

Se corrigió la configuración generada por el instalador Nginx.

Antes:

- proxy_set_header Host $host;

Después:

- proxy_set_header Host $http_host;
- proxy_set_header X-Forwarded-Host $http_host;

Con esto, Nginx conserva el host completo con puerto.

## Validación final del FIX1

Se validó en lab-pruebas:

- Configuración Nginx generada correctamente.
- nginx -t correcto.
- Nginx recargado.
- HTML autenticado genera rutas con :8080.
- CSS por 8080 devuelve 200 OK.
- Panel local por 8080 carga con diseño.
- Panel central por puerto 80 sigue funcionando.

## Estado final de accesos en laboratorio

- http://192.168.1.250/        -> panel central DASC por Nginx.
- http://192.168.1.250:8080/   -> panel local cliente por Nginx.
- http://192.168.1.250:8000/   -> backend directo del panel local.
- http://192.168.1.250:8010/   -> backend directo del panel central.

## Decisión de producto

Nginx no es un segundo panel.

Nginx es la puerta de entrada profesional al mismo panel local.

El puerto 8000 debe entenderse como backend interno de FastAPI/Uvicorn.

En cliente real, el acceso recomendado será:

- http://IP_CLIENTE/

o, si el administrador de red configura DNS local:

- http://panel.empresa.lan/
- http://dasc.empresa.lan/
- http://soporte.empresa.lan/

DASC prepara Nginx, pero no modifica automáticamente el DNS de la empresa.

## Límites actuales

R-050 no incluye todavía:

- HTTPS.
- Certbot.
- Dominio real.
- DNS local automático.
- UFW.
- Ocultar puerto 8000 mediante firewall.
- Cabeceras avanzadas de seguridad.

## Próximos pasos recomendados

- R-051 Instaladores adaptables a IPs/perfiles reales.
- Futuro: HTTPS local o certificado interno si el cliente lo requiere.
- Futuro: UFW para limitar exposición de puertos internos.

## Conclusión

DASC Server Manager supera R-050.

El panel local del cliente ya puede funcionar detrás de Nginx, manteniendo FastAPI/Uvicorn como backend interno y preparando el producto para despliegues más profesionales.
