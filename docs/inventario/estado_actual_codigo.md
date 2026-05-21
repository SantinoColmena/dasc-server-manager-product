# Inventario del estado actual del código - DASC Server Manager

## 1. Objetivo del inventario

Este documento recoge el estado actual del código heredado del proyecto académico de DASC Server Manager.

El objetivo no es copiar todo directamente al repositorio producto, sino analizar qué partes del MVP son útiles, qué partes necesitan limpieza y qué elementos deben descartarse o rehacerse antes de convertir el proyecto en un producto más serio.

Este inventario servirá como base para decidir qué código se migra al nuevo repositorio y en qué orden.

---

## 2. Estado general del proyecto heredado

El proyecto académico dispone de una base funcional de MVP.

Actualmente existe una aplicación web basada en FastAPI que permite centralizar varias funciones administrativas:

- Login y sesión de usuario.
- Gestión básica de usuarios y permisos.
- Panel principal.
- Módulo de backups.
- Módulo de logs.
- Módulo de servicios.
- Integración básica con Cacti.
- Scripts de instalación y desinstalación.
- Configuración mediante archivo config.env.
- Comunicación con otros servidores mediante SSH.
- Uso de MariaDB/MySQL para base de datos y logs.

El proyecto funciona como demostración técnica, pero todavía no está listo para ser tratado como producto final. Necesita limpieza, separación de responsabilidades, mejora de seguridad, validación de instaladores y documentación técnica más orientada a cliente real.

---

## 3. Componentes principales identificados

### 3.1 Aplicación web FastAPI

Estado: funcional para MVP.

Elementos identificados:

- Archivo principal main.py.
- Uso de FastAPI.
- Uso de Uvicorn como servidor ASGI.
- Uso de Jinja2 para plantillas HTML.
- Uso de StaticFiles para CSS e imágenes.
- Uso de SessionMiddleware para sesiones.
- Uso de formularios HTML.
- Uso de pymysql para conexión con base de datos de logs.
- Uso de subprocess para ejecutar SSH remoto.

Funciones actuales:

- Servir el panel web.
- Controlar rutas protegidas.
- Gestionar login y logout.
- Renderizar páginas HTML.
- Ejecutar acciones remotas.
- Registrar eventos en base de datos.
- Mostrar información de logs, servicios y backups.

Valor para el producto:

Alto.

Decisión inicial:

Se debe migrar, pero no directamente sin limpiar. Conviene reorganizarlo en módulos más pequeños en una fase posterior.

---

### 3.2 Sistema de autenticación

Estado: funcional básico.

Funciones actuales:

- Login mediante usuario y contraseña.
- Usuario administrador definido por variables de entorno.
- Sesión de usuario mediante middleware.
- Logout.
- Protección de rutas privadas.
- Redirección automática al login si no hay sesión.

Limitaciones:

- Contraseñas en texto plano.
- No hay hashing de contraseñas.
- No hay caducidad avanzada de sesión.
- No hay bloqueo por intentos fallidos.
- No hay recuperación de contraseña.
- No hay segundo factor.
- El administrador depende de variables en config.env.

Valor para el producto:

Medio-alto.

Decisión inicial:

Migrar la lógica base, pero marcar como prioridad futura la mejora de seguridad.

Prioridad de mejora:

Alta.

---

### 3.3 Gestión de usuarios y permisos

Estado: funcional básico.

Funciones actuales:

- Crear usuarios desde el panel.
- Eliminar usuarios.
- Asignar permisos por módulo.
- Diferenciar entre administrador y usuario normal.
- Permisos disponibles para logs, backups y servicios.

Limitaciones:

- Los usuarios secundarios se guardan en users.json.
- Las contraseñas están en texto plano.
- No hay edición de usuarios existentes.
- No hay cambio de contraseña.
- No hay roles más avanzados.
- No hay auditoría específica de cambios de usuarios.

Valor para el producto:

Alto.

Decisión inicial:

Migrar como base funcional, pero rehacer almacenamiento y seguridad en fases posteriores.

Prioridad de mejora:

Alta.

---

### 3.4 Panel principal

Estado: funcional básico.

Funciones actuales:

- Mostrar accesos disponibles según permisos.
- Mostrar usuario autenticado.
- Mostrar rol de administrador.
- Acceso a módulos principales.
- Botón de cierre de sesión.

