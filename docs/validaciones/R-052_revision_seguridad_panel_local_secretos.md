# R-052 - Revisión de seguridad de panel local y secretos

## Objetivo

Revisar la seguridad del panel local DASC y la gestión de secretos antes de continuar con nuevas funcionalidades.

## Estado

En curso.

## Contexto

Después de R-051, los instaladores ya están más preparados para perfiles reales.

R-052 se centra en revisar:

- Secretos en repositorio.
- .gitignore.
- config.env.
- users.json.
- Tokens.
- Contraseñas.
- Permisos de archivos.
- Exposición de puertos.
- Nginx.
- SSH.
- Claves.
- Servicios systemd.
- Ficheros generados por instaladores.

## Subtareas previstas

- R-052A Auditoría de secretos en repo y .gitignore.
- R-052B Auditoría de permisos en instalación local.
- R-052C Auditoría de exposición de puertos y Nginx.
- R-052D Auditoría de SSH, claves y known_hosts.
- R-052E Correcciones de permisos/config.env/users.json.
- R-052F Documentación operativa de seguridad.
- R-052G Validación final.
- R-052H Cierre global.

## Criterio de cierre

R-052 se considerará cerrada cuando:

- No haya secretos reales versionados.
- .gitignore cubra config.env, claves privadas, bases locales y ficheros temporales.
- config.env instalado tenga permisos restrictivos.
- users.json tenga permisos razonables.
- Nginx funcione correctamente.
- Los puertos internos queden documentados.
- SSH bootstrap quede documentado como riesgo/control.
- Las evidencias queden guardadas en docs/validaciones.
