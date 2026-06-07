# R-053A — Validación de instalación desde cero · Perfil Lite/single

> **Resultado:** ✅ La instalación Lite desde cero en VM limpia **funciona**, tras
> corregir **4 defectos** que la bloqueaban o la dejaban no funcional. Pendiente
> únicamente validar la **copia externa** obligatoria (F5) para el cierre formal.
>
> Relacionado: [`R-053D_checklist_instalacion_desde_cero.md`](R-053D_checklist_instalacion_desde_cero.md).

## 1. Entorno de validación

- **Herramienta:** multipass 1.16.3 (Hyper-V) sobre Windows 11.
- **VM:** Ubuntu 22.04.5 LTS limpia, 2 vCPU / 4 GiB / 20 GiB.
- **Origen:** snapshot del árbol de trabajo basado en `3f98bca` + los 4 fixes de abajo.
- **Método:** los 3 instaladores ejecutados de forma no interactiva (variables por
  entorno) en este orden — **`db` → `backup-services` → `api`** — sobre un único host.

## 2. Defectos encontrados y corregidos

| ID | Severidad | Defecto | Causa raíz | Fix |
|---|---|---|---|---|
| **B1** | 🔴 Bloqueante | `install_backup_services.sh` desinstalaba `mariadb-server` en single-host y fallaba por `mysqlbinlog` | `default-mysql-client` (MySQL 8.0) entra en conflicto con MariaDB; apt resuelve eliminando el servidor | Preferir `mariadb-client` (convive con el servidor y aporta `mariadb-binlog`); `default-mysql-client` solo como fallback |
| **B2** | 🔴 Bloqueante | Hosts quedaban como placeholder (`IP_SERVIDOR_*`) en todos los perfiles | `config.env.example` usa placeholders **sin** corchetes, pero `is_empty_or_placeholder()` solo reconocía los **con** corchetes | Reconocer ambas formas (+ contraseñas de laboratorio) en `is_empty_or_placeholder()` de `install_dasc_api.sh` |
| **F8** | 🟠 Funcional | El panel no conectaba a la BD de logs (`LOGS_DB_PASS` de laboratorio) | El instalador de la API no importaba los secretos generados por `install_db.sh` | `install_dasc_api.sh` importa `LOGS_DB_*` desde `/root/dasc-db-install-secrets.env` si está presente |
| **B3** | 🔴 Bloqueante (cloud) | `ssh-copy-id` rechazado (`Permission denied (publickey)`); el panel no instalaba su clave | Las imágenes cloud de Ubuntu traen `60-cloudimg-settings.conf` con `PasswordAuthentication no`, que gana al `sshd_config` principal | `install_db.sh` e `install_backup_services.sh` escriben un drop-in `00-dasc-ssh.conf` (se lee primero) con `PasswordAuthentication yes` |

**Ficheros modificados:**
`deploy/backup-services/install_backup_services.sh` (B1, B3) ·
`deploy/api/install_dasc_api.sh` (B2, F8) ·
`deploy/db/install_db.sh` (B3).

> **Nota de seguridad (para R-054).** El fix B3 deja `PasswordAuthentication yes`
> (que ya era la intención de los instaladores). El endurecimiento debe desactivar
> la auth por contraseña **después** del bootstrap de claves, en la fase R-054.

## 3. Verificación funcional (VM tras instalar)

| Check | Resultado |
|---|---|
| Instalación completa (3 instaladores) | ✅ `ALL STEPS DONE`, sin fallos |
| `config.env` final | ✅ hosts `127.0.0.1`; `DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost` (sin placeholders) |
| Conexión BD de logs con credenciales del panel | ✅ `SHOW TABLES` → `eventos` |
| SSH sin contraseña (clave panel → `dasc@127.0.0.1`) | ✅ ejecuta como `dasc` en `dasc-lite` |
| Scripts admin instalados | ✅ `backups_api.sh`, `restore_api.sh`, `servicios_api.sh` |
| Backup real (`mysqldump` con `.my.cnf` configurado) | ✅ `verify_employees.sql.gz` generado |
| Panel HTTP | ✅ `GET / → 303`, `GET /login → 200` |
| Servicios systemd | ✅ `dasc-api`, `mariadb`, `ssh`, `cron` activos |

## 4. Pendiente para el cierre formal de R-053A

- [ ] **F5 — Copia externa obligatoria.** El perfil Lite exige copia externa
      (`EXTERNAL_BACKUP_REQUIRED=yes`) pero el instalador la deja deshabilitada.
      Falta validar `sync_external_backup.sh` contra un destino externo (p. ej.
      `/mnt/dasc-external` montado en la VM).
- [ ] Commitear los 4 fixes en la rama y dejar `check_api_package_installable.ps1`
      en verde.

## 5. Conclusión

El perfil **Lite instala desde cero y queda operativo** en VM limpia, una vez
aplicados B1, B2, F8 y B3. La validación cumplió su objetivo: detectó defectos
reales (incluido uno que afecta a cualquier despliegue en VPS cloud — B3) que no
eran visibles sin una instalación real desde cero.
