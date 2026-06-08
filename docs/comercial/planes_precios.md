# Planes y precios — DASC Server Manager
## R-074 / Ruta 9.3

> Documento interno de definición de precios. Actualiza antes de publicar.
> Los precios de la landing page (`web/index.html`) deben coincidir con este documento.

---

## Estructura de planes

| Plan | Perfil cliente | Servidores | Precio/mes | Precio/año |
|------|---------------|-----------|-----------|-----------|
| **DASC Lite** | Autónomo o microempresa (1–3 personas) | 1 | €15 | €150 (ahorro €30) |
| **DASC Standard** | PyME 5–50 empleados | Hasta 2 | €35 | €350 (ahorro €70) |
| **DASC Pro** | Empresa con criticidad media-alta | 3+ | €65 | €650 (ahorro €130) |
| **DASC Managed** | Cliente que delega la gestión | Según acuerdo | Consultar | Consultar |

> **Nota de posicionamiento:** La competencia (Nagios XI ~€1.650/año, Zabbix Enterprise ~€500+/año)
> está pensada para equipos técnicos. DASC es 10× más barato y no requiere conocimientos avanzados.

---

## Qué incluye cada plan

### DASC Lite (€15/mes)
- ✅ Instalación en 1 servidor Ubuntu
- ✅ Copias de seguridad completas (script backups_api.sh)
- ✅ Monitoreo básico: CPU, RAM, disco, uptime
- ✅ Alertas por email cuando algo falla
- ✅ Informes periódicos por email
- ✅ Panel web con acceso por usuario y contraseña
- ✅ Soporte por email (respuesta orientativa 48h laborables)
- ❌ Backups incrementales/diferenciales
- ❌ Alertas por Telegram
- ❌ Logs avanzados con búsqueda
- ❌ Test de restauración incluido

### DASC Standard (€35/mes) — Recomendado PyME
- ✅ Todo lo de Lite
- ✅ Hasta 2 servidores (panel + backups separados)
- ✅ Backups completos + incrementales
- ✅ Monitoreo avanzado con gráficas y tendencias
- ✅ Alertas por email **y** Telegram
- ✅ Verificación SHA256 de todas las copias
- ✅ Informes personalizables (secciones, frecuencia, canal)
- ✅ Gestión de servicios remotos
- ✅ Control de usuarios con permisos por módulo
- ✅ Soporte por email prioridad (respuesta garantizada 24h laborables)
- ❌ Test de restauración mensual incluido

### DASC Pro (€65/mes)
- ✅ Todo lo de Standard
- ✅ Hasta 3 servidores distribuidos (panel, DB, backups separados)
- ✅ Backups completos + incrementales + diferenciales
- ✅ Runbook DRO (Disaster Recovery Orchestration) en el panel
- ✅ Test de restauración incluido trimestralmente
- ✅ Revisión mensual del sistema por parte del proveedor
- ✅ Soporte prioritario email + teléfono (respuesta 4h laborables)
- ✅ Informe mensual ejecutivo para dirección

### DASC Managed (precio bajo consulta)
- ✅ Todo lo de Pro
- ✅ Mantenimiento mensual activo (actualizaciones, revisiones)
- ✅ Monitorización proactiva por parte del proveedor
- ✅ SLA personalizado según criticidad del cliente
- ✅ Onboarding completo del equipo del cliente

---

## Tarifas de instalación

| Concepto | Precio |
|----------|--------|
| Instalación incluida en plan anual | €0 |
| Instalación en plan mensual | €150 (único pago) |
| Instalación en entorno multi-servidor (Standard/Pro) | €150 (único pago) |
| Migración desde otra herramienta | Consultar (€/hora) |

---

## Métodos de pago

1. **Tarjeta bancaria** — via Stripe (Visa, Mastercard, Amex). Cobro automático.
2. **Transferencia bancaria** — factura proforma previa. Para empresas que necesiten PO.
3. **Domiciliación SEPA** — disponible para contratos anuales. Solicitar.

**Factura**: Se emite factura con todos los datos fiscales. IVA incluido en los precios listados.

---

## Política de prueba / piloto

- **Demo técnica gratuita**: 30-60 minutos en entorno controlado, sin acceso a datos reales. A solicitar por email.
- **Piloto de 30 días**: precio reducido 50% el primer mes en plan Standard o Pro, con opción de cancelación sin coste.
- **POC (Proof of Concept)**: instalación en VM del cliente por €0 si se convierte en cliente en 60 días.

---

## Criterios para subir de plan

| Indicador | Lite → Standard | Standard → Pro |
|-----------|----------------|----------------|
| Nº servidores | >1 | >2 |
| Backups diferenciales necesarios | No disponible | Necesario |
| Criticidad de los datos | Baja | Media-alta |
| SLA exigido | No necesario | Necesario |

---

## Notas para ajuste futuro de precios

- Los precios actuales son de introducción al mercado. Se revisarán cuando haya >5 clientes activos.
- El IVA aplicable es el 21% (España). Los precios listados ya lo incluyen.
- Para clientes con sede fuera de España (UE), el IVA puede variar por B2B intracomunitario.
- Considerar plan anual con descuento del 15-17% para fidelizar.
