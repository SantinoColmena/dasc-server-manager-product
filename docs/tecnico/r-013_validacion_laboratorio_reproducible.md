# R-013 - Validación del laboratorio reproducible de pruebas

## Objetivo

Este documento define cómo validar que el laboratorio de pruebas de Vigex es reproducible, útil y suficiente para probar cambios antes de una versión interna.

La validación busca comprobar que el proyecto puede instalarse, probarse y revisarse en un entorno controlado sin depender de configuraciones antiguas o máquinas preparadas manualmente sin documentar.

## Qué se quiere validar

El laboratorio debe permitir probar:

- Instalación limpia.
- Reinstalación.
- Desinstalación.
- Configuración por perfiles.
- Login y permisos.
- Backups manuales.
- Logs internos.
- Gestión de servicios.
- Navegación del panel.
- Errores controlados.
- Preparación de una release interna.

## Entornos válidos

Se consideran válidos estos entornos:

| Entorno | Uso principal |
|---|---|
| Máquina virtual local | Pruebas realistas con Ubuntu, SSH y systemd |
| Docker | Pruebas rápidas y demos |
| Cloud Ubuntu | Pruebas externas o desde cualquier ubicación |
| Laboratorio de 3 máquinas | Validación completa distribuida |

## Validación de laboratorio single

El perfil `single` debe permitir probar Vigex en una sola máquina.

Debe comprobarse:

- Panel/API en la misma máquina.
- Base de datos en la misma máquina.
- Backups en la misma máquina.
- Logs en la misma máquina.
- Servicios gestionados localmente.

Resultado esperado:

- El sistema puede arrancar.
- El panel responde.
- Los backups pueden ejecutarse.
- Los logs pueden consultarse.
- No se necesita red distribuida.

## Validación de laboratorio dual

El perfil `dual` debe permitir probar Vigex con dos máquinas.

Distribución esperada:

~~~text
Servidor 1: servidor principal / base de datos / servicios
Servidor 2: Vigex / backups / logs
~~~

Debe comprobarse:

- SSH entre máquinas.
- Acceso a MariaDB remoto.
- Ejecución de backups desde nodo Vigex.
- Registro de logs.
- Separación básica de responsabilidades.

Resultado esperado:

- El sistema funciona con dos nodos.
- Es el escenario recomendado para PyMEs.
- Se puede defender como arquitectura estándar.

## Validación de laboratorio distributed

El perfil `distributed` debe permitir probar tres máquinas.

Distribución esperada:

~~~text
Servidor 1: Panel/API
Servidor 2: Base de datos
Servidor 3: Backups/servicios/logs
~~~

Debe comprobarse:

- Panel accesible.
- SSH hacia servidor de backups.
- Conexión desde backups hacia base de datos.
- Logs centralizados.
- Separación clara de responsabilidades.

Resultado esperado:

- La arquitectura distribuida funciona.
- Se valida el escenario más completo.
- Sirve para documentación técnica y demostración avanzada.

## Prueba 1 - Instalación limpia

Acción:

~~~bash
sudo ./install_vigex_api.sh
~~~

Resultado esperado:

- Instala dependencias.
- Crea `/opt/vigex/api`.
- Crea entorno virtual.
- Instala dependencias Python.
- Crea servicio `vigex-api`.
- Arranca el panel.
- Muestra resumen final.

Comprobaciones:

~~~bash
systemctl status vigex-api --no-pager
curl -I http://127.0.0.1:8000
ls -ld /opt/vigex/api
~~~

## Prueba 2 - Reinstalación

Acción:

~~~bash
sudo ./install_vigex_api.sh
sudo ./install_vigex_api.sh
~~~

Resultado esperado:

- No rompe la instalación.
- No borra configuración importante.
- No falla por carpetas existentes.
- El servicio sigue funcionando.
- El panel sigue accesible.

## Prueba 3 - Desinstalación

Acción:

~~~bash
sudo ./uninstall_vigex_api.sh
~~~

