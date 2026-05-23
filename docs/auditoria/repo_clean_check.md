# Auditoría Clean del repositorio DASC

Fecha: 2026-05-23 14:47:05

Ruta revisada:

~~~text
C:\Users\colme\Documents\dasc-server-manager-product
~~~

## 1. Estado Git

- OK: el repositorio está limpio o solo está pendiente el propio informe de auditoría.

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

## 5. Variables sensibles por categoría

### 5.1 Ejemplos permitidos

- OK: variables sensibles detectadas en archivos .example. Deben mantenerse como valores ficticios.

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
  - deploy\api\package\config.env.example -> contiene patrón `TELEGRAM_BOT_TOKEN=`
  - deploy\api\package\config.env.example -> contiene patrón `TELEGRAM_CHAT_ID=`
  - deploy\api\package\config.env.example -> contiene patrón `ADMIN_PASSWORD=`
  - deploy\api\package\config.env.example -> contiene patrón `LOGS_DB_PASS=`
  - deploy\api\package\config.env.example -> contiene patrón `SECRET_KEY=`

### 5.2 Código o instaladores

- REVISAR: hay variables sensibles en código o instaladores. Es aceptable si se generan, se leen del entorno o se usan como nombre de variable, no como secreto real.

  - deploy\api\install_dasc_api.sh -> contiene patrón `ADMIN_PASSWORD=`
  - deploy\api\install_dasc_api.sh -> contiene patrón `SECRET_KEY=`
  - deploy\api\package\main.py -> contiene patrón `SECRET_KEY=`
  - deploy\backup-services\install_backup_services.sh -> contiene patrón `DB_BACKUP_PASS=`
  - deploy\db\install_db.sh -> contiene patrón `LOGS_DB_PASS=`

### 5.3 Documentación

- REVISAR: hay variables sensibles mencionadas en documentación. Deben ser ejemplos o referencias, nunca secretos reales.

  - docs\pilotos\R-042_correccion_fallos_piloto_1.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\pilotos\piloto_1\incidencias.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\tecnico\r-006_validacion_perfiles.md -> contiene patrón `ADMIN_PASSWORD=`
  - docs\tecnico\r-006_validacion_perfiles.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\tecnico\r-006_validacion_perfiles.md -> contiene patrón `SECRET_KEY=`
  - docs\tecnico\r-007_mejoras_install_dasc_api.md -> contiene patrón `ADMIN_PASSWORD=`

### 5.4 Riesgo real

- OK: no se han encontrado patrones sensibles en archivos inesperados.

## 6. README

- OK: README contiene referencias al estado actual del producto.
- OK: README incluye aviso de límites.

## 7. Instaladores

- OK: existe `deploy\api\install_dasc_api.sh`.
- OK: existe `deploy\db\install_db.sh`.
- OK: existe `deploy\backup-services\install_backup_services.sh`.

## 8. Resultado provisional

Resultado: OK PARA SEGUIR CON LIMPIEZA Y PULIDO.

No se han encontrado archivos sensibles típicos ni secretos en ubicaciones inesperadas.

Acciones recomendadas:

- Mantener clientes y ventas en curso hasta completar limpieza funcional.
- Revisar manualmente los avisos de código, instaladores y documentación.
- Confirmar que los .example solo contienen valores ficticios.
- Repetir esta auditoría antes de cada release nueva.
