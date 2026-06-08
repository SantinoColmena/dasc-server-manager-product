# Guía anti-hackeo para servidores DASC
## R-075 / Ruta 9.5

Checklist de seguridad básica para un servidor con DASC instalado.
No sustituye una auditoría profesional, pero elimina el 90% del riesgo habitual en PYMES.

---

## 1. Acceso SSH

```bash
# Deshabilitar login de root por SSH
sudo nano /etc/ssh/sshd_config
# Cambiar: PermitRootLogin no
# Cambiar: PasswordAuthentication no  (solo claves SSH)
# Cambiar: MaxAuthTries 3
sudo systemctl restart sshd

# Verificar que el acceso con clave funciona antes de cerrar la sesión actual
ssh -i ~/.ssh/tu_clave dasc@<IP>
```

**Comprueba que la clave pública de DASC está en `/home/dasc/.ssh/authorized_keys`**
y que los permisos son correctos:
```bash
chmod 700 /home/dasc/.ssh
chmod 600 /home/dasc/.ssh/authorized_keys
```

---

## 2. Firewall (UFW)

```bash
sudo ufw status
# Debe mostrar solo los puertos necesarios:
# 22/tcp  (SSH) — solo desde IPs conocidas si es posible
# 80/tcp  (HTTP) — redirige a HTTPS
# 443/tcp (HTTPS) — panel con nginx

# Si el puerto 8000 está expuesto, cerrarlo (solo debe accederse via nginx)
sudo ufw deny 8000

# Limitar SSH a una IP específica (recomendado):
sudo ufw delete allow 22/tcp
sudo ufw allow from <TU_IP_FIJA> to any port 22
```

---

## 3. Fail2ban

```bash
# Comprobar que está instalado y activo
sudo systemctl status fail2ban
sudo fail2ban-client status sshd

# Ver IPs baneadas
sudo fail2ban-client banned

# Si no está instalado:
sudo apt install fail2ban
sudo systemctl enable --now fail2ban
```

Configuración recomendada (`/etc/fail2ban/jail.local`):
```ini
[sshd]
enabled  = true
port     = ssh
maxretry = 5
bantime  = 3600   ; 1 hora bloqueado tras 5 fallos
```

---

## 4. Contraseñas del panel DASC

- Usa contraseñas de al menos 16 caracteres con mayúsculas, números y símbolos.
- **Nunca** reutilices la contraseña del panel con otros sistemas.
- Cambia la contraseña tras la instalación inicial si usas la de ejemplo.
- Revisa periódicamente los usuarios del panel: panel → Admin → Usuarios.

```bash
# Cambiar contraseña de admin desde CLI si necesario
cd /opt/dasc/api
source venv/bin/activate
python3 -c "from passlib.context import CryptContext; print(CryptContext(['bcrypt']).hash('NUEVA_CLAVE'))"
# Copia el hash en config.env como ADMIN_PASSWORD=<hash>
sudo systemctl restart dasc-api
```

---

## 5. Actualizaciones del sistema operativo

```bash
# Actualizar el sistema operativo
sudo apt update && sudo apt upgrade -y

# Habilitar actualizaciones de seguridad automáticas
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## 6. Rotación de logs

```bash
# Comprobar que logrotate está configurado
cat /etc/logrotate.d/syslog

# Si los logs de DASC crecen demasiado:
sudo journalctl --vacuum-size=500M
sudo journalctl --vacuum-time=30d
```

---

## 7. Seguridad de config.env

```bash
# config.env solo debe ser legible por el usuario dasc
ls -la /opt/dasc/api/config.env
# Debe mostrar: -rw-r----- ... dasc dasc ...

# Corregir si es necesario:
sudo chmod 640 /opt/dasc/api/config.env
sudo chown dasc:dasc /opt/dasc/api/config.env
```

Verifica que `config.env` no está en el repositorio git:
```bash
git -C /opt/dasc/api log --all --full-history -- config.env
# No debe aparecer ningún commit con ese fichero
```

---

## 8. Monitoreo de accesos sospechosos

El panel DASC registra todos los intentos de login. Revísalos periódicamente:
- Panel → Admin → Accesos.
- Busca IPs desconocidas o intentos fallidos repetidos.

Desde CLI:
```bash
# Ver los últimos accesos fallidos SSH
sudo grep "Failed password" /var/log/auth.log | tail -20

# Ver conexiones SSH activas
who
```

---

## 9. Copia externa de los datos

Una copia en el mismo servidor no es una copia de seguridad real.
Configura sincronización a almacenamiento externo (mínimo):

```bash
# Opción simple: rsync a otro servidor o NAS
rsync -avz --delete /home/dasc/backups/ user@servidor-externo:/backups/dasc/

# Añadir como cron job (diario a las 03:00)
crontab -e
# 0 3 * * * rsync -az /home/dasc/backups/ user@servidor-externo:/backups/dasc/
```

---

## 10. Checklist mensual de seguridad

- [ ] Revisar accesos al panel (IPs, usuarios, intentos fallidos)
- [ ] Verificar que fail2ban sigue activo
- [ ] Confirmar que el sistema tiene las actualizaciones de seguridad aplicadas
- [ ] Comprobar espacio en disco (> 20% libre en todas las particiones)
- [ ] Verificar que la última copia de seguridad es de hace menos de 24 horas y tiene SHA256
- [ ] Revisar que no hay usuarios del panel que ya no deban tener acceso
