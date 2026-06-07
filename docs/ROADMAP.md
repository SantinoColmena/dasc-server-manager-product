# Hoja de ruta — DASC Server Manager

> **Fuente de verdad única.** Este documento es el roadmap canónico del producto.
> El Excel (`docs/roadmap/DASC_Roadmap.xlsx`) es una **vista derivada** que se
> genera a partir de esta información; nunca al revés. Si algo cambia, se cambia
> aquí, en el mismo commit que el trabajo, para que el plan no vuelva a
> desincronizarse del código.

- **Versión actual:** `v1.0-rc1`
- **Fase actual:** Fase 6 — Endurecimiento y producto vendible
- **Última actualización:** 2026-06-07

---

## 1. Cómo leer este roadmap

La jerarquía es **una sola**, sin duplicar conceptos:

```
Fase            → momento del producto (dónde estamos en su ciclo de vida)
 └─ Ruta        → línea temática de trabajo dentro de la fase
     └─ Tarea   → requisito concreto, identificado con R-xxx
         └─ Gate → criterio de salida real (F6-GATE-xx) que cierra un bloque
```

**Reglas fijas de numeración** (para no repetir el desorden anterior):

1. `R-xxx` es un identificador **monótono y único**: una vez asignado, **no se
   reutiliza** ni se renumera. Las sub-tareas usan sufijo de letra (`R-049A`,
   `R-049B`…), que ya es la convención del repo.
2. Los **gates** usan el prefijo de la fase (`F6-GATE-06`). Son criterios de
   salida concretos y verificables, **no** texto genérico.
3. El **estado** se ancla a evidencia real en `docs/validaciones/`. "Cerrada"
   significa que existe su cierre validado, no que "debería estar hecha".
4. **Sin fechas fijas.** Se usan horizontes (`Ahora` / `Siguiente` / `Después`)
   porque el avance real va por delante de cualquier calendario.

**Estados:** `Cerrada` ✅ · `En curso` 🔵 · `Siguiente` ▶️ · `Planificada` 🗓️ ·
`Backlog` 📦 · `Aplazada` ⏸️ · `Diferida` 🕓

---

## 2. Estado global de un vistazo

| Fase | Nombre | Rango | Estado | Horizonte |
|---|---|---|---|---|
| 0 | Preparación | R-001 → R-005 | ✅ Cerrada | — |
| 1 | Núcleo estable | R-006 → R-014 | ✅ Cerrada | — |
| 2 | Seguridad y restauración | R-015 → R-024 | ✅ Cerrada | — |
| 3 | Despliegues adaptables | R-025 → R-031 | ✅ Cerrada | — |
| 4 | Demo y validación | R-032 → R-039 | ✅ Cerrada | — |
| 5 | Pilotos reales y RC | R-040 → R-047 | ✅ Cerrada | — |
| **6** | **Endurecimiento y producto vendible** | **R-048 → R-057** | 🔵 **En curso** | **Ahora** |
| 7 | Central cloud y multi-cliente | R-058 → R-070 (aprox.) | 🗓️ Planificada | Siguiente |
| 8 | Comercial y escalado | (se numera al planificar) | 📦 Backlog | Después |
| 9 | Evolución (IA, Windows, refactor) | (se numera al planificar) | 📦 Backlog | Después |

**Próximos objetivos concretos** (lo que dicta el propio repo, en orden):

1. ~~**R-053** — Validación de instalación desde cero por perfil (VM limpia).~~ ✅ Cerrado 2026-06-07.
2. ~~**R-054** — Cierre del endurecimiento de infraestructura: UFW, HTTPS/certbot, fail2ban, `pip-audit`.~~ ✅ Cerrado 2026-06-07.
3. **R-055 / R-056** — Guía de uso desde Windows + limpieza final del repo y la documentación.
4. **R-057** — Release interna estable (freeze) → y recién entonces retomar **R-048** (primer cliente de pago).

---

## 3. Fases cerradas (resumen)

