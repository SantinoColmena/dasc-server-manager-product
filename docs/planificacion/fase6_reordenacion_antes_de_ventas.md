# Reordenación de Fase 6 antes de primeras ventas

## Motivo

Durante el inicio de la Fase 6 se detecta que algunas tareas comerciales del tracker aparecen demasiado pronto para el estado real del producto.

Aunque ya existe una release candidate `v1.0-rc1`, todavía no conviene avanzar directamente hacia clientes de pago sin antes dejar el producto más limpio, pulido e instalable.

## Decisión

La Fase 6 se mantiene abierta, pero se reordena internamente.

El bloque de clientes, ventas y seguimiento comercial queda en curso, pero se deja para el final de la fase.

Antes de intentar cerrar ventas reales se prioriza:

- Limpieza general del repositorio.
- Revisión de documentación.
- Revisión de instaladores.
- Pulido de estructura.
- Revisión del uso desde Windows.
- Definición clara de qué puede hacer un cliente desde navegador y qué debe instalarse en servidores Linux.
- Separación entre producto real, laboratorio y documentación comercial.
- Validación de que no se promete nada que todavía no exista.

## Estado de R-048

R-048 queda en curso, pero aplazada hasta que el producto esté más pulido.

No se considera correcto cerrar R-048 sin un cliente real de pago o sin feedback comercial real documentado.

## Estado de R-049

R-049 no se considera cerrada como sistema de ticketing real para clientes.

Lo creado con GitHub Issues se mantiene solo como base interna provisional para registrar incidencias del proyecto.

No sustituye todavía a un portal de soporte real, sistema de tickets externo o proceso comercial completo.

## Nuevo orden recomendado

### Bloque 1 - Limpieza previa

- Revisar README.
- Revisar estructura de carpetas.
- Revisar documentación duplicada o demasiado comercial.
- Revisar que los documentos no prometan funcionalidades no implementadas.
- Revisar secretos, ejemplos y configuraciones.

### Bloque 2 - Windows y experiencia de uso

- Documentar cómo se usa DASC desde Windows.
- Separar acceso web desde navegador y despliegue real en Linux.
- Preparar guía para usar DASC desde un PC Windows contra servidores Ubuntu.
- Valorar si hace falta script auxiliar para Windows o solo documentación.

### Bloque 3 - Instalación limpia

- Revisar instaladores.
- Revisar uninstallers.
- Validar rutas.
- Validar `config.env.example`.
- Validar despliegue mínimo reproducible.

### Bloque 4 - Soporte interno provisional

- Mantener GitHub Issues como sistema interno.
- No venderlo todavía como sistema de ticketing de cliente.
- Documentar límites.

### Bloque 5 - Clientes y primeras ventas

Solo cuando lo anterior esté limpio:

- Retomar R-048.
- Preparar contacto real.
- Preparar oferta.
- Buscar primer piloto o cliente de pago.
- Registrar feedback real.

## Conclusión

La Fase 6 no se cancela.

Se reordena para evitar vender o documentar como final algo que todavía necesita limpieza, pulido y validación práctica.
