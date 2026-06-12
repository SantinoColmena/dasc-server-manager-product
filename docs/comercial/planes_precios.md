# Planes y precios — Vigex
## R-074 / Ruta 9.3

> Documento interno de definición de precios. Actualiza antes de publicar.
> Los precios de la landing page (`web/index.html`) deben coincidir con este documento.

---

## Modelo comercial

Vigex usa un modelo de **licencia de pago único** + soporte técnico opcional de suscripción mensual.

- El cliente paga **una vez** por la licencia y el software es suyo para siempre.
- La instalación está incluida en todos los planes de licencia.
- El soporte técnico (actualizaciones, atención, IA avanzada) es **opcional** y mensual.
- Sin soporte contratado, el panel sigue funcionando con normalidad.

---

## Licencias (pago único)

| Plan | Servidores | Precio | Público objetivo |
|------|-----------|--------|-----------------|
| **Vigex Lite** | 1 | **€179** | Autónomo o microempresa (1–5 personas) |
| **Vigex Standard** | Hasta 2 | **€299** | PYME 5–50 empleados (opción recomendada) |
| **Vigex Pro** | Hasta 3 | **€499** | Empresa con criticidad media-alta |
| **Vigex Managed** | Según acuerdo | Consultar | Cliente que delega la gestión completa |

Todos los planes incluyen instalación. No hay coste adicional por instalar en 1 o 2 servidores dentro del límite del plan.

---

## Qué incluye cada licencia

### Vigex Lite — €179
- ✅ Panel instalado en 1 servidor Ubuntu
- ✅ Copias de seguridad completas (programación automática)
- ✅ Monitoreo básico: CPU, RAM, disco, uptime
- ✅ Alertas por email cuando algo falla
- ✅ Informes periódicos automáticos por email
- ✅ Control de usuarios con permisos por módulo
- ✅ Instalación incluida
- ❌ Copias incrementales/diferenciales
- ❌ Alertas por Telegram
- ❌ Asistente IA
- ❌ Gestión de servicios remotos

### Vigex Standard — €299 (recomendado)
- ✅ Todo lo de Lite
- ✅ Hasta 2 servidores (panel + copias separados)
- ✅ Copias completas + incrementales
- ✅ Monitoreo avanzado con gráficas y tendencias
- ✅ Alertas por email y Telegram
- ✅ Verificación de integridad de copias
- ✅ Informes personalizables (secciones, frecuencia, canal)
- ✅ Gestión de servicios remotos
- ✅ Asistente IA (modelo básico)
- ✅ Instalación incluida

### Vigex Pro — €499
- ✅ Todo lo de Standard
- ✅ Hasta 3 servidores distribuidos (panel, BD, copias separados)
- ✅ Copias completas + incrementales + diferenciales
- ✅ Guía de recuperación integrada en el panel
- ✅ Prueba de restauración incluida en la instalación
- ✅ Informes con historial completo
- ✅ Asistente IA avanzado incluido
- ✅ Módulo de cumplimiento NIS2/ENS/ISO 27001
- ✅ Instalación incluida

### Vigex Managed — precio bajo consulta
- ✅ Todo lo de Pro
- ✅ Mantenimiento mensual activo (actualizaciones, revisiones)
- ✅ Monitorización proactiva por parte del proveedor
- ✅ SLA personalizado según criticidad del cliente
- ✅ Informe mensual ejecutivo para dirección
- ✅ Onboarding completo del equipo del cliente

---

## Soporte técnico (suscripción mensual — opcional)

| Plan | Precio | Canal | Tiempo de respuesta | Incluye |
|------|--------|-------|---------------------|---------|
| **Básico** | €19/mes | Email | 48h laborables (orientativo) | Actualizaciones del software |
| **Plus** | €39/mes | Email | 24h laborables (garantizado) | Actualizaciones + asistente IA avanzado + acceso Central |
| **Premium** | €59/mes | Email + Teléfono | 4h laborables (garantizado) | Todo Plus + revisión trimestral del sistema |

- El soporte Plus y Premium incluyen acceso al asistente IA vía Vigex Central (cuota ampliada).
- Sin plan de soporte: el panel funciona normalmente pero sin actualizaciones ni atención técnica garantizada.
- El soporte base para plan Pro arranca en **€29/mes**.

---

## Comparativa con el mercado (referencia)

| Competidor | Precio anual | Req. técnico | Backup incluido |
|-----------|-------------|-------------|----------------|
| Vigex Standard | **€299 one-time** | No | Sí |
| PRTG Network Monitor | ~€1.650/año | Sí | No |
| Checkmk Cloud | ~€2.400/año | Sí | No |
| Atera / NinjaOne | ~€1.500–€1.800/año | Sí | No |
| Better Stack | ~€600/año | No | No |
| Acronis (backup solo) | ~€595/año/servidor | Sí | Sí |

Vigex es la única opción del segmento que combina monitorización + copias + alertas en un panel no-técnico con licencia perpetua.

---

## Métodos de pago

1. **Tarjeta bancaria** — vía Stripe (Visa, Mastercard, Amex). Cobro inmediato.
2. **Transferencia bancaria** — factura proforma previa. Para empresas que necesiten orden de compra.

**Factura**: Se emite factura con todos los datos fiscales. IVA 21% incluido en los precios listados.

---

## Política de piloto / introducción

- **Demo técnica gratuita**: 30–60 minutos en entorno controlado, sin acceso a datos reales.
- **Piloto de 30 días**: 50% de descuento el primer mes de soporte Plus o Premium, con opción de cancelación sin coste.
- **POC gratuito**: instalación en VM del cliente por €0 si se convierte en cliente en 60 días.

---

## Criterios para recomendar un plan

| Situación del cliente | Plan recomendado |
|----------------------|-----------------|
| 1 servidor, presupuesto ajustado | Lite |
| 1–2 servidores, quiere copias verificadas + Telegram | Standard |
| 3 servidores o datos críticos | Pro |
| Sin tiempo para gestionar nada | Managed |

---

## Notas para revisión futura de precios

- Los precios actuales son de introducción al mercado. Se revisarán cuando haya más de 5 clientes activos.
- El IVA aplicable es el 21% (España). Para clientes UE fuera de España, aplicar B2B intracomunitario.
- Considerar descuento por pago anticipado del soporte anual (~15%) cuando haya demanda suficiente.
