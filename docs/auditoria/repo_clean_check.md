# Auditoría Clean del repositorio DASC

Fecha: 2026-06-07 13:38:40

Ruta revisada:

~~~text
C:\Users\colme\Documents\dasc-server-manager-product
~~~

## 1. Estado Git

- AVISO: hay cambios pendientes.

~~~text
 M README.md
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
  - deploy\api\install_dasc_api.sh -> contiene patrón `LOGS_DB_PASS=`
  - deploy\api\install_dasc_api.sh -> contiene patrón `SECRET_KEY=`
  - deploy\api\package\main.py -> contiene patrón `SECRET_KEY=`
  - deploy\backup-services\install_backup_services.sh -> contiene patrón `DB_BACKUP_PASS=`
  - deploy\central-support\install_central_support.sh -> contiene patrón `SECRET_KEY=`
  - deploy\central-support\package\main.py -> contiene patrón `SECRET_KEY=`
  - deploy\db\install_db.sh -> contiene patrón `LOGS_DB_PASS=`

### 5.3 Documentación

- REVISAR: hay variables sensibles mencionadas en documentación. Deben ser ejemplos o referencias, nunca secretos reales.

  - docs\pilotos\R-042_correccion_fallos_piloto_1.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\pilotos\piloto_1\incidencias.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\plantillas\plantilla_configuracion_perfil_dasc.md -> contiene patrón `ADMIN_PASSWORD=`
  - docs\plantillas\plantilla_configuracion_perfil_dasc.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\plantillas\plantilla_configuracion_perfil_dasc.md -> contiene patrón `DB_BACKUP_PASS=`
  - docs\plantillas\plantilla_configuracion_perfil_dasc.md -> contiene patrón `SECRET_KEY=`
  - docs\tecnico\r-006_validacion_perfiles.md -> contiene patrón `ADMIN_PASSWORD=`
  - docs\tecnico\r-006_validacion_perfiles.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\tecnico\r-006_validacion_perfiles.md -> contiene patrón `SECRET_KEY=`
  - docs\tecnico\r-007_mejoras_install_dasc_api.md -> contiene patrón `ADMIN_PASSWORD=`
  - docs\validaciones\F6-GATE-02A_cierre_api_db_logs_2_servidores.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\validaciones\F6-GATE-04H_cierre_limpieza_ssh_allowed_hosts.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\validaciones\R-051A_auditoria_ips_variables_instaladores.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\validaciones\R-051A_auditoria_ips_variables_instaladores.md -> contiene patrón `DB_BACKUP_PASS=`
  - docs\validaciones\R-051E_adaptar_instalador_db_perfiles.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\validaciones\R-051E_cierre_adaptar_instalador_db_perfiles.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\validaciones\R-051F_adaptar_instalador_backup_services_perfiles.md -> contiene patrón `DB_BACKUP_PASS=`
  - docs\validaciones\R-051F_cierre_adaptar_instalador_backup_services_perfiles.md -> contiene patrón `DB_BACKUP_PASS=`
  - docs\validaciones\R-051H_cierre_global_instaladores_adaptables.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\validaciones\R-051H_cierre_global_instaladores_adaptables.md -> contiene patrón `DB_BACKUP_PASS=`
  - docs\validaciones\R-053D_checklist_instalacion_desde_cero.md -> contiene patrón `LOGS_DB_PASS=`
  - docs\validaciones\R-053D_checklist_instalacion_desde_cero.md -> contiene patrón `DB_BACKUP_PASS=`

### 5.4 Riesgo real

- OK: no se han encontrado patrones sensibles en archivos inesperados.

## 6. README

- OK: README contiene referencias al estado actual del producto.
- REVISAR: README debería incluir límites de uso antes de producción.

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
