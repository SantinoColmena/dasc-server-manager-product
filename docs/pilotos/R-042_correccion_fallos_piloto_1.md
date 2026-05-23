# R-042 - Corrección de fallos del piloto 1

## Objetivo

Consolidar las correcciones aplicadas durante el piloto 1 de DASC Server Manager y dejar preparado el proyecto para futuros pilotos con menos intervención manual.

Esta tarea parte de las incidencias medidas en R-041 y documenta qué fallos han sido corregidos, cuáles quedan aclarados y cuáles se aceptan como limitaciones del perfil de 2 servidores.

## Fuente de incidencias

Documento base:

    docs/pilotos/R-041_medicion_incidencias_piloto_1.md

Registro detallado:

    docs/pilotos/piloto_1/incidencias.md

## Resumen de correcciones aplicadas

| Nº | Incidencia | Corrección aplicada | Estado |
|---|---|---|---|
| 1 | Rutas de instaladores mal indicadas | Se corrigió el plan de ejecución usando rutas dentro de deploy | Corregida |
| 2 | Fallo SQL en install_db.sh con dasc_logs | Se escaparon las comillas invertidas en el bloque SQL | Corregida |
| 3 | LOGS_DB_PASS con valor genérico | Se configuró la contraseña real de logs en el entorno del piloto | Corregida |
| 4 | Terminal Database sin host key SSH | Se añadió la huella ED25519 al known_hosts dedicado de DASC | Corregida |
| 5 | Terminal Database sin clave pública automática | Se copió la clave pública de la API al usuario dasc de la DB | Corregida |
| 6 | Cacti no validado | Se documenta como limitación no bloqueante del perfil de 2 servidores | Documentada |
| 7 | Access denied al validar MariaDB sin sudo | Se aclaró que las validaciones locales administrativas deben hacerse con sudo mariadb | Corregida |
| 8 | mysqldump errno 32 con head | Se aclaró que no era fallo real, sino cierre esperado de tubería | Aclarada |

## Corrección principal en código

### install_db.sh

Durante el piloto se detectó que el instalador de base de datos fallaba al crear la base de logs.

Motivo:

Bash interpretaba las comillas invertidas de SQL como comandos del sistema.

Corrección:

Las referencias SQL a LOGS_DB_NAME y eventos quedan escapadas para que Bash no las ejecute como comandos.

Impacto:

- El instalador DB puede crear dasc_logs correctamente.
- La tabla eventos se crea sin fallo.
- Futuros pilotos no deberían repetir esta incidencia.

## Correcciones de documentación

Se actualizó el plan de ejecución del piloto 1 para usar las rutas reales de los instaladores:

    sudo bash deploy/db/install_db.sh
    sudo bash deploy/backup-services/install_backup_services.sh
    sudo bash deploy/api/install_dasc_api.sh

Esto evita confusión en futuras instalaciones limpias.

## Correcciones operativas

### Logs

El panel no podía registrar eventos porque LOGS_DB_PASS mantenía un valor genérico.

Corrección aplicada en el piloto:

    LOGS_DB_PASS=dasc_logs_2026

Resultado:

El panel empezó a registrar eventos correctamente en la tabla dasc_logs.eventos.

### Terminal Database

El terminal remoto hacia la máquina Database fallaba por dos motivos:

- La huella SSH de 192.168.60.20 no estaba registrada.
- La clave pública de la API no estaba autorizada en el usuario dasc de la DB.

Corrección aplicada:

- Registro de la huella ED25519 en known_hosts_dasc.
- Copia de la clave pública de la API al usuario dasc de la máquina DB.

Resultado:

Terminal Database funciona correctamente desde el panel.

## Limitaciones aceptadas

### Cacti

Cacti no se valida en este piloto porque el perfil limpio de 2 servidores no incluye instalación específica de Cacti.

Esta limitación no bloquea R-042 porque:

- El objetivo principal del piloto era validar instalación, panel, backups, logs, servicios y terminal.
- La auditoría funcional ya queda validada mediante dasc_logs.eventos.
- Cacti puede tratarse como componente opcional o como validación futura.

## Estado final tras correcciones

| Área | Estado |
|---|---|
| Instalador DB | Corregido |
| Plan de ejecución | Corregido |
| Logs | Corregidos en piloto |
| Terminal Main | OK |
| Terminal Backup | OK |
| Terminal Database | OK |
| Backups | OK |
| Panel | OK |
| Cacti | Limitación documentada |
| Incidencias críticas abiertas | 0 |

## Recomendaciones para futuros pilotos

Antes de ejecutar el siguiente piloto se recomienda:

- Revisar que config.env no mantenga valores CAMBIAR_*.
- Confirmar que los hosts de logs, backups y servicios coinciden con la arquitectura usada.
- Validar SSH entre máquinas antes de abrir la demo.
- Ejecutar un backup manual antes de validar desde panel.
- Confirmar que los logs registran actividad desde el primer acceso.
- Tratar Cacti como opcional si no se instala explícitamente en el perfil de 2 servidores.

## Conclusión

R-042 queda completada porque los fallos detectados durante el piloto 1 han sido corregidos, aclarados o documentados como limitaciones aceptadas.

No quedan incidencias críticas abiertas que obliguen a repetir el piloto 1.

## Estado

Documentado: Sí  
Implementado: Sí  
Validado: Sí  
