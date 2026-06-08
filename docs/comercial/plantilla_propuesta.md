# Plantilla de propuesta comercial — Vigex
## R-084 / Ruta 11.1

> **Uso:** copiar este documento, sustituir los campos marcados entre `[CORCHETES]`
> y enviar al prospecto. Disponible también como base para un PDF formal.

---

# Propuesta de servicio — Vigex

**Fecha:** [DD/MM/AAAA]  
**Válida hasta:** [DD/MM/AAAA + 30 días]  
**Número de propuesta:** PROP-[AAAA]-[NNN]

---

## Para

**Empresa:** [NOMBRE_EMPRESA]  
**Contacto:** [NOMBRE_CONTACTO], [CARGO]  
**Email:** [EMAIL_CONTACTO]

---

## De

**Vigex**  
[TU_NOMBRE_COMPLETO]  
[NIF/CIF]  
[DIRECCIÓN_FISCAL]  
soporte@vigexpyme.es  

---

## Resumen ejecutivo

Vigex es un panel de control web que centraliza la gestión de
backups, servicios, logs, alertas y restauración de datos de los servidores de
[NOMBRE_EMPRESA]. Se instala en la propia infraestructura del cliente — sus datos
nunca salen de sus servidores.

**El problema que resuelve:** actualmente [NOMBRE_EMPRESA] gestiona sus servidores
de forma manual o con herramientas dispersas. Un fallo de backup puede tardar días
en detectarse. Vigex lo hace visible en segundos y notifica proactivamente.

---

## Situación actual del cliente

> *(Rellenar con lo que hayas descubierto en la reunión previa)*

- Número de servidores: [N]
- Servicios críticos monitorizados: [LISTA]
- Proceso actual de backups: [DESCRIPCIÓN]
- Principal preocupación: [DESCRIBIR]

---

## Plan propuesto

### [PLAN_ELEGIDO] — [PRECIO]€/mes

| Característica | Incluido |
|----------------|---------|
| Panel web accesible desde cualquier navegador (PC/móvil) | ✅ |
| Backups automáticos programados con verificación SHA256 | ✅ |
| Alertas por email y Telegram (disco lleno, backup fallido, servicio caído) | ✅ |
| Historial de backups y estado de servicios | ✅ |
| Logs centralizados con búsqueda | ✅ |
| Runbook de recuperación ante desastres | ✅ |
| Acceso soporte técnico vía ticket desde el panel | ✅ |
| Informes automáticos (diario/semanal/mensual) | ✅ |
| Instalación y puesta en marcha | ✅ |

> **Arquitectura para [NOMBRE_EMPRESA]:** [PERFIL_ELEGIDO] — [DESCRIPCION_PERFIL]

---

## Inversión

| Concepto | Precio |
|----------|--------|
| Servicio Vigex [PLAN] — cuota mensual | [PRECIO]€/mes + IVA |
| Instalación y configuración inicial | [0€ (anual) / 150€ (mensual)] |
| Formación de 60 min (videollamada) | Incluida |

**Importe mensual total:** [PRECIO_TOTAL]€/mes + IVA (21%)

---

## Condiciones del servicio

- **Contrato:** mensual, con cancelación con 15 días de preaviso.
- **Instalación:** en la infraestructura del cliente; no requiere cloud externo.
- **Datos:** permanecen 100% en los servidores del cliente.
- **SLA:** tiempo de respuesta a incidencias P1 < [N]h en horario laboral.
  Ver `web/legal/terminos.html` para detalle completo.
- **Política piloto:** descuento del 50% el primer mes (precio especial de €[PILOTO]/mes).
- **Pago:** mensual por adelantado. Métodos: Stripe (tarjeta/SEPA) o transferencia.

---

## Siguientes pasos

1. Confirmar el plan y la fecha de instalación.
2. Proporcionar acceso SSH temporal a los servidores (o acordar asistencia presencial).
3. Firmar los términos de servicio (enlace: [URL_TERMINOS]).
4. Abonar el primer mes (Stripe Payment Link: [URL_STRIPE] o datos bancarios en factura).
5. Instalación y formación en la fecha acordada.

---

## Preguntas frecuentes

**¿Mis datos salen de mi empresa?**  
No. Vigex se instala directamente en tus servidores. Los backups y los logs
quedan en tu propia infraestructura. Solo los tickets de soporte se envían al
sistema de gestión del equipo Vigex.

**¿Necesito saber de Linux para usarlo?**  
No. El panel es web, desde cualquier navegador. Las operaciones cotidianas
(ver estado, configurar alertas, abrir un ticket) no requieren conocimientos técnicos.

**¿Qué pasa si quiero cancelar?**  
Con 15 días de preaviso, el servicio se da de baja. Te entregamos las instrucciones
para desinstalar el panel de forma limpia; todos los datos quedan en tus servidores.

**¿Funciona con Windows Server?**  
Vigex corre en el servidor Linux que gestiona tus backups y servicios. Si tus servidores
son Windows, es compatible via SSH/SFTP para transferencia de backups. Consultar caso por caso.

---

*Esta propuesta se rige por los Términos de Servicio de Vigex disponibles en
[URL_TERMINOS_COMPLETOS]. Vigex es un servicio de [TU_NOMBRE/EMPRESA],
[NIF/CIF], [DIRECCIÓN]. No garantizamos la ausencia de interrupciones del servicio;
ver SLA completo en los términos.*
