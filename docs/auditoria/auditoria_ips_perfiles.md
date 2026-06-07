# Auditoría de IPs fijas y perfiles

Fecha: 2026-06-07 01:07:23

## Objetivo

Detectar referencias a IPs fijas dentro del repositorio para preparar instaladores adaptables por perfil e IPs reales.

## Resumen

| Campo | Valor |
|---|---|
| Total referencias IP detectadas | 520 |
| Severidad ALTA | 18 |
| Severidad MEDIA | 45 |
| Severidad BAJA | 2 |
| Severidad INFO | 455 |

## Criterio de severidad

| Severidad | Significado |
|---|---|
| ALTA | IP fija en instalador o configuración real. Debe revisarse antes de usar en cliente real. |
| MEDIA | IP fija en herramienta de producto o código/recurso. Debe parametrizarse si afecta a ejecución. |
| BAJA | IP en ejemplo de configuración. Puede mantenerse temporalmente si está claro que es ejemplo. |
| INFO | IP en documentación o validaciones. No bloquea, pero debe quedar contextualizada. |

## Hallazgos

| Severidad | Zona | IP | Archivo | Línea | Contenido |
|---|---|---|---|---:|---|
| ALTA | instalador | 127.0.0.1 | `deploy\api\install_dasc_api.sh` | 229 | `write_config_if_empty "BACKUPS_HOST" "127.0.0.1"` |
| ALTA | instalador | 127.0.0.1 | `deploy\api\install_dasc_api.sh` | 230 | `write_config_if_empty "SERVICIOS_HOST" "127.0.0.1"` |
| ALTA | instalador | 127.0.0.1 | `deploy\api\install_dasc_api.sh` | 231 | `write_config_if_empty "LOGS_DB_HOST" "127.0.0.1"` |
| ALTA | instalador | 127.0.0.1 | `deploy\api\install_dasc_api.sh` | 232 | `write_config_if_empty "TERMINAL_DATABASE_HOST" "127.0.0.1"` |
| ALTA | instalador | 127.0.0.1 | `deploy\api\install_dasc_api.sh` | 516 | `DASC_ALLOWED_HOSTS="$(build_unique_csv "127.0.0.1" "localhost" "${BACKUP_HOST}" "${SERVICES_HOST}" "${DATABASE_HOST}")"` |
| ALTA | instalador | 127.0.0.1 | `deploy\api\install_dasc_api.sh` | 592 | `curl -I http://127.0.0.1:8000 // true` |
| ALTA | instalador | 127.0.0.1 | `deploy\api\install_dasc_api.sh` | 601 | `echo "URL local: http://127.0.0.1:8000"` |
| ALTA | instalador | 127.0.0.1 | `deploy\api\install_nginx_dasc_api.sh` | 9 | `APP_HOST="${APP_HOST:-127.0.0.1}"` |
| ALTA | instalador | 127.0.0.1 | `deploy\api\install_nginx_dasc_api.sh` | 84 | `curl -I "http://127.0.0.1:${PUBLIC_PORT}/" // true` |
| ALTA | instalador | 127.0.0.1 | `deploy\api\install_nginx_dasc_api.sh` | 88 | `echo "URL local: http://127.0.0.1:${PUBLIC_PORT}/"` |
| ALTA | instalador | 127.0.0.1 | `deploy\backup-services\install_backup_services.sh` | 179 | `DB_HOST="127.0.0.1"` |
| ALTA | instalador | 127.0.0.1 | `deploy\central-support\install_central_support.sh` | 174 | `curl -s "http://127.0.0.1:${APP_PORT}/health" // true` |
| ALTA | instalador | 127.0.0.1 | `deploy\central-support\install_central_support.sh` | 179 | `echo "URL local: http://127.0.0.1:${APP_PORT}"` |
| ALTA | instalador | 127.0.0.1 | `deploy\central-support\install_nginx_central_support.sh` | 8 | `APP_HOST="${APP_HOST:-127.0.0.1}"` |
| ALTA | instalador | 127.0.0.1 | `deploy\central-support\install_nginx_central_support.sh` | 79 | `curl -I "http://127.0.0.1/" // true` |
| ALTA | instalador | 127.0.0.1 | `deploy\central-support\install_nginx_central_support.sh` | 83 | `echo "URL local: http://127.0.0.1/"` |
| ALTA | instalador | 127.0.0.1 | `deploy\proxy\install_reverse_proxy.sh` | 6 | `UPSTREAM_HOST="${UPSTREAM_HOST:-127.0.0.1}"` |
| ALTA | instalador | 127.0.0.1 | `deploy\proxy\install_reverse_proxy.sh` | 101 | `curl -k -I https://127.0.0.1 // true` |
| BAJA | ejemplo_configuracion | 127.0.0.1 | `deploy\api\package\config.env.example` | 10 | `# - Se permite 127.0.0.1 para servicios locales.` |
| BAJA | ejemplo_configuracion | 127.0.0.1 | `deploy\api\package\config.env.example` | 57 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,IP_SERVIDOR_DB,IP_SERVIDOR_BACKUPS,IP_SERVIDOR_SERVICIOS` |
| INFO | documentacion | 192.168.1.250 | `docs\arquitectura\soporte_central_local_arquitectura.md` | 83 | `- Panel local cliente: http://192.168.1.250:8000` |
| INFO | documentacion | 192.168.1.250 | `docs\arquitectura\soporte_central_local_arquitectura.md` | 84 | `- Panel central DASC por Nginx: http://192.168.1.250` |
| INFO | documentacion | 192.168.1.250 | `docs\arquitectura\soporte_central_local_arquitectura.md` | 85 | `- Backend central directo: http://192.168.1.250:8010` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\cierre_fase_5_pilotos_reales.md` | 53 | `- Host SSH no permitido para 192.168.60.40.` |
| INFO | documentacion | 192.168.60.20 | `docs\pilotos\piloto_1\incidencias.md` | 16 | `/ 4 / 23/05/2026 / Terminal / Terminal Database fallaba por host key SSH no registrada para 192.168.60.20 / Media / Corregida / Se añadió la huella ED25519 al known_hosts dedicado de DASC /` |
| INFO | documentacion | 192.168.60.20 | `docs\pilotos\piloto_1\inventario_tecnico.md` | 24 | `/ Servidor cliente / Base de datos protegida / 192.168.60.20 / Pendiente /` |
| INFO | documentacion | 192.168.60.30 | `docs\pilotos\piloto_1\inventario_tecnico.md` | 25 | `/ Servidor DASC / Panel, backups, servicios, logs y validación / 192.168.60.30 / Pendiente /` |
| INFO | documentacion | 192.168.60.20 | `docs\pilotos\piloto_1\inventario_tecnico.md` | 32 | `/ IP / 192.168.60.20 /` |
| INFO | documentacion | 192.168.60.30 | `docs\pilotos\piloto_1\inventario_tecnico.md` | 45 | `/ IP / 192.168.60.30 /` |
| INFO | documentacion | 192.168.60.20 | `docs\pilotos\piloto_1\plan_ejecucion.md` | 13 | `/ Servidor cliente / MariaDB con base de datos employees / 192.168.60.20 /` |
| INFO | documentacion | 192.168.60.30 | `docs\pilotos\piloto_1\plan_ejecucion.md` | 14 | `/ Servidor DASC / Panel, backups, servicios y validación / 192.168.60.30 /` |
| INFO | documentacion | 192.168.60.20 | `docs\pilotos\piloto_1\plan_ejecucion.md` | 38 | `- IP propuesta: 192.168.60.20.` |
| INFO | documentacion | 192.168.60.30 | `docs\pilotos\piloto_1\plan_ejecucion.md` | 65 | `- IP propuesta: 192.168.60.30.` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\piloto_2\incidencias.md` | 12 | `/ 2 / 23/05/2026 / SSH / panel / El panel rechazaba 192.168.60.40 con el error Host SSH no permitido / Media / Corregida / Se añadió 192.168.60.40 a DASC_SSH_ALLOWED_HOSTS /` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\piloto_2\incidencias.md` | 12 | `/ 2 / 23/05/2026 / SSH / panel / El panel rechazaba 192.168.60.40 con el error Host SSH no permitido / Media / Corregida / Se añadió 192.168.60.40 a DASC_SSH_ALLOWED_HOSTS /` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\piloto_2\inventario_tecnico.md` | 25 | `/ IP interna DASC / 192.168.60.40 /` |
| INFO | documentacion | 192.168.1.248 | `docs\pilotos\piloto_2\inventario_tecnico.md` | 26 | `/ IP de acceso desde navegador / 192.168.1.248 /` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\piloto_2\plan_ejecucion.md` | 20 | `- IP interna DASC: 192.168.60.40.` |
| INFO | documentacion | 192.168.1.248 | `docs\pilotos\piloto_2\plan_ejecucion.md` | 21 | `- IP de acceso desde navegador: 192.168.1.248.` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\piloto_2\plan_ejecucion.md` | 56 | `sudo BACKUP_ALLOWED_HOST=192.168.60.40 LOGS_ALLOWED_HOST=192.168.60.40 bash deploy/db/install_db.sh` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\piloto_2\plan_ejecucion.md` | 56 | `sudo BACKUP_ALLOWED_HOST=192.168.60.40 LOGS_ALLOWED_HOST=192.168.60.40 bash deploy/db/install_db.sh` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\piloto_2\plan_ejecucion.md` | 60 | `sudo DB_HOST=192.168.60.40 bash deploy/backup-services/install_backup_services.sh` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\piloto_2\plan_ejecucion.md` | 84 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| INFO | documentacion | 192.168.60.20 | `docs\pilotos\piloto_2\plan_ejecucion.md` | 84 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| INFO | documentacion | 192.168.60.30 | `docs\pilotos\piloto_2\plan_ejecucion.md` | 84 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| INFO | documentacion | 127.0.0.1 | `docs\pilotos\piloto_2\plan_ejecucion.md` | 84 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| INFO | documentacion | 192.168.60.20 | `docs\pilotos\R-042_correccion_fallos_piloto_1.md` | 80 | `- La huella SSH de 192.168.60.20 no estaba registrada.` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\R-043_instalacion_piloto_2_1_servidor_externo.md` | 32 | `/ IP de gestión interna / 192.168.60.40 /` |
| INFO | documentacion | 192.168.1.248 | `docs\pilotos\R-043_instalacion_piloto_2_1_servidor_externo.md` | 33 | `/ IP de acceso desde navegador / 192.168.1.248 /` |
| INFO | documentacion | 192.168.1.248 | `docs\pilotos\R-043_instalacion_piloto_2_1_servidor_externo.md` | 54 | `http://192.168.1.248:8000` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\R-043_instalacion_piloto_2_1_servidor_externo.md` | 120 | `/ 2 / 192.168.60.40 no estaba permitido en DASC_SSH_ALLOWED_HOSTS / Media / Corregida /` |
| INFO | documentacion | 127.0.0.1 | `docs\plantillas\plantilla_configuracion_perfil_dasc.md` | 33 | `API_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\plantillas\plantilla_configuracion_perfil_dasc.md` | 34 | `DB_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\plantillas\plantilla_configuracion_perfil_dasc.md` | 35 | `BACKUPS_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\plantillas\plantilla_configuracion_perfil_dasc.md` | 36 | `SERVICIOS_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\plantillas\plantilla_configuracion_perfil_dasc.md` | 37 | `LOGS_DB_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\producto\perfiles_despliegue_dasc.md` | 59 | `- LOCAL_PANEL_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\producto\perfiles_despliegue_dasc.md` | 62 | `- DB_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\producto\perfiles_despliegue_dasc.md` | 63 | `- BACKUPS_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\producto\perfiles_despliegue_dasc.md` | 64 | `- SERVICIOS_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\producto\perfiles_despliegue_dasc.md` | 65 | `- LOGS_DB_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\producto\soporte_central_local.md` | 372 | `- Nginx reenvía tráfico hacia 127.0.0.1:8010.` |
| INFO | documentacion | 192.168.1.250 | `docs\producto\soporte_central_local.md` | 376 | `- http://192.168.1.250/` |
| INFO | documentacion | 127.0.0.1 | `docs\producto\soporte_central_local.md` | 378 | `- http://127.0.0.1:8010` |
| INFO | documentacion | 127.0.0.1 | `docs\producto\soporte_central_local.md` | 385 | `- Backend central-support en 127.0.0.1:8010` |
| INFO | documentacion | 192.168.1.50 | `docs\producto\soporte_central_local.md` | 394 | `- http://192.168.1.50` |
| INFO | documentacion | 192.168.60.10 | `docs\soporte\guia_comunicacion_tono_soporte.md` | 78 | `Access denied for user 'dasc_logs'@'192.168.60.10'` |
| INFO | documentacion | 127.0.0.1 | `docs\soporte\tickets_ejemplo\DASC-2026-001_error_acceso_panel.md` | 54 | `curl -I http://127.0.0.1:8000` |
| INFO | documentacion | 127.0.0.1 | `docs\tecnico\r-006_configuracion_por_perfiles.md` | 25 | `SERVICIOS_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\tecnico\r-006_configuracion_por_perfiles.md` | 26 | `BACKUPS_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\tecnico\r-006_configuracion_por_perfiles.md` | 27 | `LOGS_DB_HOST=127.0.0.1` |
| INFO | documentacion | 192.168.60.20 | `docs\tecnico\r-006_configuracion_por_perfiles.md` | 55 | `SERVICIOS_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\tecnico\r-006_configuracion_por_perfiles.md` | 56 | `BACKUPS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\tecnico\r-006_configuracion_por_perfiles.md` | 57 | `LOGS_DB_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\tecnico\r-006_configuracion_por_perfiles.md` | 86 | `SERVICIOS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\tecnico\r-006_configuracion_por_perfiles.md` | 87 | `BACKUPS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.20 | `docs\tecnico\r-006_configuracion_por_perfiles.md` | 88 | `LOGS_DB_HOST=192.168.60.20` |
| INFO | documentacion | 127.0.0.1 | `docs\tecnico\r-006_validacion_perfiles.md` | 38 | `- `SERVICIOS_HOST=127.0.0.1`` |
| INFO | documentacion | 127.0.0.1 | `docs\tecnico\r-006_validacion_perfiles.md` | 39 | `- `BACKUPS_HOST=127.0.0.1`` |
| INFO | documentacion | 127.0.0.1 | `docs\tecnico\r-006_validacion_perfiles.md` | 40 | `- `LOGS_DB_HOST=127.0.0.1`` |
| INFO | documentacion | 127.0.0.1 | `docs\tecnico\r-007_mejoras_install_dasc_api.md` | 211 | `URL local: http://127.0.0.1:8000` |
| INFO | documentacion | 127.0.0.1 | `docs\tecnico\r-007_validacion_instalador.md` | 112 | `curl -I http://127.0.0.1:8000` |
| INFO | documentacion | 192.168.60.30 | `docs\tecnico\r-013_laboratorio_reproducible_pruebas.md` | 310 | `192.168.60.30` |
| INFO | documentacion | 192.168.60.20 | `docs\tecnico\r-013_laboratorio_reproducible_pruebas.md` | 316 | `192.168.60.20` |
| INFO | documentacion | 192.168.60.10 | `docs\tecnico\r-013_laboratorio_reproducible_pruebas.md` | 322 | `192.168.60.10` |
| INFO | documentacion | 127.0.0.1 | `docs\tecnico\r-013_laboratorio_reproducible_pruebas.md` | 336 | `curl -I http://127.0.0.1:8000` |
| INFO | documentacion | 192.168.60.30 | `docs\tecnico\r-013_laboratorio_reproducible_pruebas.md` | 351 | `ssh dasc@192.168.60.30 hostname` |
| INFO | documentacion | 192.168.60.30 | `docs\tecnico\r-013_laboratorio_reproducible_pruebas.md` | 357 | `ssh dasc@192.168.60.30 /usr/local/bin/backups_api.sh full employees /home/dasc/backups prueba-YYYYMMDD-HHMM.sql gzip 30 manual prueba` |
| INFO | documentacion | 127.0.0.1 | `docs\tecnico\r-013_validacion_laboratorio_reproducible.md` | 129 | `curl -I http://127.0.0.1:8000` |
| INFO | documentacion | 192.168.60.30 | `docs\tecnico\R-028_R-029_copia_externa_cifrado.md` | 21 | `/ Backups / Servicios / 192.168.60.30 /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-01_validacion_instalacion_api_ubuntu.md` | 27 | `Durante la primera instalación limpia en Ubuntu `lab-pruebas`, el instalador avanzó correctamente hasta crear el servicio y preparar el entorno API, pero falló al intentar registrar la huella SSH del host de backups `192.168.60.30`.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-01_validacion_instalacion_api_ubuntu.md` | 78 | `- El panel responde en `http://127.0.0.1:8000`.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-01A_cierre_instalacion_limpia_api_ubuntu.md` | 35 | `- El panel respondió localmente en `http://127.0.0.1:8000`.` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-01A_cierre_instalacion_limpia_api_ubuntu.md` | 40 | `Durante la primera ejecución se detectó que el instalador intentaba registrar la huella SSH de hosts remotos como `192.168.60.30` y `192.168.60.20`.` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-01A_cierre_instalacion_limpia_api_ubuntu.md` | 40 | `Durante la primera ejecución se detectó que el instalador intentaba registrar la huella SSH de hosts remotos como `192.168.60.30` y `192.168.60.20`.` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-01A_cierre_instalacion_limpia_api_ubuntu.md` | 114 | `No se pudo conectar con MySQL en 192.168.60.20.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-01B_cierre_reinstalacion_api_entorno_existente.md` | 27 | `- El panel respondía localmente en `http://127.0.0.1:8000`.` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-01B_cierre_reinstalacion_api_entorno_existente.md` | 118 | `No se pudo conectar con MySQL en 192.168.60.20.` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-02A_cierre_api_db_logs_2_servidores.md` | 15 | `/ API / Panel / lab-pruebas / 192.168.60.10 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-02A_cierre_api_db_logs_2_servidores.md` | 16 | `/ DB / Logs / lab-db-gate02 / 192.168.60.20 /` |
| INFO | documentacion | 192.168.60.0 | `docs\validaciones\F6-GATE-02A_cierre_api_db_logs_2_servidores.md` | 24 | `- Comunicación por red privada DASC `192.168.60.0/24`.` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-02A_cierre_api_db_logs_2_servidores.md` | 31 | `lab-pruebas: 192.168.60.10` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-02A_cierre_api_db_logs_2_servidores.md` | 32 | `lab-db-gate02: 192.168.60.20` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-02A_cierre_api_db_logs_2_servidores.md` | 66 | `dasc_logs@192.168.60.10` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-02A_cierre_api_db_logs_2_servidores.md` | 76 | `LOGS_DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-02A_cierre_api_db_logs_2_servidores.md` | 94 | `- Conexión correcta a `192.168.60.20`.` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-02B_cierre_eventos_reales_panel_db_remota.md` | 15 | `/ API / Panel / lab-pruebas / 192.168.60.10 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-02B_cierre_eventos_reales_panel_db_remota.md` | 16 | `/ DB / Logs / lab-db-gate02 / 192.168.60.20 /` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\F6-GATE-02B_cierre_eventos_reales_panel_db_remota.md` | 54 | `http://192.168.1.250:8000` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-03_cierre_backup_completo_restauracion_2_servidores.md` | 28 | `/ API / Ejecutor backup / lab-pruebas / 192.168.60.10 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03_cierre_backup_completo_restauracion_2_servidores.md` | 29 | `/ DB / Logs / Origen datos / lab-db-gate02 / 192.168.60.20 /` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-03_cierre_backup_completo_restauracion_2_servidores.md` | 64 | `dasc_backup@192.168.60.10` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03_cierre_backup_completo_restauracion_2_servidores.md` | 81 | `- Puerto 3306 accesible hacia `192.168.60.20`.` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03_cierre_backup_completo_restauracion_2_servidores.md` | 144 | `ssh: connect to host 192.168.60.20 port 22: Connection refused` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-03_cierre_backup_completo_restauracion_2_servidores.md` | 158 | `dasc_restore@192.168.60.10` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-03D_cierre_backup_completo_automatizado_producto.md` | 15 | `/ API / Ejecutor backup / lab-pruebas / 192.168.60.10 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03D_cierre_backup_completo_automatizado_producto.md` | 16 | `/ DB / Origen datos / lab-db-gate02 / 192.168.60.20 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03D_cierre_backup_completo_automatizado_producto.md` | 59 | `BACKUP_DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03D_cierre_backup_completo_automatizado_producto.md` | 103 | `Host: 192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03D_cierre_backup_completo_automatizado_producto.md` | 135 | `host: 192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-03D_cierre_backup_completo_automatizado_producto.md` | 165 | `Durante la validación se detectó que el instalador seguía mostrando un mensaje final confuso indicando que el SSH automático estaba configurado contra `192.168.60.30`.` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-03D_validacion_backup_completo_automatizado_producto.md` | 107 | `lab-pruebas     192.168.60.10   API / ejecutor backup` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03D_validacion_backup_completo_automatizado_producto.md` | 108 | `lab-db-gate02   192.168.60.20   DB / origen datos` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-03E_cierre_backups_en_informe_operativo.md` | 15 | `/ API / Generador informe / lab-pruebas / 192.168.60.10 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03E_cierre_backups_en_informe_operativo.md` | 16 | `/ DB / Origen datos / lab-db-gate02 / 192.168.60.20 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03E_cierre_backups_en_informe_operativo.md` | 120 | `/ Host origen / `192.168.60.20` /` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-03F_cierre_retencion_limpieza_backups.md` | 15 | `/ API / Backups / Limpieza / lab-pruebas / 192.168.60.10 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03F_cierre_retencion_limpieza_backups.md` | 16 | `/ DB / Origen datos / lab-db-gate02 / 192.168.60.20 /` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-03G_cierre_restauracion_controlada_backups.md` | 15 | `/ API / Restauración / lab-pruebas / 192.168.60.10 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03G_cierre_restauracion_controlada_backups.md` | 16 | `/ DB / Destino restauración / lab-db-gate02 / 192.168.60.20 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03G_cierre_restauracion_controlada_backups.md` | 56 | `RESTORE_DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-03G_cierre_restauracion_controlada_backups.md` | 88 | `dasc_restore@192.168.60.10` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-03G_cierre_restauracion_controlada_backups.md` | 192 | `host: 192.168.60.20` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04A_auditoria_ips_perfiles.md` | 16 | `192.168.60.10` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04A_auditoria_ips_perfiles.md` | 17 | `192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04A_auditoria_ips_perfiles.md` | 18 | `192.168.60.30` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 88 | `- Si son referencias locales `127.0.0.1` para autocomprobación, pueden mantenerse justificadas.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 104 | `/ `deploy/api/install_dasc_api.sh` / `127.0.0.1` / Local aceptable / Mantener justificado /` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 105 | `/ `deploy/api/install_dasc_api.sh` / `127.0.0.1` / Test local HTTP / Mantener justificado /` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 106 | `/ `deploy/api/install_dasc_api.sh` / `127.0.0.1` / Mensaje URL local / Mantener justificado /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 107 | `/ `deploy/backup-services/install_backup_services.sh` / `192.168.60.20` / Valor por defecto de DB / Parametrizar /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 108 | `/ `deploy/db/install_db.sh` / `192.168.60.30` / Host permitido para backups / Parametrizar /` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 109 | `/ `deploy/db/install_db.sh` / `192.168.60.10` / Host permitido para logs/API / Parametrizar /` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 110 | `/ `deploy/proxy/install_reverse_proxy.sh` / `127.0.0.1` / Upstream local por defecto / Mantener justificado /` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 111 | `/ `deploy/proxy/install_reverse_proxy.sh` / `127.0.0.1` / Test local HTTPS / Mantener justificado /` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 115 | `### Mantener `127.0.0.1` cuando sea local` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 117 | `Se permite `127.0.0.1` en instaladores cuando representa:` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 131 | `192.168.60.10` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 132 | `192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 133 | `192.168.60.30` |
| INFO | documentacion | 192.168.60.40 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 134 | `192.168.60.40` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 203 | `- `127.0.0.1` permitido para servicios locales.` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 236 | `- Eliminar dependencia real de `192.168.60.30`.` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 237 | `- Eliminar dependencia real de `192.168.60.10`.` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 248 | `- Eliminar dependencia real de `192.168.60.20`.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04B_clasificacion_ips_parametrizacion.md` | 287 | `Las IPs locales `127.0.0.1` se aceptan cuando son comprobaciones internas.` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04C_cierre_parametrizacion_instalador_db.md` | 22 | `BACKUP_ALLOWED_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_cierre_parametrizacion_instalador_db.md` | 23 | `LOGS_ALLOWED_HOST=192.168.60.10` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04C_cierre_parametrizacion_instalador_db.md` | 64 | `192.168.60.30` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_cierre_parametrizacion_instalador_db.md` | 65 | `192.168.60.10` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_cierre_parametrizacion_instalador_db.md` | 75 | `sudo BACKUP_ALLOWED_HOST=192.168.60.10 LOGS_ALLOWED_HOST=192.168.60.10 bash deploy/db/install_db.sh` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_cierre_parametrizacion_instalador_db.md` | 75 | `sudo BACKUP_ALLOWED_HOST=192.168.60.10 LOGS_ALLOWED_HOST=192.168.60.10 bash deploy/db/install_db.sh` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_cierre_parametrizacion_instalador_db.md` | 83 | `BACKUP_ALLOWED_HOST=192.168.60.10` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_cierre_parametrizacion_instalador_db.md` | 84 | `LOGS_ALLOWED_HOST=192.168.60.10` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_cierre_parametrizacion_instalador_db.md` | 100 | `- Usuario `dasc_backup` creado para `192.168.60.10`.` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_cierre_parametrizacion_instalador_db.md` | 101 | `- Usuario `dasc_restore` creado para `192.168.60.10`.` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_cierre_parametrizacion_instalador_db.md` | 102 | `- Usuario `dasc_logs` creado para `192.168.60.10`.` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04C_cierre_parametrizacion_instalador_db.md` | 132 | `- El instalador DB ya no usa `192.168.60.30` como valor por defecto.` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_cierre_parametrizacion_instalador_db.md` | 133 | `- El instalador DB ya no usa `192.168.60.10` como valor por defecto.` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04C_parametrizacion_instalador_db.md` | 22 | `BACKUP_ALLOWED_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_parametrizacion_instalador_db.md` | 23 | `LOGS_ALLOWED_HOST=192.168.60.10` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_parametrizacion_instalador_db.md` | 48 | `BACKUP_ALLOWED_HOST=192.168.60.10` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_parametrizacion_instalador_db.md` | 58 | `LOGS_ALLOWED_HOST=192.168.60.10` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04C_parametrizacion_instalador_db.md` | 79 | `Puede usar `127.0.0.1` o la IP local si API y DB están en el mismo servidor.` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04C_parametrizacion_instalador_db.md` | 93 | `- `deploy/db/install_db.sh` no usa `192.168.60.30` como valor por defecto.` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04C_parametrizacion_instalador_db.md` | 94 | `- `deploy/db/install_db.sh` no usa `192.168.60.10` como valor por defecto.` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04D_cierre_parametrizacion_instalador_backup_services.md` | 22 | `DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04D_cierre_parametrizacion_instalador_backup_services.md` | 39 | `/ API / panel / lab-pruebas / 192.168.60.10 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04D_cierre_parametrizacion_instalador_backup_services.md` | 40 | `/ DB / logs / lab-db-gate02 / 192.168.60.20 /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04D_cierre_parametrizacion_instalador_backup_services.md` | 41 | `/ Backups / servicios / lab-backups-gate04d / 192.168.60.30 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04D_cierre_parametrizacion_instalador_backup_services.md` | 48 | `sudo DB_HOST=192.168.60.20 bash deploy/backup-services/install_backup_services.sh` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04D_cierre_parametrizacion_instalador_backup_services.md` | 79 | `host=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04D_cierre_parametrizacion_instalador_backup_services.md` | 82 | `host=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04D_cierre_parametrizacion_instalador_backup_services.md` | 88 | `Host: 192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04D_parametrizacion_instalador_backup_services.md` | 22 | `DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04D_parametrizacion_instalador_backup_services.md` | 48 | `DB_HOST=192.168.60.20` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04D_parametrizacion_instalador_backup_services.md` | 75 | `Puede usar `127.0.0.1` o la IP local si la base de datos está en el mismo servidor.` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04D_parametrizacion_instalador_backup_services.md` | 89 | `- `deploy/backup-services/install_backup_services.sh` no usa `192.168.60.20` como valor por defecto.` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04D_parametrizacion_instalador_backup_services.md` | 100 | `sudo DB_HOST=192.168.60.20 bash deploy/backup-services/install_backup_services.sh` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04E_cierre_config_env_example_placeholders.md` | 22 | `192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04E_cierre_config_env_example_placeholders.md` | 23 | `192.168.60.30` |
| INFO | documentacion | 192.168.60.40 | `docs\validaciones\F6-GATE-04E_cierre_config_env_example_placeholders.md` | 24 | `192.168.60.40` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04E_cierre_config_env_example_placeholders.md` | 51 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,IP_SERVIDOR_DB,IP_SERVIDOR_BACKUPS,IP_SERVIDOR_SERVICIOS` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04E_cierre_config_env_example_placeholders.md` | 60 | `Se permite `127.0.0.1` para servicios locales.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04E_cierre_config_env_example_placeholders.md` | 114 | `Las referencias `BAJA` restantes corresponden a `127.0.0.1`, aceptado como referencia local.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04E_cierre_config_env_example_placeholders.md` | 130 | `- `127.0.0.1` queda solo como referencia local aceptable.` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04E_revision_config_env_example_placeholders.md` | 22 | `192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04E_revision_config_env_example_placeholders.md` | 23 | `192.168.60.30` |
| INFO | documentacion | 192.168.60.40 | `docs\validaciones\F6-GATE-04E_revision_config_env_example_placeholders.md` | 24 | `192.168.60.40` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04E_revision_config_env_example_placeholders.md` | 48 | `Puede usar `127.0.0.1` para servicios locales, pero requiere copia externa obligatoria para backups.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04E_revision_config_env_example_placeholders.md` | 104 | `- Se mantiene `127.0.0.1` solo como referencia local aceptable.` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 17 | `/ API / panel / lab-pruebas / 192.168.60.10 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 18 | `/ DB / logs / lab-db-gate02 / 192.168.60.20 /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 19 | `/ Backups / servicios / lab-backups-gate04d / 192.168.60.30 /` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 37 | `IPs: 192.168.1.250 192.168.60.10` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 37 | `IPs: 192.168.1.250 192.168.60.10` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 45 | `SERVICIOS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 46 | `BACKUPS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 47 | `TERMINAL_DATABASE_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 48 | `LOGS_DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 49 | `BACKUP_DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 50 | `RESTORE_DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 51 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 51 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 51 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 51 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 57 | `ping 192.168.60.20 OK` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 58 | `ping 192.168.60.30 OK` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 59 | `TCP 192.168.60.20:3306 OK` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 60 | `TCP 192.168.60.30:22 OK` |
| INFO | documentacion | 192.168.1.251 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 69 | `IPs: 192.168.1.251 192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 69 | `IPs: 192.168.1.251 192.168.60.20` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 77 | `dasc_backup@192.168.60.10` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 78 | `dasc_backup@192.168.60.30` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 79 | `dasc_logs@192.168.60.10` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 80 | `dasc_restore@192.168.60.10` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 81 | `dasc_restore@192.168.60.30` |
| INFO | documentacion | 192.168.1.141 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 105 | `IPs: 192.168.1.141 192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 105 | `IPs: 192.168.1.141 192.168.60.30` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 120 | `host=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 123 | `host=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 136 | `Host: 192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_cierre_validacion_perfil_ips_explicitas.md` | 158 | `En `DASC_SSH_ALLOWED_HOSTS` aparece `192.168.60.30` duplicada.` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 17 | `/ API / panel / lab-pruebas / 192.168.60.10 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 18 | `/ DB / logs / lab-db-gate02 / 192.168.60.20 /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 19 | `/ Backups / servicios / lab-backups-gate04d / 192.168.60.30 /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 36 | `SERVICIOS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 37 | `BACKUPS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 38 | `TERMINAL_DATABASE_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 39 | `LOGS_DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 40 | `BACKUP_DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 41 | `RESTORE_DB_HOST=192.168.60.20` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 42 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 42 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 42 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 48 | `BACKUP_ALLOWED_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 49 | `LOGS_ALLOWED_HOST=192.168.60.10` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04F_validacion_perfil_ips_explicitas.md` | 55 | `DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04G_cierre_global_instaladores_perfiles.md` | 79 | `sudo BACKUP_ALLOWED_HOST=192.168.60.10 LOGS_ALLOWED_HOST=192.168.60.10 bash deploy/db/install_db.sh` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04G_cierre_global_instaladores_perfiles.md` | 79 | `sudo BACKUP_ALLOWED_HOST=192.168.60.10 LOGS_ALLOWED_HOST=192.168.60.10 bash deploy/db/install_db.sh` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04G_cierre_global_instaladores_perfiles.md` | 93 | `DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04G_cierre_global_instaladores_perfiles.md` | 101 | `sudo DB_HOST=192.168.60.20 bash deploy/backup-services/install_backup_services.sh` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04G_cierre_global_instaladores_perfiles.md` | 141 | `/ API / panel / lab-pruebas / 192.168.60.10 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04G_cierre_global_instaladores_perfiles.md` | 142 | `/ DB / logs / lab-db-gate02 / 192.168.60.20 /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04G_cierre_global_instaladores_perfiles.md` | 143 | `/ Backups / servicios / lab-backups-gate04d / 192.168.60.30 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04H_cierre_limpieza_ssh_allowed_hosts.md` | 32 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04H_cierre_limpieza_ssh_allowed_hosts.md` | 32 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04H_cierre_limpieza_ssh_allowed_hosts.md` | 32 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\F6-GATE-04H_cierre_limpieza_ssh_allowed_hosts.md` | 50 | `Access denied for user 'dasc_logs'@'192.168.60.10'` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04H_cierre_limpieza_ssh_allowed_hosts.md` | 62 | `LOGS_DB_HOST=192.168.60.20` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04H_cierre_limpieza_ssh_allowed_hosts.md` | 88 | `id 22 / dasc-web / acceso / anon / 127.0.0.1 / HEAD / / ERROR` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04H_cierre_limpieza_ssh_allowed_hosts.md` | 89 | `id 21 / dasc-web / acceso / anon / 127.0.0.1 / HEAD / / ERROR` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04H_limpieza_ssh_allowed_hosts.md` | 20 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04H_limpieza_ssh_allowed_hosts.md` | 20 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04H_limpieza_ssh_allowed_hosts.md` | 20 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04H_limpieza_ssh_allowed_hosts.md` | 20 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-04H_limpieza_ssh_allowed_hosts.md` | 46 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04H_limpieza_ssh_allowed_hosts.md` | 46 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\F6-GATE-04H_limpieza_ssh_allowed_hosts.md` | 46 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-04H_limpieza_ssh_allowed_hosts.md` | 49 | `en lugar de repetir `192.168.60.30`.` |
| INFO | documentacion | 192.168.1.244 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 11 | `/ lab-api / API / Panel / Reverse proxy / 192.168.60.10 / 192.168.1.244 /` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 11 | `/ lab-api / API / Panel / Reverse proxy / 192.168.60.10 / 192.168.1.244 /` |
| INFO | documentacion | 192.168.1.243 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 12 | `/ lab-db / Base de datos MariaDB / 192.168.60.20 / 192.168.1.243 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 12 | `/ lab-db / Base de datos MariaDB / 192.168.60.20 / 192.168.1.243 /` |
| INFO | documentacion | 192.168.1.245 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 13 | `/ lab-backup / Backups + Servicios / 192.168.60.30 / 192.168.1.245 /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 13 | `/ lab-backup / Backups + Servicios / 192.168.60.30 / 192.168.1.245 /` |
| INFO | documentacion | 192.168.60.0 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 21 | `/ Conectividad entre máquinas por red 192.168.60.0/24 / Correcto /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 34 | `/ Usuario `dasc_backup@192.168.60.30` creado / Correcto /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 35 | `/ Usuario `dasc_restore@192.168.60.30` creado / Correcto /` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 39 | `/ Usuario `dasc_logs@192.168.60.10` creado / Correcto /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 122 | `/ `BACKUPS_HOST=192.168.60.30` / Correcto /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 123 | `/ `SERVICIOS_HOST=192.168.60.30` / Correcto /` |
| INFO | documentacion | 192.168.1.137 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 143 | `login admin desde 192.168.1.137` |
| INFO | documentacion | 192.168.1.244 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 160 | `/ Acceso desde Windows por `https://192.168.1.244` / Correcto /` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 207 | `- `install_db.sh` crea el usuario `dasc_logs@192.168.60.10`.` |
| INFO | documentacion | 192.168.1.244 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 272 | `https://192.168.1.244` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\Fase_2_validacion_visual_panel.md` | 12 | `/ IP interna laboratorio / 192.168.60.10 /` |
| INFO | documentacion | 192.168.1.244 | `docs\validaciones\Fase_2_validacion_visual_panel.md` | 13 | `/ IP accesible desde Windows / 192.168.1.244 /` |
| INFO | documentacion | 192.168.1.244 | `docs\validaciones\Fase_2_validacion_visual_panel.md` | 14 | `/ Acceso validado / https://192.168.1.244 /` |
| INFO | documentacion | 192.168.1.137 | `docs\validaciones\Fase_2_validacion_visual_panel.md` | 43 | `login admin desde 192.168.1.137` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\Fase_3_cierre_despliegues_adaptables.md` | 19 | `/ API / Panel / 192.168.60.10 / Panel FastAPI, asistente de perfiles y punto de control /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\Fase_3_cierre_despliegues_adaptables.md` | 20 | `/ DB / Logs / 192.168.60.20 / Base de datos principal y base de datos de logs /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\Fase_3_cierre_despliegues_adaptables.md` | 21 | `/ Backups / Servicios / 192.168.60.30 / Ejecución de backups, servicios y copia externa /` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\Fase_3_cierre_despliegues_adaptables.md` | 81 | `- API / Panel: 192.168.60.10.` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\Fase_3_cierre_despliegues_adaptables.md` | 82 | `- DB / Logs: 192.168.60.20.` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\Fase_3_cierre_despliegues_adaptables.md` | 83 | `- Backups / Servicios: 192.168.60.30.` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\Fase_3_cierre_despliegues_adaptables.md` | 111 | `- Servidor: Backups / Servicios 192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\Fase_3_cierre_despliegues_adaptables.md` | 177 | `SERVICIOS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\Fase_3_cierre_despliegues_adaptables.md` | 178 | `BACKUPS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\Fase_3_cierre_despliegues_adaptables.md` | 179 | `LOGS_DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\Fase_3_cierre_despliegues_adaptables.md` | 180 | `DB_HOST=192.168.60.20` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-015_hash_usuarios.md` | 48 | `- Uvicorn en `127.0.0.1:8000`` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-017_reverse_proxy_https.md` | 13 | `127.0.0.1:8000` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-017_reverse_proxy_https.md` | 30 | `- El tráfico HTTPS se reenvía internamente a Uvicorn en `127.0.0.1:8000`.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-025_R-026_R-027_validacion_inicial_perfiles.md` | 20 | `El perfil single define todos los servicios en 127.0.0.1.` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-028_validacion_copia_externa_local.md` | 13 | `/ Backups / Servicios / 192.168.60.30 /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-029_validacion_copia_externa_cifrada_gpg.md` | 13 | `/ Backups / Servicios / 192.168.60.30 /` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\R-030_correccion_bom_script_perfiles.md` | 51 | `/ API / Panel - 192.168.60.10 / Se volverá a probar el script después de hacer `git pull` /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-030_correccion_bom_script_perfiles.md` | 52 | `/ DB / Logs - 192.168.60.20 / No requiere cambios /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-030_correccion_bom_script_perfiles.md` | 53 | `/ Backups / Servicios - 192.168.60.30 / No requiere cambios /` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\R-030_validacion_distributed_3_servidores.md` | 11 | `/ API / Panel / 192.168.60.10 / Servidor donde se ejecuta el panel FastAPI y donde se prueba el asistente /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-030_validacion_distributed_3_servidores.md` | 12 | `/ DB / Logs / 192.168.60.20 / Servidor de base de datos principal y base de datos de logs /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-030_validacion_distributed_3_servidores.md` | 13 | `/ Backups / Servicios / 192.168.60.30 / Servidor de backups y gestión de servicios por SSH /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-030_validacion_distributed_3_servidores.md` | 41 | `SERVICIOS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-030_validacion_distributed_3_servidores.md` | 42 | `BACKUPS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-030_validacion_distributed_3_servidores.md` | 43 | `LOGS_DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-030_validacion_distributed_3_servidores.md` | 44 | `DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\R-030_validacion_final_sin_bom.md` | 11 | `/ API / Panel / 192.168.60.10 /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-030_validacion_final_sin_bom.md` | 28 | `SERVICIOS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-030_validacion_final_sin_bom.md` | 29 | `BACKUPS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-030_validacion_final_sin_bom.md` | 30 | `LOGS_DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-030_validacion_final_sin_bom.md` | 31 | `DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-030_validacion_final_sin_bom.md` | 50 | `SERVICIOS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-030_validacion_final_sin_bom.md` | 51 | `BACKUPS_HOST=192.168.60.30` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-030_validacion_final_sin_bom.md` | 52 | `LOGS_DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-030_validacion_final_sin_bom.md` | 53 | `DB_HOST=192.168.60.20` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-040_validacion_instalacion_piloto_1.md` | 98 | `/ 4 / Terminal Database fallaba por known_hosts / Media / Corregida / Se registró la huella SSH de 192.168.60.20 /` |
| INFO | documentacion | 192.168.1.248 | `docs\validaciones\R-043_validacion_instalacion_piloto_2.md` | 25 | `/ Acceso web validado / OK / http://192.168.1.248:8000 /` |
| INFO | documentacion | 192.168.60.40 | `docs\validaciones\R-043_validacion_instalacion_piloto_2.md` | 76 | `/ Host SSH no permitido 192.168.60.40 / Corregida /` |
| INFO | documentacion | 192.168.1.140 | `docs\validaciones\R-049A_cierre_formulario_basico_soporte_panel.md` | 106 | `ip_origen 192.168.1.140` |
| INFO | documentacion | 192.168.1.140 | `docs\validaciones\R-049B_cierre_sqlite_tickets_soporte.md` | 129 | `ip_origen 192.168.1.140` |
| INFO | documentacion | 192.168.1.140 | `docs\validaciones\R-049C_cierre_vista_interna_tickets_soporte.md` | 151 | `ip_origen 192.168.1.140` |
| INFO | documentacion | 192.168.1.140 | `docs\validaciones\R-049D_cierre_estados_prioridades_tickets_soporte.md` | 204 | `ip_origen 192.168.1.140` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-049I_cierre_api_central_soporte_local.md` | 50 | `http://192.168.1.250:8010/` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-049J_cierre_detalle_ticket_panel_central.md` | 45 | `http://192.168.1.250:8010/` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-049J_cierre_detalle_ticket_panel_central.md` | 51 | `http://192.168.1.250:8010/tickets/CENTRAL-2026-0001` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-049K_cierre_estado_prioridad_panel_central.md` | 56 | `http://192.168.1.250:8010/tickets/CENTRAL-2026-0001` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049L_cierre_envio_panel_local_api_central.md` | 47 | `CENTRAL_SUPPORT_URL=http://127.0.0.1:8010/api/v1/support/tickets` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049L_envio_panel_local_api_central.md` | 71 | `CENTRAL_SUPPORT_URL=http://127.0.0.1:8010/api/v1/support/tickets` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049R_cierre_instalador_systemd_central_support.md` | 122 | `URL local: http://127.0.0.1:8010` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049R_cierre_instalador_systemd_central_support.md` | 148 | `GET http://127.0.0.1:8010/health` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049V_cierre_reverse_proxy_nginx_central_support.md` | 27 | `- Nginx reenvía tráfico hacia 127.0.0.1:8010.` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-049V_cierre_reverse_proxy_nginx_central_support.md` | 31 | `- http://192.168.1.250/` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049V_cierre_reverse_proxy_nginx_central_support.md` | 33 | `- proxy_pass hacia http://127.0.0.1:8010` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049V_cierre_reverse_proxy_nginx_central_support.md` | 91 | `- http://127.0.0.1:8010/health` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049V_cierre_reverse_proxy_nginx_central_support.md` | 104 | `- http://127.0.0.1/` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049V_cierre_reverse_proxy_nginx_central_support.md` | 117 | `- http://127.0.0.1/login` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049V_cierre_reverse_proxy_nginx_central_support.md` | 129 | `- http://127.0.0.1/` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-049V_cierre_reverse_proxy_nginx_central_support.md` | 140 | `- http://192.168.1.250/` |
| INFO | documentacion | 192.168.1.50 | `docs\validaciones\R-049V_cierre_reverse_proxy_nginx_central_support.md` | 170 | `- http://192.168.1.50` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049V_reverse_proxy_nginx_central_support.md` | 24 | `- Backend interno: 127.0.0.1:8010` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049V_reverse_proxy_nginx_central_support.md` | 37 | `- http://127.0.0.1:8010` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049V_reverse_proxy_nginx_central_support.md` | 63 | `- http://127.0.0.1/ responde.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049Y_cierre_limpieza_validacion_final_soporte.md` | 84 | `- http://127.0.0.1:8000/` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049Y_cierre_limpieza_validacion_final_soporte.md` | 97 | `- http://127.0.0.1:8010/health` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049Y_cierre_limpieza_validacion_final_soporte.md` | 110 | `- http://127.0.0.1/` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-049Y_cierre_limpieza_validacion_final_soporte.md` | 124 | `- CENTRAL_SUPPORT_URL=http://127.0.0.1:8010/api/v1/support/tickets` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-050_cierre_nginx_panel_local_cliente.md` | 26 | `- dasc-api escucha internamente en 127.0.0.1:8000.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-050_cierre_nginx_panel_local_cliente.md` | 34 | `- http://127.0.0.1:8000` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-050_cierre_nginx_panel_local_cliente.md` | 45 | `- http://192.168.1.250:8080/` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-050_cierre_nginx_panel_local_cliente.md` | 47 | `- http://127.0.0.1:8000` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-050_cierre_nginx_panel_local_cliente.md` | 52 | `- http://192.168.1.250/` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-050_cierre_nginx_panel_local_cliente.md` | 54 | `- http://127.0.0.1:8010` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-050_cierre_nginx_panel_local_cliente.md` | 93 | `- http://192.168.1.250:8080` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-050_cierre_nginx_panel_local_cliente.md` | 104 | `- http://192.168.1.250/static/css/estilo.css` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-050_cierre_nginx_panel_local_cliente.md` | 108 | `- http://192.168.1.250:8080/static/css/estilo.css` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-050_cierre_nginx_panel_local_cliente.md` | 139 | `- http://192.168.1.250/        -> panel central DASC por Nginx.` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-050_cierre_nginx_panel_local_cliente.md` | 140 | `- http://192.168.1.250:8080/   -> panel local cliente por Nginx.` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-050_cierre_nginx_panel_local_cliente.md` | 141 | `- http://192.168.1.250:8000/   -> backend directo del panel local.` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-050_cierre_nginx_panel_local_cliente.md` | 142 | `- http://192.168.1.250:8010/   -> backend directo del panel central.` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-050_FIX1_nginx_host_puerto_panel_local.md` | 15 | `- http://192.168.1.250:8080` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-050_FIX1_nginx_host_puerto_panel_local.md` | 26 | `- http://127.0.0.1/static/css/estilo.css` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-050_FIX1_nginx_host_puerto_panel_local.md` | 27 | `- http://127.0.0.1/static/img/logo-dasc.png` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-050_FIX1_nginx_host_puerto_panel_local.md` | 28 | `- http://127.0.0.1/static/img/logo-instituto.png` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-050_FIX1_nginx_host_puerto_panel_local.md` | 47 | `- http://192.168.1.250:8080` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-050_nginx_panel_local_cliente.md` | 41 | `- Nginx reenvía tráfico hacia 127.0.0.1:8000.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-050_nginx_panel_local_cliente.md` | 47 | `- http://127.0.0.1:8000` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-050_nginx_panel_local_cliente.md` | 60 | `- http://192.168.1.250:8080/` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-050_nginx_panel_local_cliente.md` | 62 | `- http://127.0.0.1:8000` |
| INFO | documentacion | 192.168.1.50 | `docs\validaciones\R-050_nginx_panel_local_cliente.md` | 71 | `- http://192.168.1.50/` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-051A_auditoria_ips_variables_instaladores.md` | 35 | `- 192.168.60.20` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-051A_auditoria_ips_variables_instaladores.md` | 36 | `- 192.168.60.30` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-051A_auditoria_ips_variables_instaladores.md` | 37 | `- 192.168.1.250` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051A_auditoria_ips_variables_instaladores.md` | 43 | `- 127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051A_auditoria_ips_variables_instaladores.md` | 50 | `- Nginx local reenviando a 127.0.0.1:8000.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051A_auditoria_ips_variables_instaladores.md` | 51 | `- Nginx central reenviando a 127.0.0.1:8010.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051A_auditoria_ips_variables_instaladores.md` | 52 | `- Comprobaciones curl contra 127.0.0.1.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051A_auditoria_ips_variables_instaladores.md` | 53 | `- DASC_ALLOWED_HOSTS incluyendo 127.0.0.1 y localhost.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051D_adaptar_instalador_api_perfiles.md` | 30 | `- BACKUPS_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051D_adaptar_instalador_api_perfiles.md` | 31 | `- SERVICIOS_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051D_adaptar_instalador_api_perfiles.md` | 32 | `- LOGS_DB_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051D_adaptar_instalador_api_perfiles.md` | 33 | `- TERMINAL_DATABASE_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051D_cierre_adaptar_instalador_api_perfiles.md` | 36 | `- BACKUPS_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051D_cierre_adaptar_instalador_api_perfiles.md` | 37 | `- SERVICIOS_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051D_cierre_adaptar_instalador_api_perfiles.md` | 38 | `- LOGS_DB_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051D_cierre_adaptar_instalador_api_perfiles.md` | 39 | `- TERMINAL_DATABASE_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051F_adaptar_instalador_backup_services_perfiles.md` | 82 | `- DB_HOST=127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051F_cierre_adaptar_instalador_backup_services_perfiles.md` | 79 | `- DB_HOST=127.0.0.1` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-051G_FIX1_eliminar_ips_laboratorio_defaults_api.md` | 19 | `- BACKUPS_HOST con default 192.168.60.30` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-051G_FIX1_eliminar_ips_laboratorio_defaults_api.md` | 20 | `- SERVICIOS_HOST con default 192.168.60.30` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-051G_FIX1_eliminar_ips_laboratorio_defaults_api.md` | 21 | `- LOGS_DB_HOST con default 192.168.60.20` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051G_FIX1_eliminar_ips_laboratorio_defaults_api.md` | 29 | `- BACKUPS_HOST -> 127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051G_FIX1_eliminar_ips_laboratorio_defaults_api.md` | 30 | `- SERVICIOS_HOST -> 127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051G_FIX1_eliminar_ips_laboratorio_defaults_api.md` | 31 | `- LOGS_DB_HOST -> 127.0.0.1` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-051G_FIX1_eliminar_ips_laboratorio_defaults_api.md` | 48 | `- No aparecen 192.168.60.20, 192.168.60.30 ni 192.168.1.250 en deploy.` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-051G_FIX1_eliminar_ips_laboratorio_defaults_api.md` | 48 | `- No aparecen 192.168.60.20, 192.168.60.30 ni 192.168.1.250 en deploy.` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-051G_FIX1_eliminar_ips_laboratorio_defaults_api.md` | 48 | `- No aparecen 192.168.60.20, 192.168.60.30 ni 192.168.1.250 en deploy.` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-051G_validacion_global_instaladores_adaptables.md` | 82 | `- 192.168.60.30` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-051G_validacion_global_instaladores_adaptables.md` | 83 | `- 192.168.60.20` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051G_validacion_global_instaladores_adaptables.md` | 97 | `- BACKUPS_HOST -> 127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051G_validacion_global_instaladores_adaptables.md` | 98 | `- SERVICIOS_HOST -> 127.0.0.1` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051G_validacion_global_instaladores_adaptables.md` | 99 | `- LOGS_DB_HOST -> 127.0.0.1` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-051G_validacion_global_instaladores_adaptables.md` | 105 | `- No quedan IPs fijas 192.168.60.20, 192.168.60.30 ni 192.168.1.250 dentro de deploy.` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-051G_validacion_global_instaladores_adaptables.md` | 105 | `- No quedan IPs fijas 192.168.60.20, 192.168.60.30 ni 192.168.1.250 dentro de deploy.` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-051G_validacion_global_instaladores_adaptables.md` | 105 | `- No quedan IPs fijas 192.168.60.20, 192.168.60.30 ni 192.168.1.250 dentro de deploy.` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-051H_cierre_global_instaladores_adaptables.md` | 194 | `- 192.168.60.30` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-051H_cierre_global_instaladores_adaptables.md` | 195 | `- 192.168.60.20` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-051H_cierre_global_instaladores_adaptables.md` | 199 | `- 127.0.0.1` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\R-051H_cierre_global_instaladores_adaptables.md` | 224 | `- No quedan IPs fijas 192.168.60.20, 192.168.60.30 ni 192.168.1.250 dentro de deploy.` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\R-051H_cierre_global_instaladores_adaptables.md` | 224 | `- No quedan IPs fijas 192.168.60.20, 192.168.60.30 ni 192.168.1.250 dentro de deploy.` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-051H_cierre_global_instaladores_adaptables.md` | 224 | `- No quedan IPs fijas 192.168.60.20, 192.168.60.30 ni 192.168.1.250 dentro de deploy.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052C_auditoria_puertos_nginx.md` | 44 | `- 127.0.0.1:8000` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052C_auditoria_puertos_nginx.md` | 45 | `- 127.0.0.1:8010` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052E_cierre_endurecer_api_usuario_dedicado.md` | 58 | `- ExecStart=/opt/dasc/api/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052E_cierre_endurecer_api_usuario_dedicado.md` | 106 | `- ExecStart usando 127.0.0.1.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052E_cierre_endurecer_api_usuario_dedicado.md` | 111 | `- puerto 8000 escucha solo en 127.0.0.1.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052E_cierre_endurecer_api_usuario_dedicado.md` | 112 | `- panel local directo local responde en 127.0.0.1:8000.` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-052E_cierre_endurecer_api_usuario_dedicado.md` | 122 | `- http://192.168.1.250:8080/` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052E_cierre_endurecer_api_usuario_dedicado.md` | 126 | `- http://127.0.0.1:8000/` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052E_endurecer_api_usuario_dedicado.md` | 34 | `- Cambia Uvicorn de 0.0.0.0 a 127.0.0.1.` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-052E_endurecer_api_usuario_dedicado.md` | 56 | `- http://192.168.1.250:8080/` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052E_endurecer_api_usuario_dedicado.md` | 70 | `- ExecStart usa --host 127.0.0.1.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_cierre_endurecer_central_support_backend_interno.md` | 15 | `- dasc-api ya escuchaba internamente en 127.0.0.1:8000.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_cierre_endurecer_central_support_backend_interno.md` | 48 | `- 127.0.0.1:8010` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-052F_cierre_endurecer_central_support_backend_interno.md` | 52 | `- http://192.168.1.250/` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_cierre_endurecer_central_support_backend_interno.md` | 57 | `- 127.0.0.1:8010` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_cierre_endurecer_central_support_backend_interno.md` | 68 | `- ExecStart=/opt/dasc/central-support/venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8010` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_cierre_endurecer_central_support_backend_interno.md` | 98 | `- 127.0.0.1:8010 0.0.0.0:*` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_cierre_endurecer_central_support_backend_interno.md` | 111 | `- systemd central usa --host 127.0.0.1.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_cierre_endurecer_central_support_backend_interno.md` | 112 | `- 8010 escucha en 127.0.0.1:8010.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_cierre_endurecer_central_support_backend_interno.md` | 128 | `- dasc-api: 127.0.0.1:8000` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_cierre_endurecer_central_support_backend_interno.md` | 129 | `- central-support: 127.0.0.1:8010` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_endurecer_central_support_backend_interno.md` | 15 | `- dasc-api ya fue corregido para escuchar en 127.0.0.1:8000.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_endurecer_central_support_backend_interno.md` | 24 | `- central-support escucha internamente en 127.0.0.1:8010.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_endurecer_central_support_backend_interno.md` | 47 | `- --host 127.0.0.1 --port 8010` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_endurecer_central_support_backend_interno.md` | 61 | `- systemd use --host 127.0.0.1.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_endurecer_central_support_backend_interno.md` | 62 | `- 8010 escuche en 127.0.0.1 y no en 0.0.0.0.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_FIX1_robustecer_health_central_support.md` | 15 | `- central-support pasó a escuchar en 127.0.0.1:8010.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_FIX1_robustecer_health_central_support.md` | 16 | `- systemd quedó usando --host 127.0.0.1.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_FIX1_robustecer_health_central_support.md` | 40 | `- 127.0.0.1:8010 0.0.0.0:*` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_FIX1_robustecer_health_central_support.md` | 58 | `- 127.0.0.1:8010` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052F_FIX1_robustecer_health_central_support.md` | 70 | `- ss confirma 127.0.0.1:8010 como dirección local.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052G_validacion_global_final_seguridad.md` | 44 | `- ExecStart con --host 127.0.0.1 --port 8000` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052G_validacion_global_final_seguridad.md` | 52 | `- ExecStart con --host 127.0.0.1 --port 8010` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052G_validacion_global_final_seguridad.md` | 58 | `- 8000 escucha en 127.0.0.1:8000.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052G_validacion_global_final_seguridad.md` | 59 | `- 8010 escucha en 127.0.0.1:8010.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052G_validacion_global_final_seguridad.md` | 136 | `- dasc-api-local en 8080 hacia 127.0.0.1:8000.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052G_validacion_global_final_seguridad.md` | 137 | `- dasc-central-support en 80 hacia 127.0.0.1:8010.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052G_validacion_global_final_seguridad.md` | 154 | `- dasc-api ejecutando uvicorn con --host 127.0.0.1 --port 8000.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052G_validacion_global_final_seguridad.md` | 155 | `- central-support ejecutando uvicorn con --host 127.0.0.1 --port 8010.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052H_cierre_global_revision_seguridad.md` | 93 | `- Uvicorn del panel local limitado a 127.0.0.1:8000.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052H_cierre_global_revision_seguridad.md` | 109 | `- central-support limitado a 127.0.0.1:8010.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052H_cierre_global_revision_seguridad.md` | 133 | `- 8000 solo en 127.0.0.1.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052H_cierre_global_revision_seguridad.md` | 134 | `- 8010 solo en 127.0.0.1.` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-052H_cierre_global_revision_seguridad.md` | 167 | `- http://192.168.1.250:8080/` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052H_cierre_global_revision_seguridad.md` | 172 | `- 127.0.0.1:8000` |
| INFO | documentacion | 192.168.1.250 | `docs\validaciones\R-052H_cierre_global_revision_seguridad.md` | 186 | `- http://192.168.1.250/` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-052H_cierre_global_revision_seguridad.md` | 191 | `- 127.0.0.1:8010` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-053D_checklist_instalacion_desde_cero.md` | 20 | `/ F2 / `install_dasc_api.sh` solo configura el SSH a sí mismo (127.0.0.1) si **ya existen `sshd` + usuario `dasc`**. Si se corre primero, salta el paso (no bloqueante) y los backups no funcionan. / Media / Por eso `db` y `backup-services` van **antes** que `api`. /` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-053D_checklist_instalacion_desde_cero.md` | 22 | `/ F4 / `install_db.sh` **no** auto-rellena `BACKUP_ALLOWED_HOST`/`LOGS_ALLOWED_HOST` a `127.0.0.1` en perfil lite: los **pregunta**. / Baja / En Lite responder `127.0.0.1` (o pasarlos por entorno). /` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-053D_checklist_instalacion_desde_cero.md` | 22 | `/ F4 / `install_db.sh` **no** auto-rellena `BACKUP_ALLOWED_HOST`/`LOGS_ALLOWED_HOST` a `127.0.0.1` en perfil lite: los **pregunta**. / Baja / En Lite responder `127.0.0.1` (o pasarlos por entorno). /` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-053D_checklist_instalacion_desde_cero.md` | 71 | `BACKUP_ALLOWED_HOST=127.0.0.1 LOGS_ALLOWED_HOST=127.0.0.1 \` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-053D_checklist_instalacion_desde_cero.md` | 71 | `BACKUP_ALLOWED_HOST=127.0.0.1 LOGS_ALLOWED_HOST=127.0.0.1 \` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-053D_checklist_instalacion_desde_cero.md` | 91 | `- [ ] Servicio `dasc-api` activo; `curl -I http://127.0.0.1:8000` responde.` |
| INFO | documentacion | 127.0.0.1 | `docs\validaciones\R-053D_checklist_instalacion_desde_cero.md` | 92 | `- [ ] Clave de la API autorizada en `dasc@127.0.0.1` (paso SSH **no** saltado).` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `config.env.example` | 12 | `SERVICIOS_HOST=192.168.60.30` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `config.env.example` | 13 | `BACKUPS_HOST=192.168.60.30` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `config.env.example` | 14 | `TERMINAL_DATABASE_HOST=192.168.60.20` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `config.env.example` | 18 | `LOGS_DB_HOST=192.168.60.20` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `config.env.example` | 37 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `config.env.example` | 37 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| MEDIA | codigo_o_recurso | 192.168.60.40 | `config.env.example` | 37 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `config.env.example` | 37 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `config\perfiles\config.distributed.env.example` | 18 | `# - DB / Logs: 192.168.60.20` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `config\perfiles\config.distributed.env.example` | 19 | `# - Backups / Servicios: 192.168.60.30` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `config\perfiles\config.distributed.env.example` | 20 | `SERVICIOS_HOST=192.168.60.30` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `config\perfiles\config.distributed.env.example` | 21 | `BACKUPS_HOST=192.168.60.30` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `config\perfiles\config.distributed.env.example` | 22 | `LOGS_DB_HOST=192.168.60.20` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `config\perfiles\config.distributed.env.example` | 23 | `DB_HOST=192.168.60.20` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `config\perfiles\config.dual.env.example` | 17 | `# - Servidor principal / DB: 192.168.60.20` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `config\perfiles\config.dual.env.example` | 18 | `# - Servidor DASC / backups / logs: 192.168.60.30` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `config\perfiles\config.dual.env.example` | 19 | `SERVICIOS_HOST=192.168.60.20` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `config\perfiles\config.dual.env.example` | 20 | `BACKUPS_HOST=192.168.60.30` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `config\perfiles\config.dual.env.example` | 21 | `LOGS_DB_HOST=192.168.60.30` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `config\perfiles\config.dual.env.example` | 22 | `DB_HOST=192.168.60.20` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `config\perfiles\config.single.env.example` | 15 | `SERVICIOS_HOST=127.0.0.1` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `config\perfiles\config.single.env.example` | 16 | `BACKUPS_HOST=127.0.0.1` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `config\perfiles\config.single.env.example` | 17 | `LOGS_DB_HOST=127.0.0.1` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `config\perfiles\config.single.env.example` | 18 | `DB_HOST=127.0.0.1` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\api\harden_dasc_api_security.sh` | 78 | `sed -i -E 's/--host[[:space:]]+[^[:space:]]+/--host 127.0.0.1/g' "$SERVICE_FILE"` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\api\harden_dasc_api_security.sh` | 140 | `curl -i -s http://127.0.0.1:8000/ / head -n 10` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\api\package\main.py` | 102 | `SERVIDOR_BACKUPS = os.getenv("BACKUPS_HOST", "127.0.0.1")` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\api\package\main.py` | 103 | `SERVIDOR_SERVICIOS = os.getenv("SERVICIOS_HOST", "127.0.0.1")` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\api\package\main.py` | 104 | `CACTI_URL = os.getenv("CACTI_URL", "http://127.0.0.1/cacti/")` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\api\package\main.py` | 106 | `LOGS_DB_HOST = os.getenv("LOGS_DB_HOST", "127.0.0.1")` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\api\package\main.py` | 112 | `TERMINAL_MAIN_HOST = os.getenv("TERMINAL_MAIN_HOST", "127.0.0.1")` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\api\package\main.py` | 3388 | `CENTRAL_SUPPORT_URL = os.getenv("CENTRAL_SUPPORT_URL", "http://127.0.0.1:8010/api/v1/support/tickets").strip()` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\api\package\scripts\retry_central_pending.py` | 46 | `ip_origen="127.0.0.1",` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\central-support\harden_central_support_security.sh` | 39 | `echo "==> Ajustando central-support para escuchar solo en 127.0.0.1"` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\central-support\harden_central_support_security.sh` | 40 | `sed -i -E 's/--host[[:space:]]+[^[:space:]]+/--host 127.0.0.1/g' "$SERVICE_FILE"` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\central-support\harden_central_support_security.sh` | 60 | `if curl -fsS http://127.0.0.1:8010/health >/tmp/dasc-central-health.json 2>/tmp/dasc-central-health.err; then` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\central-support\harden_central_support_security.sh` | 76 | `curl -i -s http://127.0.0.1/ / head -n 12` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\central-support\harden_central_support_security.sh` | 84 | `echo "El backend central debe quedar interno en 127.0.0.1:8010."` |
| MEDIA | codigo_o_recurso | 192.168.60.10 | `README.md` | 37 | `/ lab-api / API / Panel / Reverse proxy HTTPS / 192.168.60.10 / 192.168.1.244 /` |
| MEDIA | codigo_o_recurso | 192.168.1.244 | `README.md` | 37 | `/ lab-api / API / Panel / Reverse proxy HTTPS / 192.168.60.10 / 192.168.1.244 /` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `README.md` | 38 | `/ lab-db / MariaDB / Logs / Datos / 192.168.60.20 / 192.168.1.243 /` |
| MEDIA | codigo_o_recurso | 192.168.1.243 | `README.md` | 38 | `/ lab-db / MariaDB / Logs / Datos / 192.168.60.20 / 192.168.1.243 /` |
| MEDIA | codigo_o_recurso | 192.168.1.245 | `README.md` | 39 | `/ lab-backup / Backups + Servicios / 192.168.60.30 / 192.168.1.245 /` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `README.md` | 39 | `/ lab-backup / Backups + Servicios / 192.168.60.30 / 192.168.1.245 /` |
| MEDIA | herramienta_producto | 127.0.0.1 | `deploy\api\package\tools\check_api_installation.sh` | 103 | `check_command "Puerto local API responde" "curl -fsSI http://127.0.0.1:8000"` |

## Interpretación inicial

Esta auditoría no corrige automáticamente las IPs.

Sirve para decidir qué referencias deben transformarse en variables de instalación y cuáles pueden quedarse como documentación de laboratorio.

## Próximo paso

Clasificar los hallazgos en:

- A mantener como evidencia histórica o documentación.
- A convertir en valores de config.env.example.
- A preguntar desde instaladores.
- A derivar según perfil Lite, PyME 2 servidores o Pro 3 servidores.

## Resultado

Resultado: REVISAR. Hay IPs fijas de severidad ALTA.
