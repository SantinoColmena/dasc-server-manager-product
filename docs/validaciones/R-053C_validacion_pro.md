# R-053C — Validación de instalación desde cero · Perfil Pro (3 VMs)

> **Resultado:** ✅ La instalación Pro desde cero en 3 VMs limpias **funciona** y
> queda operativa sin defectos nuevos. R-053C **CERRADO** (2026-06-07).
>
> Relacionado: [`R-053A`](R-053A_validacion_lite.md) ·
> [`R-053B`](R-053B_validacion_standard.md) ·
> [`R-053D`](R-053D_checklist_instalacion_desde_cero.md).

## 1. Entorno de validación

- **Herramienta:** multipass 1.16.3 (Hyper-V) sobre Windows 11.
- **VMs:**

  | VM | IP | Rol | Recursos |
  |---|---|---|---|
  | `dasc-pro-db` | 172.19.219.190 | MariaDB + BD de logs | 2 vCPU / 4 GiB / 20 GiB |
  | `dasc-pro-backup` | 172.19.220.137 | backup-services | 2 vCPU / 4 GiB / 20 GiB |
  | `dasc-pro-api` | 172.19.213.52 | Panel API | 2 vCPU / **2 GiB** / 20 GiB |

  > La VM de panel se lanzó con 2 GiB por límite de RAM del host de desarrollo
  > (3 × 4 GiB agota la memoria disponible). No afecta a la instalación ni al
  > funcionamiento del panel.

- **Imagen:** Ubuntu 22.04 LTS cloud (misma que R-053A/B).
- **Rama/commit:** `ca049d1` (`docs/roadmap-canonico`), que incluye los fixes B1-B5.
- **Orden de instalación:**
  1. `install_db.sh` → `dasc-pro-db`
  2. `install_backup_services.sh` → `dasc-pro-backup`
  3. `install_dasc_api.sh` → `dasc-pro-api`
- **Método:** no interactivo (variables de entorno + script driver en cada VM).

## 2. Diferencias arquitectónicas respecto a Standard

| Aspecto | Standard | Pro |
|---|---|---|
| Hosts totales | 2 | 3 |
| Panel y backup-services | Mismo host (`127.0.0.1`) | Hosts separados |
| `BACKUPS_HOST` / `SERVICIOS_HOST` | `127.0.0.1` | IP de dasc-pro-backup |
| SSH del panel | Solo hacia dasc-std-db | Hacia dasc-pro-backup **y** dasc-pro-db |
| Backup real | mysqldump desde el host panel | mysqldump vía SSH desde el host panel al backup, que conecta al DB |
| Usuario `dasc` en host panel | Sí (creado por backup-services) | **No** (host panel no tiene backup-services) |

## 3. Defectos encontrados y corregidos

**Ninguno nuevo.** Los fixes B4 y B5 (comprometidos en R-053B) cubren también el
perfil Pro:

- **B4** — `mysqlbinlog` ausente en el host de backup (comportamiento idéntico
  en Pro: `dasc-pro-backup` no tiene `mariadb-server`). El AVISO no bloqueante
  se emite correctamente.
- **B5** — el bucle SSH configura 2 hosts: `dasc-pro-backup` + `dasc-pro-db`.
  Con `unset DASC_PASS` fuera del bucle, la contraseña persiste para ambas
  iteraciones. Validado sin error.

## 4. Observación: transferencia de secretos en Pro

En Standard, el fichero `/root/dasc-db-install-secrets.env` está disponible en el
mismo host donde corren los instaladores siguientes. En Pro, es necesario
**copiar el fichero desde `dasc-pro-db` a `dasc-pro-backup` y a `dasc-pro-api`**
antes de ejecutar sus respectivos instaladores. En este ciclo de validación se
usó Windows como intermediario (`multipass transfer`). Para una instalación
de producción, el operador debe replicar este paso (SCP, Ansible, etc.) o el
instalador debe documentarlo explícitamente. Se anota como mejora de UX
(no bloqueante).

## 5. Verificación funcional (3 VMs tras instalar)

| Check | Resultado |
|---|---|
| Instalación completa (3 instaladores, 3 VMs) | ✅ `Instalación completada`, sin fallos, `EXIT:0` |
| `config.env` — perfil | ✅ `DASC_PROFILE=pro` |
| `config.env` — hosts sin placeholders | ✅ `BACKUPS_HOST=172.19.220.137`, `SERVICIOS_HOST=172.19.220.137`, `LOGS_DB_HOST=172.19.219.190`, `TERMINAL_DATABASE_HOST=172.19.219.190` |
| `DASC_SSH_ALLOWED_HOSTS` | ✅ `127.0.0.1,localhost,172.19.220.137,172.19.219.190` |
| SSH sin contraseña panel→backup (`dasc@172.19.220.137`) | ✅ `hostname=dasc-pro-backup`, `uid=1001(dasc)`, exit 0 |
| SSH sin contraseña panel→db (`dasc@172.19.219.190`) | ✅ `hostname=dasc-pro-db`, `uid=1001(dasc)`, exit 0 |
| Conectividad BD de logs (172.19.219.190) | ✅ `SHOW TABLES → eventos` con credenciales del panel |
| Backup real vía red (Pro) | ✅ Panel SSH→backup→mysqldump→dasc-pro-db → `pro_backup_test.sql.gz` (840 B) |
| Panel HTTP | ✅ `GET /login → 200` |
| Servicios — dasc-pro-api | ✅ `dasc-api` activo |
| Servicios — dasc-pro-db | ✅ `mariadb` activo |
| Scripts — dasc-pro-backup | ✅ `backups_api.sh`, `restore_api.sh`, `servicios_api.sh` en `/usr/local/bin/` |

## 6. Conclusión

El perfil **Pro instala desde cero en 3 VMs limpias y queda completamente
operativo**, sin defectos nuevos respecto a Standard. Los fixes B4 y B5
son suficientes para cubrir la arquitectura distribuida de 3 hosts. El flujo
de backup Pro (panel SSH al host de backup, que conecta directamente al DB
con su `.my.cnf`) funciona correctamente en red real entre VMs separadas.