> Detalle completo y validaciones en `docs/validaciones/`. Aquí solo el resumen,
> porque están cerradas y documentadas.

### Fase 0 — Preparación · ✅ `R-001 → R-005`
Separación del proyecto académico, propuesta de valor, paquetes Lite/PyME/Pro,
inventario de código y límites de responsabilidad del servicio.

### Fase 1 — Núcleo estable · ✅ `R-006 → R-014`
Configuración por perfiles, instalador idempotente, motor de backups centralizado
con historial y programación automática, logs internos, limpieza de UX,
laboratorio reproducible y versión interna 0.1.

### Fase 2 — Seguridad y restauración · ✅ `R-015 → R-024`
Hash de contraseñas, protección de `config.env`, HTTPS/reverse proxy, endurecimiento
de SSH y comandos remotos (allowlist), restauración controlada, integridad y
retención de backups, alertas de fallo y de disco, versión interna 0.2.

### Fase 3 — Despliegues adaptables · ✅ `R-025 → R-031`
Perfiles 1/2/3 servidores, NAS/SFTP como destino, copia externa cifrada (GPG),
asistente de instalación por perfil y documentación de arquitecturas.

### Fase 4 — Demo y validación · ✅ `R-032 → R-039`
Modo demo sin datos sensibles, dominio + web mínima, manual rápido de cliente,
base de conocimiento inicial, lista de 30 prospectos, guion de demo, checklist de
instalación y selección del primer piloto técnico.

### Fase 5 — Pilotos reales y Release Candidate · ✅ `R-040 → R-047`
Piloto 1 (2 servidores), medición y corrección de incidencias, piloto 2 (1
servidor + externo), piloto 3 opcional, SLA realista, recálculo de costes reales
y **publicación de `v1.0-rc1`** (R-047).

---

## 4. Fase 6 — Endurecimiento y producto vendible · 🔵 EN CURSO

> **Objetivo de la fase:** dejar el producto limpio, seguro, instalable desde
> cero y honesto (sin prometer lo que no existe) **antes** de cerrar ventas
> reales. Decisión registrada en
> [`docs/planificacion/fase6_reordenacion_antes_de_ventas.md`](planificacion/fase6_reordenacion_antes_de_ventas.md):
> calidad antes que velocidad comercial.

### Rutas cerradas de Fase 6

| Ruta | Tareas | Estado | Evidencia |
|---|---|---|---|
| 6.1 Soporte central/local | `R-049A → R-049Y` | ✅ Cerrada | `docs/validaciones/R-049*`, `F6-GATE-05*` |
| 6.2 Operación e informes | `R-050` Informe mensual v1 | ✅ Cerrada | `R-050_cierre_informe_mensual_v1.md` |
| 6.3 Despliegue cliente | `R-050B` Nginx panel local *(ver nota)* | ✅ Cerrada | `R-050_cierre_nginx_panel_local_cliente.md` |
| 6.4 Instaladores adaptables (sin IPs fijas) | `R-051 → R-051H` | ✅ Cerrada | `R-051H_cierre_global_instaladores_adaptables.md`, `F6-GATE-04*` |
| 6.5 Seguridad de infraestructura | `R-052 → R-052H` | ✅ Cerrada | `R-052H_cierre_global_revision_seguridad.md` |
| 6.6 Auditoría de seguridad de código *(extiende R-052)* | `H-1, M-1…M-5, L-1…L-6` | ✅ Cerrada | `docs/auditoria/auditoria_codigo_aplicacion_seguridad.md` |

**Gates cerrados de Fase 6:** `F6-GATE-01` (instalación API Ubuntu) ·
`F6-GATE-02` (API + DB/logs 2 servidores) · `F6-GATE-03` (backup completo +
restauración) · `F6-GATE-04` (instaladores y perfiles) · `F6-GATE-05`
(soporte central/local). Todos con su cierre en `docs/validaciones/`.

