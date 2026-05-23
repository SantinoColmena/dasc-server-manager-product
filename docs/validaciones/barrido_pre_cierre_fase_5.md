# Barrido pre-cierre de Fase 5

## Objetivo

Revisar el repositorio antes del cierre formal de la Fase 5 para detectar incoherencias, restos de configuración, documentación desactualizada o detalles que puedan afectar a futuras fases.

## Resultado general

El repositorio no presenta bloqueos críticos para cerrar la Fase 5.

Se detectaron elementos de limpieza y coherencia que fueron corregidos antes del cierre formal.

## Elementos revisados

| Área | Resultado |
|---|---|
| README.md | Actualizado de Fase 4 a Fase 5 |
| Documentación de pilotos | R-040 a R-046 presentes |
| Validaciones | Validaciones de requisitos presentes |
| config.env.example raíz | Unificado y limpiado sin BOM |
| config.env.example del paquete API | Unificado con raíz |
| .gitignore | Limpiado sin BOM y ampliado |
| install_backup_services.sh | Sin referencias a default-mysql-client/mysql-client tras corrección de R-043 |
| install_dasc_api.sh | Mejorado para incluir host Database/Logs en SSH permitido |
| Datos runtime | Añadidos a .gitignore |
| Secretos reales | No se añaden tokens reales al repositorio |

## Incidencias corregidas en este barrido

| Nº | Incidencia | Estado |
|---|---|---|
| 1 | README desactualizado indicando Fase 4 y piloto pendiente | Corregida |
| 2 | config.env.example raíz no alineado con el paquete API | Corregida |
| 3 | Posible BOM en ficheros de texto principales | Corregida |
| 4 | .gitignore no cubría todos los datos runtime del paquete API | Corregida |
| 5 | DASC_SSH_ALLOWED_HOSTS podía no incluir la máquina Database/Logs en nuevas instalaciones | Corregida |
| 6 | LOGS_DB_PASS del ejemplo podía provocar fallo de logs si no se editaba | Corregida para entorno de laboratorio/pilotos |

## Limitaciones aceptadas

Cacti se mantiene como componente opcional/no bloqueante en los perfiles validados durante Fase 5.

El perfil Pro queda previsto como ampliación futura o presupuesto personalizado.

## Criterio de cierre

La Fase 5 puede cerrarse después de este barrido porque:

- Los requisitos R-040 a R-046 están documentados.
- Las incidencias principales de pilotos están corregidas.
- El README queda alineado con el estado real.
- Los ejemplos de configuración quedan más coherentes.
- Los datos runtime quedan protegidos por .gitignore.
- No quedan bloqueos críticos conocidos.

## Estado

Documentado: Sí  
Implementado: Sí  
Validado: Sí  