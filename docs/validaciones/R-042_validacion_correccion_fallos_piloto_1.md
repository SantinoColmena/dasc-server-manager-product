# Validación R-042 - Corrección de fallos del piloto 1

## Objetivo

Validar que las incidencias detectadas y medidas en el piloto 1 han sido corregidas, aclaradas o documentadas correctamente.

## Resultado general

R-042 se considera validada.

Las incidencias bloqueantes detectadas durante el piloto 1 han sido corregidas. Las incidencias menores han quedado aclaradas o documentadas como limitaciones no bloqueantes.

## Comprobaciones de cierre

| Comprobación | Resultado |
|---|---|
| Incidencias críticas abiertas | 0 |
| Incidencias altas revisadas | OK |
| Fallo de install_db.sh corregido | OK |
| Plan de ejecución actualizado | OK |
| Logs funcionales tras corrección | OK |
| Terminal Database funcional tras corrección SSH | OK |
| Cacti documentado como limitación | OK |
| Piloto 1 requiere repetición | No |

## Correcciones verificadas

### Instalador DB

Se corrige el problema de comillas invertidas en install_db.sh para evitar que Bash interprete nombres SQL como comandos.

Resultado esperado en próximas instalaciones:

- dasc_logs se crea correctamente.
- eventos se crea correctamente.
- El instalador DB no se bloquea en el bloque SQL de logs.

### Documentación de ejecución

Se corrigen las rutas de instalación para reflejar la estructura real del repositorio:

    deploy/db/install_db.sh
    deploy/backup-services/install_backup_services.sh
    deploy/api/install_dasc_api.sh

### Logs

Se documenta que config.env debe tener una contraseña real en LOGS_DB_PASS y no mantener el valor genérico.

### Terminal remoto

Se valida que Terminal Database funciona tras registrar known_hosts y autorizar la clave pública de la API.

## Limitaciones aceptadas

Cacti queda fuera del cierre funcional de R-042 porque no forma parte obligatoria del perfil limpio de 2 servidores usado en este piloto.

Se recomienda tratar Cacti como validación opcional o como componente de otro perfil de despliegue.

## Criterio de cierre

R-042 se cierra porque:

- Los fallos principales del piloto han sido corregidos.
- Las incidencias no bloqueantes han sido documentadas.
- No quedan incidencias críticas abiertas.
- El sistema queda preparado para continuar con R-043 o con ajustes previos si se desea.

## Estado

Documentado: Sí  
Implementado: Sí  
Validado: Sí  
