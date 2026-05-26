# R-049V - Reverse proxy Nginx para central-support

## Objetivo

Preparar el panel central DASC para acceder mediante Nginx, evitando depender directamente del puerto interno 8010.

## Estado

Cerrada.

## Contexto

Antes de R-049V, el panel central se accede directamente por:

- http://IP_SERVIDOR:8010

Esto es válido para laboratorio, pero en un entorno más profesional conviene usar un reverse proxy.

## Decisión aplicada

Se añade Nginx como reverse proxy:

- Puerto público: 80
- Backend interno: 127.0.0.1:8010
- Servicio backend: dasc-central-support

## Archivos añadidos

- deploy/central-support/install_nginx_central_support.sh
- deploy/central-support/uninstall_nginx_central_support.sh
- docs/validaciones/R-049V_reverse_proxy_nginx_central_support.md

## Funcionamiento

Nginx recibe peticiones HTTP en el puerto 80 y las reenvía al panel central en:

- http://127.0.0.1:8010

Cabeceras proxy configuradas:

- Host
- X-Real-IP
- X-Forwarded-For
- X-Forwarded-Proto

## Ventajas

- Acceso más profesional sin escribir :8010.
- Preparación para futuro HTTPS.
- Separación entre puerto público y backend interno.
- Base para dominio real.
- Base para futuras reglas de seguridad.

## Validación esperada

R-049V se considera preparada cuando:

- Nginx se instala correctamente.
- Se crea /etc/nginx/sites-available/dasc-central-support.
- Se activa /etc/nginx/sites-enabled/dasc-central-support.
- nginx -t devuelve OK.
- Nginx queda activo.
- http://127.0.0.1/ responde.
- http://IP_SERVIDOR/ muestra el login central.
- Login central sigue funcionando.
- Dashboard central sigue funcionando.
- Backend 8010 sigue funcionando.
- central-support sigue activo.

## Límites actuales

Esta tarea no incluye todavía:

- HTTPS real.
- Certbot.
- Dominio público.
- Restricción por IP.
- UFW activado.
- Cabeceras avanzadas de seguridad.
- Ocultar el puerto 8010 mediante firewall.

## Próximo paso

Validar en lab-pruebas.

## Conclusión

R-049V prepara el panel central para un despliegue más profesional usando Nginx como reverse proxy.
