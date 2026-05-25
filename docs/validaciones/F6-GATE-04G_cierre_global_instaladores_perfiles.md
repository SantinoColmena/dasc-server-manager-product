# F6-GATE-04G - Cierre global de instaladores adaptables por perfil

## Objetivo

Cerrar globalmente la puerta F6-GATE-04, dedicada a eliminar dependencias rígidas de IPs de laboratorio y validar instalaciones por perfil con IPs explícitas.

## Estado

Cerrada.

## Resumen

F6-GATE-04 se abrió para resolver un riesgo importante detectado durante la evolución de DASC Server Manager hacia producto:

Los instaladores y plantillas todavía contenían IPs de laboratorio como si fueran valores reales.

El objetivo no era eliminar la documentación histórica, sino separar correctamente:

- Evidencias de laboratorio.
- Valores de ejemplo.
- Configuración real.
- Variables de instalación.
- Perfiles de despliegue.

## Subgates cerrados

| Gate | Descripción | Estado |
|---|---|---|
| F6-GATE-04A | Auditoría de IPs fijas y perfiles | Cerrada |
| F6-GATE-04B | Clasificación de IPs fijas y plan de parametrización | Cerrada |
| F6-GATE-04C | Parametrización del instalador DB | Cerrada |
| F6-GATE-04D | Parametrización del instalador backup-services | Cerrada |
| F6-GATE-04E | Revisión de config.env.example y placeholders por perfil | Cerrada |
| F6-GATE-04F | Validación de instalación con IPs explícitas | Cerrada |

## Cambios principales realizados

### Auditoría de IPs

Se creó una herramienta de auditoría:

~~~text
tools/windows/audit_fixed_ips.ps1
~~~

Y su informe:

~~~text
docs/auditoria/auditoria_ips_perfiles.md
~~~

La auditoría permite distinguir entre:

- IPs en documentación.
- IPs en ejemplos.
- IPs en instaladores.
- IPs en herramientas de producto.

## Instalador DB

Archivo:

~~~text
deploy/db/install_db.sh
~~~

Se eliminaron valores rígidos de laboratorio para:

~~~text
BACKUP_ALLOWED_HOST
LOGS_ALLOWED_HOST
~~~

Ahora el instalador permite definirlos por variables de entorno o preguntarlos interactivamente.

Ejemplo validado:

~~~bash
sudo BACKUP_ALLOWED_HOST=192.168.60.10 LOGS_ALLOWED_HOST=192.168.60.10 bash deploy/db/install_db.sh
~~~

## Instalador backup-services

Archivo:

~~~text
deploy/backup-services/install_backup_services.sh
~~~

Se eliminó el valor rígido:

~~~text
DB_HOST=192.168.60.20
~~~

Ahora el instalador requiere `DB_HOST` explícito o lo solicita interactivamente.

Ejemplo validado:

~~~bash
sudo DB_HOST=192.168.60.20 bash deploy/backup-services/install_backup_services.sh
~~~

Durante la validación también se corrigió la instalación de dependencias para Ubuntu limpio, usando cliente MySQL por defecto y comprobando:

~~~text
mysql
mysqldump
mysqlbinlog
~~~

## config.env.example

Archivo:

~~~text
deploy/api/package/config.env.example
~~~

Se sustituyeron IPs de laboratorio por placeholders:

~~~text
IP_SERVIDOR_DB
IP_SERVIDOR_BACKUPS
IP_SERVIDOR_SERVICIOS
IP_SERVIDOR_SERVICIOS_O_BACKUPS
~~~

También se añadió explicación de perfiles:

- Lite.
- PyME 2 servidores.
- Pro 3 servidores.

## Perfil validado

Se validó un perfil equivalente a Pro 3 servidores:

| Rol | Máquina | IP |
|---|---|---|
| API / panel | lab-pruebas | 192.168.60.10 |
| DB / logs | lab-db-gate02 | 192.168.60.20 |
| Backups / servicios | lab-backups-gate04d | 192.168.60.30 |

## Resultado técnico

Se comprobó:

- API/panel activo.
- API respondiendo con redirección a `/login`.
- MariaDB activo.
- Puerto 3306 accesible.
- SSH accesible en backup-services.
- Usuarios de DB creados para API y backup-services.
- Base `dasc_logs` funcional.
- Base `employees` funcional.
- Backup-services con cliente `mysql`.
- Backup-services con `mysqldump`.
- Backup-services con `mysqlbinlog`.
- Conexión remota desde backup-services a DB.
- Dump de prueba correcto.

## Observaciones

Queda detectado como mejora menor que `DASC_SSH_ALLOWED_HOSTS` puede contener valores duplicados si `SERVICIOS_HOST` y `BACKUPS_HOST` apuntan a la misma máquina.

Esto no bloquea la puerta porque la lista sigue siendo funcional.

También se detectó aviso de compatibilidad:

~~~text
Warning: column statistics not supported by the server.
~~~

No bloquea porque el dump se genera correctamente.

## Criterio de cierre

F6-GATE-04 se considera cerrada porque:

- Se auditaron IPs fijas del repositorio.
- Se clasificaron riesgos reales frente a documentación histórica.
- Se parametrizó el instalador DB.
- Se parametrizó el instalador backup-services.
- Se revisó `config.env.example`.
- Se validó un perfil real de 3 servidores con IPs explícitas.
- Se eliminó la dependencia directa de IPs rígidas de laboratorio en los puntos críticos.
- El producto queda más preparado para despliegues reales por perfil.

## Límites

Esta puerta no valida todavía:

- Instalación completa en una red totalmente distinta a `192.168.60.x`.
- Asistente único de instalación por perfil.
- Generación automática de config.env desde wizard.
- Deduplicación automática de `DASC_SSH_ALLOWED_HOSTS`.
- Instalación guiada para cliente final no técnico.

## Próxima puerta recomendada

La siguiente puerta lógica es:

~~~text
F6-GATE-05 - Soporte real sin GitHub para cliente
~~~

Otra opción previa sería:

~~~text
F6-GATE-04H - Limpieza fina de configuración SSH y duplicados
~~~

pero no es bloqueante para cerrar F6-GATE-04.

## Conclusión

DASC Server Manager supera el bloque F6-GATE-04.

El producto deja de estar atado a una configuración rígida de laboratorio y queda validado con una arquitectura explícita de API, DB y backups separados.
