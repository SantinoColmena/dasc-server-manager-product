# R-049U - Cierre endurecimiento de credenciales del panel central

## Objetivo

Cerrar la validación del endurecimiento de credenciales del panel central DASC.

## Estado

Cerrada.

## Contexto

El panel central DASC usaba credenciales de laboratorio durante las primeras validaciones:

- admin / admin
- tecnico / tecnico

Esto era válido para laboratorio, pero no para una base de producto.

R-049U evita que esas credenciales sean válidas por defecto y añade una separación clara entre modo laboratorio y modo producto.

## Cambios principales

Se añadió la variable:

- DASC_CENTRAL_LAB_MODE

Valor seguro por defecto:

- false

Con este valor, las credenciales de laboratorio no se aceptan.

Solo se podrían usar si se activa explícitamente:

- DASC_CENTRAL_LAB_MODE=true

## Variables centrales protegidas

El panel central usa:

- DASC_CENTRAL_AUTH_ENABLED
- DASC_CENTRAL_LAB_MODE
- DASC_CENTRAL_SECRET_KEY
- DASC_CENTRAL_ADMIN_USER
- DASC_CENTRAL_ADMIN_PASSWORD
- DASC_CENTRAL_TECH_USER
- DASC_CENTRAL_TECH_PASSWORD

## Cambios en main.py

Se añadió:

- CENTRAL_LAB_MODE
- Credenciales de laboratorio separadas como constantes internas.
- is_default_lab_credential()
- Filtro para ignorar admin/admin y tecnico/tecnico cuando LAB_MODE=false.

También se actualizó el login para enviar al template:

- central_lab_mode
- configured_users_count

## Cambios en el login

El login ya no muestra las credenciales admin/admin ni tecnico/tecnico cuando el modo laboratorio no está activo.

En modo producto muestra un mensaje genérico:

- Credenciales gestionadas mediante variables de entorno del servicio.
- No se muestran usuarios ni contraseñas por seguridad.

## Cambios en el instalador

El instalador de central-support ahora puede generar:

- SECRET_KEY aleatoria.
- Contraseña admin aleatoria.
- Contraseña técnico aleatoria.
- DASC_CENTRAL_LAB_MODE=false.

También conserva config.env si ya existe.

## R-049U-FIX1

Se añadió una capa de seguridad adicional para proteger config.env.

El archivo queda con:

- propietario root:root
- permisos 600

Esto impide que usuarios normales o el usuario del servicio dasc puedan leer o editar directamente el archivo de secretos.

## Validación técnica

Se validó en lab-pruebas:

- Repo actualizado a 3ff82b1.
- main.py central R-049U compila.
- Se hicieron copias de seguridad de main.py, central_login.html y config.env.
- Se copió el nuevo código al directorio instalado.
- config.env se actualizó sin mostrar secretos.
- main.py instalado compila.
- dasc-central-support reinicia correctamente.
- dasc-central-support queda activo.
- /health responde correctamente.

## Validación de permisos

Se comprobó:

- config.env queda como root:root.
- config.env queda con permisos 600.
- Un usuario normal no puede leer config.env.
- El usuario dasc no puede leer config.env directamente.

Resultado:

- OK: usuario normal no puede leer config.env.
- OK: usuario dasc no puede leer config.env.

## Validación de variables no sensibles

Se comprobió sin mostrar secretos:

- DASC_CENTRAL_AUTH_ENABLED=true
- DASC_CENTRAL_LAB_MODE=false
- DASC_CENTRAL_ADMIN_USER=admin
- DASC_CENTRAL_TECH_USER=tecnico

## Validación de login inseguro

Se probó:

- usuario: admin
- contraseña: admin

Resultado:

- HTTP 303
- location: /login?msg=Credenciales+no+validas

Esto confirma que admin/admin queda bloqueado con LAB_MODE=false.

## Validación de login seguro

Se probó login con:

- usuario: admin
- contraseña segura configurada en config.env

Resultado:

- HTTP 303 hacia /
- cookie de sesión creada
- dashboard autenticado con HTTP 200

## Resultado

R-049U queda validada correctamente.

El panel central ya no depende de credenciales de laboratorio por defecto y config.env queda protegido mediante permisos Linux.

## Límites actuales

Esta tarea no implementa todavía:

- Hash de contraseñas.
- Usuarios centrales en base de datos.
- Rotación automática de credenciales.
- Doble factor.
- Bloqueo por intentos fallidos.
- Auditoría de login central.
- Secret manager externo.

## Seguridad real aplicada

La protección principal no es solo DASC_CENTRAL_LAB_MODE.

La protección real queda compuesta por:

- Credenciales fuertes en config.env.
- LAB_MODE=false.
- config.env fuera del repositorio.
- config.env root:root 600.
- Servicio ejecutado como usuario no privilegiado.
- Cambios de credenciales solo con sudo/root.

## Próximas tareas recomendadas

- R-049V - Reverse proxy Nginx para central-support.
- R-049W - Panel visual de cola/sincronización.
- R-049X - Documentación global del soporte central.
- Futuro: usuarios centrales con contraseña hasheada.

## Conclusión

DASC Server Manager supera R-049U.

El panel central queda más alineado con un entorno de producto real: sin credenciales débiles por defecto, con modo laboratorio explícito y con secretos protegidos por permisos del sistema operativo.