Limitaciones:

- Dashboard todavía simple.
- No muestra métricas reales resumidas.
- No muestra estado global del sistema.
- No muestra último backup de forma completa.
- No muestra alertas recientes.
- No muestra salud de servidores.

Valor para el producto:

Medio.

Decisión inicial:

Migrar como estructura inicial, pero rediseñar en una fase posterior.

Prioridad de mejora:

Media.

---

### 3.5 Módulo de backups

Estado: funcional básico con necesidad de validación.

Funciones actuales:

- Formulario web para ejecutar backups.
- Selección de tipo de backup.
- Parámetros de base de datos, destino, nombre, compresión, retención, referencia y notas.
- Ejecución remota mediante script.
- Uso de SSH hacia servidor de backups.
- Script backups_api.sh para ejecutar mysqldump.
- Soporte visual para full, incremental y differential.

Limitaciones:

- Hay que validar si incremental y differential están completamente implementados con binlogs o si todavía dependen de lógica tipo dump completo.
- Falta historial persistente completo de backups.
- Falta restauración robusta desde panel.
- Falta descarga controlada desde panel.
- Falta eliminación controlada con dependencias.
- Falta validación avanzada de nombres y rutas.
- Falta gestión clara de secuencias de backups.
- Falta comprobación automática de integridad.
- Falta prueba de restauración programada.

Valor para el producto:

Crítico.

Decisión inicial:

Migrar, pero tratarlo como el módulo principal a revisar antes de cualquier piloto real.

Prioridad de mejora:

Crítica.

---

### 3.6 Módulo de logs

Estado: funcional básico.

Funciones actuales:

- Registro de eventos en base de datos MariaDB.
- Tabla de eventos con fecha, origen, tipo, usuario, IP, recurso, resultado y detalle.
- Middleware de registro automático.
- Vista web para consultar últimos eventos.
- Registro de accesos, backups, servicios y administración.

Limitaciones:

- No hay buscador avanzado.
- No hay filtros completos por tipo, usuario, fecha o resultado.
- No hay paginación.
- No hay exportación.
- No hay clasificación avanzada de eventos.
- Algunos eventos HTTP pueden generar ruido.
- No hay retención ni archivado de logs.

Valor para el producto:

Alto.

Decisión inicial:

Migrar y mejorar con filtros, buscador y paginación.

Prioridad de mejora:

Alta.

---

### 3.7 Módulo de servicios

Estado: funcional básico.

Funciones actuales:

- Listado de servicios remotos.
- Acciones start, stop y restart.
- Uso de systemctl.
- Ejecución mediante SSH.
- Script servicios_api.sh.
- Integración con permisos del panel.

Limitaciones:

- No hay lista blanca estricta de servicios permitidos.
- Riesgo si se permite controlar demasiados servicios.
- Depende de sudoers en la máquina remota.
- Los mensajes de error pueden ser demasiado técnicos.
- Falta separar servicios críticos y no críticos.
- Falta confirmación para acciones peligrosas.

Valor para el producto:

Medio-alto.

Decisión inicial:

Migrar con restricciones más claras.

Prioridad de mejora:

Media-alta.

---

### 3.8 Alertas

Estado: parcial o en evolución.

Funciones previstas o parcialmente trabajadas:

- Alertas por Telegram.
- Variables de configuración para bot de Telegram.
- Posible base SQLite para reglas, destinatarios y entregas.
- Reglas de alerta para backups, servicios y errores.

Limitaciones:

- Debe revisarse qué parte está realmente integrada en la rama final.
- Deben evitarse tokens reales.
- Falta flujo claro de alta de destinatarios.
- Falta validación completa de envío.
- Falta separar configuración sensible.

Valor para el producto:

Alto, pero no imprescindible para la primera migración.

Decisión inicial:

Migrar solo después de revisar bien el estado real del código.

Prioridad de mejora:

Media-alta.

---

### 3.9 Cacti y monitorización

Estado: integración básica.

Funciones actuales:

- Enlace desde el panel hacia Cacti.
- Instaladores mínimos para Cacti.
- Uso como herramienta de monitorización complementaria.

Limitaciones:

