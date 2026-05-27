# R-051 - Instaladores adaptables a IPs y perfiles reales

## Objetivo

Preparar los instaladores de DASC Server Manager para que no dependan de IPs fijas de laboratorio y puedan adaptarse a perfiles reales de despliegue.

## Estado

Cerrada.

## Contexto

Durante fases anteriores se han usado IPs y nombres de laboratorio para validar funcionalidades:

- Panel/API local.
- DB.
- Backups.
- Logs.
- Central support.
- Nginx.
- Reintentos.
- Soporte central/local.

Esto es válido para laboratorio, pero para evolucionar a producto es necesario que los instaladores permitan configurar IPs, hosts, puertos y perfiles de despliegue.

## Problema a resolver

Evitar depender de valores fijos como:

- IPs concretas de laboratorio.
- Hostnames temporales.
- Cliente demo fijo.
- URLs locales no parametrizadas.
- Configuraciones pensadas solo para lab-pruebas.

## Perfiles objetivo

### Lite

Perfil para cliente pequeño.

Características previstas:

- Un servidor principal.
- Panel/API local.
- Backups locales.
- Copia externa futura obligatoria.
- Instalación sencilla.

### Standard

Perfil recomendado para PyME.

Características previstas:

- Dos servidores.
- Separación razonable entre panel/API y datos/backups.
- Mejor resiliencia que Lite.
- Coste controlado.

### Pro

Perfil avanzado.

Características previstas:

- Tres servidores.
- Panel/API.
- DB.
- Backups.
- Separación clara de responsabilidades.
- Mejor base para clientes más exigentes.

### Central DASC

Perfil propio del equipo DASC.

Características previstas:

- Servidor/VPS central.
- central-support.
- Nginx.
- HTTPS futuro.
- Tickets multi-cliente.

## Subtareas

- R-051A Auditoría de IPs fijas y variables actuales.
- R-051B Documento de perfiles Lite / Standard / Pro / Central.
- R-051C Plantilla de configuración por perfil.
- R-051D Adaptar instalador API/panel local.
- R-051E Adaptar instalador DB.
- R-051F Adaptar instalador backups.
- R-051G Validación en laboratorio.
- R-051H Cierre documental.

## Criterio de validación

R-051 se considerará cerrada cuando:

- Exista una auditoría de valores fijos actuales.
- Los perfiles estén documentados.
- Exista una plantilla clara de configuración por perfil.
- Los instaladores principales acepten variables o preguntas para IPs reales.
- No se rompa la instalación actual de laboratorio.
- Quede documentado qué valores son de laboratorio y cuáles son de producción.
