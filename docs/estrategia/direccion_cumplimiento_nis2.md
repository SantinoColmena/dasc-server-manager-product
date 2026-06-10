# Dirección estratégica — Vigex como máquina de evidencias de cumplimiento

> **Estado:** Decisión adoptada · 2026-06-11
> **Tipo:** Documento de dirección (ancla el *porqué* de la Fase 13 del `ROADMAP.md`).
> **Resumen en una frase:** Vigex deja de competir solo como "panel de backups y
> monitorización" y pasa a posicionarse como **la fuente de evidencias técnicas
> automáticas** que las plataformas de cumplimiento (GRC) piden y que hoy el
> cliente rellena a mano, aprovechando la ola regulatoria NIS2/ENS/ISO 27001.

---

## 1. Por qué este giro (y por qué ahora)

### 1.1 El problema del posicionamiento actual

Vigex, como producto de "backups + monitorización + servicios para PyME Linux
autohospedada", ocupa un nicho real y pegajoso, pero con tres techos estructurales:

1. **Mercado que se aplana.** Cada año más PyMEs migran a SaaS puro o cloud
   gestionado donde el backup ya viene incluido. El TAM no crece.
2. **Compite contra "gratis" y contra "el primo informático".** Veeam, Bacula,
   Proxmox Backup Server, Restic, Uptime Kuma existen y son gratis o baratos. El
   valor de Vigex nunca fue la tecnología: es el **servicio gestionado y el panel
   unificado**.
3. **Venta lenta y artesanal**, propia de un negocio de servicio (MSP boutique),
   no de un SaaS que escala solo.

### 1.2 La palanca regulatoria (verificada, no especulativa)

La **Directiva NIS2 ya es obligatoria en España**:

- Transposición vía **Real Decreto-ley 7/2025** + el Real Decreto que la completa,
  **en vigor desde abril de 2026**, con un plazo máximo de **9 meses** para que las
  entidades esenciales e importantes se adapten plenamente.
- España incumplió el plazo del 17-oct-2024; la Comisión elevó el caso al TJUE.
  El retraso se ha resuelto activando la obligación con urgencia.
- **Sanciones** de hasta **10 M€ o el 2 % de la facturación** (entidades
  esenciales) y **7 M€ o el 1,4 %** (importantes). Novedad potente:
  **responsabilidad personal de los administradores**, que pueden ser inhabilitados.
- **Notificación de incidentes obligatoria**: alerta temprana en **24 h** e
  informe formal en **72 h** al CSIRT nacional. El incumplimiento del plazo es
  sancionable por sí solo.

Marcos relacionados que comparten el mismo mecanismo de "demostrar con evidencias":

- **ENS** (RD 311/2022): obligatorio si se presta servicio al sector público.
- **ISO 27001:2022**: voluntaria pero la más demandada comercialmente; no depende
  de a quién se venda, lo que la hace la más "vendible".

> La conclusión: el cumplimiento no es una ola futura. Es **ahora**, con empresas
> corriendo y con miedo regulatorio real (la palanca de compra más fuerte).

### 1.3 Qué necesidad real cubre un producto de cumplimiento

Una norma como NIS2/ENS/ISO no pide "ser seguro": pide **demostrar que lo eres,
por escrito, de forma continua y ante un auditor**. El dolor no es técnico, es de
**papel y continuidad**: la PyME *quizá* hace backups y revisa logs, pero cuando
llega la auditoría (o el incidente con notificación en 24 h) **no tiene el dossier
de evidencias** — tiene capturas sueltas, un Excel y correos.

El software de cumplimiento hace solo tres cosas:
1. **Mapea la norma a controles concretos** (checklist accionable).
2. **Recoge y conserva la evidencia** de cada control (datada, íntegra, retenida).
3. **Genera el dossier y avisa de lo que caduca** (auditoría continua, no anual).

---

## 2. El hueco real: dónde encaja Vigex

### 2.1 La competencia ya existe (análisis de mercado)

La categoría **está madura, no virgen**. Mapa en tres ligas:

| Liga | Jugadores | Posición | Precio | ¿Pelea de Vigex? |
|---|---|---|---|---|
| **1 — Gigantes internacionales** | Vanta, Drata, Secureframe, Sprinto | Estándar mundial, +20 marcos, cientos de integraciones | ~7.000–15.000 €/año | ❌ No competir de frente |
| **2 — GRC español enterprise** | GlobalSuite (+2.000 empresas), ISOTools, GRCTools, Pilar/Hard2bit | Potentes pero pesados, orientados a mediana-grande con consultor | Proyecto, sin precio público | ❌ Demasiado grandes para micro-PyME |
| **3 — PyME asequible** | Mencar (225 €/mes "as a service"), RiskRegister.ai (49 €/mes), Novaciber, Cibersafety | Donde está la acción real | 49–225 €/mes | 🟡 Mercado validado pero ocupado |

**Conclusión del análisis competitivo:** construir "otro GRC genérico" llega tarde
y sin foso. **No se hará.**

### 2.2 La grieta que nadie cubre

Todos los GRC son fuertes en **el papeleo** (políticas, cuestionarios, gestión
documental) y **débiles o manuales en la evidencia técnica real**. Piden al
cliente: *"sube la prueba de que haces backups", "demuestra que monitorizas",
"adjunta el log de accesos"* — y el cliente lo sube **a mano**.

> **Eso es exactamente lo que Vigex ya genera automáticamente.**

### 2.3 El posicionamiento elegido (una frase)

