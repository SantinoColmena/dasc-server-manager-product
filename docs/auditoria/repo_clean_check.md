# Auditoría Clean del repositorio DASC

Fecha: 2026-05-23 14:44:30

Ruta revisada:

~~~text
C:\Users\colme\Documents\dasc-server-manager-product
~~~

## 1. Estado Git

- AVISO: hay cambios pendientes.

~~~text
?? docs/auditoria/
~~~

## 2. Estructura mínima obligatoria

- OK: existe `README.md`.
- OK: existe `.gitignore`.
- OK: existe `deploy`.
- OK: existe `docs`.
- OK: existe `scripts`.

## 3. Estructura recomendada

- OK: existe `LICENSE`.
- OK: existe `config.env.example`.
- OK: existe `tools`.
- OK: existe `docs\validaciones`.
- OK: existe `docs\producto`.

## 4. Archivos sensibles no recomendados

- OK: no se han encontrado archivos sensibles típicos.

## 5. Búsqueda básica de posibles secretos

- REVISAR: se han encontrado patrones que pueden ser ejemplos o secretos reales.

  - config.env.example -> contiene patrón `TELEGRAM_BOT_TOKEN=`
  - config.env.example -> contiene patrón `TELEGRAM_CHAT_ID=`
  - config.env.example -> contiene patrón `ADMIN_PASSWORD=`
  - config.env.example -> contiene patrón `LOGS_DB_PASS=`
  - config.env.example -> contiene patrón `SECRET_KEY=`
  - config\perfiles\config.distributed.env.example -> contiene patrón `ADMIN_PASSWORD=`
  - config\perfiles\config.distributed.env.example -> contiene patrón `LOGS_DB_PASS=`
  - config\perfiles\config.distributed.env.example -> contiene patrón `DB_BACKUP_PASS=`
  - config\perfiles\config.distributed.env.example -> contiene patrón `SECRET_KEY=`
  - config\perfiles\config.dual.env.example -> contiene patrón `ADMIN_PASSWORD=`
  - config\perfiles\config.dual.env.example -> contiene patrón `LOGS_DB_PASS=`
  - config\perfiles\config.dual.env.example -> contiene patrón `DB_BACKUP_PASS=`
  - config\perfiles\config.dual.env.example -> contiene patrón `SECRET_KEY=`
  - config\perfiles\config.single.env.example -> contiene patrón `ADMIN_PASSWORD=`
  - config\perfiles\config.single.env.example -> contiene patrón `LOGS_DB_PASS=`
  - config\perfiles\config.single.env.example -> contiene patrón `DB_BACKUP_PASS=`
  - config\perfiles\config.single.env.example -> contiene patrón `SECRET_KEY=`
  - deploy\api\install_dasc_api.sh -> contiene patrón `ADMIN_PASSWORD=`
  - deploy\api\install_dasc_api.sh -> contiene patrón `SECRET_KEY=`
  - deploy\api\package\config.env.example -> contiene patrón `TELEGRAM_BOT_TOKEN=`
  - deploy\api\package\config.env.example -> contiene patrón `TELEGRAM_CHAT_ID=`
  - deploy\api\package\config.env.example -> contiene patrón `ADMIN_PASSWORD=`
  - deploy\api\package\config.env.example -> contiene patrón `LOGS_DB_PASS=`
  - deploy\api\package\config.env.example -> contiene patrón `SECRET_KEY=`
  - deploy\api\package\main.py -> contiene patrón `SECRET_KEY=`
  - deploy\backup-services\install_backup_services.sh -> contiene patrón `DB_BACKUP_PASS=`
  - deploy\db\install_db.sh -> contiene patrón `LOGS_DB_PASS=`
  - docs\pilotos\R-042_correccion_fallos_piloto_1.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\pilotos\piloto_1\incidencias.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\tecnico\r-006_validacion_perfiles.md -> contiene patrón `ADMIN_PASSWORD=`
  - docs\tecnico\r-006_validacion_perfiles.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\tecnico\r-006_validacion_perfiles.md -> contiene patrón `SECRET_KEY=`
  - docs\tecnico\r-007_mejoras_install_dasc_api.md -> contiene patrón `ADMIN_PASSWORD=`

Nota: si son valores de ejemplo, deben quedar claramente marcados como ejemplo.

## 6. README

- OK: README contiene referencias al estado actual del producto.
- OK: README incluye aviso de límites.

## 7. Instaladores

- OK: existe `deploy\api\install_dasc_api.sh`.
- OK: existe `deploy\db\install_db.sh`.
- OK: existe `deploy\backup-services\install_backup_services.sh`.

## 8. Resultado provisional

Esta auditoría no sustituye una validación manual, pero sirve como primera comprobación real antes de avanzar hacia clientes.

Acciones recomendadas:

- Revisar cualquier línea marcada como REVISAR.
- Confirmar que los valores sensibles son ejemplos.
- Mantener clientes y ventas en curso hasta que el producto esté limpio.
- Repetir esta auditoría antes de crear una release nueva.
