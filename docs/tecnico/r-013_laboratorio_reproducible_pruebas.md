# R-013 - Laboratorio reproducible de pruebas

## Objetivo

El objetivo de esta tarea es definir un laboratorio reproducible para probar Vigex de forma controlada.

El proyecto ya dispone de un MVP funcional y de una arquitectura basada en varias máquinas, pero para evolucionar hacia producto es necesario poder repetir pruebas sin depender de configuraciones manuales difíciles de reconstruir.

R-013 busca que cualquier cambio importante pueda validarse en un entorno claro, documentado y repetible.

## Problema actual

Durante el desarrollo del MVP se han usado máquinas virtuales, scripts, configuraciones manuales, Docker y diferentes pruebas.

Esto ha sido útil para avanzar rápido, pero tiene varios riesgos:

- Es difícil repetir exactamente el mismo entorno.
- Una máquina puede tener configuraciones antiguas.
- Los errores pueden depender del estado previo del sistema.
- Una instalación puede funcionar en una máquina y fallar en otra.
- Es más difícil validar instaladores.
- Es más difícil preparar una demo limpia.
- Es más difícil comprobar si una release está lista.

## Objetivo técnico

El laboratorio debe permitir probar:

- Instalación limpia.
- Reinstalación.
- Actualización.
- Desinstalación.
- Backups manuales.
- Logs internos.
- Gestión de servicios.
- Permisos de usuario.
- Configuración por perfiles.
- Errores controlados.

## Tipos de laboratorio

Se contemplan tres tipos de laboratorio.

### 1. Laboratorio local con máquinas virtuales

Es el entorno más parecido al MVP original.

Puede usar:

- VirtualBox.
- VMware.
- Proxmox.
- IsardVDI.
- Máquinas Ubuntu Server.

Ventajas:

- Muy parecido a una instalación real.
- Permite probar SSH, systemd y red.
- Útil para validar instaladores.

Limitaciones:

- Requiere más recursos.
- Es más lento de preparar.
- Puede depender mucho del equipo usado.

## 2. Laboratorio Docker

El laboratorio Docker permite levantar un entorno más rápido y portable.

Ventajas:

- Más fácil de compartir.
- Más rápido de reconstruir.
- Útil para demos.
- Útil para pruebas funcionales.

Limitaciones:

- No reproduce exactamente systemd.
- No sustituye del todo al entorno de máquinas reales.
- Algunas pruebas SSH o systemctl pueden cambiar.

## 3. Laboratorio cloud

El laboratorio cloud permite probar Vigex en una máquina externa.

Puede usarse:

- Google Cloud.
- VPS económico.
- Máquina Ubuntu en proveedor cloud.

Ventajas:

- Acceso desde cualquier lugar.
- Entorno limpio.
- Útil para pruebas de instalación.
- Útil para preparar demos remotas.

Limitaciones:

- Puede tener coste.
- Hay que cuidar firewall y seguridad.
- No debe exponerse información sensible.

## Laboratorio recomendado para Fase 1

Para la Fase 1 se recomienda usar dos niveles:

### Nivel 1 - Docker o entorno local rápido

Uso:

- Revisar documentación.
- Probar interfaz.
- Validar flujos básicos.
- Preparar capturas.
- Probar cambios no críticos.

### Nivel 2 - Máquinas Ubuntu reales o cloud

Uso:

- Probar instaladores.
- Probar SSH.
- Probar systemd.
- Probar MariaDB.
- Probar backups reales.
- Probar desinstalación.

## Arquitectura mínima de pruebas

La arquitectura mínima reproducible debe contemplar:

~~~text
Servidor Panel/API
Servidor Base de Datos
Servidor Backups/Servicios
~~~

Para pruebas simplificadas se puede usar:

~~~text
Servidor único
~~~

o bien:

~~~text
Servidor principal + servidor Vigex/backups
~~~

Esto conecta con los perfiles definidos en R-006:

- `single`
- `dual`
- `distributed`

## Pruebas obligatorias del laboratorio

### 1. Prueba de instalación limpia

Objetivo:

Comprobar que Vigex puede instalarse desde cero.

Debe validarse:

- Dependencias.
- Directorios.
- Entorno virtual.
- Servicio systemd.
- `config.env`.
- Arranque de la API.
- Acceso al panel.

## 2. Prueba de reinstalación

Objetivo:

Comprobar que el instalador puede ejecutarse más de una vez.

Debe validarse:

- No se rompe `/opt/vigex/api`.
- No se pierde `config.env`.
- No se duplica configuración.
- El servicio sigue arrancando.
- El panel sigue respondiendo.

## 3. Prueba de desinstalación

Objetivo:

Comprobar que el sistema puede eliminarse correctamente.

Debe validarse:

