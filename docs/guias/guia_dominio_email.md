# Guía: Dominio profesional y email de soporte
## R-076 / Ruta 9.1

Coste estimado: ~€1/año dominio .es + €0–6/mes email.
Tiempo: 30-60 minutos para tenerlo todo activo.

---

## Paso 1 — Registrar el dominio

### Opción recomendada: dascpyme.es (mercado español, cercano al cliente)
Alternativas según disponibilidad:
- `dascservermanager.es`
- `dascmanager.es`
- `dasc.es` (si está libre, muy corto)

### Dónde registrarlo (opciones ordenadas por precio)

| Registrador | Precio .es/año | Notas |
|-------------|---------------|-------|
| Porkbun | ~€1 primer año | Renovación ~€6/año. Panel sencillo. |
| Namecheap | ~€3/año | Popular, buen soporte |
| Dinahosting | ~€8/año | Español, soporte en castellano |
| OVH | ~€6/año | Europeo, fiable, IVA incluido en precios |

> **Recomendación**: Porkbun para el precio, OVH si prefieres proveedor europeo con factura en euros.

### Cómo registrar (pasos en Porkbun)
1. Ve a porkbun.com → busca `dascpyme.es`.
2. Añade al carrito → crea cuenta.
3. Paga con tarjeta. Recibirás email de confirmación.
4. El dominio queda activo en 15–30 minutos.

---

## Paso 2 — Configurar email profesional

### Opción A: Zoho Mail (gratuito para 1 usuario, €1/mes para más)
1. Ve a [zoho.com/es/mail](https://zoho.com/es/mail) → **Free plan** (hasta 5GB, 1 cuenta).
2. Introduce tu dominio (`dascpyme.es`).
3. Zoho te dará registros DNS que debes añadir en el panel del registrador:
   - Registro MX (para recibir correo)
   - Registro TXT SPF (para no caer en spam)
   - Registro CNAME DKIM (firma digital del correo)
4. En el panel de tu registrador, ve a "DNS / Gestionar DNS" y añade los registros.
5. La propagación tarda entre 15 minutos y 2 horas.

### Opción B: Google Workspace (€5–6/mes por usuario)
1. Ve a [workspace.google.com](https://workspace.google.com) → prueba gratuita 14 días.
2. Introduce tu dominio y sigue el asistente.
3. Añade los registros DNS que Google indique.
4. Ventaja: integración perfecta con Gmail/Calendar/Drive.

### Opción C: Resend (para solo envío de emails transaccionales, gratuito 3.000/mes)
- No incluye buzón de correo. Solo sirve para enviar notificaciones desde DASC.
- Útil si ya tienes otro email y solo necesitas el SMTP.
- Configuración: [resend.com](https://resend.com) → crear dominio → añadir registros DNS.

---

## Paso 3 — Añadir registros DNS de seguridad

Una vez configurado el email, añade estos registros adicionales:

```
# SPF — evita que otros envíen en tu nombre
TXT  @   "v=spf1 include:_spf.zoho.eu ~all"
         (ajusta según proveedor: Google = _spf.google.com)

# DMARC — política ante fallos de autenticación
TXT  _dmarc   "v=DMARC1; p=quarantine; rua=mailto:soporte@dascpyme.es"

# CNAME para web (si usas Netlify/Vercel)
CNAME  www   <subdomain>.netlify.app.
A      @     <IP de tu servidor de landing>
```

---

## Paso 4 — Actualizar la landing page y el panel

1. En `web/index.html` busca todos los `TODO` con referencias a `dascpyme.es`
   y sustituye por el dominio real que hayas registrado.

2. En el servidor DASC, actualiza `config.env`:
```bash
NOTIF_SMTP_HOST=smtp.zoho.eu       # o smtp.gmail.com para Google Workspace
NOTIF_SMTP_PORT=587
NOTIF_SMTP_USER=soporte@dascpyme.es
NOTIF_SMTP_PASS=<tu_contraseña>
NOTIF_EMAIL_FROM=soporte@dascpyme.es
```

3. Reinicia el servicio: `sudo systemctl restart dasc-api`

4. Prueba enviando un informe manual desde el panel → **Informes** → **Enviar ahora**.

---

## Paso 5 — Desplegar la landing page

### Opción A: Netlify (recomendado, gratuito)
1. Ve a [netlify.com](https://netlify.com) → crea cuenta con GitHub.
2. "Add new site" → "Deploy manually" → arrastra la carpeta `web/` del repo.
3. Netlify genera una URL `*.netlify.app` gratuita.
4. En "Domain settings" → añade tu dominio personalizado.
5. Netlify te dará un registro DNS CNAME para apuntar tu dominio a Netlify.

### Opción B: GitHub Pages
1. En el repositorio GitHub: Settings → Pages.
2. Source: rama `main`, carpeta `/web` (si GitHub Pages lo soporta) o mueve `web/` a `docs/`.
3. Añade el dominio en "Custom domain" y configura el CNAME en tu registrador.

### Opción C: VPS propio (nginx)
```bash
# En el servidor donde tienes instalado DASC (o uno separado)
sudo cp -r /ruta/repo/web /var/www/dascpyme
sudo nano /etc/nginx/sites-available/dascpyme
```
```nginx
server {
    listen 80;
    server_name dascpyme.es www.dascpyme.es;
    root /var/www/dascpyme;
    index index.html;
    location / { try_files $uri $uri/ =404; }
}
```
```bash
sudo ln -s /etc/nginx/sites-available/dascpyme /etc/nginx/sites-enabled/
sudo certbot --nginx -d dascpyme.es -d www.dascpyme.es  # HTTPS gratis con Let's Encrypt
sudo systemctl reload nginx
```

---

## Checklist de activación

- [ ] Dominio registrado
- [ ] Email profesional `soporte@dascpyme.es` funcionando
- [ ] Registros MX, SPF, DKIM y DMARC configurados
- [ ] Landing page publicada con dominio personalizado y HTTPS
- [ ] config.env del servidor DASC actualizado con SMTP real
- [ ] Formulario de contacto enviando emails correctamente
- [ ] TODOs de `web/index.html` y `web/legal/terminos.html` completados