- Integración más visual que funcional.
- No hay métricas propias de Cacti integradas dentro del panel.
- No hay correlación directa entre eventos de DASC y métricas de Cacti.
- Puede ser complejo para clientes pequeños.

Valor para el producto:

Medio.

Decisión inicial:

Mantener como módulo opcional, especialmente para DASC Pro.

Prioridad de mejora:

Media.

---

### 3.10 Configuración

Estado: funcional para laboratorio.

Elementos actuales:

- Archivo config.env.
- Variables para SSH.
- Variables para hosts.
- Variables para base de datos de logs.
- Variables para usuario administrador.
- Variables para Telegram.
- Variables para Cacti.

Limitaciones:

- Existen valores por defecto inseguros.
- Puede haber credenciales reales en archivos locales.
- Falta separación clara entre ejemplo y producción.
- Falta validación de configuración al arrancar.
- Falta generación automática de SECRET_KEY segura.
- Falta documentación completa de cada variable.

Valor para el producto:

Crítico.

Decisión inicial:

Usar solo config.env.example en el repositorio producto. Nunca subir config.env real.

Prioridad de mejora:

Crítica.

---

### 3.11 Instaladores y desinstaladores

Estado: funcionales para laboratorio.

Scripts identificados:

- install_dasc_api.sh.
- uninstall_dasc_api.sh.
- install_db.sh.
- uninstall_db.sh.
- install_backup_services.sh.
- uninstall_backup_services.sh.
- install_cacti_min.sh.
- uninstall_cacti.sh.

Funciones actuales:

- Instalación de dependencias.
- Creación de carpetas.
- Copia de archivos.
- Creación de entorno virtual.
- Instalación de requirements.
- Creación de servicio systemd.
- Configuración de MariaDB.
- Configuración de usuario de backups.
- Configuración de SSH.
- Instalación de scripts administrativos.
- Desinstalación básica.

Limitaciones:

- Deben probarse en máquinas limpias.
- Deben adaptarse a perfiles Lite, PyME y Pro.
- Deben mejorar validaciones.
- Deben evitar credenciales por defecto.
- Deben generar logs de instalación.
- Deben ser más idempotentes.
- Deben separar mejor instalación, actualización y rollback.
- Deben pedir solo lo necesario según el paquete elegido.

Valor para el producto:

Crítico.

Decisión inicial:

Migrar después de revisarlos uno por uno.

Prioridad de mejora:

Crítica.

---

### 3.12 Frontend HTML y CSS

Estado: funcional y visualmente aceptable para MVP.

Elementos actuales:

- login.html.
- index.html.
- backups.html.
- logs.html.
- servicios.html.
- admin_users.html.
- Hojas CSS generales y específicas.
- Uso de Font Awesome.
- Plantillas Jinja2.

Funciones actuales:

- Login.
- Panel.
- Vista de backups.
- Vista de logs.
- Vista de servicios.
- Administración de usuarios.
- Menús condicionados por permisos.

Limitaciones:

- Falta revisión responsive.
- Falta unificar estilos.
- Falta separar componentes repetidos.
- Falta plantilla base común.
- Algunas páginas pueden tener código duplicado.
- Falta diseño más orientado a producto final.
- Falta versión móvil cuidada.

Valor para el producto:

Alto.

Decisión inicial:

Migrar lo necesario y crear después una plantilla base común.

Prioridad de mejora:

Media-alta.

---

### 3.13 Docker

Estado: útil para demostración y pruebas.

Funciones actuales o previstas:

- Entorno Docker para reproducir el MVP.
- Contenedores para panel, base de datos, backups, logs y Cacti.
- Uso de docker-compose.
- Redes y volúmenes.
- Simulación de arquitectura multi-servicio.

Limitaciones:

- No debe confundirse con la instalación real en servidores.
- Puede tener diferencias funcionales respecto a la versión multi-servidor.
- Debe mantenerse como entorno de demo o desarrollo.
- Debe evitar incluir secretos.

Valor para el producto:

Medio-alto.

Decisión inicial:

Mantener como entorno de desarrollo y demostración, no como única forma de despliegue.

Prioridad de mejora:

Media.

---

## 4. Archivos que deberían migrarse al repositorio producto

La migración debe hacerse de forma controlada, no copiando todo de golpe.

### Migración recomendada inicial

