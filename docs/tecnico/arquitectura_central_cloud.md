# Arquitectura Central Cloud — DASC Server Manager
## R-077 / Ruta 10.1

Diseño técnico del sistema DASC Central Cloud: el VPS propio del equipo DASC
que agrega el estado de todas las instalaciones de clientes.

---

## Visión general

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INTERNET / HTTPS                             │
└──────────────┬───────────────────────────────────────┬─────────────┘
               │                                       │
       ┌───────▼────────┐                   ┌──────────▼──────────┐
       │  VPS DASC      │                   │  Navegador (admin)  │
       │  central.dasc  │◄──────────────────│  Equipo DASC        │
       │  port 443      │  HTTPS+Token      └─────────────────────┘
       │                │
       │  dasc-central  │ ←─── POST /api/v1/support/tickets  (push de tickets)
       │  -support      │ ←─── POST /api/v1/heartbeat        (heartbeat cada 5 min)
       │  :8010         │ ──── GET  /api/v1/support/tickets/{id} (sync estado)
       └────────────────┘
               ▲
               │  (por HTTPS, token por cliente)
   ┌───────────┼───────────────────────────┐
   │           │                           │
┌──┴──────┐ ┌─┴───────┐            ┌──────┴──────┐
│ Panel   │ │ Panel   │   ...      │ Panel N     │
│ Cliente │ │ Cliente │            │ Cliente     │
│ A       │ │ B       │            │             │
│ (Lite)  │ │ (Std)   │            │ (Pro)       │
└─────────┘ └─────────┘            └─────────────┘
```

---

## Componentes

### 1. VPS DASC (equipo)

- **Host:** VPS externo (Hetzner CX21, DigitalOcean Droplet, o similar)
- **SO:** Ubuntu 22.04 LTS
- **Dominio:** `central.dascpyme.es` (o el dominio que se registre)
- **HTTPS:** Let's Encrypt via certbot + nginx reverse proxy
- **Puerto:** 443 → nginx → 127.0.0.1:8010 (dasc-central-support)
- **Firewall:** UFW, solo 22/tcp, 80/tcp y 443/tcp

### 2. DASC Central Support (`dasc-central-support`)

Servicio FastAPI ya implementado en `deploy/central-support/`. Recibe:
- Tickets de soporte de paneles de clientes
- Heartbeats periódicos (salud de cada instalación)

Base de datos: SQLite local (`/opt/dasc/central-support/data/central_support.db`)

### 3. Paneles de clientes (`dasc-api`)

Cada instalación de cliente envía:
- Tickets cuando el usuario reporta un problema (push inmediato)
- Heartbeat cada 5 minutos (estado del servidor: disco, backups, alertas)

Configuración en `config.env` de cada cliente:
```bash
CENTRAL_SUPPORT_ENABLED=true
CENTRAL_SUPPORT_URL=https://central.dascpyme.es
CENTRAL_SUPPORT_CLIENT_ID=cliente-empresa-a
CENTRAL_SUPPORT_TOKEN=dasc-token-xxxxxxxxxxxxxxxxx
```

---

## Flujo de datos

### Tickets de soporte
```
Usuario abre ticket (panel cliente)
    → Panel guarda ticket en SQLite local
    → Panel hace POST /api/v1/support/tickets a la Central (con X-DASC-Client-Token)
    → Central guarda ticket con su propio ID (CENTRAL-YYYY-NNNN)
    → Si falla el push → cola de reintentos (scripts/retry_central_pending.py)
    → Equipo DASC ve el ticket en /tickets del panel central
    → Equipo actualiza estado en Central
    → Panel cliente sincroniza estado via GET /api/v1/support/tickets/{id}
```

### Heartbeat de salud
```
Panel cliente (cada 5 min, daemon thread)
    → GET /api/v1/heartbeat (datos locales del servidor)
    → POST /api/v1/heartbeat a Central (con X-DASC-Client-Token)
    → Central registra en tabla central_heartbeats
    → Dashboard central muestra semáforo por cliente:
        🟢 verde  → último heartbeat < 10 min
        🟡 naranja → último heartbeat 10-60 min
        🔴 rojo   → último heartbeat > 60 min o sin heartbeat
```

---

## Seguridad

| Control | Implementación |
|---------|---------------|
| Autenticación API | Header `X-DASC-Client-Token` (token único por cliente, SHA256-comparable) |
| Acceso panel central | Login con usuario/contraseña (admin + tecnico), sesión con cookie firmada |
| HTTPS | TLS 1.2+, certificado Let's Encrypt, HSTS |
| Firewall VPS | UFW: solo 22/tcp (SSH restringido a IP fija), 80/tcp, 443/tcp |
| fail2ban | Jaula sshd activa, jaula dasc-auth para el panel central |
| Rotación de tokens | `/clientes/{id}/rotar` en el panel central; token nuevo comunicado al cliente manualmente |
| Aislamiento de datos | Cada cliente solo ve sus propios tickets (validación `cliente_id` en cada request) |

---

## Gestión de clientes

El panel central incluye una sección **Clientes** (solo admin) donde se puede:
- **Alta**: generar un nuevo cliente con token aleatorio seguro (32 bytes hex)
- **Baja lógica**: desactivar un cliente (sus tickets quedan en la BD, no acepta nuevos)
- **Rotación de token**: revocar el token actual y generar uno nuevo
- **Vista de salud**: semáforo del último heartbeat por cliente

---

## Capacidad inicial estimada

| Recurso | Límite práctico | Nota |
|---------|-----------------|------|
| Clientes activos | ~50 | Con VPS CX21 (2 vCPU, 4 GB RAM) |
| Tickets/mes | ~5.000 | SQLite es suficiente hasta ~100K registros |
| Heartbeats/mes | ~432.000 (50 clientes × 12/h × 720h) | Registros ligeros (~200 bytes cada uno) |
| Almacenamiento | ~1 GB/año | Incluyendo BD, logs y backups de Central |

Para escala mayor → migración de SQLite a MariaDB (Fase 12).

---

## Proceso de alta de nuevo cliente

1. Instalar DASC en el servidor del cliente (perfiles existentes).
2. En panel central: **Clientes → Nuevo cliente** → copiar token generado.
3. En `config.env` del cliente: configurar `CENTRAL_SUPPORT_*` con la URL y el token.
4. Reiniciar `dasc-api` en el servidor del cliente.
5. Verificar: el cliente debe aparecer en verde en el Dashboard de Salud.

---

## Decisiones de diseño registradas

| Decisión | Motivo |
|----------|--------|
| SQLite en lugar de PostgreSQL/MariaDB | Suficiente para <50 clientes; cero dependencias externas; backup trivial |
| Token en header HTTP (no OAuth) | Simplicidad: el panel cliente solo necesita `urllib.request` sin dependencias |
| Heartbeat pull (panel envía → Central recibe) | No requiere que Central tenga acceso SSH a los clientes; funciona detrás de NAT |
| Rotación manual de tokens | Suficiente para <50 clientes; no justifica automatismo hasta Fase 12 |
| Separación Central / panel cliente | Central es el CRM del equipo DASC; el panel es la herramienta del cliente |