> **"El cumplimiento que se rellena solo porque tu infraestructura ya está
> conectada."**

Vigex **no compite** con GlobalSuite/Vanta — **los alimenta**, o se queda con el
trozo concreto (continuidad, backup, monitorización, accesos, trazabilidad) que
ellos hacen a mano y Vigex automatiza. Es un diferenciador **defendible para un
solo-founder** porque reutiliza ~80 % de lo ya construido y nadie más lo tiene
atado a la infraestructura real del cliente.

---

## 3. Alcance: Camino A ahora, Camino B condicionado

| | **Camino A — Módulo dentro de Vigex** *(elegido)* | **Camino B — SaaS de evidencias independiente** *(futuro)* |
|---|---|---|
| Qué es | Pestaña "Cumplimiento" sobre el panel actual | Producto aparte que se conecta a *cualquier* infraestructura |
| Mercado | Clientes Vigex actuales (upsell) | Mucho mayor, no atado a la instalación |
| Esfuerzo | Bajo (capa fina sobre lo existente) | Alto |
| Riesgo | Bajo | Alto |
| Decisión | **Se construye primero (Fase 13)** | **Se escinde solo si A valida demanda** |

**Criterio de bifurcación A→B:** si los clientes pagan por las evidencias **más**
que por los backups, el Camino B tiene mercado y se escinde como producto. Hasta
entonces, dispersarse mata.

> **Importante — esto es una extensión, no un derribo.** La nueva dirección **no
> tira** lo construido (Fases 0–12). Las acciones pendientes de las Fases 9–11
> (dominio, web, Stripe, legal) siguen siendo prerrequisito de cualquier venta,
> con cumplimiento o sin él. La Fase 13 **añade el diferenciador comercial** que
> hace que Vigex deje de venderse como "otro panel de backups".

---

## 4. Qué de esto ya está hecho

Vigex ya cubre, de forma **automática**, el 70–80 % de la evidencia **técnica y
operativa** que piden NIS2/ENS/ISO. El detalle control-por-control está en el
documento técnico de referencia:

➡️ [`docs/cumplimiento/mapa_controles_evidencias.md`](../cumplimiento/mapa_controles_evidencias.md)

Resumen: las familias de control **fuertes** (continuidad/backup y monitorización)
están ✅ casi listas; las **operativas** (incidentes, accesos, logs, informes,
cifrado) están 🟡 a un empujón — falta convertir el dato en **evidencia auditable**
(datarla, sellarla, mapearla, retenerla). Las familias de **papeleo** (riesgos,
políticas, formación, proveedores) ❌ **no se persiguen**: ahí los GRC ganan y
Vigex se integra o cede.

---

## 5. Riesgos y cómo se mitigan

| Riesgo | Mitigación |
|---|---|
| Afirmar cobertura de un control que el auditor rechace | Ruta 13.6: validar el mapa contra el **texto normativo real** (ISO Annex A / ENS / NIS2 art. 21) antes de venderlo. Nunca prometer "cumplimiento total". |
| Que el cliente espere "cumplimiento NIS2 completo" | Mensaje acotado: *"evidencias técnicas automáticas"*, no consultoría de cumplimiento. Se complementa con consultor/GRC, no lo sustituye. |
| Responsabilidad legal por dar por bueno un cumplimiento | Mantener la línea de `docs/legal/limites_responsabilidad.md`: Vigex aporta evidencia, no certifica. |
| Competencia que copie el ángulo | El foso es la **conexión a la infraestructura real** + base de clientes Vigex, no el concepto. |

---

## 6. Decisión

Se adopta el **Camino A**: construir un **módulo de cumplimiento / evidencias
automáticas** sobre Vigex como nueva dirección estratégica del producto,
formalizado como **Fase 13** del roadmap canónico (tareas `R-091`+). Se mantiene
el parámetro rector del proyecto: **calidad real "al milímetro" por encima de
velocidad**.

---

## Fuentes (verificadas 2026-06-11)

- NIS2 ya obligatoria en España — Revista Ciberseguridad:
  <https://www.revistaciberseguridad.com/2026/06/la-directiva-nis2-ya-es-obligatoria-en-espana-que-deben-hacer-las-empresas-para-cumplir/>
- NIS2 España, plazos y obligaciones 2026 — Secra:
  <https://secra.es/es/blog/nis2-espana-como-cumplir-normativa-2026>
- Guía NIS2 para PyMEs — Fase Consulting:
  <https://www.faseconsulting.es/articulos/directiva-nis2-ciberseguridad-empresas-espana-pymes-2026>
- Software ENS y gestión de evidencias — ISOTools:
  <https://isotools.org/esquema-nacional-de-seguridad/>
- Guía ENS 2026 — Legiscope:
  <https://www.legiscope.com/blog/esquema-nacional-seguridad-ens-guia.html>
- Coste certificación ISO 27001 España — Cibersafety:
  <https://cibersafety.com/coste-certificacion-iso-27001/>
- Comparativa Vanta/Drata/Secureframe/Sprinto — Sprinto:
  <https://sprinto.com/blog/secureframe-vs-vanta-vs-drata/>
- Mencar (cumplimiento GRC PyME as-a-service): <https://www.mencargc.es/cumplimiento-as-a-service/>
- RiskRegister.ai (GRC ISO 27001/NIS2): <https://riskregister.ai/>
- GlobalSuite Solutions (GRC líder España): <https://www.globalsuitesolutions.com/es/>