Archivos o carpetas candidatas:

- main.py.
- requirements.txt.
- templates.
- static.
- install_dasc_api.sh.
- uninstall_dasc_api.sh.
- install_db.sh.
- uninstall_db.sh.
- install_backup_services.sh.
- uninstall_backup_services.sh.
- install_cacti_min.sh.
- uninstall_cacti.sh.
- backups_api.sh.
- servicios_api.sh.

### Archivos que no deben migrarse directamente

- config.env real.
- users.json real.
- logs generados.
- backups generados.
- bases SQLite generadas.
- capturas académicas.
- documentación académica completa.
- tokens.
- credenciales.
- archivos temporales.
- pruebas antiguas sin revisar.

---

## 5. Riesgos detectados

### Riesgos de seguridad

- Contraseñas en texto plano.
- Uso de config.env con secretos.
- Tokens de Telegram si se suben por error.
- SSH entre máquinas.
- sudoers demasiado permisivo.
- Falta de hash de usuarios.
- Falta de control avanzado de sesión.

### Riesgos técnicos

- Código principal demasiado concentrado en main.py.
- Dependencia de rutas absolutas.
- Instaladores todavía orientados a laboratorio.
- Diferencias entre Docker y entorno real.
- Falta de tests automáticos.
- Falta de control de errores avanzado.
- Falta de validación de entradas.

### Riesgos comerciales

- Vender antes de estabilizar backups.
- Prometer restauración avanzada sin validarla.
- No definir límites de responsabilidad.
- No diferenciar claramente Lite, PyME y Pro.
- Asumir soporte ilimitado.
- No calcular costes reales de mantenimiento.

---

## 6. Prioridades técnicas tras el inventario

### Prioridad crítica

- Validar backups completos, incrementales y diferenciales.
- Revisar restauración.
- Separar config.env real de config.env.example.
- Revisar instaladores.
- Eliminar credenciales reales.
- Definir perfiles de instalación Lite, PyME y Pro.
- Mejorar seguridad de usuarios.

### Prioridad alta

- Mejorar logs con filtros y buscador.
- Añadir historial persistente de backups.
- Mejorar gestión de usuarios.
- Revisar permisos.
- Mejorar mensajes de error.
- Documentar instalación real.

### Prioridad media

- Mejorar frontend.
- Mejorar responsive.
- Integrar alertas.
- Mejorar Cacti.
- Preparar Docker como demo estable.
- Crear tests básicos.

### Prioridad baja

- Mejoras visuales avanzadas.
- Integraciones externas.
- Informes PDF.
- Panel móvil completo.
- Multiidioma.

---

## 7. Decisión sobre el estado actual

El código actual es una buena base de MVP, pero no debe considerarse todavía producto final.

La decisión inicial es:

- Usar el código académico como base técnica.
- Migrar solo las partes necesarias.
- Limpiar configuración y secretos.
- Reorganizar el código progresivamente.
- Validar primero los módulos críticos.
- No vender como producto final hasta tener una versión interna estable.

---

## 8. Próxima acción recomendada

Después de este inventario, la siguiente acción técnica será preparar una primera migración controlada del código al repositorio producto.

Orden recomendado:

1. Copiar requirements.txt.
2. Copiar main.py.
3. Copiar templates.
4. Copiar static.
5. Copiar scripts básicos.
6. Copiar instaladores.
7. Revisar rutas.
8. Revisar config.env.example.
9. Probar arranque local.
10. Crear primer tag interno de preparación.

---

## 9. Criterio para cerrar R-004

R-004 se considera finalizada cuando:

- Existe inventario documentado del código actual.
- Se han identificado módulos funcionales.
- Se han identificado limitaciones.
- Se han identificado riesgos.
- Se ha definido qué se puede migrar y qué no.
- Se han marcado prioridades de mejora.
- El documento está subido al repositorio producto.

---

## 10. Conclusión

El MVP académico de DASC Server Manager demuestra que la idea principal funciona: centralizar backups, logs, servicios y administración básica desde un panel web.

Sin embargo, para evolucionar hacia un producto real, es necesario realizar una fase de limpieza, endurecimiento, validación y documentación.

Este inventario permite separar lo que ya aporta valor de lo que todavía debe ser revisado antes de ofrecer el producto a clientes reales.
