# Plantilla email de bienvenida post-instalación

**Cuándo enviarlo:** el mismo día que termina la instalación, antes de cerrar la videollamada o dentro de las 2 horas siguientes.

**Desde:** soporte@vigex.es  
**Asunto:** Tu panel Vigex está listo — accesos y primeros pasos

---

## Plantilla (copiar y adaptar)

---

Hola [Nombre],

Tu panel Vigex ya está instalado y funcionando en tu servidor. Aquí tienes todo lo que necesitas para empezar:

---

**Acceso al panel**

URL: https://[IP_O_DOMINIO_CLIENTE]  
Usuario: admin  
Contraseña: [CONTRASEÑA_INICIAL]

> Te recomendamos cambiar la contraseña la primera vez que entres:
> Panel → icono de usuario (arriba a la derecha) → Cambiar contraseña

---

**Qué ya está configurado**

✅ Copias de seguridad automáticas cada día a las [HORA_BACKUP]  
✅ Monitorización de servicios: [LISTA_SERVICIOS]  
✅ Alertas por [EMAIL/TELEGRAM] cuando algo falle  
✅ Informe semanal automático al email [EMAIL_CLIENTE]

---

**Primeros pasos recomendados**

1. Entra al panel y comprueba que el dashboard muestra todo en verde.
2. Ve a **Copias → Historial** y verifica que aparece el backup de hoy.
3. Si quieres activar alertas por Telegram: escríbele a @VigexPanelBot en Telegram, envía `/start`, luego `/chatid`, y pega el número en Panel → Alertas → Telegram.
4. Cambia la contraseña de admin.

---

**¿Algo no va bien?**

Abre un ticket desde el propio panel (menú → Soporte) o escríbenos directamente a soporte@vigex.es.  
[Si plan Plus/Premium: también puedes llamarnos al [TELÉFONO] en horario L-V 9:00–18:00.]

Respondemos en [48h laborables / 24h / 4h] según tu plan de soporte.

---

**Tu información de licencia**

Plan: [Lite / Standard / Pro]  
Licencia: perpetua (pago único — el software es tuyo para siempre)  
[Soporte: [plan] activo hasta [fecha] — renovación automática vía Stripe]

---

Un placer haberte ayudado. Cualquier duda, aquí estamos.

Santino Colmena  
Vigex · soporte@vigex.es  
vigex.es

---

## Campos a completar antes de enviar

| Campo | Dónde encontrarlo |
|-------|------------------|
| `[Nombre]` | Nombre del contacto del cliente |
| `[IP_O_DOMINIO_CLIENTE]` | IP o dominio configurado en el servidor |
| `[CONTRASEÑA_INICIAL]` | La que se configuró en `config.env` (ADMIN_PASSWORD) |
| `[HORA_BACKUP]` | Hora configurada en el cron de copias |
| `[LISTA_SERVICIOS]` | Los servicios añadidos durante la instalación |
| `[EMAIL/TELEGRAM]` | Canal de alertas configurado |
| `[EMAIL_CLIENTE]` | Email para informes configurado en el panel |
| `[TELÉFONO]` | Solo si plan Premium |
| `[48h / 24h / 4h]` | Según plan de soporte contratado (o eliminar línea si no hay soporte) |
| `[plan soporte]` y `[fecha]` | Solo si contrató soporte mensual; eliminar línea si no |

## Notas

- No incluyas la contraseña en texto plano si el email va por canal inseguro. En ese caso, compártela por teléfono el día de la instalación y en el email escribe "la contraseña que acordamos en la llamada".
- Si el cliente no ha contratado soporte, elimina el párrafo del SLA y la línea de información de soporte.
- Adjunta (como PDF o imagen) la guía de alertas Telegram si el cliente la ha activado: `docs/guias/guia_alertas_telegram.md`.
