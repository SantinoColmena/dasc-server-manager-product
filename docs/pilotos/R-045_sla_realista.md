# R-045 - Definición de SLA realista

## Objetivo

Definir un SLA realista para DASC Server Manager como servicio orientado a pequeñas y medianas empresas.

El objetivo no es prometer disponibilidad imposible, sino establecer compromisos asumibles para un servicio de instalación, mantenimiento, copias de seguridad, restauración, alertas, soporte e informes.

## Enfoque del SLA

DASC Server Manager se plantea como un servicio gestionado, no solo como una herramienta instalada.

El SLA se basa en:

- Atención humana.
- Soporte técnico remoto.
- Revisión de backups.
- Restauraciones bajo demanda.
- Alertas ante errores relevantes.
- Informes periódicos.
- Mantenimiento preventivo.
- Mejora continua del sistema.

## Principio realista

No se promete alta disponibilidad absoluta ni atención 24/7 en todos los planes.

El objetivo es ofrecer un servicio fiable, medible y asumible para clientes pequeños, evitando compromisos imposibles para la fase inicial del producto.

## Perfiles de servicio

| Perfil | Cliente objetivo | Arquitectura recomendada | Nivel de soporte |
|---|---|---|---|
| Lite | Autónomos, microempresas o entornos pequeños | 1 servidor + copia externa obligatoria | Básico |
| PyME estándar | Pequeñas empresas con datos importantes | 2 servidores | Recomendado |
| Pro | Empresas con mayor criticidad | 3 servidores o arquitectura ampliada | Avanzado |

## Horario de soporte

| Servicio | Horario |
|---|---|
| Soporte estándar | Lunes a viernes, horario laboral |
| Revisión de incidencias no críticas | Horario laboral |
| Incidencias críticas | Atención prioritaria según plan |
| Emergencias fuera de horario | Solo en plan Pro o servicio adicional |

## Clasificación de incidencias

| Severidad | Descripción | Ejemplos |
|---|---|---|
| Crítica | El sistema no puede operar o no se pueden realizar/restaurar backups | Caída total del panel, fallo completo de backups, pérdida de acceso a datos |
| Alta | Función importante afectada, pero existe alternativa temporal | Error en logs, fallo de alertas, backup parcial fallido |
| Media | Problema que afecta al uso, pero no bloquea el servicio | Error visual, servicio no listado, aviso de configuración |
| Baja | Consulta, mejora o problema menor | Ajuste de texto, duda de uso, mejora estética |

## Tiempos objetivo de respuesta

| Severidad | Lite | PyME estándar | Pro |
|---|---:|---:|---:|
| Crítica | 8 horas laborables | 4 horas laborables | 2 horas laborables |
| Alta | 1 día laborable | 8 horas laborables | 4 horas laborables |
| Media | 2 días laborables | 1 día laborable | 8 horas laborables |
| Baja | 5 días laborables | 3 días laborables | 2 días laborables |

## Tiempos objetivo de resolución

Los tiempos de resolución dependen del tipo de incidencia, del acceso disponible al entorno del cliente y de si existe copia externa válida.

| Severidad | Lite | PyME estándar | Pro |
|---|---:|---:|---:|
| Crítica | 1-2 días laborables | 1 día laborable | Menos de 1 día laborable si el entorno lo permite |
| Alta | 2-3 días laborables | 1-2 días laborables | 1 día laborable |
| Media | 3-5 días laborables | 2-3 días laborables | 1-2 días laborables |
| Baja | Según planificación | Según planificación | Según planificación |

## RTO y RPO orientativos

RTO: tiempo objetivo para recuperar el servicio.

RPO: pérdida máxima de datos asumible según la última copia disponible.

| Perfil | RTO orientativo | RPO orientativo | Comentario |
|---|---:|---:|---|
| Lite | 24-48 h | 24 h | Depende totalmente de la copia externa |
| PyME estándar | 8-24 h | 12-24 h | Mejor equilibrio entre coste y seguridad |
| Pro | 4-12 h | 4-12 h | Requiere más infraestructura y validaciones |

## Compromisos incluidos

