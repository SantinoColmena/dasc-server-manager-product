# Hoja de ruta — Vigex

> **Fuente de verdad única.** Este documento es el roadmap canónico del producto.
> El Excel (`docs/roadmap/Vigex_Roadmap.xlsx`) es una **vista derivada** que se
> genera a partir de esta información; nunca al revés. Si algo cambia, se cambia
> aquí, en el mismo commit que el trabajo, para que el plan no vuelva a
> desincronizarse del código.

- **Versión actual:** `v1.0-rc1`
- **Fase actual:** Fase 13 — Cumplimiento y evidencias automáticas (nueva dirección
  estratégica; Fases 7+8 cerradas, 9–12 con acción pendiente del usuario)
- **Última actualización:** 2026-06-11

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
| **6** | **Endurecimiento y producto vendible** | **R-048 → R-057** | ✅ **Cerrada** | **—** |
| **7** | **Madurez del producto** | **R-058 → R-064 (aprox.)** | 🔵 **En curso** | **Ahora** |
| **8** | **Madurez operacional** | **R-065 → R-071 (aprox.)** | ▶️ Siguiente | Siguiente |
| **9** | **Infraestructura de negocio** | **R-072 → R-078 (aprox.)** | ▶️ Siguiente | Siguiente |
| **10** | **Central cloud y multi-cliente** | **R-077 → R-083 (aprox.)** | 🟡 **En curso (acción pendiente del usuario)** | **Ahora** |
| 11 | Comercial y escalado | (se numera al planificar) | 🟡 En curso (acción pendiente del usuario) | Después |
| 12 | Evolución (IA avanzada, Windows GUI, refactor) | (se numera al planificar) | 🟡 En curso (parcial) | Después |
| **13** | **Cumplimiento y evidencias automáticas (NIS2/ENS/ISO 27001)** | **R-091 → R-096 (aprox.)** | ▶️ **Siguiente (nueva dirección)** | **Ahora** |

**Próximos objetivos concretos** (lo que dicta el propio repo, en orden):

1. ~~**R-053 → R-057** — Fases de validación, hardening, guías y freeze.~~ ✅ Todas cerradas 2026-06-07.
2. ~~**Fase 7** — Madurez del producto.~~ ✅ Cerrada 2026-06-08.
3. ~~**Fase 8** — Madurez operacional.~~ ✅ Cerrada 2026-06-08.
4. **Ahora — Fase 13 (nueva dirección):** Cumplimiento y evidencias automáticas
   (NIS2/ENS/ISO 27001) como diferenciador comercial. Ancla estratégica en
   [`docs/estrategia/direccion_cumplimiento_nis2.md`](estrategia/direccion_cumplimiento_nis2.md).
5. **En paralelo (acción del usuario) — Fases 9–11:** dominio + email, web/precios,
   Stripe y legal. Prerrequisito de cualquier venta, con cumplimiento o sin él.
6. **Gate F9-GATE + F13-GATE superados → R-048:** Primer cliente de pago real,
   ya con el diferenciador de cumplimiento.

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
- **R-053** ✅ — Instalar Vigex en VM limpia por cada perfil, sin pasos manuales
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
    Instalación desde cero en 2 VMs limpias (vigex-std-db + vigex-std-api) completamente
    funcional tras corregir 2 defectos: **B4** (`mysqlbinlog` ausente en host backup
    Standard/Pro — convertido a AVISO no bloqueante) y **B5** (`unset Vigex_PASS`
    dentro del bucle SSH multi-host causaba salida silenciosa del installer con
    `set -euo pipefail`). SSH sin contraseña panel→DB, BD logs, backup real vía red
    y HTTP 200 verificados. **Cerrada 2026-06-07.**
    Evidencia: `docs/validaciones/R-053B_validacion_standard.md`.
  - `R-053C` ✅ — Validación perfil **Pro** (3 servidores).
    Instalación desde cero en 3 VMs limpias (vigex-pro-db + vigex-pro-backup +
    vigex-pro-api) completamente funcional sin defectos nuevos. Los fixes B4 y B5
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
  - `R-054B` ✅ — **HTTPS** (autofirmado) + certbot (opcional) + `VIGEX_SESSION_HTTPS_ONLY=true` activado.
  - `R-054C` ✅ — **fail2ban**: jaulas `sshd` + `vigex-auth`; filtro Vigex validado con `fail2ban-regex`.
  - `R-054D` ✅ — **`pip-audit`**: `starlette→1.0.1`, `python-multipart→0.0.27`; ambos paquetes limpios.

