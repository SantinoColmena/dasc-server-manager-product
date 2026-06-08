# R-049G-ADJUST - Cierre aclaración de roles cliente y técnico DASC

## Objetivo

Cerrar la aclaración conceptual de roles entre el panel local del cliente y el futuro panel central DASC.

## Estado

Cerrada.

## Documento ajustado

~~~text
docs/soporte/separacion_cliente_tecnico_soporte.md
~~~

## Validación ajustada

~~~text
docs/validaciones/R-049G_ADJUST_roles_cliente_tecnico_dasc.md
~~~

## Decisión principal

La equivalencia:

~~~text
admin del panel actual = técnico DASC definitivo
~~~

no debe mantenerse como modelo final.

## Aclaración aceptada

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

El `cliente_admin` pertenece a la empresa cliente y administra elementos propios de su instalación.

No debe acceder a la gestión interna global de soporte DASC.

## Roles DASC

~~~text
dasc_tecnico
dasc_admin
dasc_superadmin
~~~

El `dasc_tecnico` pertenece al equipo DASC y debe trabajar desde un panel central propio.

## Arquitectura deseada

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

## Resultado

R-049G queda conceptualmente ajustada.

La restricción actual con `is_admin(request)` es válida para laboratorio, pero no representa la arquitectura final multi-cliente.

## Próxima tarea

~~~text
R-049H - Arquitectura de soporte central multi-cliente
~~~

## Conclusión

El proyecto queda alineado con una arquitectura más profesional:

- Panel cliente limitado.
- Panel técnico DASC separado.
- Incidencias centralizadas.
- Jira/Zammad como integración opcional futura.
