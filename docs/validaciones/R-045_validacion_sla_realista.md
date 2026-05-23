# Validación R-045 - SLA realista

## Objetivo

Validar que DASC Server Manager dispone de una propuesta de SLA realista y coherente con el estado actual del producto.

## Resultado general

R-045 se considera validada.

Se ha definido un SLA asumible para una fase inicial de producto, evitando promesas excesivas y separando claramente los compromisos por perfil de servicio.

## Comprobaciones

| Comprobación | Resultado |
|---|---|
| Perfiles de servicio definidos | OK |
| Severidades definidas | OK |
| Tiempos objetivo de respuesta definidos | OK |
| Tiempos objetivo de resolución definidos | OK |
| RTO orientativo definido | OK |
| RPO orientativo definido | OK |
| Exclusiones documentadas | OK |
| Requisitos del cliente documentados | OK |
| Indicadores de cumplimiento definidos | OK |
| SLA adaptado a Lite, PyME y Pro | OK |

## Perfiles incluidos

| Perfil | Estado |
|---|---|
| Lite | Definido |
| PyME estándar | Definido |
| Pro | Definido |

## Criterio de realismo

El SLA se considera realista porque:

- No promete 24/7 en todos los planes.
- No promete disponibilidad absoluta.
- Diferencia entre respuesta y resolución.
- Reconoce dependencia de la copia externa.
- Ajusta tiempos según criticidad y perfil.
- Incluye exclusiones claras.
- Obliga a que el cliente mantenga condiciones mínimas.

## Relación con pilotos

El SLA se apoya en los pilotos ya realizados:

| Piloto | Aporte al SLA |
|---|---|
| Piloto 1 - 2 servidores | Base para perfil PyME estándar |
| Piloto 2 - 1 servidor + externo | Base para perfil Lite |
| Piloto 3 opcional | No ejecutado; perfil Pro queda como mejora futura |

## Limitaciones aceptadas

El SLA es orientativo y debe revisarse si el producto pasa a operación real con clientes.

Los tiempos pueden variar según:

- acceso remoto disponible;
- estado de backups;
- tamaño de la base de datos;
- conectividad del cliente;
- destino externo usado;
- complejidad de la restauración.

## Criterio de cierre

R-045 se cierra porque existe una definición formal del SLA y queda documentada como parte de la Fase 5.

## Estado

Documentado: Sí  
Implementado: No aplica  
Validado: Sí  