> **Nota de numeración (corrección de colisión).** En el repo `R-050` se usó para
> **dos** trabajos distintos: "informe mensual v1" y "nginx panel local". Para
> respetar la regla de unicidad sin renumerar lo cerrado, en este roadmap el panel
> Nginx pasa a llamarse **`R-050B`**. Los ficheros existentes
> `docs/validaciones/R-050_*nginx*` se mantienen; solo se renombrará su referencia
> conceptual aquí. Es la única colisión histórica y queda resuelta.

### Rutas abiertas de Fase 6 (lo que viene)

> **Convención de subrutas.** Cuando una tarea `R-xxx` resulta más grande de lo
> previsto, se desglosa en subrutas con sufijo de letra (`R-xxxA`, `R-xxxB`…),
> cada una con su validación/cierre en `docs/validaciones/`. Las subrutas
> listadas abajo en estado 🗓️ son una **previsión razonable de calidad**: se
> confirman o ajustan al entrar en cada tarea. Así el plan absorbe lo que vaya
> surgiendo sin romper la numeración ni inflar el roadmap por adelantado.

#### Ruta 6.7 — Validación de instalación desde cero · ✅ Cerrada (Lite ✅ Standard ✅ Pro ✅)
- **R-053** ✅ — Instalar DASC en VM limpia por cada perfil, sin pasos manuales
  ocultos, partiendo del repo/tag. *Depende de:* H-1 y M/L de la auditoría (✅).
  **Cerrada 2026-06-07** — los 3 perfiles validados en VMs limpias, 5 defectos
  corregidos (B1-B5). Evidencia en `docs/validaciones/R-053A/B/C/D_*`.
  - `R-053A` ✅ — Validación perfil **Lite** (1 servidor + copia externa).
    Instalación desde cero **funcional** en VM limpia (multipass/Ubuntu 22.04)
    tras corregir 4 defectos: **B1** (backup-services desinstalaba MariaDB en
    single-host), **B2** (hosts quedaban como placeholder en todos los perfiles),
    **F8** (credenciales de logs sin importar) y **B3** (drop-in SSH de imágenes
    cloud bloqueaba el bootstrap de clave del panel). F5 (copia externa): validada
    con `sync_external_backup.sh` tipo `local`, exit 0. **Cerrada 2026-06-07.**
    Evidencia: `docs/validaciones/R-053A_validacion_lite.md`.
  - `R-053B` ✅ — Validación perfil **Standard** (2 servidores).
    Instalación desde cero en 2 VMs limpias (dasc-std-db + dasc-std-api) completamente
    funcional tras corregir 2 defectos: **B4** (`mysqlbinlog` ausente en host backup
    Standard/Pro — convertido a AVISO no bloqueante) y **B5** (`unset DASC_PASS`
    dentro del bucle SSH multi-host causaba salida silenciosa del installer con
    `set -euo pipefail`). SSH sin contraseña panel→DB, BD logs, backup real vía red
    y HTTP 200 verificados. **Cerrada 2026-06-07.**
    Evidencia: `docs/validaciones/R-053B_validacion_standard.md`.
  - `R-053C` ✅ — Validación perfil **Pro** (3 servidores).
    Instalación desde cero en 3 VMs limpias (dasc-pro-db + dasc-pro-backup +
    dasc-pro-api) completamente funcional sin defectos nuevos. Los fixes B4 y B5
    de R-053B cubren también el perfil Pro. SSH sin contraseña a 2 hosts remotos,
    backup real vía SSH panel→backup→db y HTTP 200 verificados. **Cerrada 2026-06-07.**
    Evidencia: `docs/validaciones/R-053C_validacion_pro.md`.
  - `R-053D` 🔵 — Checklist reproducible + informe consolidado por perfil
    (creado: `docs/validaciones/R-053D_checklist_instalacion_desde_cero.md`).

