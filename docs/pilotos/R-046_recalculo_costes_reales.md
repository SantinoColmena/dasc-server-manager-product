# R-046 - Recalcular costes reales

## Objetivo

Recalcular los costes reales estimados de DASC Server Manager después de ejecutar pilotos técnicos y definir un SLA realista.

El objetivo es comprobar si los perfiles Lite, PyME estándar y Pro tienen sentido económico como servicio gestionado.

## Enfoque

DASC Server Manager no se plantea como una simple licencia de software.

El modelo recomendado es venderlo como servicio gestionado:

- Instalación inicial.
- Configuración de backups.
- Configuración de logs.
- Configuración de alertas.
- Mantenimiento.
- Revisión de copias.
- Restauraciones bajo demanda.
- Soporte remoto.
- Informes periódicos.

## Costes considerados

| Tipo de coste | Descripción |
|---|---|
| Infraestructura | Servidores, almacenamiento, copia externa, red |
| Instalación | Tiempo inicial de despliegue |
| Mantenimiento | Revisión mensual, actualizaciones y comprobaciones |
| Soporte | Atención de incidencias |
| Restauración | Tiempo dedicado a recuperar datos |
| Documentación | Informes mensuales y evidencias |
| Mejora continua | Correcciones detectadas en pilotos |

## Supuestos base

Los importes son estimaciones internas para orientar el modelo de negocio.

No son precios cerrados ni presupuestos definitivos. Deben revisarse con el proveedor real de infraestructura y con el alcance exacto de cada cliente.

## Coste horario interno estimado

| Concepto | Valor estimado |
|---|---:|
| Hora técnica mínima | 20 €/h |
| Hora técnica recomendada | 30 €/h |
| Hora técnica urgente o avanzada | 45 €/h |

Para los cálculos se usa como referencia una hora técnica de 30 €/h.

## Coste de instalación inicial

| Perfil | Horas estimadas | Coste interno estimado | Precio recomendado de instalación |
|---|---:|---:|---:|
| Lite | 3-5 h | 90-150 € | 150-250 € |
| PyME estándar | 5-8 h | 150-240 € | 300-500 € |
| Pro | 8-14 h | 240-420 € | 600-1.000 € |

## Coste mensual de operación

| Perfil | Horas/mes estimadas | Coste interno mensual | Precio mensual recomendado |
|---|---:|---:|---:|
| Lite | 1-2 h | 30-60 € | 49-79 €/mes |
| PyME estándar | 2-4 h | 60-120 € | 99-179 €/mes |
| Pro | 4-8 h | 120-240 € | 249-399 €/mes |

## Infraestructura estimada

### Perfil Lite

| Elemento | Coste mensual estimado |
|---|---:|
| 1 servidor básico | 8-20 € |
| Almacenamiento externo básico | 5-15 € |
| Dominio/certificados | 0-2 € |
| Total infraestructura estimada | 13-37 €/mes |

### Perfil PyME estándar

| Elemento | Coste mensual estimado |
|---|---:|
| Servidor cliente existente | 0 € si ya existe |
| Servidor DASC/backups | 10-30 € |
| Copia externa | 5-20 € |
| Total infraestructura estimada | 15-50 €/mes |

### Perfil Pro

| Elemento | Coste mensual estimado |
|---|---:|
| Servidor panel/API | 10-30 € |
| Servidor backups | 10-40 € |
| Servidor externo o almacenamiento dedicado | 10-50 € |
| Margen para monitorización adicional | 10-30 € |
| Total infraestructura estimada | 40-150 €/mes |

## Coste total mensual estimado

| Perfil | Infraestructura | Operación interna | Coste total estimado | Precio recomendado |
|---|---:|---:|---:|---:|
| Lite | 13-37 € | 30-60 € | 43-97 € | 49-79 €/mes |
| PyME estándar | 15-50 € | 60-120 € | 75-170 € | 99-179 €/mes |
| Pro | 40-150 € | 120-240 € | 160-390 € | 249-399 €/mes |

