# R-049 - Validación del sistema básico de tickets

## Tarea

Montar sistema básico de tickets.

## Objetivo de validación

Comprobar que DASC Server Manager dispone de una forma mínima y ordenada de registrar incidencias y solicitudes de soporte.

## Elementos validados

### 1. Plantilla de incidencia técnica

Archivo esperado:

~~~text
.github/ISSUE_TEMPLATE/incidencia.yml
~~~

Uso:

- Fallos.
- Errores.
- Comportamientos inesperados.
- Problemas en backups, restauración, logs, alertas, servicios o instalación.

### 2. Plantilla de solicitud de soporte

Archivo esperado:

~~~text
.github/ISSUE_TEMPLATE/solicitud_soporte.yml
~~~

Uso:

- Dudas.
- Revisiones.
- Cambios menores.
- Validaciones.
- Soporte funcional.

### 3. Configuración de Issues

Archivo esperado:

~~~text
.github/ISSUE_TEMPLATE/config.yml
~~~

Validación:

- Las issues en blanco quedan desactivadas.
- Se fuerza el uso de plantillas.
- Se reduce el riesgo de tickets incompletos.

### 4. Documento de soporte

Archivo esperado:

~~~text
docs/soporte/sistema_tickets.md
~~~

Debe incluir:

- Objetivo del sistema.
- Tipos de ticket.
- Prioridades.
- Flujo de trabajo.
- Reglas de seguridad.
- Criterios de cierre.

## Prueba manual recomendada

Desde GitHub:

1. Entrar en el repositorio.
2. Abrir la pestaña Issues.
3. Pulsar en New issue.
4. Comprobar que aparecen las plantillas:
   - Incidencia técnica.
   - Solicitud de soporte.
5. Verificar que no se permite una issue en blanco.
6. Cancelar la creación si solo se está probando.

## Resultado esperado

El sistema debe permitir registrar incidencias de forma ordenada y evitar que el soporte quede perdido en mensajes sueltos.

## Estado

R-049 queda preparada para cierre cuando estos archivos estén subidos al repositorio y el estado de Git quede limpio.