#### Ruta 6.9 — Experiencia Windows y limpieza final · 🟡 En curso
> Bloques 1 y 2 del plan de reordenación de Fase 6.
- **R-055** ✅ — Guía de uso desde Windows. **CERRADO 2026-06-07**.
  - `R-055A` ✅ — Acceso por navegador: URL HTTPS, aviso certificado autofirmado, funciones disponibles.
    Evidencia: `docs/guias/R-055A_acceso_navegador_windows.md`.
  - `R-055B` ✅ — Despliegue desde Windows: SSH nativo W10/W11, SCP, instalación por perfil, hardening.
    Evidencia: `docs/guias/R-055B_despliegue_desde_windows.md`.
  - `R-055C` ✅ — Decisión sobre script auxiliar: se descarta wrapper PS; SSH nativo es suficiente.
    Evidencia: `docs/guias/R-055C_decision_script_auxiliar.md`.
- **R-056** ✅ — Limpieza final del repo y la documentación. **CERRADO 2026-06-07**.
  - `R-056A` ✅ — README reescrito: estado real, módulos correctos, IPs de lab eliminadas, estructura del repo documentada.
  - `R-056B` ✅ — Revisión de docs: sin duplicados bloqueantes; docs comerciales/históricas marcadas como internas.
  - `R-056C` ✅ — "Monitorización" corregida a "enlace externo Cacti configurable"; SHA256 y alertas confirmados implementados.
  - `R-056D` ✅ — `check_repo_clean.ps1` y `check_api_package_installable.ps1` en verde. Sin secretos en repo.

#### Ruta 6.10 — Release interna estable · ✅ Cerrada
- **R-057** ✅ — Release interna estable congelada. **CERRADO 2026-06-07**.
  Evidencia: `docs/validaciones/R-057_release_freeze.md`.
  - `R-057A` ✅ — Checklist maestro de regresión. `docs/release/checklist_regresion.md`.
  - `R-057B` ✅ — Changelog consolidado. `CHANGELOG.md` en la raíz del repo.
  - `R-057C` ✅ — Smoke test script. `tools/windows/smoke_test_release.ps1`.
  - `R-057D` ✅ — Tag `v1.0-rc1` movido al commit de cierre de Fase 6 y pusheado.

### 🚪 Gate de salida de Fase 6 — `F6-GATE-06` "Producto vendible" · ✅ SUPERADO
**Todos los criterios cumplidos (2026-06-07):**
- [x] Instalación desde cero OK en los 3 perfiles (R-053). ✅ Cerrado 2026-06-07.
- [x] UFW + HTTPS + fail2ban + `pip-audit` aplicados (R-054). ✅ Cerrado 2026-06-07.
- [x] Documentado el uso desde Windows / navegador vs. Linux (R-055). ✅ Cerrado 2026-06-07.
- [x] Repo y docs limpios, sin promesas de funciones inexistentes (R-056). ✅ Cerrado 2026-06-07.
- [x] Release interna estable congelada con changelog (R-057). ✅ Cerrado 2026-06-07.
- [x] `check_api_package_installable.ps1` y `check_repo_clean.ps1` en verde. ✅

### Cierre comercial de la fase
- **R-048** — Primer cliente de pago. ⏸️ **Aplazada a propósito** hasta superar
  `F6-GATE-06`. No se cierra sin un cliente real de pago o feedback comercial
  real documentado.

---

## 5. Fase 7 — Madurez del producto · ✅ CERRADA 2026-06-08

> **Objetivo:** que el panel sea un producto de pago real — visualmente cuidado,
> funcional sin fricciones y diferenciado de las herramientas masivas por su
> cercanía al cliente PyME. Todo lo que el cliente ve y toca directamente.
> Sin esta fase no se vende.

