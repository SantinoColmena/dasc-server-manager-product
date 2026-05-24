# F6-GATE-03E - Cierre integración de backups en informe operativo

## Objetivo

Validar que el informe operativo de DASC Server Manager ya muestra el estado real del último backup completo generado por la herramienta de producto.

## Estado

Cerrada.

## Entorno usado

| Rol | Máquina | IP privada DASC |
|---|---|---|
| API / Generador informe | lab-pruebas | 192.168.60.10 |
| DB / Origen datos | lab-db-gate02 | 192.168.60.20 |

## Contexto

En F6-GATE-03D se validó la herramienta:

~~~text
/opt/dasc/api/tools/run_full_db_backup.sh
~~~

Esa herramienta genera:

~~~text
.sql
.sql.sha256
.sql.meta.json
~~~

En F6-GATE-03E se valida que el informe operativo lea esa metadata y muestre el estado del backup.

## Código validado

Se actualizó:

~~~text
deploy/api/package/tools/generate_operational_report.py
~~~

El informe ahora inspecciona:

~~~text
BACKUP_OUTPUT_DIR
*.sql.meta.json
*.sql.sha256
*.sql
~~~

## Validación estructural

Se ejecutó la validación automática del paquete API.

Resultado:

~~~text
Total comprobaciones: 37
Correctas: 37
Fallidas: 0
Resultado: OK
~~~

La validación añadió comprobaciones para:

- Inspección de backups en informe operativo.
- Lectura de `BACKUP_OUTPUT_DIR`.
- Sección `Backups completos`.

## Instalación real

En `lab-pruebas` se actualizó el repo hasta:

~~~text
a86eb7f feat: integrar backups en informe operativo
~~~

Después se reinstaló el API.

Resultado:

- Servicio `dasc-api` activo.
- Panel respondiendo con redirección a `/login`.
- Variables `BACKUP_DB_*` presentes en `/opt/dasc/api/config.env`.
- Mensaje SSH final corregido como no bloqueante.

## Informe operativo generado

Se ejecutó:

~~~bash
cd /opt/dasc/api
sudo ./tools/generate_operational_report.sh "DASC validacion backup informe" "2026-05"
~~~

Archivo generado:

~~~text
/opt/dasc/api/reports/informe_operativo_2026-05.md
~~~

## Resultado del informe

El informe incluyó correctamente la sección:

~~~text
## 7. Backups completos
~~~

Datos detectados:

| Campo | Valor |
|---|---|
| Estado | OK |
| Directorio | `/var/backups/dasc/mysql/full` |
| Último backup | `/var/backups/dasc/mysql/full/dasc_logs_full_20260524-080415_F6-GATE-03D.sql` |
| Base de datos | `dasc_logs` |
| Host origen | `192.168.60.20` |
| Usuario backup | `dasc_backup` |
| Tamaño bytes | `4386` |
| Archivo SQL existe | OK |
| Archivo SHA256 existe | OK |
| Contiene CREATE TABLE | True |
| Contiene INSERT INTO | True |
| Binario dump | `/usr/bin/mariadb-dump` |
| Etiqueta | `F6-GATE-03D` |

Hash SHA256 detectado:

~~~text
64b0a829de533a13ec870104e1cb55cccdcbe8c1b76687f406d0a829008e2b15
~~~

## Conclusión del informe

El informe concluyó:

~~~text
Resultado: BASE OPERATIVA OK CON BACKUP.
~~~

Esto confirma que el informe operativo ya no solo valida configuración y logs, sino también evidencia real del último backup completo válido.

## Observación durante la prueba

Durante la reinstalación apareció un bloqueo temporal de `apt` por `unattended-upgr`.

La instalación pudo continuar después de liberar el bloqueo y el resultado final fue correcto.

Esta observación no invalida la puerta, pero queda como mejora futura para hacer el instalador más robusto ante locks de `apt`.

## Criterio de cierre

F6-GATE-03E se considera cerrada porque:

- El informe operativo lee `BACKUP_OUTPUT_DIR`.
- Detecta metadata real de backups.
- Comprueba existencia del backup `.sql`.
- Comprueba existencia del `.sha256`.
- Muestra hash SHA256.
- Muestra datos de origen del backup.
- Valida estructura del backup.
- Lista últimos backups detectados.
- Concluye `BASE OPERATIVA OK CON BACKUP`.

## Límites

Esta puerta no valida todavía:

- Restauración automática incluida en el informe.
- Retención automática.
- Cifrado de backups.
- Copia externa.
- Exportación PDF.
- Envío al cliente.
- Alertas ante fallo de backup.

## Próxima puerta recomendada

La siguiente puerta lógica es:

~~~text
F6-GATE-03F - Automatización, retención y limpieza de backups
~~~

Después:

~~~text
F6-GATE-03G - Restauración automática o semiautomática controlada
~~~

## Conclusión

DASC Server Manager supera la validación de integración de backups en el informe operativo.

El producto ya puede generar un informe operativo que combina configuración, logs reales y evidencia del último backup completo válido.