#### Ruta 6.8 — Cierre de endurecimiento de infraestructura · ✅ Cerrada
> Pendientes explícitamente listados en `R-052H` y en la auditoría de código.
- **R-054** ✅ — Endurecimiento de infraestructura completado. **CERRADO 2026-06-07**.
  Evidencia: `docs/validaciones/R-054_validacion_endurecimiento.md`.
  - `R-054A` ✅ — **UFW** por host: `harden_ufw_api.sh`, `harden_ufw_db.sh`, `harden_ufw_backup.sh`.
  - `R-054B` ✅ — **HTTPS** (autofirmado) + certbot (opcional) + `DASC_SESSION_HTTPS_ONLY=true` activado.
  - `R-054C` ✅ — **fail2ban**: jaulas `sshd` + `dasc-auth`; filtro DASC validado con `fail2ban-regex`.
  - `R-054D` ✅ — **`pip-audit`**: `starlette→1.0.1`, `python-multipart→0.0.27`; ambos paquetes limpios.

#### Ruta 6.9 — Experiencia Windows y limpieza final · 🗓️ Planificada
> Bloques 1 y 2 del plan de reordenación de Fase 6.
- **R-055** — Guía de uso desde Windows.
  - `R-055A` 🗓️ — Acceso **por navegador**: qué puede hacer el cliente.
  - `R-055B` 🗓️ — Despliegue real en **Linux** desde un PC Windows.
  - `R-055C` 🗓️ — Valorar **script auxiliar** Windows vs. solo documentación.
- **R-056** — Limpieza final del repo y la documentación.
  - `R-056A` 🗓️ — Revisión de estructura de carpetas y README.
  - `R-056B` 🗓️ — Revisión de docs duplicadas / demasiado comerciales.
  - `R-056C` 🗓️ — Verificar que **nada promete funciones no implementadas**.
  - `R-056D` 🗓️ — Barrido final de secretos / ejemplos / `config`.

#### Ruta 6.10 — Release interna estable · 🗓️ Planificada
- **R-057** — Congelar release interna estable consolidada. Corte antes de lo
  comercial.
  - `R-057A` 🗓️ — Checklist maestro de regresión.
  - `R-057B` 🗓️ — Changelog consolidado.
  - `R-057C` 🗓️ — Smoke tests básicos (script).
  - `R-057D` 🗓️ — Congelado del tag + validación instalable.

### 🚪 Gate de salida de Fase 6 — `F6-GATE-06` "Producto vendible"
**No se pasa a actividad comercial real hasta cumplir TODO esto:**
- [x] Instalación desde cero OK en los 3 perfiles (R-053). ✅ Cerrado 2026-06-07.
- [x] UFW + HTTPS + fail2ban + `pip-audit` aplicados (R-054). ✅ Cerrado 2026-06-07.
- [ ] Documentado el uso desde Windows / navegador vs. Linux (R-055).
- [ ] Repo y docs limpios, sin promesas de funciones inexistentes (R-056).
- [ ] Release interna estable congelada con changelog (R-057).
- [ ] `check_api_package_installable.ps1` y `check_repo_clean.ps1` en verde.

### Cierre comercial de la fase
- **R-048** — Primer cliente de pago. ⏸️ **Aplazada a propósito** hasta superar
  `F6-GATE-06`. No se cierra sin un cliente real de pago o feedback comercial
  real documentado.

---

## 5. Fase 7 — Central cloud y multi-cliente · 🗓️ PLANIFICADA

> **Objetivo:** convertir DASC en producto multi-cliente de verdad: una Central
> propia (VPS DASC) que agregue el estado de todas las instalaciones. Detalle
> medio; cada tarea se afina al entrar en la fase. Rango orientativo
> `R-058 → R-070`.

| Ruta | Contenido | Estado |
|---|---|---|
| 7.1 Diseño central cloud | Arquitectura de la Central en VPS, modelo HTTPS, topología | 🗓️ Planificada |
| 7.2 Central VPS + HTTPS productivo | Despliegue real de Central Support con dominio + TLS + Nginx | 🗓️ Planificada |
| 7.3 Panel multi-cliente | Gestión de clientes, tokens por cliente, rotación y revocación | 🗓️ Planificada |
| 7.4 Dashboard de salud | Heartbeat de instalaciones: último backup, alertas, soporte, último contacto | 🗓️ Planificada |
| 7.5 Seguridad central | 2FA para el equipo DASC, backup de la propia Central, auditoría de login central | 🗓️ Planificada |