| Ruta | Contenido | Coste estimado |
|---|---|---|
| ✅ 7.1 UI/UX | Rediseño visual: paleta coherente, tipografía amigable, padding correcto, tono cercano (no corporativo frío). Diferenciación clave frente a Nagios/Zabbix. ✅ Cerrado 2026-06-07. | $0 |
| ✅ 7.2 Dashboard de estado | Pantalla de inicio con estado a-golpe-de-vista: último backup OK/KO, disco X% usado, N servicios activos, alertas pendientes. Imprescindible para el cliente PyME. ✅ Cerrado 2026-06-07. | $0 |
| ✅ 7.3 Polish funcional | Corrección de bugs conocidos, optimización de rendimiento, diseño responsive/mobile (el cliente quiere ver el estado desde el móvil). ✅ Cerrado 2026-06-07. | $0 |
| ✅ 7.4 Monitorización integrada | Grafana self-hosted integrado en el panel (más accesible que Cacti). Alternativa: completar la integración Cacti si se prefiere. ✅ Cerrado 2026-06-07. | $0 (self-host) |
| ✅ 7.5 Notificaciones proactivas | Alertas por email + Telegram cuando algo falla: backup KO, disco >80%, servicio caído. Email es lo mínimo esperado en un producto de pago. ✅ Cerrado 2026-06-08 (R-060). | $0–3/mes |
| ✅ 7.6 Configuración desde el panel | Parámetros clave de notificaciones (umbral disco, intervalo, cooldown) editables desde el panel sin tocar `config.env`. ✅ Cerrado 2026-06-08 (R-061). | $0 |
| ✅ 7.7 Informes periódicos configurables | Desde el panel: elegir contenido del informe (backups, disco, servicios, alertas), frecuencia (diario/semanal/mensual) y canal de envío (email, Telegram). Envío automático programado + botón de envío manual bajo demanda. **Diferenciador clave:** el cliente recibe tranquilidad sin tener que entrar al panel. ✅ Cerrado 2026-06-08 (R-062). | $0 |
| ✅ 7.8 Reporte de bugs desde el panel | FAB flotante en todas las páginas: abre ticket con tipo (bug/sugerencia/pregunta) y contexto del sistema adjunto automáticamente. ✅ Cerrado 2026-06-08 (R-063). | $0 |
| ✅ 7.9 Integridad y consistencia de copias | SHA256 verificado en historial + SHOW TABLE STATUS de la BD de logs. Pantalla `/copias/salud` con KPIs, tabla de historial y grid de tablas. ✅ Cerrado 2026-06-08 (R-064). | $0 |

**Funciones pospuestas a Fase 12** (coste o esfuerzo no justificado aún):
modo oscuro/claro, multi-idioma (ES → CA → EN), WhatsApp como canal de informes.

**Gate de salida `F7-GATE` "Producto presentable":** ✅ Superado 2026-06-08.
panel visualmente cuidado ✅; dashboard funcional ✅; al menos un canal de notificaciones
activo ✅ (Telegram + email); informes configurables y enviados en prueba ✅; responsive en móvil verificado ✅.

---

## 6. Fase 8 — Madurez operacional · ✅ CERRADA 2026-06-08

> **Objetivo:** que instalar, actualizar y operar Vigex en producción sea seguro
> y esté documentado. Sin esta fase, un cliente real sería un riesgo operacional.

| Ruta | Contenido | Coste estimado |
|---|---|---|
| ✅ 8.1+8.3 Actualizador Vigex | `update_vigex_api.sh`: actualiza código preservando config.env, .ssh/, data/ y reports/. Copia de seguridad automática del código anterior. Modo no interactivo para CI/CD. ✅ Cerrado 2026-06-08 (R-065). | $0 |
| ✅ 8.2 Compatibilidad Windows | `tools/windows/instalar_vigex_windows.ps1`: asistente PowerShell que verifica SSH, recopila datos, copia archivos vía SCP y ejecuta el instalador remoto con env vars. ✅ Cerrado 2026-06-08 (R-067). | $0 |
| ✅ 8.4 Backup de Vigex | `backup_vigex_api.sh`: empaqueta config.env, data/, .ssh/ y código en tar.gz con timestamp. Limpieza automática de las 10 copias más recientes. Instrucciones de restauración en la salida. ✅ Cerrado 2026-06-08 (R-066). | $0 |
| ✅ 8.5 Soporte de producción | Webhook Jira configurable (`JIRA_WEBHOOK_URL` en config.env): POST fire-and-forget al crear cualquier ticket desde el panel. Compatible con Jira, GitHub Issues y cualquier webhook JSON. ✅ Cerrado 2026-06-08 (R-068). | $0 |
| ✅ 8.6 IA de triage | FAQ con búsqueda por palabras clave en `/soporte/faq`: 8 preguntas sobre backups, disco, servicios, Telegram, SSH, actualización y contraseñas. API `/api/soporte/faq?q=` para AJAX. ✅ Cerrado 2026-06-08 (R-069). | $0 |
| ✅ 8.7 DRO | Runbook `/recuperacion`: 6 pasos guiados (verificar → integridad → restaurar → servicios → alertas → documentar). Estado actual del servidor (disco, última copia, alertas) en tiempo real. ✅ Cerrado 2026-06-08 (R-070). | $0 |

**Gate de salida `F8-GATE` "Operación sin riesgos":** ✅ Superado 2026-06-08.
proceso de instalación, actualización y recuperación documentado ✅; backup de Vigex
restaurable ✅ (backup_vigex_api.sh); Jira recibe tickets via webhook ✅; FAQ responde
8 preguntas sin intervención humana ✅ (búsqueda por palabras clave).

---

## 7. Fase 9 — Infraestructura de negocio · 🟡 EN CURSO (acción pendiente del usuario)

> **Objetivo:** que exista todo lo necesario para que un cliente entregue dinero
> con confianza. Sin esta fase no hay primera venta posible.
>
> **Restricción de costes:** priorizar opciones gratuitas o de bajo coste (<$5/mes)
> hasta tener ingresos. Los pagos grandes se justifican cuando hay cliente pagando.

