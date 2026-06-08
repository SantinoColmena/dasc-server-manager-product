# API de producto — DASC Server Manager
## R-086 / Ruta 12.2

Documentación de los endpoints de la API del panel DASC disponibles para
integraciones externas. La API sigue convenciones REST estándar y responde en JSON.

> **Autenticación:** Los endpoints marcados como (autenticado) requieren una sesión
> activa (cookie de sesión). Los endpoints públicos no requieren autenticación.
> **Nota de seguridad:** El panel no expone credenciales en query params ni URLs.

---

## Endpoints públicos

### `GET /health`

Estado básico del servicio. Útil para healthchecks de nginx/HAProxy.

```http
GET /health HTTP/1.1
Host: panel.cliente.local
```

**Respuesta:**
```json
{
    "status": "ok",
    "app": "DASC Server Manager"
}
```

---

### `GET /api/v1/info`

Información de la instalación DASC. Para verificar versión y compatibilidad.

```http
GET /api/v1/info HTTP/1.1
```

**Respuesta:**
```json
{
    "producto": "DASC Server Manager",
    "api_version": "1.0",
    "panel_version": "1.0-rc1",
    "build_date": "2026-06-08",
    "endpoints_publicos": ["GET /health", "GET /api/v1/info", "GET /api/v1/heartbeat"],
    "endpoints_autenticados": ["GET /api/soporte/faq", "..."],
    "documentacion": "/api/docs"
}
```

---

### `GET /api/v1/heartbeat`

Métricas de salud del servidor en tiempo real. Usado por DASC Central Support
para el dashboard de salud global.

```http
GET /api/v1/heartbeat HTTP/1.1
```

**Respuesta:**
```json
{
    "cliente_id": "empresa-sl",
    "nombre_cliente": "Empresa S.L.",
    "version_panel": "1.0-rc1",
    "disco_pct": 62,
    "backups_ok": 1,
    "ultimo_backup": "2026-06-08 03:00:15",
    "alertas_activas": 0,
    "servicios_activos": 4,
    "uptime_segundos": 86400
}
```

---

## Endpoints autenticados

Todos los endpoints de esta sección requieren sesión activa (cookie `session`).
Si la sesión no existe, se devuelve `{"error": "no autenticado"}` con HTTP 401.

---

### `GET /api/soporte/faq`

Búsqueda en la base de conocimiento (FAQ) del panel.

**Query params:**
| Param | Tipo | Descripción |
|-------|------|-------------|
| `q` | string | Texto de búsqueda (opcional; sin `q` devuelve todas) |
| `desde` | string | URL de la página de origen (para boost de relevancia) |

```http
GET /api/soporte/faq?q=backup+fallo&desde=/backups HTTP/1.1
Cookie: session=<cookie>
```

**Respuesta:**
```json
{
    "resultados": [
        {
            "id": "backup-fallo",
            "pregunta": "¿Qué hago si una copia de seguridad falló?",
            "respuesta": "Ve a Copias en el menú lateral...",
            "palabras_clave": ["backup", "copia", "fallo", "error"]
        }
    ],
    "total": 1
}
```

---

### `POST /api/soporte/tickets`

Crea un ticket de soporte desde una aplicación externa (equivale al FAB del panel).

**Body (JSON):**
```json
{
    "tipo": "bug",
    "descripcion": "El informe no se envía por email.",
    "url_pagina": "/informes"
}
```

**Headers:**
```http
Content-Type: application/json
X-CSRF-Token: <token_csrf>
```

**Respuesta:**
```json
{
    "ok": true,
    "msg": "Ticket creado con ID LOCAL-2026-0042",
    "ticket_id": "LOCAL-2026-0042"
}
```

---

### `GET /api/soporte/estado/{ticket_id}`

Devuelve el estado actual de un ticket (local y en Central Support si está configurado).

```http
GET /api/soporte/estado/LOCAL-2026-0042 HTTP/1.1
Cookie: session=<cookie>
```

**Respuesta:**
```json
{
    "ok": true,
    "ticket_id": "LOCAL-2026-0042",
    "estado": "En análisis",
    "central_ticket_id": "CENTRAL-2026-0001",
    "estado_central": "En análisis",
    "sincronizado": true
}
```

---

## Códigos de estado HTTP

| Código | Significado en DASC |
|--------|---------------------|
| 200 | Operación exitosa |
| 303 | Redirección (respuestas de formularios) |
| 401 | No autenticado (sesión no válida o expirada) |
| 403 | Permisos insuficientes (el usuario no tiene el permiso requerido) |
| 404 | Recurso no encontrado |
| 422 | Parámetros de entrada inválidos (Pydantic validation error) |
| 500 | Error interno del panel |

---

## OpenAPI / Swagger

El panel expone automáticamente la documentación interactiva generada por FastAPI:
- **Swagger UI:** `http://panel.cliente.local/docs`
- **ReDoc:** `http://panel.cliente.local/redoc`
- **Schema JSON:** `http://panel.cliente.local/openapi.json`

---

## Versioning de la API

La API sigue versionado semántico en la URL (`/api/v1/`).
La versión `v1` es la actual y se mantendrá compatible hasta que DASC llegue a v2.0.
Los cambios que rompen la compatibilidad hacia atrás siempre suben la versión mayor.

---

## Integraciones de terceros conocidas

| Sistema | Integración | Configuración |
|---------|-------------|---------------|
| DASC Central Support | Push de tickets + heartbeat | `CENTRAL_SUPPORT_*` en `config.env` |
| Jira / GitHub Issues | Webhook POST al crear ticket | `JIRA_WEBHOOK_URL` en `config.env` |
| Grafana | Iframe embed del dashboard | `GRAFANA_URL` en `config.env` |
| Cacti | Iframe del gráfico de red | `CACTI_URL` en `config.env` |
| Email (SMTP) | Alertas + informes + tickets | `NOTIF_SMTP_*` en `config.env` |
| Telegram | Alertas en tiempo real | `NOTIF_TELEGRAM_*` en `config.env` |