- Se detiene el servicio.
- Se elimina systemd.
- Se elimina `/opt/vigex/api`.
- Se ejecuta `daemon-reload`.
- No quedan errores graves.

## 4. Prueba de login y permisos

Objetivo:

Comprobar que el acceso funciona.

Debe validarse:

- Login correcto.
- Login incorrecto.
- Logout.
- Usuario administrador.
- Usuario limitado.
- Acceso bloqueado a secciones sin permiso.

## 5. Prueba de backups

Objetivo:

Comprobar que se puede ejecutar un backup.

Debe validarse:

- Backup completo.
- Error por base inexistente.
- Error por SSH.
- Mensaje visible en panel.
- Evento registrado en logs.
- Preparación para historial.

## 6. Prueba de servicios

Objetivo:

Comprobar la gestión remota de servicios.

Debe validarse:

- Listado de servicios.
- Reinicio de servicio.
- Error por servicio inexistente.
- Error de permisos.
- Registro en logs.

## 7. Prueba de logs

Objetivo:

Comprobar que los eventos se guardan y muestran.

Debe validarse:

- Eventos de acceso.
- Eventos de login.
- Eventos de backup.
- Eventos de servicios.
- Eventos de administración.
- Resultado OK y ERROR.

## 8. Prueba de navegación

Objetivo:

Comprobar que el panel es coherente.

Debe validarse:

- Menú visible.
- Sección activa.
- Botón de logout.
- Mensajes claros.
- Permisos respetados.

## Datos de prueba recomendados

Base de datos:

~~~text
employees
~~~

Usuario administrador:

~~~text
admin
~~~

Usuario limitado de prueba:

~~~text
operador
~~~

Permisos recomendados del usuario limitado:

~~~text
logs
servicios
~~~

Servidor de backups en laboratorio:

~~~text
192.168.60.30
~~~

Servidor de base de datos en laboratorio:

~~~text
192.168.60.20
~~~

Servidor del panel:

~~~text
192.168.60.10
~~~

## Comandos de validación mínimos

Comprobar servicio:

~~~bash
systemctl status vigex-api --no-pager
~~~

Comprobar puerto:

~~~bash
curl -I http://127.0.0.1:8000
~~~

Comprobar estructura:

~~~bash
ls -ld /opt/vigex
ls -ld /opt/vigex/api
ls -l /opt/vigex/api/main.py
ls -l /opt/vigex/api/config.env
~~~

Comprobar SSH:

~~~bash
ssh vigex@192.168.60.30 hostname
~~~

Comprobar script de backups:

~~~bash
ssh vigex@192.168.60.30 /usr/local/bin/backups_api.sh full employees /home/vigex/backups prueba-YYYYMMDD-HHMM.sql gzip 30 manual prueba
~~~

Comprobar logs en base de datos:

~~~sql
SELECT id, fecha, tipo, usuario, recurso, resultado, detalle
FROM eventos
ORDER BY fecha DESC
LIMIT 20;
~~~

## Evidencias recomendadas

Para cada prueba importante conviene guardar:

- Captura del panel.
- Comando ejecutado.
- Resultado esperado.
- Resultado obtenido.
- Error si existe.
- Solución aplicada.
- Fecha de prueba.

## Estructura recomendada de documentación

Se recomienda crear una carpeta:

~~~text
docs/pruebas/
~~~

Y dentro:

~~~text
laboratorio_reproducible.md
checklist_release_0.1.md
pruebas_instalador.md
pruebas_backups.md
pruebas_logs.md
pruebas_permisos.md
~~~

No es obligatorio crear todos los documentos en esta tarea, pero sí dejar definida la estructura.

## Criterio de salida

R-013 se considerará completada cuando:

- Exista diseño de laboratorio reproducible.
- Estén definidos los tipos de laboratorio.
- Esté definida la arquitectura mínima.
- Estén definidas las pruebas obligatorias.
- Estén definidos comandos mínimos de validación.
- Estén definidas evidencias recomendadas.
- Quede preparada la release R-014.

## Decisión actual

La decisión recomendada es usar dos entornos:

1. Docker o entorno local para pruebas rápidas.
2. Ubuntu real o cloud para validar instaladores y comportamiento real.

Esto permite avanzar rápido sin perder realismo técnico.

## Estado

Estado actual: Pendiente de implementación práctica.

Prioridad: Alta.

Dependencias:

- R-006 - Configuración por perfiles.
- R-007 - Instalador base idempotente.
- R-008 - Motor centralizado de backups.
- R-009 - Historial persistente de backups.
- R-010 - Programación automática de backups.
- R-011 - Mejora de logs internos.
- R-012 - Limpieza de navegación y mensajes.

Bloque siguiente:

- R-014 - Publicación versión interna 0.1.
