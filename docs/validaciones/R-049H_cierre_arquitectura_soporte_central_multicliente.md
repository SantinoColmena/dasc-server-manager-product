# R-049H - Cierre arquitectura de soporte central multi-cliente

## Objetivo

Cerrar la definición de arquitectura objetivo para centralizar incidencias de varios clientes en un panel central DASC propio.

## Estado

Cerrada.

## Documento creado

~~~text
docs/soporte/arquitectura_soporte_central_multicliente.md
~~~

## Validación creada

~~~text
docs/validaciones/R-049H_arquitectura_soporte_central_multicliente.md
~~~

## Decisión principal

DASC Server Manager tendrá un panel central propio para soporte multi-cliente.

Jira, Zammad, email, WhatsApp Business u otras herramientas externas quedan como integraciones opcionales futuras.

No serán el núcleo inicial del soporte.

## Arquitectura definida

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
        ↓
Integraciones opcionales
~~~

## Separación establecida

Se separan claramente:

~~~text
Panel local del cliente
Panel central DASC
Roles del cliente
Roles internos DASC
Integraciones opcionales
Partes gratuitas
Partes que pueden requerir pago
~~~

## Roles del cliente

~~~text
cliente_admin
cliente_operador
cliente_lector
~~~

## Roles internos DASC

~~~text
dasc_tecnico
dasc_admin
dasc_superadmin
~~~

## Regla de coste

Se acuerda la siguiente regla de producto:

~~~text
Implementar primero todo lo que pueda hacerse sin coste de licencia.
Pausar cualquier parte que requiera pago.
Documentar claramente lo que queda pendiente por coste.
Retomar partes de pago cuando haya cliente real, presupuesto o necesidad comercial.
~~~

## Qué se puede implementar ahora sin pagar

~~~text
Prototipo local del panel central
API central en FastAPI
SQLite central
Clientes demo
Tokens locales
Recepción de incidencias
Vista técnica central
Validación en laboratorio
~~~

## Qué queda en pausa si requiere coste

~~~text
Dominio público real
VPS público permanente
Correo profesional
Plan Jira de pago
Plan Zammad hosted de pago
WhatsApp Business API
SLA contractual real
Monitorización externa comercial
~~~

## Decisión sobre el módulo actual de soporte

El módulo actual en `/soporte` queda clasificado como:

~~~text
Prototipo funcional
Base técnica reutilizable
No arquitectura final multi-cliente
No panel cliente definitivo
No integración real con Jira/Zammad
~~~

## Criterio de cierre

R-049H se considera cerrada porque:

- Existe documento de arquitectura central.
- Se define el panel local del cliente.
- Se define el panel central DASC.
- Se separan roles de cliente y roles DASC.
- Se aclara que Jira/Zammad son opcionales.
- Se separa lo gratuito de lo que puede requerir pago.
- Se deja claro que el módulo actual es prototipo funcional.
- Se prepara el camino para un prototipo gratuito de API central.

## Próxima tarea recomendada

~~~text
R-049I - Prototipo local de API central de soporte
~~~

## Conclusión

DASC Server Manager queda alineado con una arquitectura más profesional de servicio gestionado.

El soporte no dependerá de que el técnico entre en cada panel local de cliente, sino que evolucionará hacia un panel central propio de DASC.
