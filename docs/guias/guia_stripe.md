# Guía: Activar pagos con Stripe
## R-074 / Ruta 9.3

Stripe es la forma más rápida de empezar a cobrar sin banco ni TPV propio.
Plan gratuito + comisión por transacción: ~1,5% + €0,25 por cobro (tarjetas europeas).

---

## Paso 1 — Crear la cuenta

1. Ve a [stripe.com](https://stripe.com) y pulsa **Empezar**.
2. Introduce tu email y crea contraseña.
3. Activa la verificación en dos pasos (obligatorio para recibir pagos).

---

## Paso 2 — Completar el perfil de empresa

Stripe necesita estos datos para activar los cobros reales:

- **Tipo de entidad**: Autónomo o Sociedad (según tu alta en Hacienda).
- **NIF/CIF**.
- **Domicilio fiscal**.
- **Cuenta bancaria española** (IBAN) donde recibirás los pagos.
- **Documento de identidad** (DNI/NIE para verificación KYC).

> La verificación puede tardar 1-3 días laborables.

---

## Paso 3 — Crear los productos/precios

En el panel de Stripe → **Catálogo de productos**:

1. **Crear producto** por cada plan:
   - DASC Lite — €15/mes (tipo: recurrente, mensual)
   - DASC Standard — €35/mes
   - DASC Pro — €65/mes
   - Añadir opción anual con descuento a cada producto.

2. Stripe generará un **Price ID** por cada variante (p.ej. `price_1AbCdEfGhIjKlMnO`).

---

## Paso 4 — Crear Payment Links (opción sin código)

Para empezar sin integrar código en la web:

1. Panel Stripe → **Payment Links** → **Crear enlace**.
2. Selecciona el producto (p.ej. DASC Standard mensual).
3. Activa: "Recopilar dirección de facturación" + "Número fiscal del cliente".
4. Copia el enlace generado y pégalo en el botón "Empezar con Standard" de `web/index.html`.

> Los Payment Links redirigen al cliente a una página de Stripe segura. No necesitas backend propio.

---

## Paso 5 — Conectar el formulario de contacto con Formspree

El formulario de `web/index.html` usa Formspree como intermediario.

1. Ve a [formspree.io](https://formspree.io) y crea cuenta gratuita (hasta 50 envíos/mes gratis).
2. Crea un nuevo formulario → copia la URL del tipo `https://formspree.io/f/XXXXXXXX`.
3. En `web/index.html`, busca el `TODO` del `action` del formulario y sustituye la URL.

---

## Paso 6 — Recibir pagos por transferencia (alternativa)

Para clientes empresariales que necesiten factura proforma:

1. Recibe la petición por email.
2. Genera la factura con tus datos fiscales (puedes usar Holded, Quipu o Factura Directa — todos tienen plan gratuito).
3. Envía la factura con los datos bancarios (IBAN).
4. Activa el servicio cuando el pago aparezca en tu cuenta.

---

## Configuración SMTP para DASC (una vez tengas email profesional)

Cuando hayas activado el email profesional (ver `guia_dominio_email.md`), actualiza
`config.env` en el servidor del cliente con los datos SMTP correspondientes:

```bash
# Para Google Workspace (Gmail empresarial)
NOTIF_SMTP_HOST=smtp.gmail.com
NOTIF_SMTP_PORT=587
NOTIF_SMTP_USER=soporte@dascpyme.es
NOTIF_SMTP_PASS=<contraseña_de_aplicación_de_google>
NOTIF_EMAIL_FROM=soporte@dascpyme.es
NOTIF_EMAIL_TO=admin@clienteempresa.com

# Para Zoho Mail (alternativa más barata)
NOTIF_SMTP_HOST=smtp.zoho.eu
NOTIF_SMTP_PORT=587
NOTIF_SMTP_USER=soporte@dascpyme.es
NOTIF_SMTP_PASS=<contraseña_zoho>
```

Reinicia el servicio tras el cambio: `sudo systemctl restart dasc-api`
