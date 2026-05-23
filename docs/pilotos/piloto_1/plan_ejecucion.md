# Plan de ejecución - Piloto 1

## Objetivo

Ejecutar el primer piloto técnico de DASC Server Manager en perfil PyME de 2 servidores.

La finalidad es comprobar si el producto puede instalarse y validarse en un entorno parecido al de una pequeña empresa, separando el servidor que contiene los datos del servidor que gestiona el panel, backups, logs y validaciones.

## Arquitectura usada

| Servidor | Función | IP propuesta |
|---|---|---|
| Servidor cliente | MariaDB con base de datos employees | 192.168.60.20 |
| Servidor DASC | Panel, backups, servicios y validación | 192.168.60.30 |

## Orden de ejecución

1. Preparar servidor cliente.
2. Instalar MariaDB y base de datos de prueba.
3. Crear usuario de backup limitado.
4. Preparar servidor DASC.
5. Instalar scripts de backups y servicios.
6. Instalar panel DASC.
7. Validar acceso web.
8. Ejecutar backup completo.
9. Comprobar archivo generado.
10. Validar logs.
11. Probar usuario limitado.
12. Probar restauración o validación equivalente.
13. Registrar incidencias.
14. Cerrar R-040.

## Bloque 1 - Servidor cliente

Máquina esperada:

- Ubuntu Server.
- IP propuesta: 192.168.60.20.
- MariaDB instalado.
- Base de datos: employees.
- Usuario de backup: dasc_backup.
- Acceso permitido desde servidor DASC.

Acciones previstas:

    sudo apt update
    sudo apt install -y git
    git clone https://github.com/SantinoColmena/dasc-server-manager-product.git
    cd dasc-server-manager-product
    sudo bash install_db.sh

Resultado esperado:

- MariaDB activo.
- Puerto 3306 escuchando.
- Base de datos employees creada.
- Usuario dasc_backup creado.
- Servidor DASC autorizado para hacer backups.

## Bloque 2 - Servidor DASC

Máquina esperada:

- Ubuntu Server.
- IP propuesta: 192.168.60.30.
- SSH activo.
- Usuario dasc preparado.
- Scripts administrativos instalados.
- Panel DASC instalado en /opt/dasc/api.

Acciones previstas:

    sudo apt update
    sudo apt install -y git
    git clone https://github.com/SantinoColmena/dasc-server-manager-product.git
    cd dasc-server-manager-product
    sudo bash install_backup_services.sh
    sudo bash install_dasc_api.sh

Resultado esperado:

- Usuario dasc creado.
- Scripts backups_api.sh y servicios_api.sh instalados.
- Servicio dasc-api activo.
- Panel accesible por navegador.
- Comunicación SSH preparada.

## Bloque 3 - Validación funcional

Pruebas mínimas:

| Prueba | Resultado esperado |
|---|---|
| Acceso al panel | Login correcto |
| Login incorrecto | Error controlado |
| Usuario limitado | Solo ve permisos asignados |
| Backup completo | Archivo generado |
| Logs | Eventos visibles |
| Servicios | Listado o acción controlada |
| Restauración | Prueba segura o equivalente |
| Alertas | Alerta real o simulada |

## Bloque 4 - Evidencias

Se guardarán capturas de:

- Panel accesible.
- Login correcto.
- Usuario limitado.
- Backup ejecutado.
- Archivo generado en disco.
- Logs registrados.
- Restauración o validación equivalente.
- Alerta real o simulada.
- Estado de servicios systemd.

## Criterio de cierre

El piloto 1 se considera ejecutado correctamente si:

- DASC se instala en el servidor previsto.
- El panel arranca como servicio.
- El backup completo funciona.
- Los logs registran actividad.
- Existe prueba de usuario con permisos limitados.
- Existe restauración o validación equivalente.
- Las incidencias quedan documentadas.
