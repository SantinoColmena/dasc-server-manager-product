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

- [ ] **Dominio profesional activo** (p.ej. `vigexpyme.es`) ⏳
- [ ] **Email profesional** (`soporte@vigexpyme.es`) funcionando ⏳
- [ ] **Cuenta Stripe activa** con verificación KYC completada ⏳
- [ ] **Payment Links** creados para cada plan ⏳
- [ ] **Landing page publicada** con HTTPS real ⏳
- [ ] **Términos de servicio** con datos fiscales reales publicados ⏳
- [ ] **Política de privacidad** con datos fiscales reales publicados ⏳

## 3. Legal y fiscal

- [ ] **Alta como autónomo o empresa** en la Agencia Tributaria ⏳
      *(si no tienes alta, no puedes emitir facturas)*
- [ ] **Número de factura registrado** en tu sistema de facturación (Holded/Quipu) ⏳
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
