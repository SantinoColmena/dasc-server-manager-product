# Cierre de Fase 5 - Pilotos reales

## Objetivo de la fase

Validar DASC Server Manager en escenarios reales o controlados mediante pilotos técnicos, registrar incidencias, corregir fallos detectados y ajustar la propuesta de servicio con SLA y costes realistas.

## Resultado general

La Fase 5 queda completada correctamente.

Se han ejecutado y documentado los pilotos principales del producto:

- Perfil PyME estándar de 2 servidores.
- Perfil Lite de 1 servidor + copia externa.
- Piloto 3 opcional cerrado mediante justificación técnica.

También se han definido los elementos de negocio necesarios para avanzar hacia una presentación o propuesta comercial:

- SLA realista.
- Costes reales estimados.
- Perfil recomendado de venta.
- Limitaciones aceptadas.

## Requisitos cerrados

| Requisito | Descripción | Estado |
|---|---|---|
| R-040 | Instalar piloto 1 en perfil 2 servidores | Cerrado |
| R-041 | Medir incidencias del piloto 1 | Cerrado |
| R-042 | Corregir fallos del piloto 1 | Cerrado |
| R-043 | Instalar piloto 2 en perfil Lite | Cerrado |
| R-044 | Piloto 3 opcional | Cerrado |
| R-045 | Definir SLA realista | Cerrado |
| R-046 | Recalcular costes reales | Cerrado |

## Pilotos validados

| Piloto | Perfil | Resultado |
|---|---|---|
| Piloto 1 | 2 servidores | Validado |
| Piloto 2 | 1 servidor + copia externa | Validado |
| Piloto 3 | Opcional | No ejecutado, justificado |

## Incidencias importantes corregidas

Durante la fase se detectaron y corrigieron incidencias reales:

- Rutas incorrectas de instaladores en documentación inicial.
- Error SQL en install_db.sh con dasc_logs.
- Contraseña de logs pendiente en config.env.
- Problemas SSH con known_hosts y claves.
- Sustitución accidental de MariaDB por paquetes MySQL en perfil Lite.
- Host SSH no permitido para 192.168.60.40.

## Decisión técnica final

El perfil recomendado para venta inicial es:

    PyME estándar

Motivos:

- Mejor equilibrio técnico.
- Más separación de responsabilidades.
- Mejor margen.
- SLA más defendible.
- Menor riesgo que el perfil Lite.

El perfil Lite queda como opción económica de entrada, siempre con copia externa obligatoria.

El perfil Pro queda como ampliación futura o presupuesto personalizado.

## Estado final

Documentado: Sí  
Implementado: Sí  
Validado: Sí  

## Conclusión

La Fase 5 queda cerrada.

DASC Server Manager dispone de pilotos reales/controlados, incidencias medidas, correcciones aplicadas, SLA definido y costes recalculados.
