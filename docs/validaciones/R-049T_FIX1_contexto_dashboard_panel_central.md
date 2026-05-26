# R-049T-FIX1 - Corregir contexto dashboard panel central

## Objetivo

Corregir la lógica del dashboard central para que entregue al template las métricas y filtros añadidos en R-049T.

## Estado

En curso.

## Problema detectado

Durante la aplicación inicial de R-049T, la sustitución automática del bloque `dashboard()` no localizó el patrón esperado en `main.py`.

Como resultado, se actualizaron las plantillas visuales, pero el backend seguía enviando solo:

- tickets
- total
- demo_client_id

El nuevo template necesita además:

- total_filtrado
- nuevos
- en_gestion
- cerrados
- criticos
- estados
- prioridades
- filters

## Solución aplicada

Se reemplaza el bloque completo del dashboard usando búsqueda por índices entre:

- @app.get("/", response_class=HTMLResponse)
- @app.get("/health")

## Validación esperada

- main.py central compila.
- Dashboard carga sin variables vacías.
- Métricas aparecen correctamente.
- Filtros por estado, prioridad y búsqueda funcionan.
