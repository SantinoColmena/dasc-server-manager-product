# Mapa control → evidencia — NIS2 / ENS / ISO 27001:2022

> **Estado:** Referencia técnica viva · creado 2026-06-11 · ancla la **Fase 13**.
> **Propósito:** documentar, control por control, qué evidencia genera Vigex hoy,
> con qué grado de madurez, y qué falta para convertirla en **evidencia
> auditable**. Es la base del módulo de cumplimiento (Camino A).
>
> **Aviso de rigor (parámetro "al milímetro"):** este mapa es una correspondencia
> *de trabajo*. Antes de afirmar cobertura ante un cliente o auditor debe validarse
> contra el **texto normativo real** (Ruta 13.6 / `R-096`). Vigex **aporta
> evidencia, no certifica cumplimiento** (ver `docs/legal/limites_responsabilidad.md`).

---

## 1. Leyenda

| Símbolo | Significado |
|---|---|
| ✅ | Evidencia **generada automáticamente** por Vigex hoy |
| 🟡 | **Parcial** — el dato existe, falta empaquetarlo/datarlo/sellarlo como evidencia auditable |
| ❌ | **No existe** en Vigex (y, salvo nota, **no se perseguirá** — es papeleo de GRC) |

Las referencias técnicas apuntan a capacidades reales del código
(`deploy/api/package/main.py` salvo indicación) confirmadas a 2026-06-11.

---

## 2. Tabla de cobertura

| # | Familia de control | NIS2 art. 21 / ENS / ISO 27001:2022 | Qué pide la norma | Evidencia que Vigex produce hoy | Estado |
|---|---|---|---|---|---|
| 1 | **Continuidad y copias de seguridad** | NIS2 21.2(c) · ENS `op.exp.8` · ISO A.8.13 | Backups regulares, probados, con retención definida y restauración verificable | Historial datado con tipo (full/incremental) y estado OK/fallo (`cargar_historial_backups`), programación cron (`build_backup_cron_expression`), **planes de restauración** (`plan_restauracion_backups`), retención/cascada (`plan_eliminacion_backups`, `eliminar_backups_cascada_remoto`), copia externa (`sync_external_backup.sh`), `audit.log` en host de backups (R-022) | ✅ |
| 2 | **Monitorización y disponibilidad** | NIS2 21.2(a) · ENS `op.mon` · ISO A.8.16 | Vigilar sistemas, detectar anomalías, registrar capacidad | Métricas disco/CPU/memoria/uptime (`monitoreo_metrics`, `_parse_*`), estado de servicios systemd, histórico embebido en informes periódicos | ✅ |
| 3 | **Gestión de incidentes (detección/alerta)** | NIS2 21.2(b) · ENS `op.exp.7` · ISO A.5.24–A.5.26 | Detectar, registrar, escalar y **notificar** incidentes | Motor de alertas multicanal (`emit_alert`, Telegram + email) + chequeos proactivos disco/backup (`_check_disk_proactive`, `_check_backup_proactive`) con registro y stats (`get_alert_stats`) | 🟡 — detecta y avisa; **falta el ciclo de vida del incidente y la notificación NIS2 24 h / 72 h** (→ R-095) |
| 4 | **Control de accesos y autenticación** | NIS2 21.2(i)/(j) · ENS `op.acc` · ISO A.5.15–A.5.18, A.8.5 | Gestión de accesos, mínimo privilegio, registro de quién accede a qué | Permisos por módulo (`AVAILABLE_PERMISSIONS`), roles admin/usuario, bcrypt (`hash_password`/`verify_password`), bloqueo por IP (`login_is_blocked`) | 🟡 — control sí; **falta MFA** y **revisión periódica de accesos** documentada |
| 5 | **Registro y trazabilidad (logs)** | NIS2 21.2(a) · ENS `op.exp.8`/`op.mon` · ISO A.8.15 | Registro de actividad/accesos/eventos, conservado y protegido | `auth_logs.json` (login/logout/fallos vía `register_auth_log`), `log_event`, BD de logs MariaDB (pymysql) | 🟡 — se registra; **falta retención garantizada + integridad/sellado** del log |
| 6 | **Informe de cumplimiento / evidencia datada** | Transversal (todas) | Demostrar ante auditor de forma continua y datada | Informes periódicos en Markdown/HTML (`_reports_worker`, `_informe_html`) con disco/backups/servicios/alertas, guardados en `reports/` y enviados por email/Telegram | 🟡 — existe el motor; **no está mapeado a controles ni firmado/datado como evidencia** (→ R-092) |
| 7 | **Cifrado** | NIS2 21.2(h) · ENS `mp.info.3` · ISO A.8.24 | Cifrado de datos en reposo y en tránsito | SSH ed25519 endurecido para gestión remota (`build_ssh_base_command`, allowlist), HTTPS por reverse proxy (R-054B), copia externa cifrada GPG (R-029) | 🟡 — canal y copia externa sí; **falta evidenciar cifrado de los backups/datos en reposo** de forma sistemática |
| 8 | **Gestión de vulnerabilidades / parches** | NIS2 21.2(e) · ENS `op.exp.4` · ISO A.8.8 | Inventario de vulnerabilidades, parcheo, versiones | Puntual: `pip-audit` aplicado una vez (R-054D); no hay inventario continuo | 🟡/❌ — **candidato menor**: podría evidenciarse versión de SO/paquetes vía SSH ya permitido, pero no es prioridad |
| 9 | **Análisis de riesgos** | NIS2 21.2(a) · ENS `op.pl.1` · ISO cláusula 6, A.5.2 | Metodología de riesgos documentada | — | ❌ Papeleo — no se persigue |
| 10 | **Políticas y procedimientos** | NIS2 21.2(a) · ENS `org.*` · ISO A.5.1 | Política de seguridad y procedimientos escritos | — | ❌ Papeleo — no se persigue |
| 11 | **Formación y concienciación** | NIS2 21.2(g) · ENS `mp.per.3` · ISO A.6.3 | Formación continua con métricas | — | ❌ No se persigue |
| 12 | **Seguridad de proveedores** | NIS2 21.2(d) · ENS `op.ext` · ISO A.5.19–A.5.22 | Evaluar y vigilar la cadena de suministro | — | ❌ No se persigue |
| 13 | **Inventario de activos** | ENS `op.pl.2` · ISO A.5.9 | Inventario de activos y su clasificación | Conoce hosts/servicios/BBDD gestionados (config de perfil, estado de servicios) | 🟡 — base parcial reutilizable |

