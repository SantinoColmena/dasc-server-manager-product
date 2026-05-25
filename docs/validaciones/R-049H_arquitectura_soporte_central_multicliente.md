# R-049H - Arquitectura de soporte central multi-cliente

## Objetivo

Definir la arquitectura objetivo para centralizar incidencias de varios clientes en un panel central DASC propio.

## Estado

Cerrada.

## Contexto

Durante R-049A a R-049F se implementó un módulo funcional de soporte dentro del panel actual.

En R-049G se restringió el acceso a rutas internas de soporte.

En R-049G-ADJUST se aclaró que `admin` es solo una simplificación de laboratorio y que en producto real deben separarse `cliente_admin` y `dasc_tecnico`.

R-049H define la arquitectura final recomendada: panel local del cliente separado de panel central DASC.

## Decisión tomada

DASC tendrá un panel central propio.

Jira, Zammad y otras herramientas serán integraciones opcionales futuras.

## Regla de coste

Se implementará todo lo posible sin coste de licencia.

Cualquier parte que requiera pago se dejará documentada y en pausa hasta que exista cliente real, presupuesto o necesidad comercial.

## Documento creado

~~~text
docs/soporte/arquitectura_soporte_central_multicliente.md
~~~

## Arquitectura objetivo

~~~text
Panel local del cliente
        ↓
API central DASC
        ↓
Panel central DASC
        ↓
Equipo técnico DASC
        ↓
Integraciones opcionales
~~~

## Separación de roles

Roles del cliente:

~~~text
cliente_admin
cliente_operador
cliente_lector
~~~

Roles internos DASC:

~~~text
dasc_tecnico
dasc_admin
dasc_superadmin
~~~

## Qué se puede hacer ahora sin pagar

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
Dominio público
VPS permanente
Correo profesional
Jira de pago
Zammad hosted de pago
WhatsApp Business API
SLA contractual real
~~~

## Criterio de validación

R-049H se considera preparada cuando:

- Existe documento de arquitectura central.
- Se define panel local cliente.
- Se define panel central DASC.
- Se separan roles cliente y DASC.
- Se aclara que Jira/Zammad son opcionales.
- Se separa lo gratuito de lo que puede requerir pago.
- Se deja claro que el módulo actual es prototipo funcional, no arquitectura final multi-cliente.

## Próximo paso recomendado

Crear la primera estructura gratuita del panel central:

~~~text
R-049I - Prototipo local de API central de soporte
~~~

## Conclusión

R-049H corrige el enfoque hacia una arquitectura profesional de servicio gestionado multi-cliente.
