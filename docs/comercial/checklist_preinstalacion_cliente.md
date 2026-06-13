# Checklist de pre-instalación — Para el cliente

**Rellena este formulario y envíalo a soporte@vigex.es antes del día de la instalación.**
Cuantos más detalles incluyas, más rápido y sin interrupciones haremos la instalación.

---

## 1. Datos del contacto técnico

| Campo | Tu respuesta |
|-------|-------------|
| Nombre y apellidos | |
| Email de contacto técnico | |
| Teléfono (para el día de la instalación) | |
| Empresa / organización | |

---

## 2. Servidores involucrados

Rellena una fila por servidor. Si tienes un solo servidor, solo necesitas rellenar la primera.

| Rol | IP o hostname | Sistema operativo | Versión OS | Acceso SSH |
|-----|--------------|-------------------|------------|------------|
| Panel principal | | | | root / sudo |
| Base de datos (si plan Standard/Pro) | | | | root / sudo |
| Copias de seguridad (si plan Pro) | | | | root / sudo |

**¿Cuál es el puerto SSH?** (por defecto 22): ___________

**¿Hay firewall o VPN que restrinja el acceso SSH externo?**
- [ ] No, acceso SSH directo desde cualquier IP
- [ ] Sí, hay que añadir IP a whitelist → indica cómo: ___________
- [ ] Acceso vía VPN → indica cómo conectarse: ___________

---

## 3. Servicios que quieres monitorizar

Lista los servicios que el panel debe vigilar (p.ej. nginx, postgresql, mysql, redis, docker, etc.).
Si no estás seguro, escribe "los principales" y lo configuramos juntos.

```
Servicios a monitorizar:


```

---

## 4. Alertas

**¿Cómo quieres recibir las alertas cuando algo falle?**
- [ ] Solo por email → email de alertas: ___________
- [ ] Solo por Telegram (necesitarás instalar @VigexPanelBot)
- [ ] Email + Telegram
- [ ] Ya te lo explican durante la instalación

---

## 5. Correo saliente (SMTP)

El panel envía informes y alertas por email. Tienes dos opciones:

- [ ] **Usar Gmail con contraseña de aplicación** — lo más rápido. Solo necesitas una cuenta Gmail y generar una contraseña de aplicación en myaccount.google.com → Seguridad → Contraseñas de aplicaciones.
- [ ] **Usar vuestro servidor de correo propio** → proporciona:
  - Host SMTP: ___________
  - Puerto: ___________
  - Usuario: ___________
  - ¿TLS/SSL?: ___________

---

## 6. Ventana de mantenimiento

**¿Cuándo podemos hacer la instalación?** (La instalación dura entre 30 y 60 minutos. El servidor no se apaga pero los servicios pueden reiniciarse una vez.)

- Fecha preferida: ___________
- Hora preferida: ___________
- ¿Hay algún horario que debamos evitar? (p.ej. horario de facturación, backups nocturnos existentes): ___________

---

## 7. Configuración de copias de seguridad

**¿A qué hora prefieres que se hagan las copias automáticas?**
- [ ] 02:00 (recomendado — mínima actividad)
- [ ] 03:00
- [ ] Otro horario: ___________

**¿Cuántos días de retención quieres?** (cuántos días atrás guardar copias)
- [ ] 7 días (recomendado para Lite)
- [ ] 14 días
- [ ] 30 días
- [ ] Otro: ___________

---

## 8. Acceso SSH para la instalación

El instalador necesita acceso SSH con permisos de root o sudo al servidor principal.

**Método de acceso:**
- [ ] Contraseña root/sudo — la facilitaré el día de la instalación de forma segura
- [ ] Clave pública SSH — os enviamos la clave pública antes y la añadís a `authorized_keys`
- [ ] Otro método: ___________

---

## 9. ¿Alguna particularidad técnica?

Espacio libre para comentar cualquier detalle relevante: configuraciones especiales, restricciones de red, servicios críticos que no deben interrumpirse, etc.

```




```

---

**Envía este documento a soporte@vigex.es con asunto: "Pre-instalación — [Nombre de tu empresa]"**

Te confirmamos día y hora en menos de 24 horas laborables.