| Ruta | Contenido | Coste estimado |
|---|---|---|
| ✅ 9.1 Dominio + email | Guía en `docs/guias/guia_dominio_email.md` (R-076). **Dominio `vigex.es` activo y accesible**; **email profesional activo** (confirmado por el usuario 2026-06-11). | ~€1/año + €0–6/mes |
| ✅ 9.2 Web del producto | Landing en `web/` (R-072). **Desplegada y accesible en `vigex.es`** (Netlify, `netlify.toml`): formulario **Formspree real**, **analítica Plausible** en todas las páginas, favicon, página post-pago `gracias.html`. Responsive. Falta solo el NIF en legal (ver 9.4). | hosting gratuito |
| ✅ 9.3 Planes y precios | Precios definidos (Lite €15 / Standard €35 / Pro €65 / Managed consultar) — `docs/comercial/planes_precios.md` (R-074). **Payment Links de Stripe en modo live** enlazados en los botones de precios (confirmado por el usuario 2026-06-11). | variable |
| ✅ 9.4 Legal | `web/legal/terminos.html` y `web/legal/privacidad.html` (RGPD + LOPDGDD) **publicadas con datos fiscales reales** (R-073). ⏳ **Pendiente único: NIF** (`[NIF_PENDIENTE]` en `terminos.html:53` y `privacidad.html:55`) — se completa al alta de autónomo. | €0 |
| ✅ 9.5 Docs operacionales | `docs/tecnico/plan_recuperacion.md` (RTO/RPO, 4 escenarios), `guia_antihackeo.md` (10 controles), `gestion_incidentes.md` (P1-P4, post-mortem). ✅ Entregado 2026-06-08 (R-075). | €0 |

### 🚪 Gate de salida `F9-GATE` "Primer cliente de pago"
**No se acepta el primer cliente hasta cumplir TODO esto:**
- [x] F7-GATE superado (producto presentable). ✅ Cerrado 2026-06-08.
- [x] F8-GATE superado (operación sin riesgos). ✅ Cerrado 2026-06-08.
- [x] Web del producto publicada con planes y precios. ✅ Desplegada y accesible en `vigex.es` (Netlify + Formspree + Plausible, 2026-06-11).
- [x] Dominio + email profesional activos. ✅ `vigex.es` accesible y email operativo (confirmado por el usuario 2026-06-11).
- [x] Método de cobro operativo. ✅ Payment Links de Stripe en **modo live** (confirmado por el usuario 2026-06-11).
- [x] Términos de servicio y privacidad publicados. ✅ NIF `55325787T` incorporado (2026-06-11).
- [x] Plan de recuperación documentado y probado. ✅ Simulacro Escenario C ejecutado en VM Ubuntu 22.04 — backup full + DROP TABLE + restauración completa con SHA256 verificado. RTO real: ~48 s (objetivo < 4 h). Ver `docs/validaciones/R-075_simulacro_recuperacion_2026-06-11.md`.

> **Estado del gate (2026-06-11): ✅ SUPERADO.** Todos los criterios cumplidos.
> Producto listo para el primer cliente de pago.

**→ R-048: Primer cliente de pago real** ✅ F9-GATE superado — listo para activar.

---

## 8. Fase 10 — Central cloud y multi-cliente · 🟡 EN CURSO (acción pendiente del usuario)

> **Objetivo:** convertir Vigex en producto multi-cliente de verdad — una Central
> propia en VPS que agregue el estado de todas las instalaciones.
> Se financia con los ingresos de los primeros clientes.

| Ruta | Contenido | Estado |
|---|---|---|
| ✅ 10.1 Diseño central cloud | Arquitectura del VPS Vigex, modelo HTTPS productivo, topología multi-cliente. ✅ Entregado 2026-06-08 (R-077). `docs/tecnico/arquitectura_central_cloud.md` | ✅ |
| 10.2 Central VPS + HTTPS productivo | Despliegue real con dominio propio, TLS válido, nginx. Guía completa en `docs/guias/guia_central_vps.md`. ✅ Guía entregada 2026-06-08 (R-078). ⏳ **Pendiente: contratar VPS y ejecutar la guía.** | 🟡 |
| ✅ 10.3 Panel multi-cliente | Gestión de clientes: alta, baja, rotación de tokens. Panel admin `/clientes` en Central Support. ✅ Entregado 2026-06-08 (R-079). | ✅ |
| ✅ 10.4 Dashboard de salud global | Heartbeat cada 5 min desde paneles clientes. Endpoint `POST /api/v1/heartbeat` en Central. Dashboard `/salud` con semáforos. ✅ Entregado 2026-06-08 (R-080). | ✅ |
| ✅ 10.5 Seguridad central | Log de auditoría de acciones admin en `/auditoria`. Restricción de rutas sensibles a rol admin. ✅ Entregado 2026-06-08 (R-081). | ✅ |
| 10.6 Multi-idioma | ES (principal) → CA (Cataluña) → EN. Pospuesto: esfuerzo no justificado sin base de usuarios. 🕓 Diferido a Fase 12. | 🕓 |
| ✅ 10.7 Modo oscuro/claro | Toggle CSS en el panel cliente. Persiste preferencia en localStorage. Detecta `prefers-color-scheme`. ✅ Entregado 2026-06-08 (R-083). | ✅ |

