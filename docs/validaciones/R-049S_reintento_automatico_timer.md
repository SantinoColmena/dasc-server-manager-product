# R-049S - Reintento automático mediante systemd timer

## Objetivo

Automatizar el reintento de envío de tickets locales pendientes hacia el panel central DASC.

## Estado

En curso.

## Contexto

R-049O añadió cola offline y botón manual de reintento.

R-049S añade un temporizador systemd para ejecutar ese reintento de forma automática cada cierto intervalo.

## Archivos añadidos

~~~text
deploy/api/package/scripts/retry_central_pending.py
deploy/api/install_central_retry_timer.sh
deploy/api/uninstall_central_retry_timer.sh
~~~

## Servicio systemd

~~~text
dasc-central-retry.service
~~~

Tipo:

~~~text
oneshot
~~~

## Timer systemd

~~~text
dasc-central-retry.timer
~~~

Frecuencia por defecto:

~~~text
Cada 5 minutos
~~~

## Funcionamiento

El timer ejecuta el script:

~~~text
/opt/dasc/api/scripts/retry_central_pending.py
~~~

El script importa `main.py` del panel local y ejecuta:

~~~text
retry_pending_central_sync_tickets(limit=50)
~~~

Después registra un evento en MariaDB usando:

~~~text
log_event()
~~~

## Ruta funcional equivalente

El timer automatiza la misma lógica que el botón manual:

~~~text
POST /soporte/tickets/reintentar-central
~~~

## Criterio de validación

R-049S se considera preparada cuando:

- El script Python compila.
- El instalador copia el script a `/opt/dasc/api/scripts`.
- Se crea `dasc-central-retry.service`.
- Se crea `dasc-central-retry.timer`.
- El timer queda enabled y active.
- `systemctl start dasc-central-retry.service` ejecuta el reintento.
- Un ticket pendiente con `central_sync_status=error` pasa a `sent` cuando central-support está disponible.
- MariaDB registra el evento automático con usuario `systemd-timer`.
- El temporizador aparece en `systemctl list-timers`.

## Límites

Esta versión todavía no incluye:

- Backoff progresivo.
- Número máximo de intentos por ticket.
- Fecha separada de último intento.
- Panel visual específico para cola automática.
- Alertas por fallo prolongado.

## Próximo paso

Validar en `lab-pruebas`.

## Conclusión

R-049S permite que el soporte local-central sea más autónomo: los tickets pendientes ya no dependen únicamente de una acción manual del técnico.
