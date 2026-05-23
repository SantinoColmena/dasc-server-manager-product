# R-047 - Validación de release candidate v1.0-rc1

## Tarea

Publicar versión 1.0 candidata.

## Objetivo de validación

Comprobar que el repositorio está preparado para crear una primera versión candidata orientada a cliente real o piloto de pago.

## Validaciones realizadas

### 1. Estado del repositorio

Comando recomendado:

~~~powershell
git status
~~~

Resultado esperado:

~~~text
nothing to commit, working tree clean
~~~

### 2. Historial reciente

Comando recomendado:

~~~powershell
git log --oneline -8
~~~

Debe aparecer el cierre de Fase 5 y la limpieza previa a Fase 6.

### 3. Documentación mínima existente

Debe existir documentación relacionada con:

- Fase 5 cerrada.
- Pilotos reales.
- SLA.
- Costes reales.
- Checklist de instalación.
- Paquetes comerciales.
- Arquitecturas Lite, PyME y Pro.

### 4. Release candidate documentada

Debe existir el archivo:

~~~text
docs/release/v1.0-rc1.md
~~~

### 5. Revisión de secretos

Antes de crear el tag se debe comprobar que no se suben claves, tokens ni contraseñas reales.

Comandos recomendados:

~~~powershell
git grep -n "TELEGRAM_BOT_TOKEN"
git grep -n "ADMIN_PASSWORD"
git grep -n "dascpass"
~~~

Si aparecen valores de ejemplo en documentación o plantillas, deben estar claramente marcados como ejemplo.

### 6. Tag propuesto

El tag recomendado para esta versión candidata es:

~~~text
v1.0-rc1
~~~

No debe crearse hasta que esta validación quede revisada.

## Resultado

Estado actual:

- Release candidate preparada documentalmente.
- Pendiente de revisión final del repositorio.
- Pendiente de creación del tag `v1.0-rc1`.

## Conclusión

R-047 puede avanzar a estado "En curso".

Solo se marcará como "Hecha" cuando se cree el tag de release candidate y el repositorio quede limpio después del commit.