| Área | Compromiso |
|---|---|
| Instalación | Instalación inicial del sistema según perfil contratado |
| Backups | Configuración de copias locales y externas según perfil |
| Revisión | Revisión periódica del estado de backups |
| Restauración | Asistencia en restauraciones bajo demanda |
| Alertas | Configuración de alertas relevantes |
| Logs | Revisión de eventos del panel |
| Informes | Informe periódico de estado |
| Mantenimiento | Actualizaciones controladas y correcciones |
| Soporte | Atención remota según severidad |

## Informes periódicos

| Perfil | Frecuencia de informe |
|---|---|
| Lite | Mensual básico |
| PyME estándar | Mensual completo |
| Pro | Mensual completo y revisión adicional si procede |

## Contenido mínimo del informe

El informe mensual debe incluir:

- Estado general del sistema.
- Número de backups generados.
- Última copia válida.
- Errores detectados.
- Restauraciones o pruebas realizadas.
- Incidencias abiertas y cerradas.
- Recomendaciones.
- Riesgos detectados.

## Exclusiones del SLA

El SLA no cubre:

- Fallos causados por manipulación directa no autorizada del servidor.
- Pérdida de datos si el cliente elimina o desactiva la copia externa.
- Cortes de Internet o electricidad del cliente.
- Fallos de proveedores externos no gestionados.
- Ataques graves de seguridad no cubiertos por el servicio contratado.
- Cambios manuales hechos fuera del procedimiento acordado.
- Recuperaciones imposibles por inexistencia de backups válidos.

## Requisitos para que el SLA sea aplicable

Para que el SLA sea válido, el cliente debe:

- Mantener acceso remoto autorizado para soporte.
- No modificar manualmente archivos críticos sin avisar.
- Mantener activo el destino de copia externa.
- Permitir la revisión periódica del sistema.
- Comunicar incidencias con información suficiente.
- Aceptar ventanas de mantenimiento planificadas.

## SLA por perfil

### Perfil Lite

Pensado para clientes pequeños o con presupuesto ajustado.

Incluye:

- Panel DASC en un servidor.
- Backups locales.
- Copia externa obligatoria.
- Logs básicos.
- Soporte en horario laboral.
- Informe mensual básico.

Limitación principal:

Si el único servidor falla completamente, la recuperación depende de la copia externa.

### Perfil PyME estándar

Perfil recomendado.

Incluye:

- Separación entre servidor cliente y servidor DASC/backups.
- Backups locales en servidor DASC.
- Posibilidad de copia externa.
- Logs centralizados.
- Terminal y servicios.
- Soporte con prioridad media/alta.
- Informe mensual completo.

Ventaja principal:

Mejor equilibrio entre coste, seguridad y facilidad de mantenimiento.

### Perfil Pro

Perfil avanzado para clientes con mayor criticidad.

Incluye:

- Mayor separación de componentes.
- Mejor capacidad de recuperación.
- Revisiones más frecuentes.
- Prioridad superior en incidencias.
- Posibilidad de soporte extendido.
- Informes más detallados.

Limitación:

Requiere más infraestructura y coste mensual superior.

## Indicadores de cumplimiento

| Indicador | Uso |
|---|---|
| Backups completados | Medir fiabilidad de copias |
| Backups fallidos | Detectar riesgo operativo |
| Última copia válida | Medir seguridad real |
| Tiempo de respuesta | Medir soporte |
| Tiempo de resolución | Medir eficacia |
| Incidencias por severidad | Medir estabilidad |
| Restauraciones probadas | Medir capacidad de recuperación |

## Conclusión

El SLA definido es realista para la fase actual de DASC Server Manager.

No promete disponibilidad absoluta ni recuperación instantánea, pero sí establece compromisos claros, medibles y adecuados para PYMES.

R-045 queda completada porque se han definido:

- Perfiles de servicio.
- Severidades.
- Tiempos de respuesta.
- Tiempos de resolución.
- RTO y RPO orientativos.
- Exclusiones.
- Requisitos para aplicar el SLA.
- Indicadores de seguimiento.

## Estado

Documentado: Sí  
Implementado: No aplica  
Validado: Sí  
