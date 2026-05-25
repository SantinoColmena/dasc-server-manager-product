# F6-GATE-04E - Revisión de config.env.example y placeholders por perfil

## Objetivo

Evitar que `config.env.example` parezca una configuración real fija de laboratorio.

## Estado

En curso.

## Archivo revisado

~~~text
deploy/api/package/config.env.example
~~~

## Problema detectado

El archivo de ejemplo contenía IPs de laboratorio como:

~~~text
192.168.60.20
192.168.60.30
192.168.60.40
~~~

Aunque eran útiles para el laboratorio, podían interpretarse como valores obligatorios del producto.

## Cambio aplicado

Se sustituyen las IPs de laboratorio por placeholders:

~~~text
IP_SERVIDOR_DB
IP_SERVIDOR_BACKUPS
IP_SERVIDOR_SERVICIOS
IP_SERVIDOR_SERVICIOS_O_BACKUPS
~~~

También se añade una cabecera explicando que el archivo es una plantilla y debe adaptarse según perfil.

## Perfiles contemplados

### Lite

Un solo servidor principal.

Puede usar `127.0.0.1` para servicios locales, pero requiere copia externa obligatoria para backups.

### PyME 2 servidores

Servidor 1:

~~~text
API / panel / backups
~~~

Servidor 2:

~~~text
DB / logs
~~~

### Pro 3 servidores

Servidor 1:

~~~text
API / panel
~~~

Servidor 2:

~~~text
DB / logs
~~~

Servidor 3:

~~~text
Backups / almacenamiento
~~~

## Variables afectadas

~~~env
SERVICIOS_HOST
BACKUPS_HOST
TERMINAL_DATABASE_HOST
LOGS_DB_HOST
BACKUP_DB_HOST
RESTORE_DB_HOST
DASC_SSH_ALLOWED_HOSTS
~~~

## Criterio de validación

F6-GATE-04E se considera preparada cuando:

- `config.env.example` no usa IPs `192.168.60.x` como ejemplo principal.
- Los valores de red se muestran como placeholders.
- El archivo explica que debe adaptarse al perfil.
- La auditoría de IPs refleja que las IPs de laboratorio ya no aparecen en ese archivo.
- Se mantiene `127.0.0.1` solo como referencia local aceptable.

## Conclusión

`config.env.example` deja de representar un laboratorio fijo y pasa a funcionar como plantilla de producto adaptable por perfil.
