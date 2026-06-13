# Checklist de primera venta — Vigex
## R-084 / Ruta 11.1

Lista de verificación que DEBE estar completa antes de aceptar dinero de un cliente.
No es burocracia: cada punto evita un problema real.

---

## 1. Producto listo

- [ ] **F7-GATE superado** — panel visualmente cuidado, dashboard funcional. ✅ 2026-06-08
- [ ] **F8-GATE superado** — proceso de actualización y recuperación documentado. ✅ 2026-06-08
- [ ] **La instalación funciona en el perfil del cliente** — ejecutar el smoke test:
      `tools/windows/smoke_test_release.ps1` en verde.

## 2. Infraestructura de negocio lista

- [x] **Dominio profesional activo** — `vigex.es` ✅ 2026-06-13
- [x] **Email profesional** — `soporte@vigex.es` funcionando ✅ 2026-06-13
- [x] **Cuenta Stripe activa** con Payment Links creados ✅ 2026-06-13
  - Lite €179 · Standard €299 · Pro €499 (pago único)
  - Soporte Básico €19 · Plus €39 · Premium €59 · Básico Pro €29 (mensual)
- [x] **Landing page publicada** en `vigex.es` con HTTPS (Netlify) ✅ 2026-06-13
- [x] **Términos de servicio** con datos fiscales y NIF reales publicados ✅ 2026-06-13
- [x] **Política de privacidad** con datos fiscales reales publicados ✅ 2026-06-13
- [ ] **Vigex Central en VPS con HTTPS** — actualmente en instancia temporal; mover a VPS
      antes de la primera renovación de soporte. No bloquea la primera venta.

## 3. Legal y fiscal

- [ ] **Alta como autónomo** en la Agencia Tributaria — hacer antes de emitir la primera factura.
      El DNI (55325787T) ya consta en los documentos legales.
- [ ] **Número de factura registrado** en sistema de facturación (Holded/Quipu) ⏳
- [ ] **Entiende las obligaciones fiscales**: IVA trimestral, IRPF si procede ⏳
      *(recomendado: consultar con gestor antes de la primera factura)*

## 4. Operativo listo para el cliente

- [ ] **Vigex Central** en VPS con HTTPS real ⏳
      *(ver `docs/guias/guia_central_vps.md`)*
- [ ] **Proceso de onboarding** probado en al menos una instalación real
      *(usar `deploy/api/onboarding_nuevo_cliente.sh`)*
- [ ] **Tiempo de respuesta definido** para incidencias P1-P4
      *(ver SLA en `web/legal/terminos.html`)*
- [ ] **Plan de recuperación** documentado y probado una vez
      *(ver `docs/tecnico/plan_recuperacion.md`)*

## 5. El cliente específico

- [ ] **Presentación demo** realizada — cliente ha visto el panel en funcionamiento
- [ ] **Perfil acordado** (Lite / Standard / Pro) con IPs de los servidores confirmadas
- [ ] **Acceso SSH temporal** obtenido para la instalación
- [ ] **Email de contacto técnico** del cliente confirmado
- [ ] **Fecha de instalación** acordada

---

## Qué pasa si falta algún punto

Si falta algún punto de **Producto** o **Legal**:
> No vender. El riesgo para el cliente y para ti no está controlado.

Si falta algún punto de **Infraestructura de negocio**:
> Puedes hacer un piloto informal (precio reducido, factura manual, sin contrato),
> pero complétalo antes de la segunda renovación.

Si falta algún punto de **El cliente específico**:
> No instalar sin acceso SSH y fecha confirmada.

---

## Primer cliente de pago (R-048)

Este es el criterio real de cierre del **F9-GATE "Primer cliente de pago"**.

- [ ] Todos los puntos anteriores en verde ✅
- [ ] Instalación realizada
- [ ] Primer pago recibido y factura emitida
- [ ] **R-048 puede cerrarse** → primera venta documentada en `docs/validaciones/R-048_primer_cliente.md`
