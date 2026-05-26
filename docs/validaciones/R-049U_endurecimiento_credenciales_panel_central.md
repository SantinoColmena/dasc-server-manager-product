# R-049U - Endurecimiento de credenciales del panel central

## Objetivo

Endurecer la autenticación del panel central DASC para que las credenciales de laboratorio no sean válidas por defecto en un entorno de producto.

## Estado

Cerrada.

## Problema detectado

Antes de R-049U, el panel central podía usar credenciales por defecto:

- admin / admin
- tecnico / tecnico

Además, el login mostraba explícitamente esas credenciales como ayuda de laboratorio.

Esto era aceptable durante la validación inicial, pero no es adecuado para una base de producto.

## Decisión aplicada

Se añade una variable explícita:

- DASC_CENTRAL_LAB_MODE

Valor seguro por defecto:

- false

Con este valor, las credenciales admin/admin y tecnico/tecnico no se aceptan aunque estén como valores por defecto.

## Modo laboratorio

Solo si se configura:

- DASC_CENTRAL_LAB_MODE=true

pueden usarse credenciales de laboratorio.

Esto permite conservar pruebas rápidas, pero evita que el comportamiento inseguro sea el valor normal.

## Variables implicadas

- DASC_CENTRAL_AUTH_ENABLED
- DASC_CENTRAL_LAB_MODE
- DASC_CENTRAL_SECRET_KEY
- DASC_CENTRAL_ADMIN_USER
- DASC_CENTRAL_ADMIN_PASSWORD
- DASC_CENTRAL_TECH_USER
- DASC_CENTRAL_TECH_PASSWORD

## Cambios en main.py

Se añade:

- CENTRAL_LAB_MODE
- DEFAULT_LAB_ADMIN_USER
- DEFAULT_LAB_ADMIN_PASSWORD
- DEFAULT_LAB_TECH_USER
- DEFAULT_LAB_TECH_PASSWORD
- is_default_lab_credential()

Se modifica get_central_users para ignorar credenciales de laboratorio si el modo laboratorio no está activo.

## Cambios en el login

El login deja de mostrar admin/admin o tecnico/tecnico cuando no está activo el modo laboratorio.

Si no hay usuarios centrales configurados, muestra aviso para revisar config.env.

## Cambios en instalador

El instalador ahora detecta si config.env no existe, está vacío o no contiene DASC_CENTRAL_SECRET_KEY.

En ese caso genera:

- SECRET_KEY aleatoria.
- Password admin aleatoria.
- Password técnico aleatoria.
- DASC_CENTRAL_LAB_MODE=false.

## Criterio de validación

R-049U se considera preparada cuando:

- main.py central compila.
- central_login.html no muestra credenciales por defecto en modo producto.
- install_central_support.sh no genera admin/admin ni tecnico/tecnico por defecto.
- DASC_CENTRAL_LAB_MODE=false bloquea admin/admin.
- Credenciales fuertes configuradas en config.env permiten login.
- dasc-central-support reinicia correctamente.
- Dashboard central sigue cargando.
- Detalle de ticket central sigue cargando.

## Límites

Esta tarea no implementa todavía:

- Hash de contraseñas.
- Usuarios centrales en base de datos.
- Rotación automática de credenciales.
- Doble factor.
- Bloqueo por intentos fallidos.
- Auditoría de login central.

## Próximo paso

Validar en lab-pruebas.

## Conclusión

R-049U reduce el riesgo de dejar credenciales de laboratorio activas en un despliegue real del panel central.
