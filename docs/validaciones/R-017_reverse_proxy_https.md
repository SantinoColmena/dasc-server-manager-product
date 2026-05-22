# Validación R-017 - Reverse proxy y HTTPS

## Objetivo

Añadir una capa de reverse proxy delante del panel DASC Server Manager para no exponer directamente Uvicorn en producción o laboratorio real.

## Decisión técnica

Se utiliza Nginx como reverse proxy.

El panel FastAPI/Uvicorn seguirá escuchando internamente en:

    127.0.0.1:8000

Nginx será el punto de entrada externo mediante:

    HTTP  puerto 80
    HTTPS puerto 443

En laboratorio se usa un certificado autofirmado. En un despliegue real con dominio se podrá sustituir por un certificado válido, por ejemplo usando Let's Encrypt.

## Cambios realizados

- Se crea `deploy/proxy/install_reverse_proxy.sh`.
- Se crea `deploy/proxy/uninstall_reverse_proxy.sh`.
- El instalador instala Nginx y OpenSSL.
- El instalador genera un certificado autofirmado de laboratorio.
- El instalador crea un sitio Nginx para DASC.
- El tráfico HTTP redirige a HTTPS.
- El tráfico HTTPS se reenvía internamente a Uvicorn en `127.0.0.1:8000`.
- Se añaden cabeceras `X-Real-IP`, `X-Forwarded-For` y `X-Forwarded-Proto`.
- Se valida la configuración con `nginx -t`.

## Archivos añadidos

- `deploy/proxy/install_reverse_proxy.sh`
- `deploy/proxy/uninstall_reverse_proxy.sh`

## Comandos de instalación previstos

En la máquina del panel/API:

    cd deploy/proxy
    sudo bash install_reverse_proxy.sh

Opcionalmente, para indicar dominio o IP:

    sudo SERVER_NAME=dasc.local bash install_reverse_proxy.sh

## Pruebas pendientes en VM Ubuntu

| Prueba | Estado |
|---|---|
| Instalar Nginx correctamente | Pendiente |
| Generar certificado autofirmado | Pendiente |
| Validar `nginx -t` | Pendiente |
| Acceder por HTTP y comprobar redirección a HTTPS | Pendiente |
| Acceder por HTTPS al panel | Pendiente |
| Comprobar que Uvicorn sigue escuchando en 8000 | Pendiente |
| Comprobar servicio `nginx` activo | Pendiente |
| Validación completa en VM Ubuntu | Pendiente |

## Estado de cierre

R-017 queda implementado a nivel de scripts y pendiente de validación en VM Ubuntu.
