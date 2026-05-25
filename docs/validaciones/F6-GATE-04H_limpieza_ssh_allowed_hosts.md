# F6-GATE-04H - Limpieza fina de configuración SSH y duplicados

## Objetivo

Evitar duplicados en `DASC_SSH_ALLOWED_HOSTS` cuando varios roles apuntan a la misma máquina.

## Estado

En curso.

## Contexto

Durante F6-GATE-04F se validó un perfil de 3 servidores con IPs explícitas.

En esa validación se detectó que `DASC_SSH_ALLOWED_HOSTS` podía contener valores repetidos cuando `SERVICIOS_HOST` y `BACKUPS_HOST` tenían la misma IP.

Ejemplo observado:

~~~text
DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.30,192.168.60.20
~~~

Esto no bloqueaba la instalación, pero no es una salida limpia para producto.

## Archivo modificado

~~~text
deploy/api/install_dasc_api.sh
~~~

## Cambio aplicado

Se añade una función para construir listas CSV únicas:

~~~text
build_unique_csv
~~~

El instalador API pasa a generar `DASC_SSH_ALLOWED_HOSTS` eliminando duplicados.

## Resultado esperado

Si `BACKUPS_HOST` y `SERVICIOS_HOST` apuntan a la misma máquina, el resultado debe ser:

~~~text
DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,192.168.60.30,192.168.60.20
~~~

en lugar de repetir `192.168.60.30`.

## Criterio de validación

F6-GATE-04H se considera preparada cuando:

- El instalador API genera `DASC_SSH_ALLOWED_HOSTS` mediante lista única.
- No se repiten hosts si dos roles usan la misma IP.
- El cambio no rompe el instalador.
- La configuración real de laboratorio puede limpiarse sin afectar al servicio API.

## Conclusión

F6-GATE-04H es una limpieza menor, pero mejora la calidad final del bloque de instaladores adaptables por perfil.