**Gate de salida `F7-GATE` "Central productiva":** Central accesible por HTTPS,
al menos 1 instalación reportando estado real, tokens gestionables y backup de la
Central verificado.

---

## 6. Fase 8 — Comercial y escalado · 📦 BACKLOG (objetivos gruesos)

> Se desglosa en tareas `R-xxx` solo cuando se planifique. Aquí, los objetivos.

- **Oferta y onboarding** listos (paquetes finales Lite/Standard/Pro, precios,
  proceso de alta del cliente).
- **SLA y legal** definitivos (tiempos de respuesta, exclusiones, condiciones de
  servicio).
- **Pilotos pagados** (1 y 2) ejecutados y feedback aplicado.
- **Marketing** mínimo (web actualizada, material comercial honesto).
- **Release v1.0 comercial limitada** — solo si los pilotos y la seguridad pasan.
- **Decisión Go/No-Go comercial** documentada (puede ser No-Go).

---

## 7. Fase 9 — Evolución · 📦 BACKLOG (objetivos gruesos)

- **IA de soporte / diagnóstico interno** (ayuda al técnico: resumen de logs y
  sugerencias; no sustituye al humano).
- **Agente Windows** (servicio que reporta estado / backup de carpetas).
- **Refactor de `main.py`** (deuda L-6 de la auditoría: ~5000 líneas en un
  fichero). 🕓 Diferida con justificación.
- **Integraciones / API de producto** y **observabilidad avanzada**.
- **Migración de la Central de SQLite a PostgreSQL/MariaDB** si crece el número de
  clientes.

---

## 8. Perfiles de despliegue (referencia)

| Perfil | Arquitectura | Uso recomendado | Decisión |
|---|---|---|---|
| **Lite** | 1 servidor + copia externa **obligatoria** | PyME muy pequeña / laboratorio | No vender sin copia externa real |
| **Standard** | 2 servidores (panel/API + DB/backups) | **Objetivo inicial** PyME | Perfil objetivo de las primeras ventas |
| **Pro** | 3 servidores (API / DB-logs / backups) | Cliente con más criticidad | No priorizar antes de Standard estable |
| **Central DASC** | VPS propio del equipo DASC | Equipo DASC (multi-cliente) | Clave para producto real (Fase 7) |

---

## 9. Registro de decisiones de roadmap

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-06-06 | `ROADMAP.md` pasa a ser la **fuente de verdad única**; el Excel es vista derivada | Los 3 Excel previos se desincronizaron del repo |
| 2026-06-06 | Se **congela la numeración real del repo** (R-001…R-052x); no se renumera lo existente | Mínimo cambio, no romper referencias en `docs/` y commits |
| 2026-06-06 | Colisión de `R-050` resuelta: Nginx panel local → **`R-050B`** | `R-050` se había usado para dos trabajos distintos |
| 2026-06-06 | Fase 6 redefinida como "Endurecimiento y producto vendible"; ventas (R-048) al final | Calidad antes que velocidad comercial (plan de reordenación) |
| 2026-06-06 | Se detalla solo Fase 6–7; Fase 8–9 quedan como backlog grueso | Evitar el churn de planificar 2028 al detalle |
| 2026-06-06 | Gates: se mantiene la convención real `F6-GATE-xx`; se descartan los `G-00…G-36` genéricos del Excel integral | Eran texto de relleno idéntico, sin criterio real |

---

> **Origen.** Este roadmap consolida y reemplaza a los tres Excel previos
> (`DASC_Roadmap_Producto_Tracker`, `DASC_Roadmap_Fase6_v2`,
> `DASC_Roadmap_Integral_R001_R140`), tomando de cada uno lo válido y anclándolo
> al estado real del repositorio.