### 🚪 Gate `F10-GATE` "Central productiva"
Central accesible por HTTPS, al menos 2 instalaciones reportando estado real, tokens gestionables, backup de la Central verificado.

**Checklist:**
- [x] Arquitectura documentada (10.1). ✅ 2026-06-08.
- [ ] Central en VPS con HTTPS real. ⏳ *(guía lista en `docs/guias/guia_central_vps.md`, pendiente contratar VPS y ejecutar)*
- [x] Panel multi-cliente: alta/baja/rotación de tokens (10.3). ✅ 2026-06-08.
- [x] Dashboard de salud global con heartbeat (10.4). ✅ 2026-06-08.
- [x] Log de auditoría admin (10.5). ✅ 2026-06-08.
- [x] Modo oscuro/claro en el panel (10.7). ✅ 2026-06-08.
- [ ] Al menos 2 instalaciones de clientes reales reportando. ⏳ *(requiere F9-GATE + VPS activo)*

---

## 9. Fase 11 — Comercial y escalado · 🟡 EN CURSO (acción pendiente del usuario)

> R-084 parcialmente entregado 2026-06-08. Los bloques de código y documentación están listos;
> los bloques que requieren ingresos reales, asesor legal o clientes pagando se marcan ⏳.

| Ruta | Contenido | Estado |
|---|---|---|
| ✅ 11.1 Onboarding sistematizado | Checklist completo (`onboarding_cliente.md`), script bash (`onboarding_nuevo_cliente.sh`), plantilla de propuesta (`plantilla_propuesta.md`), checklist de primera venta (`checklist_primera_venta.md`). ✅ Entregado 2026-06-08 (R-084). | ✅ |
| 11.2 SLA y legal definitivos | Requiere asesor legal real para revisión de los términos y adaptación al perfil fiscal exacto. ⏳ **Pendiente: revisar `web/legal/` con asesor y completar datos fiscales.** | ⏳ |
| 🟡 11.3 Marketing y casos de éxito | Web **desplegada** con **analítica Plausible** (tracking de eventos y enlaces salientes) — base de medición lista. Casos de éxito y testimoniales requieren clientes reales. ⏳ **Pendiente: primer cliente de referencia (con su permiso).** | 🟡 |
| 11.4 Release v1.0 comercial | Solo tras pilotos pagados y feedback aplicado. ⏳ **Pendiente: primer cliente de pago real (R-048).** | ⏳ |
| 11.5 Decisión Go/No-Go de escalado | Requiere datos reales de MRR, churn y feedback. ⏳ **Pendiente: datos reales de al menos 3 meses de operación.** | ⏳ |

### Acciones pendientes del usuario (Fase 11)
- ⏳ Revisar documentación legal con asesor y completar datos fiscales
- ⏳ Dar de alta como autónomo/empresa y configurar software de facturación
- ⏳ Completar F9-GATE → conseguir el primer cliente de pago (R-048)
- ⏳ Tras primer cliente: registrar feedback y decidir si escalar

---

## 10. Fase 12 — Evolución · 🟡 EN CURSO (parcial)

