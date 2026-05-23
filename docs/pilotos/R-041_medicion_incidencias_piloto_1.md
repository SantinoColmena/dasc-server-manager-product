# R-041 - Medición de incidencias del piloto 1

## Objetivo

Medir y analizar las incidencias detectadas durante el primer piloto técnico de DASC Server Manager.

Esta tarea toma como base el registro de incidencias del piloto 1 y permite valorar si el sistema está preparado para seguir avanzando hacia más pilotos o si antes deben corregirse errores bloqueantes.

## Fuente analizada

Documento base:

    docs/pilotos/piloto_1/incidencias.md

## Resumen cuantitativo

| Métrica | Resultado |
|---|---|
| Total de incidencias registradas | 8 |
| Incidencias críticas | 0 |
| Incidencias altas | 2 |
| Incidencias medias | 3 |
| Incidencias bajas | 3 |
| Incidencias corregidas | 6 |
| Incidencias aclaradas | 1 |
| Incidencias documentadas como limitación | 1 |
| Incidencias críticas abiertas | 0 |

## Distribución por área

| Área | Nº incidencias | Comentario |
|---|---:|---|
| Documentación | 1 | Rutas de instaladores mal indicadas inicialmente |
| Base de datos | 1 | Fallo SQL en install_db.sh por comillas invertidas |
| Logs | 1 | Contraseña de logs pendiente de configurar en config.env |
| Terminal SSH | 2 | known_hosts y clave pública hacia la máquina DB |
| Cacti | 1 | No validado en perfil limpio de 2 servidores |
| Validaciones DB | 1 | Uso de mariadb sin sudo |
| Backups | 1 | Aviso no crítico de mysqldump con head |

## Incidencias de mayor impacto

### 1. Fallo SQL en install_db.sh

Gravedad: Alta.

El instalador de base de datos falló al crear la base de logs porque Bash interpretaba las comillas invertidas como comandos.

Impacto:

- Bloqueaba la instalación limpia de la base de logs.
- Impedía completar la instalación del servidor cliente sin corrección manual.

Estado:

Corregida en el repositorio.

### 2. Contraseña de logs no configurada

Gravedad: Alta.

El panel no podía escribir eventos en la base dasc_logs porque el archivo config.env mantenía el valor genérico CAMBIAR_PASSWORD_LOGS.

Impacto:

- El panel funcionaba.
- Los logs no se guardaban correctamente hasta corregir la contraseña.

Estado:

Corregida en el entorno del piloto.

## Incidencias medias

| Incidencia | Impacto | Estado |
|---|---|---|
| Rutas de instaladores mal documentadas | Confusión durante instalación | Corregida |
| Terminal Database sin host key registrada | Bloqueaba terminal remoto a DB | Corregida |
| Terminal Database sin clave pública | Requería contraseña manual | Corregida |

## Incidencias bajas

| Incidencia | Impacto | Estado |
|---|---|---|
| Cacti no validado | No bloquea el perfil de 2 servidores | Documentada |
| Access denied al usar mariadb como usuario normal | Error de validación manual | Corregida |
| mysqldump errno 32 con head | Aviso esperado por cierre de tubería | Aclarada |

## Evaluación de estabilidad del piloto

El piloto se considera estable para el alcance R-040 porque:

- No quedan incidencias críticas abiertas.
- Las incidencias altas fueron corregidas.
- El panel quedó accesible.
- Los backups funcionan.
- Los logs funcionan.
- La terminal remota funciona.
- La limitación de Cacti queda documentada y no bloquea este perfil.

## Conclusión

R-041 queda completada porque las incidencias del piloto 1 han sido medidas, clasificadas y evaluadas.

El sistema puede avanzar a R-042 para consolidar correcciones y dejar el producto más limpio antes de futuros pilotos.

## Estado

Documentado: Sí  
Implementado: Sí  
Validado: Sí  
