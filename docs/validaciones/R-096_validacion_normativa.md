# R-096 — Validación del catálogo de controles contra texto normativo real

**Fecha:** 2026-06-11  
**Versión catálogo validada:** v1.0 → v1.1  
**Realizada por:** Revisión técnica interna contra fuentes primarias (texto normativo oficial)  
**Normas contrastadas:**
- NIS2: Directiva (UE) 2022/2555, Art. 21 — transpuesta en España por RD-ley 7/2025
- ENS: Real Decreto 311/2022 (Esquema Nacional de Seguridad), Anexo II
- ISO 27001:2022: Annex A (controles de referencia)

---

## Metodología

Cada fila del catálogo `_COMPLIANCE_CATALOG` (en `main.py`) fue revisada contra el texto articulado real
de cada norma. Para cada control se verificó:

1. **Artículo / apartado correcto** — que el identificador apuntaba al lugar exacto del texto normativo.
2. **Requisito bien redactado** — que la descripción era fiel al texto del artículo.
3. **Madurez honesta** — que el nivel (`completa / parcial / ausente`) era defendible ante un auditor real,
   teniendo en cuenta la evidencia técnica que Vigex genera, no la que idealmente debería generar.
4. **Fuentes de evidencia actualizadas** — que referenciaban los colectores y tablas reales del sistema.

---

## Hallazgos y correcciones (v1.0 → v1.1)

### Corrección 1 — Familia 5 (Logs), control `5-ENS`: artículo incorrecto

| | Antes (v1.0) | Después (v1.1) |
|---|---|---|
| Artículo | `op.exp.8/op.mon` | `op.exp.10/op.mon.1` |
| Motivo | `op.exp.8` es el control ENS de **copias de seguridad**, no de registros de actividad. El control correcto para el registro de actividad de usuarios y administradores es `op.exp.10` ("Registro de la actividad de los usuarios"). `op.mon.1` cubre la vigilancia de sistemas. | — |

**Impacto:** sin esta corrección, una auditoría ENS detectaría la referencia errónea y desacreditaría toda la fila.

---

### Corrección 2 — Familia 5 (Logs), control `5-NIS2`: artículo más preciso

| | Antes (v1.0) | Después (v1.1) |
|---|---|---|
| Artículo | `21.2(a)` | `21.2(a)/21.2(b)` |
| Motivo | El logging es parte de las políticas de seguridad de los sistemas (21.2(a)), pero también es infraestructura de detección de incidentes (21.2(b)). Ambas referencias son defensibles; incluir las dos es más preciso. | — |

**Impacto:** menor; el auditora aceptaría solo (a) pero la doble referencia es más rigurosa.

---

### Corrección 3 — Familia 3 (Incidentes): notas caducadas, R-095 entregado

Los tres controles de la familia 3 (`3-NIS2`, `3-ENS`, `3-ISO`) tenían notas que indicaban
que el ciclo de vida de incidentes 24h/72h estaba pendiente (`→ R-095`). R-095 fue entregado
el 2026-06-11 con:
- Tabla `incidentes` en `cumplimiento.db` con ciclo de vida completo
- Página `/incidentes` con cuenta atrás visual
- Plantilla CSIRT descargable (formato Art. 23 NIS2 + guía ENISA)

**Madurez actualizada:** sigue siendo `parcial` — el sistema de gestión técnica existe y es
funcional, pero los controles NIS2 21.2(b), ENS op.exp.7 e ISO A.5.24-A.5.26 también
requieren **procesos organizativos** (roles de respuesta definidos, plan de comunicación
aprobado, ejercicios de simulacro documentados, análisis post-mortem) que no pueden
automatizarse y deben ser aportados por el cliente como documentación.

---

### Corrección 4 — Familia 6 (Evidencia datada): madurez `parcial` → `completa`

La familia 6 (Transversal) estaba como `parcial` en v1.0 porque el motor de evidencias
no existía todavía. Con R-091–R-095 completados:

| Requisito del control | Estado |
|---|---|
| Catálogo de controles versionado | ✅ R-091 |
| Evidencia datada con SHA256 inmutable | ✅ R-092 |
| Panel con cobertura en tiempo real | ✅ R-093 |
| Dossier exportable para auditor | ✅ R-094 |
| Ciclo de vida de incidentes NIS2 | ✅ R-095 |

La familia 6 es ahora `completa` en términos de lo que Vigex puede automatizar. La nota
deja claro que la **validación ante auditor real** es el paso siguiente del cliente.

---

## Referencias verificadas como correctas (sin cambios)

Los siguientes artículos se verificaron contra el texto normativo y se confirmaron correctos:

| Control | Norma | Artículo | Verificación |
|---|---|---|---|
| 1-NIS2 | NIS2 | 21.2(c) | ✅ "Continuidad del negocio, gestión de copias de seguridad y recuperación en caso de catástrofe" |
| 1-ENS | ENS | op.exp.8 | ✅ "Copias de seguridad (backup)" — Anexo II, medida operacional |
| 1-ISO | ISO 27001 | A.8.13 | ✅ "Information backup" — Annex A, Technology controls |
| 2-NIS2 | NIS2 | 21.2(a) | ✅ Monitorización como parte de las políticas de SI |
| 2-ENS | ENS | op.mon | ✅ Monitorización del sistema — categoría de medidas operacionales |
| 2-ISO | ISO 27001 | A.8.16 | ✅ "Monitoring activities" — Annex A |
| 3-NIS2 | NIS2 | 21.2(b) | ✅ "Gestión de incidentes" |
| 3-ENS | ENS | op.exp.7 | ✅ "Gestión de incidentes de seguridad" — Anexo II |
| 3-ISO | ISO 27001 | A.5.24–A.5.26 | ✅ Planificación, evaluación y respuesta a incidentes |
| 4-NIS2 | NIS2 | 21.2(i)/(j) | ✅ (i) gestión de accesos y activos, (j) MFA |
| 4-ENS | ENS | op.acc | ✅ Control de acceso — Anexo II |
| 4-ISO | ISO 27001 | A.5.15–A.5.18/A.8.5 | ✅ Identidades, acceso y acceso privilegiado |
| 5-ISO | ISO 27001 | A.8.15 | ✅ "Logging" — Annex A |
| 7-NIS2 | NIS2 | 21.2(h) | ✅ "Uso de criptografía y, cuando proceda, cifrado" |
| 7-ENS | ENS | mp.info.3 | ✅ "Cifrado de la información" — Anexo II |
| 7-ISO | ISO 27001 | A.8.24 | ✅ "Use of cryptography" — Annex A |
| 8-NIS2 | NIS2 | 21.2(e) | ✅ Adquisición, desarrollo y mantenimiento de SRI, incluida la gestión de vulnerabilidades |
| 8-ENS | ENS | op.exp.4 | ✅ "Gestión de la configuración" — Anexo II |
| 8-ISO | ISO 27001 | A.8.8 | ✅ "Management of technical vulnerabilities" — Annex A |
| 9-NIS2 | NIS2 | 21.2(a) | ✅ Políticas de análisis de riesgos |
| 9-ENS | ENS | op.pl.1 | ✅ "Análisis de riesgos" — Anexo II |
| 9-ISO | ISO 27001 | Cláusula 6 | ✅ "Planning" — risk assessment and treatment |
| 10-NIS2 | NIS2 | 21.2(a) | ✅ Políticas de seguridad |
| 10-ENS | ENS | org.* | ✅ Marco organizativo — Anexo II |
| 10-ISO | ISO 27001 | A.5.1 | ✅ "Information security policies" — Annex A |
| 11-NIS2 | NIS2 | 21.2(g) | ✅ "Prácticas básicas de ciberhigiene y formación" |
| 11-ENS | ENS | mp.per.3 | ✅ "Concienciación" — Anexo II |
| 11-ISO | ISO 27001 | A.6.3 | ✅ "Information security awareness, education and training" |
| 12-NIS2 | NIS2 | 21.2(d) | ✅ "Seguridad de la cadena de suministro" |
| 12-ENS | ENS | op.ext | ✅ Servicios externos — Anexo II |
| 12-ISO | ISO 27001 | A.5.19–A.5.22 | ✅ Supplier relationships |
| 13-ENS | ENS | op.pl.2 | ✅ "Adquisición de componentes" / inventario |
| 13-ISO | ISO 27001 | A.5.9 | ✅ "Inventory of information and associated assets" — Annex A |

---

## Controles NIS2 Art. 21 no cubiertos por el catálogo actual

El artículo 21.2 de NIS2 tiene 10 apartados. Los no cubiertos por el catálogo actual son:

| Apartado | Requisito | Decisión |
|---|---|---|
| 21.2(f) | Evaluar la eficacia de las medidas de gestión de riesgos | Solapado con familia 6 (evidencias) y familia 9 (análisis). Aceptable como ausente en el catálogo explícito. |
| 21.2(d) | Seguridad de la cadena de suministro | Familia 12 — marcado correctamente como `ausente` |
| 21.2(g) | Ciberhigiene y formación | Familia 11 — marcado correctamente como `ausente` |

No se identifican controles obligatorios que estén ausentes del catálogo y deberían estar cubiertos
por Vigex. Las ausencias reflejan controles organizativos/GRC deliberadamente fuera del alcance del producto.

---

## Conclusión

El catálogo v1.1 es **técnicamente defendible ante un auditor** con las siguientes reservas:

1. Las familias `parcial` requieren evidencia complementaria del cliente (documentos de política,
   roles, contratos, planes de formación) que no puede generarse automáticamente.
2. Las familias `ausente` (9–12) están deliberadamente fuera del alcance de Vigex y se
   documentan como tales para que el cliente sepa que debe cubrirlas con herramientas GRC externas
   o documentación propia.
3. La cobertura de NIS2 Art. 21 por parte de Vigex se centra en los controles **técnicos**
   (21.2(b)(c)(e)(h)(i)) — los controles organizativos quedan fuera del alcance declarado.

**Estado del F13-GATE:** con R-091–R-096 entregados, todos los criterios técnicos del gate
están cumplidos. El criterio "revisado contra el texto normativo" queda satisfecho por este documento.

---

## Próximos pasos recomendados

- Contratar una revisión por consultor externo antes de la primera venta del módulo a un cliente
  con obligación NIS2 real (entidad esencial o importante según RD-ley 7/2025).
- Añadir familia 14 (ENS `op.exp.11` — pruebas de intrusión periódicas) en un ciclo posterior
  si la base de clientes lo demanda.
- Revisar si `op.mon.1` vs `op.mon.2` es necesario distinguir para nivel ENS alto.
