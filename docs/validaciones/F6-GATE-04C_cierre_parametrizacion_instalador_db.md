# F6-GATE-04C - Cierre parametrización del instalador DB

## Objetivo

Validar que el instalador de base de datos ya no depende de IPs fijas de laboratorio para configurar los hosts permitidos de backup, restauración y logs.

## Estado

Cerrada.

## Archivo modificado

~~~text
deploy/db/install_db.sh
~~~

## Problema original

La auditoría de IPs detectó que el instalador DB usaba valores de laboratorio como valores por defecto reales:

~~~text
BACKUP_ALLOWED_HOST=192.168.60.30
LOGS_ALLOWED_HOST=192.168.60.10
~~~

Estos valores eran válidos para laboratorio, pero no deben condicionar instalaciones reales.

## Cambio aplicado

Se eliminaron los valores por defecto rígidos.

Ahora el instalador exige definir:

~~~text
BACKUP_ALLOWED_HOST
LOGS_ALLOWED_HOST
~~~

Si no se pasan como variables de entorno, el instalador los solicita de forma interactiva.

## Validación de auditoría

Tras el cambio se regeneró:

~~~text
docs/auditoria/auditoria_ips_perfiles.md
~~~

Resultado:

~~~text
Total referencias IP detectadas: 234
Severidad ALTA: 6
Severidad MEDIA: 36
Severidad BAJA: 10
Severidad INFO: 182
~~~

La severidad ALTA bajó de 8 a 6.

Esto confirma que desaparecieron las dos IPs rígidas del instalador DB:

~~~text
192.168.60.30
192.168.60.10
~~~

como valores por defecto reales dentro de `deploy/db/install_db.sh`.

## Validación real en Ubuntu

Se clonó el repositorio en `lab-db-gate02` y se ejecutó el instalador de forma no interactiva:

~~~bash
sudo BACKUP_ALLOWED_HOST=192.168.60.10 LOGS_ALLOWED_HOST=192.168.60.10 bash deploy/db/install_db.sh
~~~

## Resultado del instalador

El instalador mostró correctamente:

~~~text
BACKUP_ALLOWED_HOST=192.168.60.10
LOGS_ALLOWED_HOST=192.168.60.10
~~~

Y terminó con:

~~~text
Base de datos instalada correctamente
~~~

## Comprobaciones realizadas

Se verificó:

- Servicio MariaDB activo.
- Puerto `3306` escuchando.
- SSH activo en puerto `22`.
- Usuario `dasc_backup` creado para `192.168.60.10`.
- Usuario `dasc_restore` creado para `192.168.60.10`.
- Usuario `dasc_logs` creado para `192.168.60.10`.
- Grants de backup correctos.
- Grants de restauración correctos.
- Grants de logs correctos.
- Base `dasc_logs` existente.
- Tabla `eventos` existente.
- Conteo de eventos conservado.

Resultado de eventos:

~~~text
total_eventos = 20
~~~

## Observación

Durante la creación del usuario SSH `dasc` apareció un aviso de contraseña débil:

~~~text
CONTRASEÑA INCORRECTA: La contraseña no supera la verificación de diccionario
~~~

El instalador continuó y configuró la contraseña.

Esto no bloquea F6-GATE-04C, pero queda como mejora futura para endurecer validación de contraseñas o explicar requisitos mínimos al usuario.

## Criterio de cierre

F6-GATE-04C se considera cerrada porque:

- El instalador DB ya no usa `192.168.60.30` como valor por defecto.
- El instalador DB ya no usa `192.168.60.10` como valor por defecto.
- Los hosts se pueden pasar por variables de entorno.
- El instalador muestra los valores efectivos usados.
- La auditoría refleja reducción de hallazgos ALTA.
- El instalador fue ejecutado correctamente en Ubuntu real.
- MariaDB, usuarios, grants y logs quedaron funcionales.

## Próxima puerta

La siguiente puerta lógica es:

~~~text
F6-GATE-04D - Parametrizar instalador backup-services
~~~

## Conclusión

DASC Server Manager supera la validación de parametrización del instalador DB.

El instalador de base de datos deja de depender de IPs fijas de laboratorio y empieza a adaptarse a entornos reales mediante variables explícitas.
