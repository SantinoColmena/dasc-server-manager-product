# Guía: Despliegue de Vigex Central en VPS
## R-078 / Ruta 10.2

Pasos para tener la Central Vigex funcionando en un VPS propio con HTTPS real.
Tiempo estimado: 60-90 minutos.

**Prerequisito:** haber completado la Ruta 9.1 (dominio y email profesionales activos).

---

## Paso 1 — Contratar el VPS

### Requisitos mínimos

| Recurso | Mínimo | Recomendado |
|---------|--------|-------------|
| vCPU | 1 | 2 |
| RAM | 1 GB | 2 GB |
| Disco | 20 GB | 40 GB |
| SO | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |
| Tráfico | 1 TB/mes | ilimitado |

### Proveedores recomendados (precio ~€3-6/mes)

| Proveedor | Plan | Precio/mes | Nota |
|-----------|------|-----------|------|
| **Hetzner** | CX21 | ~€4,15 | Mejor precio/rendimiento. Data center en Alemania/Finlandia. |
| DigitalOcean | Droplet Basic | ~€5 | Interfaz muy fácil. NYC/Amsterdam. |
| Contabo | VPS S | ~€4 | Mucho disco. Factura en euros. |
| Ionos | VPS S | ~€2 primer año | Buena opción de entrada. |

> **Recomendación:** Hetzner CX21. Factura en euros, RGPD-compliant, soporte rápido.

---

## Paso 2 — Configuración inicial del VPS

Conéctate por SSH con el usuario root:

```bash
# Actualizar el sistema
apt update && apt upgrade -y

# Crear usuario vigex (sin contraseña SSH, solo clave)
adduser --disabled-password --gecos "" vigex
usermod -aG sudo vigex

# Copiar tu clave pública al nuevo usuario
mkdir -p /home/vigex/.ssh
cp /root/.ssh/authorized_keys /home/vigex/.ssh/authorized_keys
chown -R vigex:vigex /home/vigex/.ssh
chmod 700 /home/vigex/.ssh && chmod 600 /home/vigex/.ssh/authorized_keys

# Desactivar login root por SSH
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd

# Firewall básico
apt install ufw -y
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
```

---

## Paso 3 — Instalar Vigex Central

Desde tu máquina Windows (con el repo clonado), transfiere los archivos:

```powershell
# En PowerShell (Windows) — desde la raíz del repo
$VPS_IP = "IP.DEL.VPS"
$Vigex_USER = "vigex"

# Copiar el paquete al VPS
scp -r deploy\central-support "$Vigex_USER@${VPS_IP}:/tmp/"

# Ejecutar el instalador
ssh "$Vigex_USER@${VPS_IP}" "sudo bash /tmp/central-support/install_central_support.sh"
```

O desde Linux/WSL:
```bash
VPS_IP="IP.DEL.VPS"
scp -r deploy/central-support/ vigex@${VPS_IP}:/tmp/
ssh vigex@${VPS_IP} "sudo bash /tmp/central-support/install_central_support.sh"
```

El instalador:
1. Instala Python 3 y dependencias.
2. Copia el paquete a `/opt/vigex/central-support/`.
3. Crea el servicio systemd `vigex-central`.
4. Arranca el servicio en el puerto 8010.

---

## Paso 4 — Configurar variables de entorno

El servicio lee variables del entorno. Créalas en el fichero de override de systemd:

```bash
sudo systemctl edit vigex-central
```

Añade este contenido (ajusta las contraseñas):
```ini
[Service]
Environment="Vigex_CENTRAL_AUTH_ENABLED=true"
Environment="Vigex_CENTRAL_LAB_MODE=false"
Environment="Vigex_CENTRAL_ADMIN_USER=admin"
Environment="Vigex_CENTRAL_ADMIN_PASSWORD=CAMBIA_ESTO_POR_UNA_PASSWORD_SEGURA"
Environment="Vigex_CENTRAL_TECH_USER=tecnico"
Environment="Vigex_CENTRAL_TECH_PASSWORD=CAMBIA_ESTO_POR_UNA_PASSWORD_SEGURA"
Environment="Vigex_CENTRAL_SECRET_KEY=GENERA_UN_SECRET_CON_python3_-c_secrets.token_hex(48)"
```

