# Modelo de soporte al cliente - Vigex

## Objetivo

Definir un modelo de soporte realista para clientes PyME sin obligarles a usar GitHub.

Vigex se vende como servicio gestionado, no como una simple licencia técnica.

Por tanto, el cliente debe tener canales simples para pedir ayuda, reportar incidencias o solicitar cambios.

## Principio general

GitHub es una herramienta interna del equipo Vigex.

El cliente no debe usar GitHub Issues, Pull Requests ni repositorios para pedir soporte.

## Canales de soporte para cliente

### Email de soporte

Canal recomendado como base.

Uso previsto:

- Incidencias no urgentes.
- Consultas generales.
- Solicitud de informes.
- Solicitud de cambios menores.
- Envío de evidencias o capturas.

Ejemplo:

~~~text
soporte@vigex.local
~~~

En una versión real se sustituirá por un dominio comercial.

### Formulario de soporte

Canal recomendado para estandarizar solicitudes.

Campos mínimos:

- Nombre de la empresa.
- Persona de contacto.
- Email o teléfono.
- Tipo de solicitud.
- Prioridad percibida.
- Descripción.
- Captura o evidencia opcional.
- Servicio afectado.

### WhatsApp o teléfono controlado

Canal opcional para planes con soporte más cercano.

Uso previsto:

- Incidencias urgentes.
- Confirmación rápida.
- Coordinación de ventanas de mantenimiento.

No debe sustituir el registro interno de tickets.

Toda incidencia recibida por WhatsApp o teléfono debe registrarse después internamente.

### Portal de cliente futuro

Canal recomendado a medio plazo.

Uso previsto:

- Ver estado de tickets.
- Descargar informes.
- Consultar historial de soporte.
- Solicitar restauraciones.
- Solicitar cambios de configuración.

## Registro interno

Aunque el cliente contacte por email, formulario, WhatsApp o teléfono, el equipo Vigex debe registrar internamente la incidencia.

El registro interno puede estar en:

- GitHub Issues privado.
- Hoja de cálculo interna.
- Sistema de tickets futuro.
- Panel interno Vigex.

## Flujo de soporte

~~~text
Cliente contacta por canal simple
        ↓
Equipo Vigex revisa solicitud
        ↓
Se registra ticket interno
        ↓
Se clasifica prioridad
        ↓
Se actúa o se planifica intervención
        ↓
Se comunica resultado al cliente
        ↓
Se cierra ticket con evidencia
~~~

## Clasificación de solicitudes

| Tipo | Descripción |
|---|---|
| Incidencia | Algo no funciona correctamente |
| Consulta | Pregunta operativa o técnica |
| Cambio | Modificación de configuración |
| Mantenimiento | Acción planificada |
| Restauración | Solicitud de recuperación de datos |
| Informe | Solicitud de informe o revisión |

## Prioridades

| Prioridad | Descripción | Ejemplo |
|---|---|---|
| Crítica | Servicio esencial caído o pérdida de datos | DB inaccesible, backup crítico fallido |
| Alta | Funcionalidad importante afectada | Panel no responde, restauración urgente |
| Media | Problema parcial sin parada total | Error en informe, alerta no enviada |
| Baja | Consulta, mejora o cambio menor | Cambio de texto, duda operativa |

## SLA orientativo

Los tiempos exactos dependen del plan contratado.

| Plan | Respuesta objetivo | Observación |
|---|---|---|
| Lite | 1-2 días laborables | Soporte básico |
| PyME | Mismo día laborable | Soporte estándar |
| Pro | Prioritario | Mejor respuesta y seguimiento |

## Qué no debe hacer el cliente

El cliente no debe:

- Entrar en GitHub.
- Crear issues.
- Editar scripts.
- Tocar `config.env`.
- Ejecutar comandos de restauración sin acompañamiento.
- Cambiar contraseñas internas sin avisar.
- Modificar permisos de MariaDB o SSH.

## Qué debe hacer el equipo Vigex

El equipo Vigex debe:

- Recibir solicitudes por canales simples.
- Registrar internamente cada caso.
- Clasificar prioridad.
- Mantener evidencias.
- Informar al cliente en lenguaje claro.
- Documentar acciones técnicas.
- Cerrar tickets con resultado verificable.

## Relación con GitHub

GitHub queda reservado para:

- Desarrollo interno.
- Seguimiento técnico.
- Roadmap.
- Bugs internos.
- Pull requests.
- Documentación técnica.
- Historial de cambios.

No se presenta como canal de atención al cliente.

## Conclusión

Vigex debe ofrecer soporte humano y cercano.

El cliente usa canales simples.

El equipo Vigex traduce esas solicitudes a trabajo técnico interno.
