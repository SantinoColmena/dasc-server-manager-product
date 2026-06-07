# Checklist de regresión — DASC Server Manager

> **Propósito:** Verificaciones obligatorias antes de crear o actualizar cualquier tag
> de versión. Ejecutar siempre desde la raíz del repositorio en el PC de desarrollo.
>
> Tiempo estimado: ~15 min (estático) + ~45 min (VM, si aplica).

---

## 1. Estado del repositorio git

```powershell
git status            # debe ser "nothing to commit, working tree clean"
git log --oneline -3  # confirmar que HEAD es el commit esperado
git branch            # confirmar que estamos en main
```

| Criterio | OK si… |
|---|---|
| Sin cambios sin commitear | `git status` → árbol limpio |
| Sin `config.env` real | No aparece en `git ls-files config.env` |
| En rama `main` | `git branch` muestra `* main` |

---

## 2. Validaciones estáticas (PowerShell, obligatorias)

Desde la raíz del repositorio:

```powershell
.\tools\windows\check_repo_clean.ps1
.\tools\windows\check_api_package_installable.ps1
.\tools\windows\audit_fixed_ips.ps1
```

| Script | Criterio de éxito |
|---|---|
| `check_repo_clean.ps1` | Sin ficheros sensibles commiteados; sin secretos |
| `check_api_package_installable.ps1` | Exit code 0; todos los checks en verde |
| `audit_fixed_ips.ps1` | Sin IPs de laboratorio en instaladores de producción |

> `check_api_package_installable.ps1` falla con exit 1 si detecta cualquier problema
> crítico (CRLF en scripts `.sh`, fichero faltante, `config.env` real incluido).

---

## 3. Auditoría de dependencias Python

```powershell
python -m pip install pip-audit --quiet
python -m pip_audit -r deploy\api\package\requirements.txt
python -m pip_audit -r deploy\central-support\package\requirements.txt
```

**Criterio:** `No known vulnerabilities found` en ambos paquetes.

Si hay CVEs nuevos: actualizar las versiones afectadas en `requirements.txt`,
comentar con el ID del CVE y volver a ejecutar hasta que esté limpio.

---

## 4. Verificación de documentación mínima

| Fichero | Qué comprobar |
|---|---|
| `README.md` | Estado de hitos actualizado; sin módulos prometidos que no existan |
| `CHANGELOG.md` | Entrada para la versión que se va a publicar |
| `docs/ROADMAP.md` | Todos los requisitos del sprint marcados ✅ |
| `config.env.example` | Sin credenciales reales; refleja las variables actuales |
| `config/perfiles/` | Plantillas de perfil coherentes con los instaladores |
| `deploy/api/package/requirements.txt` | Versiones fijadas y comentadas donde proceda |

---

## 5. Prueba de humo en VM (obligatoria si cambian instaladores o requirements)

Aplica siempre que haya modificaciones en:
- `deploy/*/install_*.sh` o `deploy/*/harden_*.sh`
- `deploy/api/package/requirements.txt`
- `deploy/api/package/main.py`

### 5.1 Preparar VM

```powershell
multipass launch 22.04 --name dasc-smoke --cpus 2 --memory 4G --disk 20G
git archive --format=tar.gz -o C:\Temp\dasc-src.tgz HEAD
multipass transfer C:\Temp\dasc-src.tgz dasc-smoke:/home/ubuntu/dasc-src.tgz
multipass exec dasc-smoke -- bash -c "mkdir -p ~/dasc && tar xzf ~/dasc-src.tgz -C ~/dasc"
```

### 5.2 Instalar perfil Lite (mínimo exigible)

```bash
# En la VM (multipass shell dasc-smoke):
cd ~/dasc/deploy/db
sudo -E DASC_PROFILE=lite APP_PASSWORD='Test1234' \
    BACKUP_ALLOWED_HOST=127.0.0.1 LOGS_ALLOWED_HOST=127.0.0.1 \
    bash install_db.sh

cd ~/dasc/deploy/backup-services
sudo -E DASC_PROFILE=lite APP_PASSWORD='Test1234' bash install_backup_services.sh

cd ~/dasc/deploy/api
sudo -E DASC_PROFILE=lite ADMIN_PASSWORD_INPUT='Admin1234' \
    DASC_PASS='Test1234' bash install_dasc_api.sh </dev/null

cd ~/dasc/deploy/proxy
sudo bash install_reverse_proxy.sh

cd ~/dasc/deploy/api
sudo bash harden_ufw_api.sh
sudo bash harden_fail2ban_api.sh
```

### 5.3 Verificar servicios

```bash
systemctl is-active dasc-api mariadb nginx fail2ban
# → active active active active

curl -sk https://127.0.0.1 -o /dev/null -w "%{http_code}"
# → 200 o 303 (login redirect)
```

### 5.4 Verificar circuito backup

1. Login en el panel (`https://<IP>`).
2. Lanzar backup completo desde `/backups`.
3. Confirmar estado "Completado" e integridad SHA256 en la vista de historial.
4. Restaurar el backup y verificar que los ficheros existen en destino.

### 5.5 Limpiar VM

```powershell
multipass delete dasc-smoke
multipass purge
```

---

## 6. Crear o actualizar el tag de versión

Solo ejecutar si **todos** los pasos anteriores están en verde:

```powershell
# Actualizar tag existente al commit actual:
git tag -f v1.0-rc1
git push --force origin v1.0-rc1

# Crear nuevo tag para una versión diferente:
git tag -a v1.1-rc1 -m "release: v1.1-rc1"
git push origin v1.1-rc1
```

---

## 7. Checklist de publicación final

- [ ] `git status` limpio antes del tag.
- [ ] `check_api_package_installable.ps1` → exit 0.
- [ ] `check_repo_clean.ps1` → sin hallazgos críticos.
- [ ] `pip-audit` limpio en ambos paquetes.
- [ ] `CHANGELOG.md` actualizado.
- [ ] `README.md` refleja el nuevo estado.
- [ ] `docs/ROADMAP.md` → sprint cerrado.
- [ ] Tag creado/movido y pusheado a GitHub.
- [ ] VM de humo destruida.
- [ ] (Opcional) Comunicación a clientes/resellers si hay cambios que les afecten.
