# F6-GATE-04E - Cierre revisión de config.env.example y placeholders por perfil

## Objetivo

Validar que `config.env.example` ya no representa una configuración fija de laboratorio y funciona como plantilla adaptable por perfil.

## Estado

Cerrada.

## Archivo revisado

~~~text
deploy/api/package/config.env.example
~~~

## Problema original

El archivo de ejemplo contenía IPs de laboratorio:

~~~text
192.168.60.20
192.168.60.30
192.168.60.40
~~~

Aunque eran útiles para pruebas internas, podían interpretarse como valores obligatorios del producto.

## Cambio aplicado

Se añadieron comentarios iniciales indicando que el archivo es una plantilla y debe adaptarse al perfil de instalación.

También se sustituyeron las IPs de laboratorio por placeholders:

~~~text
IP_SERVIDOR_DB
IP_SERVIDOR_BACKUPS
IP_SERVIDOR_SERVICIOS
IP_SERVIDOR_SERVICIOS_O_BACKUPS
~~~

## Variables actualizadas

~~~env
SERVICIOS_HOST=IP_SERVIDOR_SERVICIOS_O_BACKUPS
BACKUPS_HOST=IP_SERVIDOR_BACKUPS
TERMINAL_DATABASE_HOST=IP_SERVIDOR_DB
LOGS_DB_HOST=IP_SERVIDOR_DB
BACKUP_DB_HOST=IP_SERVIDOR_DB
RESTORE_DB_HOST=IP_SERVIDOR_DB
DASC_SSH_ALLOWED_HOSTS=127.0.0.1,localhost,IP_SERVIDOR_DB,IP_SERVIDOR_BACKUPS,IP_SERVIDOR_SERVICIOS
~~~

## Perfiles documentados en la plantilla

### Lite

Un solo servidor principal.

Se permite `127.0.0.1` para servicios locales.

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

## Auditoría posterior

Se regeneró:

~~~text
docs/auditoria/auditoria_ips_perfiles.md
~~~

Resultado:

~~~text
Total referencias IP detectadas: 251
Severidad ALTA: 5
Severidad MEDIA: 36
Severidad BAJA: 2
Severidad INFO: 208
~~~

Las referencias `BAJA` restantes corresponden a `127.0.0.1`, aceptado como referencia local.

## Resultado

`config.env.example` ya no contiene IPs `192.168.60.x` como valores principales de ejemplo.

Las IPs de laboratorio quedan limitadas a documentación, pilotos y validaciones históricas.

## Criterio de cierre

F6-GATE-04E se considera cerrada porque:

- La plantilla ya no fija IPs de laboratorio.
- Los valores de red usan placeholders.
- Se documentan perfiles Lite, PyME 2 servidores y Pro 3 servidores.
- La auditoría confirma la reducción de IPs de laboratorio en el ejemplo.
- `127.0.0.1` queda solo como referencia local aceptable.

## Próxima puerta

~~~text
F6-GATE-04F - Validación de instalación con perfiles e IPs explícitas
~~~

## Conclusión

DASC Server Manager supera la revisión de `config.env.example`.

La configuración de ejemplo deja de estar atada al laboratorio y pasa a funcionar como plantilla de producto adaptable por perfil.
