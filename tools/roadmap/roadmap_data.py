# -*- coding: utf-8 -*-
"""Datos estructurados del roadmap de Vigex.

Esta es la cara ESTRUCTURADA del roadmap; su equivalente narrativo para leer
es ``docs/ROADMAP.md``. Ambos describen el mismo plan y se editan juntos.

El Excel ``docs/roadmap/Vigex_Roadmap.xlsx`` se genera SIEMPRE desde aquí con
``generar_roadmap_xlsx.py`` y NUNCA se edita a mano (se regenera).

Convenciones:
- ``tipo``:      Fase | Ruta | Tarea | Subtarea
- ``estado``:    Cerrada | En curso | Siguiente | Planificada | Backlog |
                 Aplazada | Diferida
- ``horizonte``: "" | Ahora | Siguiente | Después
- ``id``:        identificador R-xxx monótono y único; subrutas con sufijo
                 de letra (R-049A). Nunca se reutiliza ni se renumera.
"""

META = {
    "producto": "Vigex",
    "version": "v1.0-rc1",
    "fase_actual": "Fase 6 - Endurecimiento y producto vendible",
    "actualizado": "2026-06-06",
    "fuente": "docs/ROADMAP.md (fuente de verdad). Este Excel es una vista derivada.",
}

# Columnas de la hoja Roadmap, en orden.
COLUMNAS = [
    "Fase", "Ruta", "ID", "Título", "Tipo", "Estado", "Horizonte",
    "Gate", "Entregable / Notas", "Evidencia",
]


def fila(fase, ruta, rid, titulo, tipo, estado, horizonte="", gate="",
         notas="", evidencia=""):
    """Construye una fila del roadmap como dict homogéneo."""
    return {
        "Fase": fase, "Ruta": ruta, "ID": rid, "Título": titulo, "Tipo": tipo,
        "Estado": estado, "Horizonte": horizonte, "Gate": gate,
        "Entregable / Notas": notas, "Evidencia": evidencia,
    }


