# R-049U-FIX1 - Proteger config.env del panel central

## Objetivo

Proteger el archivo config.env del panel central DASC para que no pueda ser modificado por usuarios normales ni por el usuario de ejecución del servicio.

## Estado

Cerrada.

## Contexto

R-049U endurece las credenciales del panel central evitando que admin/admin y tecnico/tecnico funcionen por defecto.

Sin embargo, la seguridad real no depende solo de DASC_CENTRAL_LAB_MODE.

Si una persona puede modificar config.env, podría cambiar:

- DASC_CENTRAL_LAB_MODE
- DASC_CENTRAL_ADMIN_PASSWORD
- DASC_CENTRAL_TECH_PASSWORD
- DASC_CENTRAL_SECRET_KEY

Por tanto, el archivo de configuración debe protegerse mediante permisos del sistema operativo.

## Decisión aplicada

El instalador deja config.env con:

- propietario root:root
- permisos 600

Comando equivalente:

- chown root:root /opt/dasc/central-support/config.env
- chmod 600 /opt/dasc/central-support/config.env

## Motivo técnico

systemd lee EnvironmentFile como root antes de iniciar el proceso del servicio.

Después, la aplicación se ejecuta como usuario dasc, pero ya recibe las variables de entorno cargadas.

Por tanto, el usuario dasc no necesita poder leer ni editar config.env directamente.

## Beneficio

Esta protección impide que el usuario de servicio pueda modificar su propia configuración sensible.

También obliga a que cualquier cambio de credenciales requiera permisos administrativos.

## Archivos modificados

- deploy/central-support/install_central_support.sh

## Criterio de validación

R-049U-FIX1 se considera preparado cuando:

- install_central_support.sh aplica chown root:root a config.env.
- install_central_support.sh aplica chmod 600 a config.env.
- El servicio dasc-central-support sigue arrancando correctamente.
- /health responde correctamente.
- Login central funciona con credenciales configuradas.
- Un usuario normal no puede leer config.env sin sudo.

## Límites

Esta tarea no cifra config.env.

La protección se basa en permisos Linux y control de acceso al servidor.

Si alguien obtiene root, puede modificar el archivo. En sistemas Linux esto se considera compromiso del servidor.

## Próximo paso

Validar en lab-pruebas.

## Conclusión

R-049U-FIX1 añade una capa de seguridad realista y profesional para proteger los secretos del panel central.
