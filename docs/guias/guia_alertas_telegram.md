# Guía de alertas por Telegram — Vigex

> **Destinatario:** usuario final o responsable técnico de la PyME.
> Tiempo estimado de configuración: **5 minutos**.

---

## Cómo funciona

Vigex utiliza un bot centralizado (**@VigexPanelBot**) para enviarte notificaciones
directamente a Telegram. No necesitas crear ningún bot propio ni pedir ninguna API key.

Solo necesitas dos cosas:

1. Tu **Chat ID** de Telegram (un número que identifica tu conversación con el bot).
2. Introducir ese número en el panel Vigex.

---

## Paso 1 — Obtener tu Chat ID

1. Abre Telegram en el móvil o en [web.telegram.org](https://web.telegram.org).
2. Busca el bot **@VigexPanelBot** en el buscador de Telegram.
3. Pulsa **Iniciar** (o escribe `/start`).
4. Escribe `/chatid` y envíalo.
5. El bot te responderá con tu Chat ID, un número como `123456789`.
   Cópialo — lo necesitarás en el siguiente paso.

> Si el bot no responde, asegúrate de haber pulsado **Iniciar** primero.

---

## Paso 2 — Añadir el Chat ID como destinatario

1. Accede al panel Vigex con tu usuario y contraseña.
2. En el menú lateral, ve a **Alertas**.
3. Baja hasta la sección **Destinatarios Telegram** y rellena el formulario:
   - **Empresa** — nombre de tu empresa (ej: "Mi Empresa").
   - **Nombre visible** — etiqueta para identificar este destino (ej: "Alertas IT").
   - **Tipo** — selecciona **Usuario individual** si es tu chat personal, o **Grupo** si añadiste el bot a un grupo.
   - **Chat ID** — pega el número obtenido en el Paso 1.
4. Pulsa **Guardar destinatario**.
5. En la tabla de destinatarios, haz clic en el botón **Por defecto** (estrella ★) junto al destinatario recién creado.

---

## Paso 3 — Probar que funciona

1. En la parte superior de la pantalla **Alertas**, pulsa **Enviar prueba al destino por defecto**.
2. Deberías recibir en Telegram un mensaje de prueba de **@VigexPanelBot**
   en pocos segundos.

Si no recibes el mensaje en 30 segundos, revisa:
- Que hayas pulsado **Por defecto** en el destinatario correcto.
- Que el Chat ID sea correcto (sin espacios ni guiones).
- Que hayas pulsado **Iniciar** con @VigexPanelBot antes de enviar.
- Que no hayas bloqueado al bot en Telegram.

---

## Tipos de alertas que recibirás

| Evento | Cuándo se envía |
|---|---|
| Backup completado | Tras cada copia de seguridad exitosa |
| Error en backup | Si una copia falla o termina con advertencias |
| Servicio caído | Si un servicio monitorizado se detiene |
| Error de API | Si el panel detecta un error interno grave |
| Incidente NIS2 | Al registrar un nuevo incidente de seguridad |
| Alerta de prueba | Cuando tú mismo pulsas "Probar alertas" |

---

## Preguntas frecuentes

**¿Necesito crear un bot de Telegram propio?**
No. El bot **@VigexPanelBot** es gestionado por Vigex. Solo necesitas tu Chat ID.

**¿Puedo recibir alertas en un grupo de Telegram?**
Sí. Añade **@VigexPanelBot** al grupo, escribe `/chatid` en el grupo, y usa ese ID.

**¿Qué pasa si cambio de móvil o de cuenta de Telegram?**
Tu Chat ID no cambia aunque cambies de dispositivo. Solo cambia si creas una cuenta nueva.

**¿El bot puede ver mis mensajes?**
No. El bot solo envía mensajes, no lee ni almacena tu conversación.

**¿Puedo usar email en vez de Telegram?**
Sí. En **Alertas → Canal por defecto**, selecciona **Email** e introduce tu dirección.
Puedes activar ambos canales simultáneamente.

---

## Si tienes problemas

Contacta con soporte desde el panel: **Panel → Soporte → Nuevo ticket**.
Indica tu Chat ID y describe qué ocurre. El equipo técnico lo revisará.
