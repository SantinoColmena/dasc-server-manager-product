# R-044 - Piloto 3 opcional

## Objetivo

Evaluar si es necesario ejecutar un tercer piloto técnico de DASC Server Manager después de haber validado los perfiles principales del producto.

## Decisión

El piloto 3 no se ejecuta como despliegue adicional.

Se considera una tarea opcional y queda cerrada mediante justificación técnica, ya que los dos perfiles principales ya han sido validados:

| Piloto | Perfil | Estado |
|---|---|---|
| Piloto 1 | Perfil PyME de 2 servidores | Validado |
| Piloto 2 | Perfil Lite de 1 servidor + copia externa | Validado |

## Motivo de la decisión

No se ejecuta un tercer piloto porque:

- El perfil estándar PyME ya ha sido probado.
- El perfil Lite ya ha sido probado.
- Las incidencias reales detectadas ya han sido medidas y corregidas.
- Crear una tercera VM no aporta una validación proporcional al tiempo invertido.
- La fase actual está orientada al cierre final, presentación y documentación.
- El MVP ya está entregado y la prioridad es consolidar evidencias, costes y SLA.

## Qué habría validado un piloto 3

Un tercer piloto podría haberse usado para validar uno de estos escenarios:

| Escenario | Utilidad |
|---|---|
| Perfil Pro de 3 servidores | Mayor separación de responsabilidades |
| Destino externo real SFTP/NAS | Validación de copia externa real |
| Segundo cliente simulado | Validación comercial |
| Instalación repetida desde cero | Robustez de instaladores |

## Sustitución del piloto 3

En lugar de ejecutar un tercer despliegue completo, se toma como evidencia:

- Piloto 1 en arquitectura de 2 servidores.
- Piloto 2 en arquitectura Lite.
- Incidencias reales documentadas.
- Correcciones aplicadas al repositorio.
- Comparativa de limitaciones entre perfiles.

## Resultado

R-044 queda cerrada como requisito opcional documentado.

No quedan acciones técnicas obligatorias asociadas a este requisito.

## Estado

Documentado: Sí  
Implementado: No aplica  
Validado: Sí  