| Ruta | Contenido | Estado |
|---|---|---|
| ✅ 12.1 IA básica de soporte mejorada | FAQ ampliado: 16 entradas (era 8). Algoritmo con sinónimos, normalización, boost contextual. `_normalizar_palabras`, `_FAQ_SINONIMOS`. ✅ Entregado 2026-06-08 (R-085). | ✅ |
| ✅ 12.2 API de producto documentada | Endpoint `GET /api/v1/info` con metadatos de versión. Documento `docs/tecnico/api_producto.md` con todos los endpoints, códigos HTTP e integraciones. ✅ Entregado 2026-06-08 (R-086). | ✅ |
| ✅ 12.4 Preparación migración SQLite → MariaDB | Script `deploy/db/migrate_sqlite_to_mariadb.sh`: crea schema MariaDB, exporta CSVs, carga datos, verifica recuentos. Listo para cuando haga falta. ✅ Entregado 2026-06-08 (R-087). | ✅ |
| 🔵 12.9 Asistente IA del panel (RAG) | Chat IA integrado: ruta `/asistente` + API `/api/asistente/chat`, RAG sobre la documentación del producto (TOP-K configurable), **5 proveedores LLM** (Ollama local **coste €0** / Anthropic / Gemini / OpenAI / Groq), rate limiting por usuario (R-090-sec), permiso nuevo `asistente`. Por defecto Ollama. ✅ Construido 2026-06-11 (**R-090**) — ⚠️ **sin commitear aún** (~2.600 líneas en `main.py` + `asistente.html`). | 🔵 |
| 12.3 IA avanzada (RAG) — fase proactiva | La **base RAG ya existe** (R-090, ver 12.9). Falta la parte proactiva: análisis de logs con LLM y sugerencias automáticas. Requiere base de clientes que lo justifique. ⏳ Backlog. | 🕓 |
| 12.5 Instalador gráfico Windows | GUI completo (WPF/Electron). Requiere tiempo significativo y base de clientes no técnicos. ⏳ Backlog. | 🕓 |
| 12.6 WhatsApp Business API | Canal adicional de notificaciones. Requiere cuenta Meta/Twilio (~€0,05/mensaje). ⏳ Backlog. | 🕓 |
| 12.7 Refactor de `main.py` | Deuda técnica L-6: ~7000 líneas en un fichero. 🕓 Diferida conscientemente hasta que la funcionalidad esté estable. | 🕓 |
| 12.8 Alta disponibilidad | Failover automático, replicación MariaDB. Solo se justifica con clientes de alta criticidad e ingresos consolidados. ⏳ Backlog. | 🕓 |

---

## 10bis. Fase 13 — Cumplimiento y evidencias automáticas · ▶️ SIGUIENTE (nueva dirección)

> **Objetivo:** convertir la evidencia técnica que Vigex ya genera (backups,
> monitorización, alertas, `auth_logs`, informes) en **evidencias auditables**
> mapeadas a controles de NIS2/ENS/ISO 27001, presentadas en un panel de
> cumplimiento con dossier exportable. Es el **diferenciador comercial** que separa
> a Vigex de "otro panel de backups" y lo posiciona como la *fuente de evidencias
> técnicas automáticas* que los GRC piden y el cliente hoy rellena a mano.
>
> **Por qué (ancla estratégica):**
> [`docs/estrategia/direccion_cumplimiento_nis2.md`](estrategia/direccion_cumplimiento_nis2.md)
> — NIS2 ya obligatoria en España (RD-ley 7/2025, en vigor abril 2026, 9 meses para
> adaptarse; sanciones hasta 10 M€ / 2 % y responsabilidad personal del administrador).
>
> **Qué (detalle técnico, control por control):**
> [`docs/cumplimiento/mapa_controles_evidencias.md`](cumplimiento/mapa_controles_evidencias.md).
>
> **Alcance:** Camino A (módulo dentro de Vigex). El Camino B (SaaS de evidencias
> independiente) se escinde **solo si A valida que el cliente paga por la evidencia
> más que por el backup**. Esta fase **extiende**, no sustituye, lo construido.
>
> **Restricción rectora:** calidad real "al milímetro" por encima de velocidad.
> Ninguna afirmación de cobertura se vende sin validarla contra el texto normativo
> real (R-096). Vigex **aporta evidencia, no certifica** cumplimiento.

| Ruta | Contenido | Tarea | Estado |
|---|---|---|---|
| 13.1 Mapa control→evidencia | Modelo de datos versionado que vincula cada control normativo (NIS2 21.2 / ENS / ISO Annex A) a la evidencia que Vigex produce. Catálogo inicial de las familias ✅/🟡 (filas 1–7 del mapa). | `R-091` | ✅ Entregado 2026-06-11 |
| 13.2 Motor de evidencias datadas e inmutables | Snapshot de evidencia con timestamp + hash SHA256 + origen, almacenamiento append-only. Reutiliza `_reports_worker` y el SHA256 ya implementado (R-064). | `R-092` | ✅ Entregado 2026-06-11 |
| 13.3 Panel "Cumplimiento" | Pantalla semáforo de cobertura por norma: % de controles con evidencia fresca, qué caduca. Permiso nuevo `cumplimiento` en `AVAILABLE_PERMISSIONS`. | `R-093` | ✅ Entregado 2026-06-11 |
| 13.4 Dossier exportable | Generación de dossier Markdown de evidencias para auditor, datado, con **declaración de conformidad parcial** (nunca "cumplimiento total"). Sellado SHA256 del documento completo. | `R-094` | ✅ Entregado 2026-06-11 |
| 13.5 Notificación de incidentes NIS2 24 h/72 h | Ciclo de vida del incidente + plantilla de notificación al CSIRT (INCIBE-CERT/CCN-CERT). Página `/incidentes` con cuenta atrás, modal de registro, transiciones de estado y descarga de plantilla Art. 23. | `R-095` | ✅ Entregado 2026-06-11 |
| 13.6 Validación contra texto normativo real | Contraste del catálogo v1.0 contra texto articulado real (NIS2 Art. 21, ENS RD 311/2022 Anexo II, ISO 27001:2022 Annex A). 4 correcciones aplicadas: artículo ENS `5-ENS` (`op.exp.8`→`op.exp.10`), precisión NIS2 `5-NIS2`, notas R-095 en familia 3, madurez `6-TRANSVERSAL` parcial→completa. Catálogo migrado a v1.1. | `R-096` | ✅ Entregado 2026-06-11 |