---

## 3. Lectura estratégica de la tabla

- **Filas 1–2 (✅):** el diferenciador más fuerte y defendible. Ningún GRC genérico
  tiene continuidad+monitorización conectadas a la infraestructura real. **Es el
  gancho comercial.**
- **Filas 3–7 (🟡):** el dato ya existe; falta la **capa de evidencia auditable**.
  Ese "empujón" *es* el producto de la Fase 13.
- **Filas 8, 13 (🟡 menores):** oportunidades secundarias, no bloqueantes.
- **Filas 9–12 (❌):** papeleo puro. **No se construye.** Vigex se integra con un
  GRC o cede ese terreno. Perseguirlo sería competir donde no hay foso.

---

## 4. El gap a construir (resumen del MVP — detalle en ROADMAP Fase 13)

Para pasar de 🟡 a ✅ basta una **capa fina** sobre lo existente:

1. **Mapa control → evidencia** como modelo de datos versionado (`R-091`).
2. **Evidencia datada e inmutable**: snapshot con fecha + hash SHA256 + origen,
   almacenamiento append-only, reutilizando el motor de informes y el SHA256 ya
   implementado (R-064) (`R-092`).
3. **Panel "Cumplimiento"**: semáforo de cobertura por norma, qué caduca, permiso
   nuevo `cumplimiento` (`R-093`).
4. **Dossier exportable** datado para el auditor, con declaración de conformidad
   *parcial* (`R-094`).
5. **Notificación de incidentes NIS2 24 h / 72 h** + ciclo de vida del incidente,
   para cerrar la fila 3 (`R-095`).
6. **Validación contra texto normativo real** para que la cobertura sea defendible
   (`R-096`).

> Todo reutiliza backups, alertas, `auth_logs` e informes ya escritos: es **un
> módulo, no un proyecto nuevo**.

---

## 5. Mantenimiento de este documento

Este mapa es **vivo**: cada tarea de la Fase 13 que cierre debe actualizar la
columna *Estado* y, cuando proceda, la fila correspondiente. La fuente de verdad
del plan sigue siendo [`docs/ROADMAP.md`](../ROADMAP.md); este documento es el
detalle técnico que lo respalda. El *porqué* está en
[`docs/estrategia/direccion_cumplimiento_nis2.md`](../estrategia/direccion_cumplimiento_nis2.md).
