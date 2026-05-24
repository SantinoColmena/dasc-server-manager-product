# AuditorÃ­a de IPs fijas y perfiles

Fecha: 2026-05-24 08:40:55

## Objetivo

Detectar referencias a IPs fijas dentro del repositorio para preparar instaladores adaptables por perfil e IPs reales.

## Resumen

| Campo | Valor |
|---|---|
| Total referencias IP detectadas | 415 |
| Severidad ALTA | 8 |
| Severidad MEDIA | 36 |
| Severidad BAJA | 10 |
| Severidad INFO | 361 |

## Criterio de severidad

| Severidad | Significado |
|---|---|
| ALTA | IP fija en instalador o configuraciÃ³n real. Debe revisarse antes de usar en cliente real. |
| MEDIA | IP fija en herramienta de producto o cÃ³digo/recurso. Debe parametrizarse si afecta a ejecuciÃ³n. |
| BAJA | IP en ejemplo de configuraciÃ³n. Puede mantenerse temporalmente si estÃ¡ claro que es ejemplo. |
| INFO | IP en documentaciÃ³n o validaciones. No bloquea, pero debe quedar contextualizada. |

## Hallazgos

| Severidad | Zona | IP | Archivo | LÃ­nea | Contenido |
|---|---|---|---|---:|---|
| ALTA | instalador | 127.0.0.1 | `deploy\api\install_dasc_api.sh` | 342 | `write_env_value "DASC_SSH_ALLOWED_HOSTS" "127.0.0.1,localhost,${BACKUP_HOST},${SERVICES_HOST},${DATABASE_HOST}"` |
| ALTA | instalador | 127.0.0.1 | `deploy\api\install_dasc_api.sh` | 417 | `curl -I http://127.0.0.1:8000 // true` |
| ALTA | instalador | 127.0.0.1 | `deploy\api\install_dasc_api.sh` | 426 | `echo "URL local: http://127.0.0.1:8000"` |
| ALTA | instalador | 192.168.60.20 | `deploy\backup-services\install_backup_services.sh` | 9 | `DB_HOST="${DB_HOST:-192.168.60.20}"` |
| ALTA | instalador | 192.168.60.30 | `deploy\db\install_db.sh` | 10 | `BACKUP_ALLOWED_HOST="${BACKUP_ALLOWED_HOST:-192.168.60.30}"` |
| ALTA | instalador | 192.168.60.10 | `deploy\db\install_db.sh` | 16 | `LOGS_ALLOWED_HOST="${LOGS_ALLOWED_HOST:-192.168.60.10}"` |
| ALTA | instalador | 127.0.0.1 | `deploy\proxy\install_reverse_proxy.sh` | 6 | `UPSTREAM_HOST="${UPSTREAM_HOST:-127.0.0.1}"` |
| ALTA | instalador | 127.0.0.1 | `deploy\proxy\install_reverse_proxy.sh` | 101 | `curl -k -I https://127.0.0.1 // true` |
| BAJA | ejemplo_configuracion | 192.168.60.30 | `deploy\api\package\config.env.example` | 12 | `SERVICIOS_HOST=192.168.60.30` |
| BAJA | ejemplo_configuracion | 192.168.60.30 | `deploy\api\package\config.env.example` | 13 | `BACKUPS_HOST=192.168.60.30` |
| BAJA | ejemplo_configuracion | 192.168.60.20 | `deploy\api\package\config.env.example` | 14 | `TERMINAL_DATABASE_HOST=192.168.60.20` |
| BAJA | ejemplo_configuracion | 192.168.60.20 | `deploy\api\package\config.env.example` | 18 | `LOGS_DB_HOST=192.168.60.20` |
| BAJA | ejemplo_configuracion | 127.0.0.1 | `deploy\api\package\config.env.example` | 37 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| BAJA | ejemplo_configuracion | 192.168.60.40 | `deploy\api\package\config.env.example` | 37 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| BAJA | ejemplo_configuracion | 192.168.60.30 | `deploy\api\package\config.env.example` | 37 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| BAJA | ejemplo_configuracion | 192.168.60.20 | `deploy\api\package\config.env.example` | 37 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| BAJA | ejemplo_configuracion | 192.168.60.20 | `deploy\api\package\config.env.example` | 39 | `BACKUP_DB_HOST=192.168.60.20` |
| BAJA | ejemplo_configuracion | 192.168.60.20 | `deploy\api\package\config.env.example` | 48 | `RESTORE_DB_HOST=192.168.60.20` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 32 | `/ ALTA / instalador / 127.0.0.1 / $fileSafe / 342 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 33 | `/ ALTA / instalador / 127.0.0.1 / $fileSafe / 417 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 34 | `/ ALTA / instalador / 127.0.0.1 / $fileSafe / 426 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 35 | `/ ALTA / instalador / 192.168.60.20 / $fileSafe / 9 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 36 | `/ ALTA / instalador / 192.168.60.30 / $fileSafe / 10 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 37 | `/ ALTA / instalador / 192.168.60.10 / $fileSafe / 16 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 38 | `/ ALTA / instalador / 127.0.0.1 / $fileSafe / 6 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 39 | `/ ALTA / instalador / 127.0.0.1 / $fileSafe / 101 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 40 | `/ BAJA / ejemplo_configuracion / 192.168.60.30 / $fileSafe / 12 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 41 | `/ BAJA / ejemplo_configuracion / 192.168.60.30 / $fileSafe / 13 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 42 | `/ BAJA / ejemplo_configuracion / 192.168.60.20 / $fileSafe / 14 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 43 | `/ BAJA / ejemplo_configuracion / 192.168.60.20 / $fileSafe / 18 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 44 | `/ BAJA / ejemplo_configuracion / 192.168.60.30 / $fileSafe / 37 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 45 | `/ BAJA / ejemplo_configuracion / 192.168.60.40 / $fileSafe / 37 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 46 | `/ BAJA / ejemplo_configuracion / 127.0.0.1 / $fileSafe / 37 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 47 | `/ BAJA / ejemplo_configuracion / 192.168.60.20 / $fileSafe / 37 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 48 | `/ BAJA / ejemplo_configuracion / 192.168.60.20 / $fileSafe / 39 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 49 | `/ BAJA / ejemplo_configuracion / 192.168.60.20 / $fileSafe / 48 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 50 | `/ INFO / documentacion / 192.168.60.40 / $fileSafe / 53 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 51 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 16 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 52 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 24 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 53 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 25 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 54 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 32 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 55 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 45 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 56 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 13 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 57 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 14 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 58 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 38 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 59 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 65 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 60 | `/ INFO / documentacion / 192.168.60.40 / $fileSafe / 12 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 61 | `/ INFO / documentacion / 192.168.60.40 / $fileSafe / 12 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 62 | `/ INFO / documentacion / 192.168.60.40 / $fileSafe / 25 / $lineSafe /` |
| INFO | documentacion | 192.168.1.248 | `docs\auditoria\auditoria_ips_perfiles.md` | 63 | `/ INFO / documentacion / 192.168.1.248 / $fileSafe / 26 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 64 | `/ INFO / documentacion / 192.168.60.40 / $fileSafe / 20 / $lineSafe /` |
| INFO | documentacion | 192.168.1.248 | `docs\auditoria\auditoria_ips_perfiles.md` | 65 | `/ INFO / documentacion / 192.168.1.248 / $fileSafe / 21 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 66 | `/ INFO / documentacion / 192.168.60.40 / $fileSafe / 56 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 67 | `/ INFO / documentacion / 192.168.60.40 / $fileSafe / 56 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 68 | `/ INFO / documentacion / 192.168.60.40 / $fileSafe / 60 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 69 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 84 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 70 | `/ INFO / documentacion / 192.168.60.40 / $fileSafe / 84 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 71 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 84 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 72 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 84 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 73 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 80 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 74 | `/ INFO / documentacion / 192.168.60.40 / $fileSafe / 32 / $lineSafe /` |
| INFO | documentacion | 192.168.1.248 | `docs\auditoria\auditoria_ips_perfiles.md` | 75 | `/ INFO / documentacion / 192.168.1.248 / $fileSafe / 33 / $lineSafe /` |
| INFO | documentacion | 192.168.1.248 | `docs\auditoria\auditoria_ips_perfiles.md` | 76 | `/ INFO / documentacion / 192.168.1.248 / $fileSafe / 54 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 77 | `/ INFO / documentacion / 192.168.60.40 / $fileSafe / 120 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 78 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 25 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 79 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 26 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 80 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 27 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 81 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 55 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 82 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 56 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 83 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 57 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 84 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 86 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 85 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 87 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 86 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 88 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 87 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 38 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 88 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 39 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 89 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 40 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 90 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 211 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 91 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 112 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 92 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 310 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 93 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 316 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 94 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 322 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 95 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 336 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 96 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 351 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 97 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 357 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 98 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 129 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 99 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 21 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 100 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 27 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 101 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 78 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 102 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 35 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 103 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 40 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 104 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 40 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 105 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 114 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 106 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 27 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 107 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 118 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 108 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 15 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 109 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 16 / $lineSafe /` |
| INFO | documentacion | 192.168.60.0 | `docs\auditoria\auditoria_ips_perfiles.md` | 110 | `/ INFO / documentacion / 192.168.60.0 / $fileSafe / 24 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 111 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 31 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 112 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 32 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 113 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 66 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 114 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 76 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 115 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 94 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 116 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 15 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 117 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 16 / $lineSafe /` |
| INFO | documentacion | 192.168.1.250 | `docs\auditoria\auditoria_ips_perfiles.md` | 118 | `/ INFO / documentacion / 192.168.1.250 / $fileSafe / 54 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 119 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 28 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 120 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 29 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 121 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 64 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 122 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 81 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 123 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 144 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 124 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 158 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 125 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 15 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 126 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 16 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 127 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 59 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 128 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 103 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 129 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 135 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 130 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 165 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 131 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 107 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 132 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 108 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 133 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 15 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 134 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 16 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 135 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 120 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 136 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 15 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 137 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 16 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 138 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 15 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 139 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 16 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 140 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 56 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 141 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 88 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 142 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 192 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 143 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 11 / $lineSafe /` |
| INFO | documentacion | 192.168.1.244 | `docs\auditoria\auditoria_ips_perfiles.md` | 144 | `/ INFO / documentacion / 192.168.1.244 / $fileSafe / 11 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 145 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 12 / $lineSafe /` |
| INFO | documentacion | 192.168.1.243 | `docs\auditoria\auditoria_ips_perfiles.md` | 146 | `/ INFO / documentacion / 192.168.1.243 / $fileSafe / 12 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 147 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 13 / $lineSafe /` |
| INFO | documentacion | 192.168.1.245 | `docs\auditoria\auditoria_ips_perfiles.md` | 148 | `/ INFO / documentacion / 192.168.1.245 / $fileSafe / 13 / $lineSafe /` |
| INFO | documentacion | 192.168.60.0 | `docs\auditoria\auditoria_ips_perfiles.md` | 149 | `/ INFO / documentacion / 192.168.60.0 / $fileSafe / 21 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 150 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 34 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 151 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 35 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 152 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 39 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 153 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 122 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 154 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 123 / $lineSafe /` |
| INFO | documentacion | 192.168.1.137 | `docs\auditoria\auditoria_ips_perfiles.md` | 155 | `/ INFO / documentacion / 192.168.1.137 / $fileSafe / 143 / $lineSafe /` |
| INFO | documentacion | 192.168.1.244 | `docs\auditoria\auditoria_ips_perfiles.md` | 156 | `/ INFO / documentacion / 192.168.1.244 / $fileSafe / 160 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 157 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 207 / $lineSafe /` |
| INFO | documentacion | 192.168.1.244 | `docs\auditoria\auditoria_ips_perfiles.md` | 158 | `/ INFO / documentacion / 192.168.1.244 / $fileSafe / 272 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 159 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 12 / $lineSafe /` |
| INFO | documentacion | 192.168.1.244 | `docs\auditoria\auditoria_ips_perfiles.md` | 160 | `/ INFO / documentacion / 192.168.1.244 / $fileSafe / 13 / $lineSafe /` |
| INFO | documentacion | 192.168.1.244 | `docs\auditoria\auditoria_ips_perfiles.md` | 161 | `/ INFO / documentacion / 192.168.1.244 / $fileSafe / 14 / $lineSafe /` |
| INFO | documentacion | 192.168.1.137 | `docs\auditoria\auditoria_ips_perfiles.md` | 162 | `/ INFO / documentacion / 192.168.1.137 / $fileSafe / 43 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 163 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 19 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 164 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 20 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 165 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 21 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 166 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 81 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 167 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 82 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 168 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 83 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 169 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 111 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 170 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 177 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 171 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 178 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 172 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 179 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 173 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 180 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 174 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 48 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 175 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 13 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 176 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 30 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 177 | `/ INFO / documentacion / 127.0.0.1 / $fileSafe / 20 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 178 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 13 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 179 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 13 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 180 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 51 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 181 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 52 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 182 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 53 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 183 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 11 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 184 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 12 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 185 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 13 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 186 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 41 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 187 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 42 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 188 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 43 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 189 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 44 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 190 | `/ INFO / documentacion / 192.168.60.10 / $fileSafe / 11 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 191 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 28 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 192 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 29 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 193 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 30 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 194 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 31 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 195 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 50 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 196 | `/ INFO / documentacion / 192.168.60.30 / $fileSafe / 51 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 197 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 52 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 198 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 53 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 199 | `/ INFO / documentacion / 192.168.60.20 / $fileSafe / 98 / $lineSafe /` |
| INFO | documentacion | 192.168.1.248 | `docs\auditoria\auditoria_ips_perfiles.md` | 200 | `/ INFO / documentacion / 192.168.1.248 / $fileSafe / 25 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 201 | `/ INFO / documentacion / 192.168.60.40 / $fileSafe / 76 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 202 | `/ MEDIA / codigo_o_recurso / 192.168.60.30 / $fileSafe / 12 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 203 | `/ MEDIA / codigo_o_recurso / 192.168.60.30 / $fileSafe / 13 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 204 | `/ MEDIA / codigo_o_recurso / 192.168.60.20 / $fileSafe / 14 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 205 | `/ MEDIA / codigo_o_recurso / 192.168.60.20 / $fileSafe / 18 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 206 | `/ MEDIA / codigo_o_recurso / 192.168.60.30 / $fileSafe / 37 / $lineSafe /` |
| INFO | documentacion | 192.168.60.40 | `docs\auditoria\auditoria_ips_perfiles.md` | 207 | `/ MEDIA / codigo_o_recurso / 192.168.60.40 / $fileSafe / 37 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 208 | `/ MEDIA / codigo_o_recurso / 127.0.0.1 / $fileSafe / 37 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 209 | `/ MEDIA / codigo_o_recurso / 192.168.60.20 / $fileSafe / 37 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 210 | `/ MEDIA / codigo_o_recurso / 192.168.60.20 / $fileSafe / 18 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 211 | `/ MEDIA / codigo_o_recurso / 192.168.60.30 / $fileSafe / 19 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 212 | `/ MEDIA / codigo_o_recurso / 192.168.60.30 / $fileSafe / 20 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 213 | `/ MEDIA / codigo_o_recurso / 192.168.60.30 / $fileSafe / 21 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 214 | `/ MEDIA / codigo_o_recurso / 192.168.60.20 / $fileSafe / 22 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 215 | `/ MEDIA / codigo_o_recurso / 192.168.60.20 / $fileSafe / 23 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 216 | `/ MEDIA / codigo_o_recurso / 192.168.60.20 / $fileSafe / 17 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 217 | `/ MEDIA / codigo_o_recurso / 192.168.60.30 / $fileSafe / 18 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 218 | `/ MEDIA / codigo_o_recurso / 192.168.60.20 / $fileSafe / 19 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 219 | `/ MEDIA / codigo_o_recurso / 192.168.60.30 / $fileSafe / 20 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 220 | `/ MEDIA / codigo_o_recurso / 192.168.60.30 / $fileSafe / 21 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 221 | `/ MEDIA / codigo_o_recurso / 192.168.60.20 / $fileSafe / 22 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 222 | `/ MEDIA / codigo_o_recurso / 127.0.0.1 / $fileSafe / 15 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 223 | `/ MEDIA / codigo_o_recurso / 127.0.0.1 / $fileSafe / 16 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 224 | `/ MEDIA / codigo_o_recurso / 127.0.0.1 / $fileSafe / 17 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 225 | `/ MEDIA / codigo_o_recurso / 127.0.0.1 / $fileSafe / 18 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 226 | `/ MEDIA / codigo_o_recurso / 192.168.60.30 / $fileSafe / 43 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 227 | `/ MEDIA / codigo_o_recurso / 192.168.60.30 / $fileSafe / 44 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 228 | `/ MEDIA / codigo_o_recurso / 127.0.0.1 / $fileSafe / 45 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 229 | `/ MEDIA / codigo_o_recurso / 192.168.60.20 / $fileSafe / 47 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 230 | `/ MEDIA / codigo_o_recurso / 127.0.0.1 / $fileSafe / 53 / $lineSafe /` |
| INFO | documentacion | 192.168.60.10 | `docs\auditoria\auditoria_ips_perfiles.md` | 231 | `/ MEDIA / codigo_o_recurso / 192.168.60.10 / $fileSafe / 37 / $lineSafe /` |
| INFO | documentacion | 192.168.1.244 | `docs\auditoria\auditoria_ips_perfiles.md` | 232 | `/ MEDIA / codigo_o_recurso / 192.168.1.244 / $fileSafe / 37 / $lineSafe /` |
| INFO | documentacion | 192.168.1.243 | `docs\auditoria\auditoria_ips_perfiles.md` | 233 | `/ MEDIA / codigo_o_recurso / 192.168.1.243 / $fileSafe / 38 / $lineSafe /` |
| INFO | documentacion | 192.168.60.20 | `docs\auditoria\auditoria_ips_perfiles.md` | 234 | `/ MEDIA / codigo_o_recurso / 192.168.60.20 / $fileSafe / 38 / $lineSafe /` |
| INFO | documentacion | 192.168.60.30 | `docs\auditoria\auditoria_ips_perfiles.md` | 235 | `/ MEDIA / codigo_o_recurso / 192.168.60.30 / $fileSafe / 39 / $lineSafe /` |
| INFO | documentacion | 192.168.1.245 | `docs\auditoria\auditoria_ips_perfiles.md` | 236 | `/ MEDIA / codigo_o_recurso / 192.168.1.245 / $fileSafe / 39 / $lineSafe /` |
| INFO | documentacion | 127.0.0.1 | `docs\auditoria\auditoria_ips_perfiles.md` | 237 | `/ MEDIA / herramienta_producto / 127.0.0.1 / $fileSafe / 103 / $lineSafe /` |
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
| INFO | documentacion | 192.168.60.30 | `docs\pilotos\piloto_2\plan_ejecucion.md` | 84 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\piloto_2\plan_ejecucion.md` | 84 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| INFO | documentacion | 127.0.0.1 | `docs\pilotos\piloto_2\plan_ejecucion.md` | 84 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| INFO | documentacion | 192.168.60.20 | `docs\pilotos\piloto_2\plan_ejecucion.md` | 84 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| INFO | documentacion | 192.168.60.20 | `docs\pilotos\R-042_correccion_fallos_piloto_1.md` | 80 | `- La huella SSH de 192.168.60.20 no estaba registrada.` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\R-043_instalacion_piloto_2_1_servidor_externo.md` | 32 | `/ IP de gestión interna / 192.168.60.40 /` |
| INFO | documentacion | 192.168.1.248 | `docs\pilotos\R-043_instalacion_piloto_2_1_servidor_externo.md` | 33 | `/ IP de acceso desde navegador / 192.168.1.248 /` |
| INFO | documentacion | 192.168.1.248 | `docs\pilotos\R-043_instalacion_piloto_2_1_servidor_externo.md` | 54 | `http://192.168.1.248:8000` |
| INFO | documentacion | 192.168.60.40 | `docs\pilotos\R-043_instalacion_piloto_2_1_servidor_externo.md` | 120 | `/ 2 / 192.168.60.40 no estaba permitido en DASC_SSH_ALLOWED_HOSTS / Media / Corregida /` |
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
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\F6-GATE-01A_cierre_instalacion_limpia_api_ubuntu.md` | 40 | `Durante la primera ejecución se detectó que el instalador intentaba registrar la huella SSH de hosts remotos como `192.168.60.30` y `192.168.60.20`.` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\F6-GATE-01A_cierre_instalacion_limpia_api_ubuntu.md` | 40 | `Durante la primera ejecución se detectó que el instalador intentaba registrar la huella SSH de hosts remotos como `192.168.60.30` y `192.168.60.20`.` |
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
| INFO | documentacion | 192.168.1.244 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 11 | `/ lab-api / API / Panel / Reverse proxy / 192.168.60.10 / 192.168.1.244 /` |
| INFO | documentacion | 192.168.60.10 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 11 | `/ lab-api / API / Panel / Reverse proxy / 192.168.60.10 / 192.168.1.244 /` |
| INFO | documentacion | 192.168.60.20 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 12 | `/ lab-db / Base de datos MariaDB / 192.168.60.20 / 192.168.1.243 /` |
| INFO | documentacion | 192.168.1.243 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 12 | `/ lab-db / Base de datos MariaDB / 192.168.60.20 / 192.168.1.243 /` |
| INFO | documentacion | 192.168.60.30 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 13 | `/ lab-backup / Backups + Servicios / 192.168.60.30 / 192.168.1.245 /` |
| INFO | documentacion | 192.168.1.245 | `docs\validaciones\Fase_2_validacion_real_laboratorio.md` | 13 | `/ lab-backup / Backups + Servicios / 192.168.60.30 / 192.168.1.245 /` |
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
| MEDIA | codigo_o_recurso | 192.168.60.30 | `config.env.example` | 12 | `SERVICIOS_HOST=192.168.60.30` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `config.env.example` | 13 | `BACKUPS_HOST=192.168.60.30` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `config.env.example` | 14 | `TERMINAL_DATABASE_HOST=192.168.60.20` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `config.env.example` | 18 | `LOGS_DB_HOST=192.168.60.20` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `config.env.example` | 37 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| MEDIA | codigo_o_recurso | 192.168.60.40 | `config.env.example` | 37 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `config.env.example` | 37 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `config.env.example` | 37 | `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.20,192.168.60.30,192.168.60.40` |
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
| MEDIA | codigo_o_recurso | 192.168.60.30 | `deploy\api\package\main.py` | 43 | `SERVIDOR_BACKUPS = os.getenv("BACKUPS_HOST", "192.168.60.30")` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `deploy\api\package\main.py` | 44 | `SERVIDOR_SERVICIOS = os.getenv("SERVICIOS_HOST", "192.168.60.30")` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\api\package\main.py` | 45 | `CACTI_URL = os.getenv("CACTI_URL", "http://127.0.0.1/cacti/")` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `deploy\api\package\main.py` | 47 | `LOGS_DB_HOST = os.getenv("LOGS_DB_HOST", "192.168.60.20")` |
| MEDIA | codigo_o_recurso | 127.0.0.1 | `deploy\api\package\main.py` | 53 | `TERMINAL_MAIN_HOST = os.getenv("TERMINAL_MAIN_HOST", "127.0.0.1")` |
| MEDIA | codigo_o_recurso | 192.168.60.10 | `README.md` | 37 | `/ lab-api / API / Panel / Reverse proxy HTTPS / 192.168.60.10 / 192.168.1.244 /` |
| MEDIA | codigo_o_recurso | 192.168.1.244 | `README.md` | 37 | `/ lab-api / API / Panel / Reverse proxy HTTPS / 192.168.60.10 / 192.168.1.244 /` |
| MEDIA | codigo_o_recurso | 192.168.1.243 | `README.md` | 38 | `/ lab-db / MariaDB / Logs / Datos / 192.168.60.20 / 192.168.1.243 /` |
| MEDIA | codigo_o_recurso | 192.168.60.20 | `README.md` | 38 | `/ lab-db / MariaDB / Logs / Datos / 192.168.60.20 / 192.168.1.243 /` |
| MEDIA | codigo_o_recurso | 192.168.60.30 | `README.md` | 39 | `/ lab-backup / Backups + Servicios / 192.168.60.30 / 192.168.1.245 /` |
| MEDIA | codigo_o_recurso | 192.168.1.245 | `README.md` | 39 | `/ lab-backup / Backups + Servicios / 192.168.60.30 / 192.168.1.245 /` |
| MEDIA | herramienta_producto | 127.0.0.1 | `deploy\api\package\tools\check_api_installation.sh` | 103 | `check_command "Puerto local API responde" "curl -fsSI http://127.0.0.1:8000"` |

## InterpretaciÃ³n inicial

Esta auditorÃ­a no corrige automÃ¡ticamente las IPs.

Sirve para decidir quÃ© referencias deben transformarse en variables de instalaciÃ³n y cuÃ¡les pueden quedarse como documentaciÃ³n de laboratorio.

## PrÃ³ximo paso

Clasificar los hallazgos en:

- A mantener como evidencia histÃ³rica o documentaciÃ³n.
- A convertir en valores de config.env.example.
- A preguntar desde instaladores.
- A derivar segÃºn perfil Lite, PyME 2 servidores o Pro 3 servidores.

## Resultado

Resultado: REVISAR. Hay IPs fijas de severidad ALTA.
