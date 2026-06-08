# Arquitectura soporte central/local Vigex

## Resumen

La arquitectura de soporte central/local se divide en tres capas:

- Cliente.
- Panel local Vigex.
- Panel central Vigex.

## Diagrama lógico textual

Cliente PyME
    |
    | crea solicitud
    v
Panel local Vigex del cliente
    |
    | guarda ticket local
    |
    | intenta enviar a central
    v
Panel central Vigex
    |
    | equipo Vigex gestiona
    v
Estado central actualizado
    |
    | sincronización desde local
    v
Vista cliente del estado del ticket

## Separación de vistas

### Cliente

Rutas:

- /soporte
- /soporte/estado/{ticket_id}

Uso:

- Crear solicitud.
- Consultar estado.
- Ver seguimiento básico.

### Técnico local Vigex

Rutas:

- /soporte/tickets
- /soporte/tickets/{ticket_id}
- /soporte/sincronizacion

Uso:

- Diagnóstico.
- Gestión local.
- Reintentos.
- Sincronización.
- Plantillas.
- Resumen técnico.

### Equipo central Vigex

Rutas:

- /
- /tickets/{central_ticket_id}

Uso:

- Gestión centralizada.
- Multi-cliente.
- Estado y prioridad central.
- Historial central.

## Despliegue de laboratorio

En lab-pruebas:

- Panel local cliente: http://192.168.1.250:8000
- Panel central Vigex por Nginx: http://192.168.1.250
- Backend central directo: http://192.168.1.250:8010

## Despliegue objetivo

En producto real:

- Panel local cliente: servidor local o cloud del cliente.
- Panel central Vigex: VPS/servidor propio.
- Dominio central: central.vigex.es o soporte.vigex.es.
- Comunicación: HTTPS + token de cliente.

## Decisión sobre DNS local

Vigex puede preparar Nginx local, pero no debe asumir control del DNS del cliente.

Modo básico:

- Acceso por IP.

Modo recomendado:

- Cliente crea registro DNS interno.
- Ejemplo: panel.empresa.lan -> IP del servidor local.

## Conclusión

La arquitectura permite operar Vigex como servicio gestionado: cada cliente conserva su panel local y Vigex mantiene una central propia para soporte multi-cliente.
