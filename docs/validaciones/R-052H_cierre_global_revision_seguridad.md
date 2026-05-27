# R-052H - Cierre global revisión de seguridad de panel local y secretos

## Objetivo

Cerrar globalmente la tarea R-052, dedicada a revisar y endurecer la seguridad del panel local, central-support, secretos, permisos, usuarios de servicio, puertos internos y repositorio.

## Estado

Cerrada.

## Contexto

R-052 se inició después de R-051, una vez adaptados los instaladores a IPs y perfiles reales.

El objetivo principal era revisar si DASC Server Manager estaba suficientemente protegido para evolucionar desde laboratorio hacia una base de producto más realista.

## Subtareas realizadas

### R-052A - Auditoría de secretos en repositorio y .gitignore

Se auditó el repositorio para comprobar si existían secretos reales versionados.

Resultado:

- No hay config.env real versionado.
- No hay .env real versionado.
- No hay claves privadas SSH versionadas.
- No hay bases runtime versionadas.
- No hay users.json real versionado.
- .gitignore cubre ficheros sensibles principales.

Conclusión:

- Repositorio correcto a nivel de secretos runtime.

### R-052B - Auditoría de permisos de instalación local API

Se auditó `/opt/dasc/api`.

Problemas detectados:

- dasc-api se ejecutaba como usuario humano santino.
- config.env API pertenecía a santino:santino.
- santino podía leer config.env.
- data/users.json, alerts.db y support_tickets.db tenían permisos demasiado abiertos.
- users.json usaba hash y no password plano.

Conclusión:

- La autenticación de usuarios estaba razonablemente bien.
- La separación de usuario de servicio y permisos debía corregirse.

### R-052C - Auditoría de exposición de puertos y Nginx

Se detectó:

- 8000 escuchando en 0.0.0.0.
- 8010 escuchando en 0.0.0.0.
- Nginx funcionando correctamente.
- UFW inactivo.

Conclusión:

- Los backends debían pasar a localhost.
- Nginx debía quedar como punto de entrada.

### R-052D - Auditoría SSH, claves y ficheros runtime

Se validó:

- Clave privada SSH del API con permisos 600.
- Carpeta .ssh con permisos restrictivos.
- Ficheros runtime en data/ demasiado abiertos.

Conclusión:

- SSH estaba bastante bien.
- data/ debía endurecerse junto con el usuario de servicio.

### R-052E - Endurecer panel local API con usuario dedicado

Se creó y aplicó:

- deploy/api/harden_dasc_api_security.sh

Cambios realizados:

- Creación de usuario técnico dasc-api.
- Servicio dasc-api ejecutándose como dasc-api:dasc-api.
- config.env API protegido como root:dasc-api 640.
- data/ protegido como dasc-api:dasc-api.
- .ssh del API protegido como dasc-api:dasc-api.
- Uvicorn del panel local limitado a 127.0.0.1:8000.

Resultado:

- santino ya no puede leer config.env API.
- 8000 deja de estar expuesto en 0.0.0.0.
- Panel local sigue accesible mediante Nginx.

### R-052F - Endurecer central-support como backend interno

Se creó y aplicó:

- deploy/central-support/harden_central_support_security.sh

Cambios realizados:

- central-support limitado a 127.0.0.1:8010.
- config.env central mantenido como root:root 600.
- Panel central accesible mediante Nginx puerto 80.
- Backend 8010 deja de estar expuesto directamente.

### R-052F-FIX1 - Robustecer validación health central-support

Se corrigió:

- Espera controlada de /health tras reiniciar central-support.
- Validación precisa de dirección local de escucha en 8010.

Motivo:

- La primera validación produjo un falso negativo al interpretar la columna remota de `ss`.
- La validación correcta revisa solo la dirección local.

### R-052G - Validación global final de seguridad

Se validó globalmente:

- Servicios activos y enabled.
- dasc-api como dasc-api.
- central-support como dasc.
- 8000 solo en 127.0.0.1.
- 8010 solo en 127.0.0.1.
- config.env API protegido.
- config.env central protegido.
- usuario normal sin acceso a config.env.
- data/ API protegido.
- .ssh API protegido.
- users.json sin password plano.
- Nginx válido.
- Panel local por Nginx funcionando.
- Panel central por Nginx funcionando.
- Procesos sin secretos visibles.
- Sin IPs fijas de laboratorio en deploy.
- Sin defaults débiles activos.
- Sin archivos runtime sensibles versionados.
- Repo limpio.

## Commits principales

- d80fe28 docs: iniciar revision seguridad panel local
- d4d2606 docs: auditar seguridad panel local
- 17f6ff5 feat: endurecer seguridad api local
- 5cfdc61 docs: cerrar hardening api local
- e662c66 feat: endurecer central support interno
- 5ec9940 fix: robustecer health central support
- ec7efe9 docs: cerrar hardening central support
- 999316f docs: validar seguridad global

## Estado final de arquitectura

### Panel local cliente

Acceso recomendado en laboratorio:

- http://192.168.1.250:8080/

Flujo:

- Nginx puerto 8080
- 127.0.0.1:8000
- dasc-api

Estado:

- backend interno.
- usuario de servicio dedicado.
- config.env protegido.
- data/ protegido.

### Panel central DASC

Acceso recomendado en laboratorio:

- http://192.168.1.250/

Flujo:

- Nginx puerto 80
- 127.0.0.1:8010
- central-support

Estado:

- backend interno.
- usuario de servicio técnico dasc.
- config.env protegido.
- health validado.

## Estado final de seguridad

R-052 deja el proyecto en un estado bastante más profesional:

- Ya no se ejecuta el panel local como usuario humano.
- Los secretos no son legibles por usuario normal.
- Los backends internos ya no escuchan públicamente.
- Nginx queda como punto de entrada.
- Los ficheros runtime quedan con permisos restrictivos.
- users.json mantiene hashes.
- No hay secretos runtime versionados.
- No hay IPs fijas de laboratorio en deploy.
- No hay defaults débiles activos.

## Límites actuales

R-052 no incluye todavía:

- Activar UFW.
- Configurar HTTPS real.
- Certbot o certificados internos.
- Limpieza profunda de backups .bak antiguos en /opt/dasc/api.
- Hardening avanzado de cabeceras Nginx.
- Fail2ban.
- Auditoría completa de dependencias Python.
- Rotación formal de secretos ya usados.
- Despliegue seguro desde cero en máquina limpia.

Estos puntos quedan para tareas posteriores.

## Próximo paso recomendado

Continuar con:

- R-053 - Validación completa de instalación desde cero

Motivo:

Después de endurecer seguridad e instaladores, conviene comprobar que una instalación limpia puede reproducirse correctamente con los nuevos scripts y perfiles.