Resultado esperado:

- Detiene el servicio.
- Deshabilita `vigex-api`.
- Elimina el archivo systemd.
- Elimina `/opt/vigex/api`.
- Recarga systemd.

Comprobaciones:

~~~bash
systemctl status vigex-api --no-pager
ls -ld /opt/vigex/api
~~~

## Prueba 4 - Login

Acciones:

- Entrar con usuario correcto.
- Entrar con contraseña incorrecta.
- Cerrar sesión.
- Intentar acceder al panel sin sesión.

Resultado esperado:

- Login correcto permite entrar.
- Login incorrecto muestra error.
- Logout devuelve a `/login`.
- Rutas privadas redirigen a login.

## Prueba 5 - Permisos

Acciones:

- Crear usuario limitado.
- Darle permisos de logs y servicios.
- Entrar con ese usuario.
- Intentar acceder a copias o administración.

Resultado esperado:

- Solo ve las secciones permitidas.
- No accede a secciones sin permiso.
- Recibe mensaje claro si intenta entrar por URL.

## Prueba 6 - Backups

Acciones:

- Ejecutar backup completo correcto.
- Ejecutar backup con base de datos inexistente.
- Simular error de SSH.
- Revisar mensaje del panel.

Resultado esperado:

- Backup correcto devuelve OK.
- Backup fallido devuelve ERROR.
- No aparece traceback.
- El evento queda registrado en logs.
- Queda preparado para historial persistente.

## Prueba 7 - Servicios

Acciones:

- Listar servicios.
- Reiniciar servicio válido.
- Intentar acción sobre servicio inexistente.
- Simular error de permisos.

Resultado esperado:

- Tabla de servicios visible.
- Acción correcta muestra mensaje claro.
- Error muestra mensaje entendible.
- Evento registrado en logs.

## Prueba 8 - Logs

Acciones:

- Entrar en `/logs`.
- Comprobar eventos recientes.
- Generar login fallido.
- Generar backup.
- Generar acción de servicio.

Resultado esperado:

- Los eventos aparecen en la tabla.
- Se distinguen OK y ERROR.
- Los eventos están ordenados por fecha.
- No se rompe la página si la base no responde.

## Prueba 9 - Navegación

Acciones:

- Entrar como admin.
- Entrar como usuario limitado.
- Navegar por todas las secciones visibles.
- Comprobar botón de logout.

Resultado esperado:

- Menú coherente.
- Sección activa correcta.
- Botón logout visible.
- Mensajes claros.
- Sin enlaces rotos visibles.

## Prueba 10 - Preparación de release

Antes de publicar una versión interna, se debe comprobar:

~~~bash
git status
git log --oneline -5
~~~

Resultado esperado:

- Rama limpia.
- Cambios subidos a GitHub.
- Documentación de la fase actual completada.
- No quedan archivos temporales sin revisar.

## Evidencias mínimas

Para validar el laboratorio se recomienda guardar:

- Captura del panel funcionando.
- Captura de `/logs`.
- Captura de backup correcto.
- Captura de error controlado.
- Salida de `systemctl status`.
- Salida de `curl -I`.
- Salida de `git status`.

## Checklist de cierre

R-013 se considerará validada cuando se pueda marcar:

- [ ] Existe documento de laboratorio reproducible.
- [ ] Existe documento de validación.
- [ ] Están definidos los entornos válidos.
- [ ] Está validado perfil `single`.
- [ ] Está validado perfil `dual`.
- [ ] Está preparado perfil `distributed`.
- [ ] Está definida prueba de instalación limpia.
- [ ] Está definida prueba de reinstalación.
- [ ] Está definida prueba de desinstalación.
- [ ] Está definida prueba de login.
- [ ] Está definida prueba de permisos.
- [ ] Está definida prueba de backups.
- [ ] Está definida prueba de servicios.
- [ ] Está definida prueba de logs.
- [ ] Está preparada la publicación de R-014.

## Estado

Estado actual: Diseño y validación documentados.

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