## Observación sobre rentabilidad

El perfil Lite solo es rentable si:

- la instalación está muy automatizada;
- la copia externa es sencilla;
- el soporte queda limitado;
- el cliente acepta un SLA básico;
- no se dedica más de 1-2 horas mensuales de media.

El perfil PyME estándar es el más equilibrado porque permite mayor valor percibido y más margen.

El perfil Pro solo tiene sentido si el cliente necesita más garantías, más soporte y más infraestructura.

## Comparativa de margen aproximado

| Perfil | Precio mensual recomendado | Coste total estimado | Margen aproximado |
|---|---:|---:|---:|
| Lite | 49-79 € | 43-97 € | Bajo / ajustado |
| PyME estándar | 99-179 € | 75-170 € | Medio |
| Pro | 249-399 € | 160-390 € | Medio / alto según alcance |

## Precio recomendado por perfil

### Lite

Precio recomendado:

    49-79 €/mes

Instalación:

    150-250 €

Uso recomendado:

- Autónomos.
- Microempresas.
- Entornos con bajo presupuesto.
- Clientes que aceptan menor separación técnica.

Condición obligatoria:

La copia externa debe estar activa.

### PyME estándar

Precio recomendado:

    99-179 €/mes

Instalación:

    300-500 €

Uso recomendado:

- Pequeñas empresas.
- Empresas con datos importantes.
- Clientes que quieren un equilibrio entre coste y seguridad.

Perfil recomendado comercialmente.

### Pro

Precio recomendado:

    249-399 €/mes

Instalación:

    600-1.000 €

Uso recomendado:

- Empresas con mayor dependencia de sus datos.
- Clientes que requieren mejor RTO/RPO.
- Entornos con más infraestructura.

## Costes no incluidos por defecto

Los siguientes costes pueden presupuestarse aparte:

| Concepto | Motivo |
|---|---|
| Migraciones complejas | Dependen del origen |
| Restauraciones urgentes fuera de horario | Requieren disponibilidad especial |
| Alta disponibilidad real | Requiere arquitectura adicional |
| Auditorías de seguridad profundas | Alcance diferente |
| Monitorización avanzada externa | Coste adicional |
| Copias en almacenamiento de terceros | Depende del proveedor |
| Soporte 24/7 | No incluido en planes base |

## Relación con el SLA

Los costes se alinean con el SLA definido en R-045.

No se debe vender un SLA avanzado con precio Lite.

| Perfil | SLA coherente |
|---|---|
| Lite | Básico |
| PyME estándar | Recomendado |
| Pro | Avanzado |

## Relación con pilotos

| Piloto | Impacto en costes |
|---|---|
| Piloto 1 - 2 servidores | Confirma coste y complejidad del perfil PyME estándar |
| Piloto 2 - Lite | Confirma que el perfil Lite es viable, pero con margen ajustado |
| Piloto 3 opcional | No ejecutado; perfil Pro queda como ampliación futura |

## Decisión de negocio

El perfil recomendado para venta inicial es:

    PyME estándar

Motivos:

- Mejor equilibrio técnico.
- Mayor separación de responsabilidades.
- Más valor percibido.
- Mejor margen.
- SLA más defendible.
- Menor riesgo que el perfil Lite.

El perfil Lite puede ofrecerse como entrada económica.

El perfil Pro queda como evolución futura o presupuesto personalizado.

## Conclusión

R-046 queda completada.

Después de los pilotos y del SLA, el modelo de costes más razonable es:

| Perfil | Instalación | Mensualidad |
|---|---:|---:|
| Lite | 150-250 € | 49-79 €/mes |
| PyME estándar | 300-500 € | 99-179 €/mes |
| Pro | 600-1.000 € | 249-399 €/mes |

El producto es más viable si se vende como servicio gestionado y no como licencia aislada.

## Estado

Documentado: Sí  
Implementado: No aplica  
Validado: Sí  