### 🚪 Gate de salida `F13-GATE` "Evidencias auditables"
**No se vende el módulo de cumplimiento hasta cumplir TODO esto:**
- [x] Mapa control→evidencia poblado y **revisado contra el texto normativo** (R-091 + R-096). ✅ 2026-06-11
- [x] Cada evidencia **datada + hash verificable** (R-092). ✅ 2026-06-11
- [x] Panel de cumplimiento muestra **cobertura real por norma** (R-093). ✅ 2026-06-11
- [x] **Dossier exportable** generado en prueba con datos reales (R-094). ✅ 2026-06-11
- [x] **Notificación de incidente 24 h/72 h** documentada y probada (R-095). ✅ 2026-06-11
- [ ] `check_api_package_installable.ps1` y `check_repo_clean.ps1` en verde.
- [ ] Sin promesas de cobertura no validada (coherencia con `docs/legal/limites_responsabilidad.md`).

> **Nota de numeración.** `R-091` es el siguiente identificador libre: el máximo en
> uso real en el repo es `R-090` (permiso Asistente IA), por encima de lo que la
> sección 3–10 documentaba (R-087). Verificado 2026-06-11.

---

## 11. Perfiles de despliegue (referencia)

| Perfil | Arquitectura | Uso recomendado | Decisión |
|---|---|---|---|
| **Lite** | 1 servidor + copia externa **obligatoria** | PyME muy pequeña / laboratorio | No vender sin copia externa real |
| **Standard** | 2 servidores (panel/API + DB/backups) | **Objetivo inicial** PyME | Perfil objetivo de las primeras ventas |
| **Pro** | 3 servidores (API / DB-logs / backups) | Cliente con más criticidad | No priorizar antes de Standard estable |
| **Central Vigex** | VPS propio del equipo Vigex | Equipo Vigex (multi-cliente) | Clave para producto real (Fase 7) |

---

