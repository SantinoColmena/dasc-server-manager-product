# R-049T-FIX1 - Corregir contexto dashboard panel central

## Objetivo

Corregir la lógica del dashboard central para que entregue al template las métricas y filtros añadidos en R-049T.

## Estado

En curso.

## Problema detectado

Durante la aplicación inicial de R-049T, la sustitución automática del bloque dashboard no localizó el patrón esperado en main.py.

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

## Incidencia adicional

El primer intento de FIX1 solo creó documentación, pero no modificó main.py.

El cambio real se aplica posteriormente sustituyendo el bloque del dashboard desde:

- @app.get("/", response_class=HTMLResponse)

hasta el siguiente decorador FastAPI encontrado en el archivo.

## Solución aplicada

Se actualiza la función dashboard para:

- Cargar hasta 500 tickets centrales.
- Calcular métricas de estado y prioridad.
- Filtrar por estado.
- Filtrar por prioridad.
- Buscar por texto libre.
- Enviar al template todas las variables necesarias.

## Validación esperada

- main.py central compila.
- Dashboard carga sin variables vacías.
- Métricas aparecen correctamente.
- Filtros por estado, prioridad y búsqueda funcionan.
