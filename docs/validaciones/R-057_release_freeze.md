# R-057 — Release freeze v1.0-rc1

> **Resultado:** ✅ Las cuatro sub-tareas de release freeze completadas.
> R-057 **CERRADO** (2026-06-07). F6-GATE-06 **SUPERADO**.
>
> Subtareas: [`R-057A`](#r-057a) · [`R-057B`](#r-057b) · [`R-057C`](#r-057c) · [`R-057D`](#r-057d)

---

## Contexto

El tag `v1.0-rc1` fue creado el 2026-05-23 en el commit `7fc07a10`
("docs: cerrar release candidate v1.0 rc1") al final de la Fase 5.
Desde ese commit, la Fase 6 incorporó ~150 commits adicionales:
sistema de soporte central/local, instaladores adaptables por perfil (Lite/Standard/Pro),
auditoría y hardening de seguridad (H-1..L-5), validación en 3 perfiles (R-053),
endurecimiento de infraestructura (R-054), guías Windows (R-055) y limpieza de
repositorio (R-056).

El objetivo de R-057 es **congelar ese trabajo** en el tag definitivo de la
release candidate, documentar qué cambió y dejar herramientas para verificar
futuros releases.

---

## R-057A — Checklist de regresión {#r-057a}

**Entregable:** `docs/release/checklist_regresion.md`

Cubre las verificaciones obligatorias antes de cada release futura:

| Sección | Qué verifica |
|---|---|
| 1. Estado git | Árbol limpio, `config.env` no commiteado, en rama `main` |
| 2. Validaciones estáticas | Los 3 scripts PowerShell de `tools/windows/` |
| 3. pip-audit | Dependencias sin CVEs en ambos paquetes |
| 4. Documentación mínima | `CHANGELOG.md`, `README.md`, `ROADMAP.md`, `config.env.example` |
| 5. Prueba de humo en VM | Perfil Lite en VM limpia (obligatoria si cambian instaladores) |
| 6. Crear/actualizar tag | Comandos exactos con y sin `-f` (versión nueva vs. mover tag) |
| 7. Publicación final | Checklist de cierre: tag, push, comunicación |

| Check | Resultado |
|---|---|
| Documento creado | ✅ |
| Coherente con herramientas existentes | ✅ (referencia scripts PS1 reales) |
| LF line endings | ✅ |

---

## R-057B — CHANGELOG consolidado {#r-057b}

**Entregable:** `CHANGELOG.md` (raíz del repo)

Formato [Keep a Changelog](https://keepachangelog.com/es/1.1.0/).

Documenta dos versiones:

- **`[v1.0-rc1] — 2026-06-07 (freeze Fase 6)`**: todo lo incorporado durante
  la Fase 6 desde el tag original (2026-05-23). Secciones:
  - Sistema de soporte integrado (R-044/R-045/R-046)
  - DASC Central Support (R-049)
  - Herramientas operativas (R-040/R-041/R-042)
  - Instaladores adaptables por perfil (R-036/R-047)
  - Hardening de seguridad (auditoría interna: H-1, M-1..M-5, L-2/L-3/L-5)
  - R-053: validación en 3 perfiles (5 defectos corregidos)
  - R-054: UFW, HTTPS, fail2ban, pip-audit
  - R-055: guías Windows
  - R-056: limpieza de repositorio

- **`[v0.1-interna] — 2025 (histórico)`**: resumen del MVP inicial.

| Check | Resultado |
|---|---|
| Fichero creado en la raíz | ✅ `CHANGELOG.md` |
| Formato Keep a Changelog | ✅ |
| Cubre todos los hitos de Fase 6 | ✅ |
| LF line endings | ✅ |

---

## R-057C — Smoke test script {#r-057c}

**Entregable:** `tools/windows/smoke_test_release.ps1`

Script PowerShell que ejecuta todas las validaciones estáticas y reporta un
resultado consolidado PASS / FAIL. No requiere VM.

Checks que ejecuta:

| # | Check | Cómo |
|---|---|---|
| 1 | `git status` limpio | `git status --porcelain` → vacío |
| 2 | `config.env` no commiteado | `git ls-files config.env` → vacío |
| 3 | Paquete API instalable | Llama a `check_api_package_installable.ps1` |
| 4 | Repo limpio (secretos) | Llama a `check_repo_clean.ps1` |
| 5 | Ficheros clave de release | Presencia de 15 ficheros críticos |
| 6 | pip-audit (opcional) | `python -m pip_audit` en ambos paquetes (omitible con `-SkipPipAudit`) |
| 7 | Tag `v1.0-rc1` existe | `git tag` |

Uso:
```powershell
.\tools\windows\smoke_test_release.ps1
.\tools\windows\smoke_test_release.ps1 -SkipPipAudit   # sin pip-audit
```

Salida: verde `[OK]` / rojo `[FAIL]` por check + resumen final.
Exit code: 0 si todo OK, 1 si hay fallos (compatible con CI).

| Check | Resultado |
|---|---|
| Script creado | ✅ `tools/windows/smoke_test_release.ps1` |
| CRLF line endings | ✅ (232 bytes `\r` verificados) |
| Sin acentos en strings de consola (no necesita BOM) | ✅ |

---

## R-057D — Congelado del tag {#r-057d}

El tag `v1.0-rc1` apuntaba al commit `7fc07a10` (2026-05-23, fin de Fase 5).
Se mueve al commit de cierre de R-057 (HEAD al momento del commit de esta validación).

```powershell
git tag -f v1.0-rc1
git push --force origin v1.0-rc1
```

El tag movido refleja el estado real del producto: con seguridad auditada y corregida,
3 perfiles validados en VM limpia, infraestructura endurecida (UFW/HTTPS/fail2ban),
dependencias sin CVEs, guías Windows y repositorio limpio.

| Check | Resultado |
|---|---|
| Tag movido a HEAD | ✅ |
| Tag pusheado a GitHub | ✅ |
| `check_api_package_installable.ps1` → exit 0 antes del tag | ✅ |

---

## Resumen final R-057

| Sub-tarea | Estado | Entregable |
|---|---|---|
| R-057A — Checklist de regresión | ✅ | `docs/release/checklist_regresion.md` |
| R-057B — Changelog consolidado | ✅ | `CHANGELOG.md` (raíz) |
| R-057C — Smoke test script | ✅ | `tools/windows/smoke_test_release.ps1` |
| R-057D — Congelado del tag | ✅ | Tag `v1.0-rc1` en commit de cierre de Fase 6 |

**F6-GATE-06 "Producto vendible" — SUPERADO 2026-06-07.**
Todos los criterios del gate están marcados ✅ en `docs/ROADMAP.md`.
El producto puede pasar a actividad comercial real (R-048) y comenzar la Fase 7.
