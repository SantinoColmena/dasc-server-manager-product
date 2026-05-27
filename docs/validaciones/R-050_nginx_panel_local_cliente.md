# R-050 - Preparación de despliegue cliente/panel local con Nginx

## Objetivo

Preparar el panel local DASC del cliente para poder acceder mediante Nginx, evitando depender directamente del puerto interno 8000.

## Estado

En curso.

## Contexto

Hasta ahora, el panel local del cliente se accede directamente por:

- http://IP_CLIENTE:8000

Esto funciona en laboratorio, pero en un despliegue más profesional conviene usar Nginx como reverse proxy.

## Decisión aplicada

Se añade un instalador Nginx para el panel local:

- deploy/api/install_nginx_dasc_api.sh
- deploy/api/uninstall_nginx_dasc_api.sh

El instalador permite configurar:

- SERVICE_NAME
- NGINX_SITE_NAME
- APP_HOST
- APP_PORT
- PUBLIC_PORT
- SERVER_NAME

## Arquitectura prevista

En producción cliente:

- Nginx escucha en puerto 80.
- dasc-api escucha internamente en puerto 8000.
- Nginx reenvía tráfico hacia 127.0.0.1:8000.

Flujo:

- http://IP_CLIENTE/
- Nginx puerto 80
- http://127.0.0.1:8000
- DASC API / panel local

## Validación en laboratorio

En lab-pruebas ya existe el panel central DASC usando Nginx en puerto 80.

Por tanto, para no romper el panel central, R-050 se validará usando:

- PUBLIC_PORT=8080

Flujo de laboratorio:

- http://192.168.1.250:8080/
- Nginx puerto 8080
- http://127.0.0.1:8000
- DASC API / panel local

## DNS local

DASC prepara Nginx en el servidor local.

El acceso puede quedar por IP:

- http://192.168.1.50/

Si el cliente quiere un nombre interno, su administrador de red debe crear el DNS local.

Ejemplos:

- panel.empresa.lan
- dasc.empresa.lan
- soporte.empresa.lan

DASC no debe modificar automáticamente el DNS de la empresa salvo autorización y acceso explícito.

## Criterio de validación

R-050 se considera preparada cuando:

- El instalador existe.
- El desinstalador existe.
- Nginx se instala o reutiliza correctamente.
- Se crea el sitio dasc-api-local.
- nginx -t devuelve OK.
- Nginx queda activo.
- El panel local responde por Nginx.
- El backend directo 8000 sigue funcionando.
- El panel central por Nginx puerto 80 no se rompe en lab-pruebas.
- La documentación queda versionada en GitHub.

## Límites

Esta tarea no incluye todavía:

- HTTPS.
- Certbot.
- Dominio real.
- DNS local automático.
- UFW.
- Ocultar puerto 8000 mediante firewall.
- Cabeceras avanzadas de seguridad.

## Próximo paso

Validar en lab-pruebas con PUBLIC_PORT=8080.
