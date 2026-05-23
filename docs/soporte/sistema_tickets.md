# R-049 - Sistema básico de tickets

## Objetivo

Montar un sistema básico de tickets para que las incidencias, solicitudes y tareas de soporte de DASC Server Manager no se pierdan en conversaciones informales como WhatsApp.

## Estado

En curso.

## Decisión adoptada

Para la primera versión del producto se usará GitHub Issues como sistema básico de tickets.

La decisión se toma porque:

- Ya existe repositorio del producto.
- Permite registrar incidencias de forma ordenada.
- Permite usar etiquetas.
- Permite tener historial.
- Permite diferenciar incidencias técnicas y solicitudes de soporte.
- Evita depender únicamente de mensajes sueltos por WhatsApp.
- No añade coste mensual inicial.

## Alcance de R-049

R-049 incluye:

- Plantilla de incidencia técnica.
- Plantilla de solicitud de soporte.
- Documento de funcionamiento del sistema de tickets.
- Reglas mínimas de prioridad.
- Criterios de seguridad para no subir secretos.
- Flujo de entrada, revisión, resolución y cierre.

## Fuera de alcance

R-049 no incluye todavía:

- Portal de cliente propio.
- Sistema avanzado tipo Jira, Freshdesk o Zendesk.
- Automatización de SLA.
- Integración con correo.
- Integración con IA.
- Panel interno de soporte.
- Métricas automáticas avanzadas.

## Tipos de ticket

### Incidencia técnica

Se usa cuando algo falla.

Ejemplos:

- Error al ejecutar backup.
- Fallo al restaurar.
- Problema con SSH.
- El panel no carga.
- Las alertas no se envían.
- Los logs no aparecen.
- Un instalador falla.

### Solicitud de soporte

Se usa cuando el cliente necesita ayuda o una revisión.

Ejemplos:

- Revisar estado mensual.
- Validar una restauración.
- Cambiar configuración.
- Revisar logs.
- Configurar alertas.
- Resolver una duda de uso.

## Prioridades

### Baja

No bloquea el uso del sistema.

Ejemplos:

- Duda de documentación.
- Mejora visual.
- Texto poco claro.
- Consulta general.

### Media

Afecta a una función, pero existe alternativa.

Ejemplos:

- Una alerta no llega, pero los backups funcionan.
- Un filtro no responde.
- Un informe necesita corrección.

### Alta

Afecta a una función importante.

Ejemplos:

- No se puede lanzar un backup manual.
- No se puede revisar el historial.
- No se puede conectar con el nodo de backups.

### Crítica

Afecta a restauración, pérdida de datos o caída completa.

Ejemplos:

- No se puede restaurar.
- No existen backups recientes.
- El panel no arranca.
- Error grave en base de datos.
- Riesgo de pérdida de datos.

## Flujo de trabajo

1. El cliente comunica el problema.
2. Se crea un ticket en GitHub Issues.
3. Se clasifica por tipo, módulo y prioridad.
4. Se revisa si falta información.
5. Se investiga el problema.
6. Se propone solución.
7. Se documenta lo realizado.
8. Se cierra el ticket.
9. Si procede, se crea una mejora futura.

## Reglas de seguridad

Nunca se debe incluir en un ticket:

- Contraseñas.
- Tokens.
- Claves privadas.
- Backups reales.
- Datos personales.
- Datos de clientes.
- Capturas con información sensible.
- IP pública sensible si no es necesario.

Si hace falta compartir información delicada, se hará por canal privado y se documentará en el ticket solo una referencia genérica.

## Etiquetas recomendadas

Etiquetas mínimas:

- `incidencia`
- `soporte`
- `backup`
- `restauracion`
- `logs`
- `alertas`
- `servicios`
- `instalacion`
- `documentacion`
- `prioridad-baja`
- `prioridad-media`
- `prioridad-alta`
- `prioridad-critica`

## Criterio de cierre de R-049

R-049 se podrá cerrar cuando:

- Existan plantillas de Issues.
- Exista documentación del sistema de tickets.
- Se haya definido el flujo de trabajo.
- Se haya definido cómo priorizar tickets.
- Se haya documentado la regla de no incluir secretos.
- El repositorio quede limpio tras el commit.

## Resultado esperado

A partir de R-049, cualquier incidencia o solicitud de soporte debe registrarse como ticket.

WhatsApp o correo pueden usarse para avisar, pero no deben ser el lugar principal donde se pierde la información técnica.
