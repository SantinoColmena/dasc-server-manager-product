# Plan de recuperación ante desastres — Vigex
## R-075 / Ruta 9.5
## Complemento del runbook `/recuperacion` del panel

---

## Objetivos de recuperación

| Métrica | Objetivo | Justificación |
|---------|----------|--------------|
| **RTO** (Recovery Time Objective) | < 4 horas | Tiempo máximo para restaurar el servicio en caso de desastre |
| **RPO** (Recovery Point Objective) | < 24 horas | Máximo de datos que podemos permitirnos perder (una jornada) |
| **Copia mínima exigida** | 1 backup completo + último incremental | Validado con SHA256 antes de restaurar |

---

## Escenarios contemplados

### Escenario A — Fallo del panel (servidor API)
**Síntoma**: Panel no accesible, `curl http://localhost:8000` no responde.
**Causa más probable**: Servicio caído, disco lleno, Python error.

```bash
# Diagnóstico (desde SSH)
systemctl status vigex-api
journalctl -u vigex-api -n 50
df -h /opt/vigex

# Solución más común: reiniciar el servicio
sudo systemctl restart vigex-api

# Si el disco está lleno:
sudo journalctl --vacuum-size=200M       # libera logs del sistema
sudo du -sh /opt/vigex/reports/*          # revisar informes generados
```

**RTO estimado**: 5-15 minutos.

---

### Escenario B — Fallo del servidor de backups
**Síntoma**: Los backups fallan, SSH al servidor de backups no responde.
**Causa más probable**: Servidor apagado, disco lleno, SSH roto.

```bash
# Comprobar conectividad
ping -c 3 <IP_BACKUPS>
ssh -i /opt/vigex/api/.ssh/id_rsa_vigex vigex@<IP_BACKUPS> hostname

# Si el servidor responde pero falla el SSH de Vigex:
# Revisar authorized_keys en el servidor remoto
ssh root@<IP_BACKUPS> "cat /home/vigex/.ssh/authorized_keys"
# Debe contener la clave pública de /opt/vigex/api/api_panel.pub
```

**RTO estimado**: 15-30 minutos.

---

### Escenario C — Pérdida de datos (restauración completa)
**Síntoma**: Base de datos corrupta o borrada, ficheros críticos perdidos.

**Procedimiento**:

1. **Verificar integridad de la copia** (panel: `/copias/salud` o CLI):
```bash
# Ver las últimas copias disponibles
cat /home/vigex/backups/.vigex/history.tsv | tail -20
# Verificar SHA256 de la copia elegida
sha256sum /home/vigex/backups/<nombre_copia>.sql.gz
```

2. **Parar servicios que usen la BD**:
```bash
sudo systemctl stop vigex-api
```

3. **Restaurar desde el panel** (panel → Copias → Restaurar) o CLI:
```bash
sudo -u vigex bash /opt/vigex/api/deploy/backup-services/package/restore_api.sh \
  <ID_BACKUP> <DB_NAME>
```

4. **Verificar restauración**:
```bash
# Conectar a MariaDB y comprobar tablas
mysql -u vigex_user -p vigex_logs -e "SHOW TABLE STATUS\G"
```

5. **Reiniciar servicios**:
```bash
sudo systemctl start vigex-api
curl -I http://localhost:8000
```

6. **Documentar el incidente** (panel: `/soporte` → Abrir ticket).

**RTO estimado**: 1-4 horas (según tamaño de la BD).

---

### Escenario D — Reinstalación completa del panel
**Cuándo**: El servidor del panel se ha perdido completamente (fallo de hardware, migración).

**Prerrequisito**: Tener el backup del panel (`backup_vigex_api.sh`) en un almacenamiento externo.

```bash
# En el nuevo servidor Ubuntu 22.04
# 1. Copiar el backup desde el almacenamiento externo
scp admin@<origen>:/backups/vigex_panel_backup_<ts>.tar.gz /tmp/

# 2. Instalar Vigex desde cero con el nuevo instalador
sudo bash deploy/api/install_vigex_api.sh

# 3. Restaurar datos y configuración sobre la instalación nueva
sudo systemctl stop vigex-api
sudo tar -xzf /tmp/vigex_panel_backup_<ts>.tar.gz -C /opt/vigex/
sudo systemctl start vigex-api
```

**RTO estimado**: 30-90 minutos.

---

## Prueba de restauración — procedimiento trimestral

Para validar que el plan funciona, realizar trimestralmente:

1. Crear una VM Ubuntu limpia (multipass o VirtualBox).
2. Restaurar en ella la última copia completa disponible.
3. Verificar que el servicio arranca y los datos son coherentes.
4. Registrar el resultado en `docs/validaciones/` con fecha y tiempo empleado.
5. Actualizar los RTO/RPO si los tiempos reales difieren de los objetivos.

**Responsable**: Desarrollador / proveedor del servicio.

---

## Contactos de emergencia

<!-- TODO: completar con datos reales del cliente antes de entregar -->
| Rol | Nombre | Teléfono | Email |
|-----|--------|----------|-------|
| Administrador principal | — | — | — |
| Proveedor Vigex | — | — | soporte@vigexpyme.es |
| Proveedor de hosting/VPS | — | — | — |

---

## Historial de pruebas de recuperación

| Fecha | Escenario | Resultado | RTO real | Notas |
|-------|-----------|-----------|----------|-------|
| — | — | — | — | Sin pruebas realizadas aún |