Guarda y reinicia:
```bash
sudo systemctl restart vigex-central
sudo systemctl status vigex-central
```

---

## Paso 5 — Instalar nginx + HTTPS con Let's Encrypt

```bash
# Instalar nginx y certbot
sudo apt install nginx certbot python3-certbot-nginx -y

# Ejecutar el instalador de nginx incluido en el repo
sudo bash /tmp/central-support/install_nginx_central_support.sh
```

El instalador de nginx configura el proxy a `127.0.0.1:8010`.

Luego obtén el certificado TLS:
```bash
# Sustituye por tu dominio real
sudo certbot --nginx -d central.vigexpyme.es
```

Certbot se encarga de renovar automáticamente via cron.

Verifica que funciona:
```bash
curl -I https://central.vigexpyme.es/health
# Debe devolver HTTP/2 200
```

---

## Paso 6 — Hardening de seguridad

```bash
# Ejecutar el script de hardening incluido
sudo bash /tmp/central-support/harden_central_support_security.sh

# Instalar y configurar fail2ban
sudo apt install fail2ban -y
sudo systemctl enable --now fail2ban

# Limitar SSH a tu IP fija (recomendado si tienes IP fija en casa/oficina)
sudo ufw delete allow 22/tcp
sudo ufw allow from TU_IP_FIJA to any port 22
sudo ufw reload
```

---

## Paso 7 — Registrar el primer cliente

1. Accede al panel central: `https://central.vigexpyme.es`
2. Inicia sesión con el usuario `admin`.
3. Navega a **Clientes → Registrar nuevo cliente**.
4. Introduce el ID y nombre del cliente. Se generará un token seguro.
5. **Copia el token** — solo se muestra una vez.
6. En el servidor del cliente, añade a `config.env`:
   ```bash
   CENTRAL_SUPPORT_ENABLED=true
   CENTRAL_SUPPORT_URL=https://central.vigexpyme.es/api/v1/support/tickets
   CENTRAL_SUPPORT_CLIENT_ID=<id_del_cliente>
   CENTRAL_SUPPORT_CLIENT_NAME=<nombre_del_cliente>
   CENTRAL_SUPPORT_TOKEN=<token_copiado>
   CENTRAL_HEARTBEAT_INTERVAL=300
   ```
7. Reinicia el panel del cliente: `sudo systemctl restart vigex-api`
8. En el panel central, ve a **Salud global** — el cliente debe aparecer en verde en ≤ 10 minutos.

---

## Paso 8 — Backup de la Central

Ejecuta periódicamente (recomendado: semanal via cron):
```bash
# En el VPS
tar -czf /root/backups/central_$(date +%Y%m%d_%H%M%S).tar.gz \
    --exclude=/opt/vigex/central-support/venv \
    /opt/vigex/central-support/

# Copiar a almacenamiento externo
rsync -avz /root/backups/ tu_servidor_externo:/backups/vigex-central/
```

---

## Checklist de activación de la Central

- [ ] VPS contratado y accesible por SSH
- [ ] Usuario `vigex` creado, acceso root desactivado
- [ ] `vigex-central` arrancado y en verde con `systemctl status`
- [ ] Variables de entorno configuradas con contraseñas reales
- [ ] nginx + HTTPS (Let's Encrypt) activo en `https://central.vigexpyme.es`
- [ ] Hardening aplicado (fail2ban, UFW)
- [ ] Al menos un cliente de prueba registrado y aparece en verde en Salud global
- [ ] Backup de la Central configurado
- [ ] URL actualizada en `config.env` de los paneles clientes

---

## Troubleshooting rápido

```bash
# Ver logs del servicio central
sudo journalctl -u vigex-central -n 100 -f

# Comprobar que el puerto 8010 está escuchando
sudo ss -tlnp | grep 8010

# Probar el endpoint de salud directamente
curl http://127.0.0.1:8010/health

# Comprobar que nginx hace el proxy correctamente
curl -I https://central.vigexpyme.es/health

# Recargar nginx si cambias la config
sudo nginx -t && sudo systemctl reload nginx
```