ROADMAP = [
    # ------------------------------------------------------------------ Fase 0-5 (cerradas, resumen)
    fila("Fase 0", "", "R-001 -> R-005", "Preparación", "Fase", "Cerrada", "",
         "", "Separación académico/producto, propuesta de valor, paquetes, inventario, límites de responsabilidad.",
         "docs/validaciones/"),
    fila("Fase 1", "", "R-006 -> R-014", "Núcleo estable", "Fase", "Cerrada", "",
         "", "Perfiles, instalador idempotente, motor de backups (historial + scheduler), logs, UX, laboratorio, v0.1.",
         "docs/validaciones/"),
    fila("Fase 2", "", "R-015 -> R-024", "Seguridad y restauración", "Fase", "Cerrada", "",
         "", "Hash de claves, secretos, HTTPS/proxy, endurecimiento SSH (allowlist), restauración controlada, retención, alertas, v0.2.",
         "docs/validaciones/"),
    fila("Fase 3", "", "R-025 -> R-031", "Despliegues adaptables", "Fase", "Cerrada", "",
         "", "Perfiles 1/2/3 servidores, NAS/SFTP, copia externa cifrada GPG, asistente por perfil, docs de arquitectura.",
         "docs/validaciones/"),
    fila("Fase 4", "", "R-032 -> R-039", "Demo y validación", "Fase", "Cerrada", "",
         "", "Modo demo, dominio + web, manual rápido, base de conocimiento, 30 prospectos, guion de demo, checklist, 1er piloto.",
         "docs/validaciones/"),
    fila("Fase 5", "", "R-040 -> R-047", "Pilotos reales y Release Candidate", "Fase", "Cerrada", "",
         "", "Pilotos 1/2/3, SLA realista, costes reales y publicación de v1.0-rc1 (R-047).",
         "docs/validaciones/"),

    # ------------------------------------------------------------------ Fase 6 (en curso)
    fila("Fase 6", "", "R-048 -> R-057", "Endurecimiento y producto vendible", "Fase", "En curso", "Ahora",
         "F6-GATE-06", "Dejar el producto limpio, seguro, instalable desde cero y honesto ANTES de cerrar ventas.",
         "docs/planificacion/fase6_reordenacion_antes_de_ventas.md"),

    # Rutas cerradas de Fase 6
    fila("Fase 6", "6.1 Soporte central/local", "R-049A -> R-049Y", "Soporte central/local", "Ruta", "Cerrada", "",
         "F6-GATE-05", "Formulario, SQLite, estados, plantillas, panel central, sincronización bidireccional, cola offline.",
         "docs/validaciones/R-049*, F6-GATE-05*"),
    fila("Fase 6", "6.2 Operación e informes", "R-050", "Informe mensual v1", "Tarea", "Cerrada", "",
         "", "Informe operativo de backups/restore/alertas.",
         "docs/validaciones/R-050_cierre_informe_mensual_v1.md"),
    fila("Fase 6", "6.3 Despliegue cliente", "R-050B", "Nginx panel local", "Tarea", "Cerrada", "",
         "", "Reverse proxy del panel local (corrección de colisión de R-050).",
         "docs/validaciones/R-050_cierre_nginx_panel_local_cliente.md"),
    fila("Fase 6", "6.4 Instaladores adaptables", "R-051 -> R-051H", "Instaladores adaptables (sin IPs fijas)", "Ruta", "Cerrada", "",
         "F6-GATE-04", "Parametrización de IPs/perfiles en los instaladores; eliminadas IPs de laboratorio.",
         "docs/validaciones/R-051H_cierre_global_instaladores_adaptables.md, F6-GATE-04*"),
    fila("Fase 6", "6.5 Seguridad de infraestructura", "R-052 -> R-052H", "Seguridad de infraestructura", "Ruta", "Cerrada", "",
         "", "Secretos, permisos, puertos, SSH runtime, usuario dedicado, endurecimiento de Central Support.",
         "docs/validaciones/R-052H_cierre_global_revision_seguridad.md"),
    fila("Fase 6", "6.6 Auditoría de código", "H-1, M-1..M-5, L-1..L-6", "Auditoría de seguridad de código (extiende R-052)", "Ruta", "Cerrada", "",
         "", "Inyección SSH (H-1), CORS/CSRF, cookie, fuerza bruta, hash central PBKDF2, token tiempo constante. L-4 y L-6 diferidos.",
         "docs/auditoria/auditoria_codigo_aplicacion_seguridad.md"),

    # Ruta 6.7 - Validación instalación desde cero
    fila("Fase 6", "6.7 Validación instalación desde cero", "R-053", "Validación de instalación desde cero por perfil", "Tarea", "Siguiente", "Ahora",
         "F6-GATE-06", "Instalar en VM limpia por perfil, sin pasos manuales ocultos. Informe + checklist reproducible.", ""),
    fila("Fase 6", "6.7 Validación instalación desde cero", "R-053A", "Validación perfil Lite (1 servidor + copia externa)", "Subtarea", "Planificada", "Ahora", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.7 Validación instalación desde cero", "R-053B", "Validación perfil Standard (2 servidores)", "Subtarea", "Planificada", "Ahora", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.7 Validación instalación desde cero", "R-053C", "Validación perfil Pro (3 servidores)", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.7 Validación instalación desde cero", "R-053D", "Checklist reproducible + informe consolidado", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),

    # Ruta 6.8 - Endurecimiento infraestructura
    fila("Fase 6", "6.8 Endurecimiento de infraestructura", "R-054", "Cierre de endurecimiento de infraestructura", "Tarea", "Planificada", "Siguiente",
         "F6-GATE-06", "Pendientes de R-052H y de la auditoría. Al activar HTTPS: VIGEX_SESSION_HTTPS_ONLY=true.", ""),
    fila("Fase 6", "6.8 Endurecimiento de infraestructura", "R-054A", "UFW (firewall) por host", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.8 Endurecimiento de infraestructura", "R-054B", "HTTPS real / certbot + sesión https_only", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.8 Endurecimiento de infraestructura", "R-054C", "fail2ban sobre el log de login", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.8 Endurecimiento de infraestructura", "R-054D", "pip-audit (auditoría de dependencias)", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),

    # Ruta 6.9 - Windows y limpieza final
    fila("Fase 6", "6.9 Experiencia Windows y limpieza final", "R-055", "Guía de uso desde Windows", "Tarea", "Planificada", "Siguiente",
         "F6-GATE-06", "Qué hace el cliente por navegador vs qué se instala en Linux.", ""),
    fila("Fase 6", "6.9 Experiencia Windows y limpieza final", "R-055A", "Acceso por navegador (qué hace el cliente)", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.9 Experiencia Windows y limpieza final", "R-055B", "Despliegue real en Linux desde PC Windows", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.9 Experiencia Windows y limpieza final", "R-055C", "Valorar script auxiliar Windows vs solo docs", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.9 Experiencia Windows y limpieza final", "R-056", "Limpieza final de repo y documentación", "Tarea", "Planificada", "Siguiente",
         "F6-GATE-06", "Estructura, docs duplicadas/comerciales, y verificar que nada promete funciones no implementadas.", ""),
    fila("Fase 6", "6.9 Experiencia Windows y limpieza final", "R-056A", "Revisión estructura de carpetas y README", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.9 Experiencia Windows y limpieza final", "R-056B", "Revisión docs duplicadas / demasiado comerciales", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.9 Experiencia Windows y limpieza final", "R-056C", "Verificar que nada promete funciones no implementadas", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.9 Experiencia Windows y limpieza final", "R-056D", "Barrido final de secretos / ejemplos / config", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),

    # Ruta 6.10 - Release interna estable
    fila("Fase 6", "6.10 Release interna estable", "R-057", "Release interna estable (freeze)", "Tarea", "Planificada", "Siguiente",
         "F6-GATE-06", "Congelar versión interna estable consolidada. Corte antes de lo comercial.", ""),
    fila("Fase 6", "6.10 Release interna estable", "R-057A", "Checklist maestro de regresión", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.10 Release interna estable", "R-057B", "Changelog consolidado", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.10 Release interna estable", "R-057C", "Smoke tests básicos (script)", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),
    fila("Fase 6", "6.10 Release interna estable", "R-057D", "Congelado del tag + validación instalable", "Subtarea", "Planificada", "Siguiente", "F6-GATE-06", "", ""),

    # Cierre comercial de Fase 6
    fila("Fase 6", "Cierre comercial", "R-048", "Primer cliente de pago", "Tarea", "Aplazada", "Después",
         "F6-GATE-06", "Aplazada a propósito hasta superar F6-GATE-06. No cerrar sin cliente real de pago o feedback documentado.", ""),

    # ------------------------------------------------------------------ Fase 7 (planificada, detalle medio)
    fila("Fase 7", "", "R-058 -> R-070 (aprox.)", "Central cloud y multi-cliente", "Fase", "Planificada", "Siguiente",
         "F7-GATE", "Convertir Vigex en producto multi-cliente: una Central propia (VPS Vigex) que agregue el estado de todas las instalaciones.", ""),
    fila("Fase 7", "7.1 Diseño central cloud", "", "Arquitectura de la Central (VPS, HTTPS, topología)", "Ruta", "Planificada", "Siguiente", "F7-GATE", "", ""),
    fila("Fase 7", "7.2 Central VPS + HTTPS productivo", "", "Despliegue real de Central Support con dominio + TLS + Nginx", "Ruta", "Planificada", "Siguiente", "F7-GATE", "", ""),
    fila("Fase 7", "7.3 Panel multi-cliente", "", "Gestión de clientes, tokens por cliente, rotación y revocación", "Ruta", "Planificada", "Siguiente", "F7-GATE", "", ""),
    fila("Fase 7", "7.4 Dashboard de salud", "", "Heartbeat de instalaciones: último backup, alertas, soporte, último contacto", "Ruta", "Planificada", "Siguiente", "F7-GATE", "", ""),
    fila("Fase 7", "7.5 Seguridad central", "", "2FA del equipo Vigex, backup de la Central, auditoría de login central", "Ruta", "Planificada", "Siguiente", "F7-GATE", "", ""),

    # ------------------------------------------------------------------ Fase 8 (backlog grueso)
    fila("Fase 8", "", "(se numera al planificar)", "Comercial y escalado", "Fase", "Backlog", "Después",
         "", "Se desglosa en R-xxx solo cuando se planifique.", ""),
    fila("Fase 8", "Objetivo", "", "Oferta y onboarding (paquetes finales, precios, alta de cliente)", "Ruta", "Backlog", "Después", "", "", ""),
    fila("Fase 8", "Objetivo", "", "SLA y legal definitivos (tiempos, exclusiones, condiciones)", "Ruta", "Backlog", "Después", "", "", ""),
    fila("Fase 8", "Objetivo", "", "Pilotos pagados (1 y 2) ejecutados y feedback aplicado", "Ruta", "Backlog", "Después", "", "", ""),
    fila("Fase 8", "Objetivo", "", "Marketing mínimo (web actualizada, material honesto)", "Ruta", "Backlog", "Después", "", "", ""),
    fila("Fase 8", "Objetivo", "", "Release v1.0 comercial limitada (solo si pilotos+seguridad pasan)", "Ruta", "Backlog", "Después", "", "", ""),
    fila("Fase 8", "Objetivo", "", "Decisión Go/No-Go comercial documentada (puede ser No-Go)", "Ruta", "Backlog", "Después", "", "", ""),

    # ------------------------------------------------------------------ Fase 9 (backlog grueso)
    fila("Fase 9", "", "(se numera al planificar)", "Evolución (IA, Windows, refactor)", "Fase", "Backlog", "Después",
         "", "Se desglosa en R-xxx solo cuando se planifique.", ""),
    fila("Fase 9", "Objetivo", "", "IA de soporte / diagnóstico interno (ayuda al técnico, no sustituye)", "Ruta", "Backlog", "Después", "", "", ""),
    fila("Fase 9", "Objetivo", "", "Agente Windows (reporta estado / backup de carpetas)", "Ruta", "Backlog", "Después", "", "", ""),
    fila("Fase 9", "Objetivo", "", "Refactor de main.py (deuda L-6 de la auditoría)", "Ruta", "Diferida", "Después", "", "~5000 líneas en un fichero; refactor mayor.", "docs/auditoria/auditoria_codigo_aplicacion_seguridad.md"),
    fila("Fase 9", "Objetivo", "", "Integraciones / API de producto y observabilidad avanzada", "Ruta", "Backlog", "Después", "", "", ""),
    fila("Fase 9", "Objetivo", "", "Migración de la Central de SQLite a PostgreSQL/MariaDB", "Ruta", "Backlog", "Después", "", "Si crece el número de clientes.", ""),
]


GATES = [
    # gate, nombre, estado, criterio de salida (real), evidencia
    ("F6-GATE-01", "Instalación API en Ubuntu", "Cerrada",
     "Instalación limpia y reinstalación sobre entorno existente OK.",
     "F6-GATE-01A / 01B"),
    ("F6-GATE-02", "API + DB/logs (2 servidores)", "Cerrada",
     "Eventos reales visibles en el panel desde la DB remota.",
     "F6-GATE-02A / 02B"),
    ("F6-GATE-03", "Backup completo + restauración (2 servidores)", "Cerrada",
     "Backup automatizado, retención/limpieza y restauración controlada validados.",
     "F6-GATE-03 / 03D / 03E / 03F / 03G"),
    ("F6-GATE-04", "Instaladores y perfiles", "Cerrada",
     "IPs parametrizadas por perfil; sin IPs de laboratorio; SSH allowed_hosts limpio.",
     "F6-GATE-04A..04H"),
    ("F6-GATE-05", "Soporte central/local", "Cerrada",
     "Soporte sin GitHub: canales reales, plantillas, separación cliente/técnico.",
     "F6-GATE-05A..05G"),
    ("F6-GATE-06", "Producto vendible", "Pendiente",
     "Instalación desde cero OK en 3 perfiles (R-053) + UFW/HTTPS/fail2ban/pip-audit "
     "(R-054) + docs Windows (R-055) + repo/docs limpios sin promesas falsas (R-056) "
     "+ release interna congelada (R-057) + check_api_package_installable.ps1 y "
     "check_repo_clean.ps1 en verde.",
     "-"),
    ("F7-GATE", "Central productiva", "Pendiente",
     "Central accesible por HTTPS, >=1 instalación reportando estado real, tokens "
     "gestionables y backup de la Central verificado.",
     "-"),
]


PERFILES = [
    # perfil, arquitectura, uso recomendado, decisión
    ("Lite", "1 servidor + copia externa OBLIGATORIA", "PyME muy pequeña / laboratorio",
     "No vender sin copia externa real."),
    ("Standard", "2 servidores (panel/API + DB/backups)", "Objetivo inicial PyME",
     "Perfil objetivo de las primeras ventas."),
    ("Pro", "3 servidores (API / DB-logs / backups)", "Cliente con más criticidad",
     "No priorizar antes de Standard estable."),
    ("Central Vigex", "VPS propio del equipo Vigex", "Equipo Vigex (multi-cliente)",
     "Clave para producto real (Fase 7)."),
]


DECISIONES = [
    # fecha, decisión, motivo
    ("2026-06-06", "ROADMAP.md pasa a ser la fuente de verdad única; el Excel es vista derivada.",
     "Los 3 Excel previos se desincronizaron del repo."),
    ("2026-06-06", "Se congela la numeración real del repo (R-001..R-052x); no se renumera lo existente.",
     "Mínimo cambio, no romper referencias en docs/ y commits."),
    ("2026-06-06", "Colisión de R-050 resuelta: Nginx panel local -> R-050B.",
     "R-050 se había usado para dos trabajos distintos."),
    ("2026-06-06", "Fase 6 redefinida como 'Endurecimiento y producto vendible'; ventas (R-048) al final.",
     "Calidad antes que velocidad comercial (plan de reordenación)."),
    ("2026-06-06", "Se detalla solo Fase 6-7; Fase 8-9 quedan como backlog grueso.",
     "Evitar el churn de planificar 2028 al detalle."),
    ("2026-06-06", "Gates: se mantiene la convención real F6-GATE-xx; se descartan los G-00..G-36 genéricos.",
     "Eran texto de relleno idéntico, sin criterio real."),
]
