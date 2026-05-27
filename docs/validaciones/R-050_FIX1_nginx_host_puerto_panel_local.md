# R-050-FIX1 - Conservar host y puerto en Nginx panel local

## Objetivo

Corregir la visualización del panel local cuando se accede mediante Nginx usando un puerto distinto de 80.

## Estado

Cerrada.

## Problema detectado

Durante la validación de R-050, el panel local por Nginx en:

- http://192.168.1.250:8080

cargaba el HTML, pero se veía sin estilos.

La causa no era que Nginx no sirviera los estáticos, ya que:

- /static/css/estilo.css por 8000 devolvía 200 OK.
- /static/css/estilo.css por 8080 devolvía 200 OK.

El problema era que el HTML autenticado generaba rutas absolutas sin conservar el puerto 8080:

- http://127.0.0.1/static/css/estilo.css
- http://127.0.0.1/static/img/logo-dasc.png
- http://127.0.0.1/static/img/logo-instituto.png

Esto provoca que el navegador busque recursos en un host/puerto incorrecto.

## Solución aplicada

Se cambia la cabecera proxy de Nginx:

Antes:

- proxy_set_header Host $host;

Después:

- proxy_set_header Host $http_host;
- proxy_set_header X-Forwarded-Host $http_host;

Con esto se conserva el puerto cuando se accede por:

- http://192.168.1.250:8080

## Archivos modificados

- deploy/api/install_nginx_dasc_api.sh

## Validación esperada

R-050-FIX1 se considera correcto cuando:

- nginx -t devuelve OK.
- El panel local por 8080 carga con CSS.
- El HTML genera rutas estáticas con host/puerto correcto.
- El panel central por puerto 80 sigue funcionando.
- El backend directo 8000 sigue funcionando.

## Corrección real aplicada

Durante la primera aplicación del fix se documentó el problema, pero el instalador no cambió porque la línea real dentro del script Bash era:

- proxy_set_header Host \$host;

El símbolo dólar estaba escapado para que Bash no lo expandiera al generar la configuración Nginx.

Se corrige el instalador sustituyendo esa línea por:

- proxy_set_header Host \$http_host;
- proxy_set_header X-Forwarded-Host \$http_host;

Con esto, al reinstalar la configuración, Nginx genera:

- proxy_set_header Host $http_host;
- proxy_set_header X-Forwarded-Host $http_host;

y conserva el puerto 8080 en laboratorio.