# Validación visual del panel - Fase 2

## Objetivo

Validar visualmente que el panel DASC Server Manager funciona correctamente después de la validación real de Fase 2 en laboratorio Ubuntu.

## Entorno

| Elemento | Valor |
|---|---|
| API / Panel | lab-api |
| IP interna laboratorio | 192.168.60.10 |
| IP accesible desde Windows | 192.168.1.244 |
| Acceso validado | https://192.168.1.244 |
| Reverse proxy | Nginx |
| HTTPS | Certificado autofirmado |
| Usuario validado | admin |

## Pantallas comprobadas

| Pantalla | Estado |
|---|---|
| Login | Correcto |
| Dashboard / Inicio | Correcto |
| Backups | Correcto |
| Servicios | Correcto |
| Logs | Correcto |

## Resultado visual

El panel carga correctamente desde Windows mediante HTTPS usando la IP accesible de la VM API.

El navegador muestra aviso de certificado autofirmado, comportamiento esperado en laboratorio.

El login con usuario administrador funciona correctamente.

## Validación de eventos del panel

Se validó que los accesos y login quedan registrados en la base remota `dasc_logs.eventos`.

Evidencia observada:

    login admin desde 192.168.1.137
    POST /login
    resultado OK
    Inicio de sesión correcto

También se registraron accesos autenticados a recursos del panel y carga de recursos estáticos.

## Validación de estado real de backups

Después de revisar el panel, se comprobó en `lab-backup` el estado real de backups:

- `history.tsv` existe.
- `audit.log` existe.
- Hay backups en estado `OK`.
- Hay un backup en estado `PRUNED`.
- Hay backup incremental referenciando una base.
- Los ficheros físicos existen en `/home/dasc/backups`.
- La auditoría registra creación, integridad, simulacro, restauración y retención.

## Evidencias principales

Backups observados:

- `fase2-full-YYYYMMDD-HHMM.sql.gz`
- `fase2-retention-trigger.sql.gz`
- `fase2-chain-base.sql.gz`
- `fase2-chain-inc.sql.gz`
- `fase2-chain-trigger.sql.gz`

Eventos de auditoría observados:

- `backup.create`
- `backup.integrity`
- `backup.restore_drill`
- `backup.restore.start`
- `backup.restore`
- `backup.prune`

## Resultado

La validación visual del panel queda completada.

La Fase 2 no solo queda validada por scripts y terminal, sino también mediante acceso real al panel web por HTTPS desde Windows.
