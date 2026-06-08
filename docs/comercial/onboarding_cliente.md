# Onboarding de nuevo cliente — Vigex
## R-084 / Ruta 11.1

Checklist completo para activar un nuevo cliente desde el primer contacto
hasta que el panel esté funcionando en producción y el cliente lo use con autonomía.

---

## Fase A — Preventa (antes de firmar)

| # | Tarea | Responsable | Estado |
|---|-------|-------------|--------|
| A1 | Enviar propuesta comercial (`docs/comercial/plantilla_propuesta.md`) | Vigex | ☐ |
| A2 | Clarificar perfil: número de servidores, servicios monitorizados, BD | Vigex | ☐ |
| A3 | Confirmar plan (Lite / Standard / Pro) y precio mensual | Vigex + Cliente | ☐ |
| A4 | Acordar fecha de instalación (recomendar: martes-jueves, horario de menos actividad) | Vigex + Cliente | ☐ |
| A5 | Obtener datos técnicos: IPs de los servidores, OS, acceso SSH root/sudo | Cliente | ☐ |
| A6 | Cliente acepta términos y política de privacidad | Cliente | ☐ |
| A7 | Configurar método de pago (Stripe Payment Link o transferencia + factura) | Cliente | ☐ |

---

## Fase B — Instalación técnica

### B1 — Preparar la instalación

```bash
# En tu máquina Windows, desde la raíz del repo:
# 1. Copiar config.env.example del cliente
cp deploy/api/package/config.env.example /tmp/config_cliente_EMPRESA.env

# 2. Editar con los datos del cliente:
#    - IPs de los servidores según perfil
#    - SECRET_KEY (generar nuevo)
#    - ADMIN_PASSWORD (hash bcrypt)
#    - Configuración SMTP del cliente
#    - CENTRAL_SUPPORT_TOKEN (generado en el panel central)
notepad /tmp/config_cliente_EMPRESA.env
```

### B2 — Ejecutar el instalador

```powershell
# Usar el asistente Windows (Ruta 8.2):
.\tools\windows\instalar_vigex_windows.ps1
```

O desde SSH directamente:
```bash
# Copiar el repo y ejecutar el instalador en el servidor API del cliente
ssh admin@IP_SERVIDOR_CLIENTE
sudo bash /tmp/deploy/api/install_vigex_api.sh
```

### B3 — Verificación técnica post-instalación

| Check | Comando | Esperado |
|-------|---------|---------|
| Servicio activo | `systemctl status vigex-api` | `Active: active (running)` |
| Panel accesible | `curl -I http://localhost:8000` | `HTTP/1.1 200 OK` |
| HTTPS (si nginx instalado) | `curl -I https://IP_CLIENTE` | `HTTP/2 200` |
| SSH al servidor DB | `ssh vigex@IP_DB hostname` | hostname sin contraseña |
| Backup de prueba | Panel → Copias → Ejecutar ahora | Estado `OK` en historial |
| Alerta de prueba | Panel → Alertas → Probar alertas | Email/Telegram recibido |
| Heartbeat Central | Central → Salud global | Cliente aparece en 🟢 verde |

---

## Fase C — Formación del cliente

### Duración: 60-90 minutos (videollamada o presencial)

| # | Tema | Tiempo |
|---|------|--------|
| C1 | Acceder al panel (URL, contraseña, móvil) | 10 min |
| C2 | Dashboard: qué significa cada tarjeta | 10 min |
| C3 | Copias de seguridad: cuándo se hacen, cómo verificarlas | 15 min |
| C4 | Servicios monitorizados: añadir/quitar servicios | 10 min |
| C5 | Alertas: configurar email/Telegram, probar | 15 min |
| C6 | Cómo abrir un ticket de soporte desde el panel | 5 min |
| C7 | Runbook `/recuperacion`: qué hacer si algo falla | 10 min |
| C8 | Preguntas | ∞ |

### Material para entregar al cliente

- [ ] URL del panel con HTTPS
- [ ] Usuario y contraseña admin (en papel o gestor de contraseñas)
- [ ] Guía rápida PDF: `deploy/api/package/static/docs/guia_alertas_telegram.pdf`
- [ ] Contacto de soporte: `soporte@vigexpyme.es` y cómo abrir ticket desde el panel

---

## Fase D — Primera semana (seguimiento)

| Día | Acción |
|-----|--------|
| Día 1 (post-instalación) | Verificar que el backup nocturno se ejecutó correctamente |
| Día 3 | Llamada de 15 min: ¿alguna duda? ¿ha visto las alertas? |
| Día 7 | Revisar el historial de backups (7 ejecuciones, todas OK) |
| Día 7 | Verificar que el cliente ha cambiado la contraseña por defecto |
| Día 30 | Primera revisión mensual: disco, servicios, alertas, informe enviado |

---

## Fase E — Alta en sistemas Vigex

| Acción | Herramienta | Notas |
|--------|-------------|-------|
| Alta en panel central | Central → Clientes → Nuevo | Genera token, configúralo en config.env del cliente |
| Alta en hoja de clientes | Propia hoja de cálculo | Nombre, plan, IP, fecha alta, próxima renovación |
| Crear carpeta del cliente | `docs/clientes/<empresa>/` | IP, notas técnicas, incidencias |
| Configurar recordatorio de renovación | Calendario | 7 días antes del vencimiento |
| Registrar factura inicial | Holded / Quipu | Número de factura, importe, fecha |

---

## Checklist de cierre de onboarding

**Técnico:**
- [ ] Panel instalado y accesible con HTTPS
- [ ] Primer backup OK en historial
- [ ] Alertas configuradas y probadas (email o Telegram)
- [ ] Heartbeat llegando a la Central (🟢 en Salud global)
- [ ] Cliente en panel central con token activo

**Comercial:**
- [ ] Primer pago recibido (Stripe o transferencia)
- [ ] Factura emitida
- [ ] Datos del cliente registrados en hoja de clientes
- [ ] Recordatorio de renovación en el calendario

**Relación:**
- [ ] Formación realizada y confirmada por el cliente
- [ ] Material de soporte entregado
- [ ] Seguimiento a 7 días completado
- [ ] Cliente puede abrir un ticket de soporte de forma autónoma
