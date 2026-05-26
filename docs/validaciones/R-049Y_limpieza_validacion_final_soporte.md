# R-049Y - Limpieza y validación final del bloque soporte central/local

## Objetivo

Realizar una auditoría final del bloque de soporte central/local antes de darlo por cerrado.

## Estado

En curso.

## Comprobaciones realizadas

Se revisó:

- Estado del repositorio.
- Documentación R-049.
- Documentación global de soporte.
- Credenciales de laboratorio en deploy.
- Tokens demo en deploy.
- Rutas de soporte local.
- Rutas de soporte central.
- Servicios systemd.
- Nginx.
- Timer de reintento automático.
- Permisos de config.env central.
- Variables no sensibles.
- Bases SQLite local y central.
- Logs de acceso y soporte.

## Resultado de auditoría

La auditoría fue correcta en general.

Se detectaron dos ajustes de limpieza:

- Sustituir token demo fijo del instalador central por token generado aleatoriamente.
- Dejar DASC_LOCAL_INTERNAL_SUPPORT_ENABLED=false como estado final limpio para cliente.

## Corrección aplicada en repo

El instalador central deja de escribir:

- dasc-central-demo-token-lab

y pasa a generar un token aleatorio mediante secrets.token_urlsafe(32), salvo que se proporcione DASC_CENTRAL_DEMO_TOKEN desde el entorno.

## Criterio de cierre

R-049Y se podrá cerrar cuando:

- El repo quede limpio.
- El token demo fijo no aparezca en deploy.
- El entorno instalado use token rotado.
- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED=false quede aplicado en lab-pruebas.
- Servicios sigan activos.
- Nginx siga activo.
- Logs sigan correctos.
