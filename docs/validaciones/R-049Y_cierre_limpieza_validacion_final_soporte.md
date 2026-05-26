# R-049Y - Cierre limpieza y validación final soporte central/local

## Objetivo

Cerrar la limpieza y validación final del bloque de soporte central/local de DASC Server Manager.

## Estado

Cerrada.

## Contexto

Después de completar R-049L a R-049X, se realizó una auditoría final del módulo de soporte para comprobar que el bloque quedaba estable, documentado y alineado con una base de producto.

## Comprobaciones realizadas en repositorio

Se validó:

- Repositorio actualizado.
- Rama main sincronizada con origin/main.
- Árbol de trabajo limpio.
- Documentación R-049 completa.
- Documentación global de soporte creada.
- Rutas de soporte local identificadas.
- Rutas de soporte central identificadas.
- Sin credenciales admin/admin ni tecnico/tecnico en deploy.
- Token demo fijo detectado y corregido.

## Corrección aplicada

Durante la auditoría se detectó que el instalador central escribía un token demo fijo:

- dasc-central-demo-token-lab

Se corrigió el instalador:

- deploy/central-support/install_central_support.sh

Ahora el token se genera aleatoriamente con:

- secrets.token_urlsafe(32)

salvo que se proporcione explícitamente DASC_CENTRAL_DEMO_TOKEN desde el entorno.

## Commit funcional

- 2d43e9f fix: limpiar token demo soporte central

## Limpieza aplicada en lab-pruebas

Se rotó el token local-central instalado sin mostrarlo por pantalla.

Se actualizó:

- /opt/dasc/central-support/config.env
- /opt/dasc/api/config.env

También se dejó:

- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED=false

como estado final limpio para cliente.

## Validación de servicios

Se comprobó que siguen activos:

- dasc-api
- dasc-central-support
- dasc-central-retry.timer
- nginx

Resultado:

- active
- active
- active
- active

## Validación de panel local

Se comprobó:

- http://127.0.0.1:8000/

Resultado:

- HTTP 303
- location: /login

Esto confirma que el panel local sigue protegido por login.

## Validación de panel central directo

Se comprobó:

- http://127.0.0.1:8010/health

Resultado:

- status: ok
- app: DASC Central Support
- db: /opt/dasc/central-support/data/central_support.db
- demo_client_id: cliente-demo-a

## Validación de panel central por Nginx

Se comprobó:

- http://127.0.0.1/

Resultado:

- HTTP 303
- location: /login?msg=Sesion+requerida

Esto confirma que Nginx sigue funcionando como reverse proxy del panel central.

## Validación de variables no sensibles locales

Se comprobó:

- CENTRAL_SUPPORT_ENABLED=true
- CENTRAL_SUPPORT_URL=http://127.0.0.1:8010/api/v1/support/tickets
- CENTRAL_SUPPORT_CLIENT_ID=cliente-demo-a
- CENTRAL_SUPPORT_CLIENT_NAME=Cliente Demo A
- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED=false

## Validación de variables no sensibles centrales

Se comprobó:

- DASC_CENTRAL_AUTH_ENABLED=true
- DASC_CENTRAL_LAB_MODE=false
- DASC_CENTRAL_ADMIN_USER=admin
- DASC_CENTRAL_TECH_USER=tecnico

## Validación de permisos

Se comprobó:

- /opt/dasc/central-support/config.env

Resultado:

- root:root
- permisos 600

También se comprobó que un usuario normal no puede leer el archivo.

Resultado:

- OK: usuario normal no puede leer config.env central

## Validación de rutas técnicas

Se comprobó que la ruta técnica local:

- /soporte/sincronizacion

sin sesión redirige a login.

Además, el entorno queda con:

- DASC_LOCAL_INTERNAL_SUPPORT_ENABLED=false

por lo que la vista técnica local queda desactivada como estado final limpio para cliente.

## Resultado

R-049Y queda validada correctamente.

El bloque de soporte central/local queda limpio, documentado y con estado final coherente para cliente.

## Estado final del bloque R-049

El bloque soporte central/local queda compuesto por:

- R-049L Envío local a central.
- R-049M Guardado de referencia central.
- R-049N Visualización de referencia central.
- R-049O Cola offline y reintentos.
- R-049P Sincronización central-local.
- R-049Q Login central.
- R-049R Instalador systemd central.
- R-049S Timer automático.
- R-049T-A Separación local cliente / central DASC.
- R-049T Mejoras visuales central.
- R-049U Endurecimiento credenciales.
- R-049V Nginx reverse proxy.
- R-049W Panel visual de sincronización y vista cliente limpia.
- R-049X Documentación global.
- R-049Y Limpieza y validación final.

## Conclusión

DASC Server Manager supera R-049Y.

El módulo de soporte central/local queda cerrado como bloque funcional de producto base, con separación clara entre cliente, técnico local y panel central DASC.
