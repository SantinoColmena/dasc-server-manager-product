# Protocolo de uso de canales de soporte

## Objetivo

Definir cómo debe actuar el equipo DASC según el canal por el que entra una solicitud de cliente.

## Canal: Email

### Uso recomendado

Canal principal para la mayoría de solicitudes.

### Protocolo

1. Leer solicitud.
2. Confirmar recepción.
3. Crear ticket interno.
4. Clasificar prioridad.
5. Solicitar más información si falta.
6. Diagnosticar.
7. Responder con resultado o siguiente paso.
8. Cerrar ticket con evidencia.

## Canal: Formulario

### Uso recomendado

Canal estructurado para evitar información incompleta.

### Protocolo

1. Revisar campos recibidos.
2. Crear ticket interno.
3. Validar prioridad.
4. Contactar si falta información.
5. Actuar según tipo de solicitud.
6. Cerrar con evidencia.

## Canal: WhatsApp

### Uso recomendado

Canal rápido, pero controlado.

### Protocolo

1. Confirmar recepción de forma breve.
2. No resolver cambios complejos solo por chat.
3. Crear ticket interno.
4. Pedir evidencia formal si hace falta.
5. Informar del seguimiento por email o canal acordado.

## Canal: Teléfono

### Uso recomendado

Solo para urgencias o planes con soporte prioritario.

### Protocolo

1. Escuchar incidencia.
2. Confirmar datos mínimos.
3. Crear ticket interno.
4. Ejecutar diagnóstico inicial.
5. Enviar resumen por escrito.
6. Cerrar con evidencia.

## Canal: Portal futuro

### Uso recomendado

Cuando exista, será el canal más completo.

### Protocolo esperado

1. Cliente abre ticket.
2. Sistema registra datos.
3. Equipo DASC clasifica.
4. Cliente consulta estado.
5. Equipo cierra con evidencia.

## Regla común

Independientemente del canal de entrada:

~~~text
Toda solicitud debe terminar registrada internamente.
~~~

## Conclusión

Los canales externos deben ser simples para el cliente.

La trazabilidad y gestión técnica se mantienen dentro del equipo DASC.

## Relación con Jira o Zammad

Si DASC adopta una herramienta de ticketing, el protocolo no cambia para el cliente.

El cambio está en la gestión interna:

~~~text
Solicitud recibida por email, formulario, WhatsApp o teléfono
        ↓
Registro interno en Jira o Zammad
        ↓
Clasificación
        ↓
Diagnóstico
        ↓
Respuesta al cliente
        ↓
Cierre con evidencia
~~~

Jira Service Management Free queda como opción recomendada inicial.

Zammad self-hosted queda como alternativa open source.

Freshdesk se reserva para una fase comercial real.

GLPI se descarta temporalmente para no añadir complejidad.

## Relación con Jira o Zammad

Si DASC adopta una herramienta de ticketing, el protocolo no cambia para el cliente.

El cambio está en la gestión interna:

~~~text
Solicitud recibida por email, formulario, WhatsApp o teléfono
        ↓
Registro interno en Jira o Zammad
        ↓
Clasificación
        ↓
Diagnóstico
        ↓
Respuesta al cliente
        ↓
Cierre con evidencia
~~~

Jira Service Management Free queda como opción recomendada inicial.

Zammad self-hosted queda como alternativa open source.

Freshdesk se reserva para una fase comercial real.

GLPI se descarta temporalmente para no añadir complejidad.
