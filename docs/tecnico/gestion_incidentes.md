# Gestión de incidentes — Vigex
## R-075 / Ruta 9.5

Protocolo para gestionar incidentes de forma ordenada, tanto del propio software Vigex
como de la infraestructura del cliente.

---

## Clasificación de severidad

| Nivel | Descripción | Tiempo de respuesta | Ejemplos |
|-------|-------------|---------------------|---------|
| **P1 — Crítico** | Pérdida de datos o servicio completamente caído | < 2 horas (horario laboral) | BD inaccesible, todos los backups fallan, panel sin acceso |
| **P2 — Alto** | Función clave degradada | < 8 horas | Alertas no se envían, un backup falla |
| **P3 — Medio** | Función secundaria afectada | < 24 horas | Gráficas no se cargan, un servicio monitoreado caído |
| **P4 — Bajo** | Mejora o cosmétic | < 72 horas | Texto incorrecto, sugerencia de mejora |

---

## Flujo de atención a incidencias

```
Cliente detecta el problema
        ↓
Abre ticket en el panel (FAB → Reportar problema)
  o envía email a soporte@vigexpyme.es
        ↓
Proveedor Vigex recibe notificación
        ↓
Clasifica severidad (P1–P4)
        ↓
Diagnóstico (acceso SSH si el cliente autoriza)
        ↓
Solución o workaround
        ↓
Verificación con el cliente
        ↓
Cierre del ticket con descripción de la causa y solución
        ↓
Post-mortem si P1 (qué falló, cómo evitarlo)
```

---

## Diagnóstico inicial por tipo de incidencia

### Panel no responde
```bash
systemctl status vigex-api
journalctl -u vigex-api -n 100
df -h   # disco lleno?
free -m # RAM?
```

### Backups fallan
```bash
tail -50 /home/vigex/backups/.vigex/history.tsv
# Buscar líneas con estado distinto de OK
ssh -i /opt/vigex/api/.ssh/id_rsa_vigex vigex@<BACKUP_HOST> "df -h && ls -la /home/vigex/backups/"
```

### Alertas no se reciben
```bash
# Probar envío manual desde el panel: Alertas → Probar alertas
# Revisar config.env
grep "NOTIF_" /opt/vigex/api/config.env
# Probar SMTP manualmente
python3 -c "import smtplib; s=smtplib.SMTP('smtp.gmail.com',587); s.starttls(); s.login('user','pass'); print('OK')"
```

### Servicio caído detectado por Vigex
```bash
# Ver qué servicio y cuándo
systemctl status <nombre-servicio>
journalctl -u <nombre-servicio> -n 50
# Reiniciar desde el panel o CLI
systemctl restart <nombre-servicio>
```

---

## Plantilla de post-mortem (P1)

```markdown
## Post-mortem — [Descripción breve] — [Fecha]

### Resumen
[2-3 frases: qué ocurrió, cuánto duró, impacto]

### Línea temporal
- HH:MM — Se detectó el problema (por quién)
- HH:MM — Se abrió ticket / se notificó al proveedor
- HH:MM — Diagnóstico completado
- HH:MM — Solución aplicada
- HH:MM — Verificación y cierre

### Causa raíz
[Explicación técnica de por qué ocurrió]

### Solución aplicada
[Qué se hizo para resolverlo]

### Medidas preventivas
- [ ] [Acción 1 para evitar que vuelva a ocurrir]
- [ ] [Acción 2]

### Métricas
- RTO real: XX minutos
- RPO real: XX horas de datos perdidos (si aplica)
```

---

## Comunicación con el cliente durante P1

1. **Confirmación de recepción** (en <30 min): "Hemos recibido tu incidencia y estamos investigando."
2. **Actualización de estado** (cada 60 min mientras dura): "Diagnóstico: [X]. Trabajando en [Y]. ETA: [Z]."
3. **Resolución**: "El problema ha sido resuelto. Causa: [X]. Para evitarlo: [Y]."
4. **Seguimiento** (24h después): "¿Todo sigue funcionando correctamente?"

---

## Registro de incidencias

Todos los incidentes P1 y P2 deben quedar registrados en `docs/validaciones/incidentes/`
con el formato `AAAA-MM-DD_titulo.md`.

Esto permite:
- Detectar patrones recurrentes.
- Documentar el historial de fiabilidad.
- Respaldar decisiones de mejora del producto.