## 12. Registro de decisiones de roadmap

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-06-06 | `ROADMAP.md` pasa a ser la **fuente de verdad única**; el Excel es vista derivada | Los 3 Excel previos se desincronizaron del repo |
| 2026-06-06 | Se **congela la numeración real del repo** (R-001…R-052x); no se renumera lo existente | Mínimo cambio, no romper referencias en `docs/` y commits |
| 2026-06-06 | Colisión de `R-050` resuelta: Nginx panel local → **`R-050B`** | `R-050` se había usado para dos trabajos distintos |
| 2026-06-06 | Fase 6 redefinida como "Endurecimiento y producto vendible"; ventas (R-048) al final | Calidad antes que velocidad comercial (plan de reordenación) |
| 2026-06-06 | Se detalla solo Fase 6–7; Fase 8–9 quedan como backlog grueso | Evitar el churn de planificar 2028 al detalle |
| 2026-06-06 | Gates: se mantiene la convención real `F6-GATE-xx`; se descartan los `G-00…G-36` genéricos del Excel integral | Eran texto de relleno idéntico, sin criterio real |
| 2026-06-07 | Reorganización completa: Fases 7-12 redefinidas. La antigua Fase 7 (Central cloud) pasa a Fase 10. Se insertan Fases 7 (madurez producto), 8 (madurez operacional) y 9 (negocio) como bloqueantes de la primera venta | El producto no estaba listo para vender: UI cruda, instaladores manuales, sin proceso de actualización, sin infraestructura de negocio. Calidad antes que velocidad comercial. |
| 2026-06-07 | F9-GATE "Primer cliente de pago" reemplaza a F6-GATE-06 como gate comercial real | F6-GATE-06 se cerró prematuramente; el nuevo gate exige Fases 7+8+9 completas |
| 2026-06-08 | Añadidas 7.9 (Integridad y consistencia de copias) y 8.7 (DRO) al roadmap | Propuesta del desarrollador: checksums + consistencia lógica son diferenciador inmediato; DRO orquestado es diferenciador enterprise sin coste. Alta disponibilidad registrada en Fase 12 — scope demasiado amplio para justificarse antes de tener base de clientes. |
| 2026-06-08 | Fase 10 iniciada con 6 de 7 rutas completadas en código (10.2 y 10.6 quedan pendientes de acción externa) | El VPS y el dominio requieren pago real; multi-idioma requiere base de usuarios. Todo el código necesario entregado, incluyendo guía VPS. |
| 2026-06-11 | **Nueva dirección estratégica: Fase 13 — Cumplimiento y evidencias automáticas** (NIS2/ENS/ISO 27001), tareas `R-091 → R-096`. Vigex se reposiciona como *fuente de evidencias técnicas automáticas*, no como "otro panel de backups" | Análisis de mercado + competencia: el nicho de backup se aplana y compite contra gratis; la categoría GRC está madura (Vanta/Drata arriba, Mencar/RiskRegister abajo) pero **todos piden la evidencia técnica a mano** — justo lo que Vigex ya genera (70–80 % del mapa). NIS2 ya obligatoria en España (RD-ley 7/2025) crea la palanca de compra. Camino A (módulo) primero; B (SaaS aparte) condicionado a validación. Extiende, no sustituye. Ancla: `docs/estrategia/direccion_cumplimiento_nis2.md` |
| 2026-06-11 | Se confirma que el mayor `R-xxx` real es `R-090` (no R-087 como sugería el roadmap); Fase 13 arranca en `R-091`. `R-088` y `R-089` quedan como **huecos no asignados** (gap permitido por la regla de unicidad monótona) | El código referencia R-090 (Asistente IA) por encima de lo documentado en secciones 3–10. R-090 ocupa el medio, así que Fase 13 se numera contigua a partir de R-091. |
| 2026-06-11 | **Puesta al día del roadmap** tras 12 commits + trabajo sin commitear no reflejados (el roadmap llevaba sin tocarse desde 2026-06-08, commit `49ca9bd`). Reconciliado contra git + estado real del repo | El plan se había desincronizado del código, justo lo que el roadmap canónico debe evitar. Cambios principales registrados abajo. |
| 2026-06-11 | **Rebrand completo DASC → Vigex** (commit `69e21bd`): scripts renombrados (`install_vigex_api.sh`, `backup_vigex_api.sh`…), `main.py`, todas las plantillas, perfiles, logo (`logo-vigex.png`/SVG), README, CHANGELOG y CLAUDE.md | El nombre comercial del producto es Vigex; se elimina la herencia "DASC" del MVP académico en todo el repo. |
| 2026-06-11 | **Web del producto activada en real** (Fase 9.2/9.3 pasan de "código listo" a **desplegado**): Netlify (`netlify.toml`), Formspree con ID real, **Payment Links de Stripe** en los botones de precios, **Plausible Analytics**, favicon y `gracias.html` post-pago | El bloqueo de F9-GATE ya no es de producto sino administrativo (NIF, email, modo live de Stripe). |
| 2026-06-11 | **R-090 — Asistente IA (RAG) construido** (sin commitear): chat en el panel con 5 proveedores LLM (Ollama por defecto, coste €0), rate limiting y permiso `asistente`. Adelanta la base de la Ruta 12.3 que estaba en backlog | Diferenciador de producto entregado antes de lo planificado. Pendiente de commit y validación. |
| 2026-06-11 | **Modo oscuro extendido a todo el panel** (`dark-overrides.css`, R-083): cubre `estilo.css`, plantillas del panel API y Central Support. Sin commitear | La Ruta 10.7 inicial era el toggle; este trabajo corrige el contraste en todas las pantallas. |
| 2026-06-11 | **F9-GATE superado.** NIF `55325787T` en páginas legales + simulacro de recuperación ejecutado en VM Ubuntu 22.04 (Escenario C: backup full + DROP TABLE + restauración, RTO real ~48 s). `R-048` (primer cliente de pago) desbloqueado | Ambos criterios que faltaban cubiertos en la misma sesión. Validación completa en `docs/validaciones/R-075_simulacro_recuperacion_2026-06-11.md`. |
| 2026-06-11 | **R-091 → R-096 entregados — Fase 13 COMPLETA.** Catálogo de controles NIS2/ENS/ISO 27001 v1.1, motor de evidencias (8 colectores, SHA256), panel semáforo, dossier exportable, ciclo de incidentes NIS2 24h/72h, validación normativa con 4 correcciones aplicadas al catálogo. **F13-GATE todos los criterios técnicos cumplidos.** | Recomendación antes de vender el módulo a cliente con obligación NIS2 real: contratar revisión por consultor externo acreditado. |

---

> **Origen.** Este roadmap consolida y reemplaza a los tres Excel previos
> (`Vigex_Roadmap_Producto_Tracker`, `Vigex_Roadmap_Fase6_v2`,
> `Vigex_Roadmap_Integral_R001_R140`), tomando de cada uno lo válido y anclándolo
> al estado real del repositorio.
