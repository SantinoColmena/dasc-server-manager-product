# R-049G-ADJUST - Aclaración de roles cliente y equipo técnico DASC

## Objetivo

Aclarar que la restricción actual de soporte usando `admin` es una medida temporal de laboratorio y no el modelo final de producto.

## Estado

Cerrada.

## Contexto

En R-049G se restringieron las rutas internas de soporte para evitar que usuarios normales pudieran acceder a:

~~~text
/soporte
/soporte/tickets
/soporte/tickets/{ticket_id}
/soporte/tickets/{ticket_id}/estado
~~~

La validación confirmó que un usuario normal recibe el aviso:

~~~text
Acceso reservado al equipo técnico DASC.
~~~

## Duda detectada

Se detecta una posible confusión:

~~~text
admin del panel actual = técnico DASC
~~~

Esa equivalencia no debe mantenerse como modelo final.

## Decisión

En laboratorio se acepta:

~~~text
admin = usuario con permisos máximos para validar restricciones
~~~

Pero en producto real debe separarse:

~~~text
cliente_admin != dasc_tecnico
~~~

## Roles del cliente

~~~text
cliente_admin
cliente_operador
cliente_lector
~~~

El `cliente_admin` pertenece a la empresa cliente.

Puede administrar elementos propios de su instalación, pero no debe acceder a la gestión interna global de soporte DASC.

## Roles DASC

~~~text
dasc_tecnico
dasc_admin
dasc_superadmin
~~~

El `dasc_tecnico` pertenece al equipo DASC y debe trabajar desde un panel central propio.

## Arquitectura deseada

El técnico DASC no debería entrar en cada panel local de cliente para revisar incidencias.

La arquitectura objetivo debe ser:

~~~text
Panel local cliente A
Panel local cliente B
Panel local cliente C
        ↓
API central DASC
        ↓
Panel central DASC
        ↓
Equipo técnico DASC
~~~

## Qué representa lo implementado hasta ahora

El módulo actual de soporte representa:

~~~text
Prototipo funcional
Base técnica reutilizable
Validación de tickets, estados, historial y plantillas
No arquitectura final multi-cliente
No panel central definitivo
~~~

## Qué debe ocurrir después

Antes de avanzar a integraciones reales con Jira/Zammad, debe documentarse la arquitectura de soporte central multi-cliente.

Siguiente tarea recomendada:

~~~text
R-049H - Arquitectura de soporte central multi-cliente
~~~

## Criterio de cierre

Este ajuste se considera cerrado cuando:

- Se documenta que `admin` es una simplificación de laboratorio.
- Se diferencia `cliente_admin` de `dasc_tecnico`.
- Se aclara que el soporte técnico debe centralizarse.
- Se evita presentar el panel local del cliente como panel técnico DASC final.
- Se prepara el camino para R-049H.

## Conclusión

R-049G queda conceptualmente ajustada.

La restricción actual es válida para laboratorio, pero el diseño final debe separar panel cliente y panel central DASC.
