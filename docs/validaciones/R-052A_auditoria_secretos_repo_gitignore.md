# R-052A - Auditoría de secretos en repositorio y .gitignore

## Objetivo

Auditar el repositorio para comprobar si existen secretos reales versionados y si `.gitignore` cubre correctamente ficheros sensibles.

## Estado

Cerrada.

## Resultado general

La auditoría local en Windows confirma:

- Repositorio limpio.
- No hay `config.env` real versionado.
- No hay `.env` real versionado.
- No hay claves privadas SSH versionadas.
- No hay bases SQLite reales versionadas.
- No hay `users.json` real versionado.
- Existen ficheros `.example`, documentación y plantillas, lo cual es correcto.

## Archivos sensibles detectados por Git

Se detectan únicamente ejemplos o documentación:

- config.env.example
- config/perfiles/config.distributed.env.example
- config/perfiles/config.dual.env.example
- config/perfiles/config.single.env.example
- deploy/api/package/config.env.example
- deploy/api/package/static/docs/guia_alertas_telegram.pdf
- docs/validaciones/R-016_config_secretos.md

## .gitignore

El `.gitignore` cubre:

- config.env
- .env
- *.env
- bases .db/.sqlite
- users.json runtime
- auth_logs.json
- alerts.db
- logs
- backups
- claves SSH
- known_hosts
- venv
- __pycache__
- reports generados

## Observación

El `.gitignore` tiene algunas reglas duplicadas, pero no es crítico. A futuro se puede limpiar para dejarlo más ordenado.

## Conclusión

R-052A queda validada.

No se detectan secretos reales versionados en Git.
