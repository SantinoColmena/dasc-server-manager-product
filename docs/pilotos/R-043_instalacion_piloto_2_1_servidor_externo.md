# R-043 - Instalación piloto 2 en perfil 1 servidor + externo

## Objetivo

Ejecutar el segundo piloto técnico de DASC Server Manager usando el perfil Lite de 1 servidor más copia externa.

La finalidad es comprobar si DASC puede funcionar en una arquitectura más económica y sencilla que el perfil PyME de 2 servidores, pensada para microempresas o entornos con menos presupuesto.

## Tipo de piloto

Piloto técnico controlado.

## Arquitectura prevista

Perfil: DASC Lite - 1 servidor + copia externa.

| Componente | Ubicación | Estado |
|---|---|---|
| Panel DASC | Mismo servidor | Pendiente |
| Base de datos MariaDB | Mismo servidor | Pendiente |
| Backups locales | Mismo servidor | Pendiente |
| Logs | Mismo servidor | Pendiente |
| Copia externa | Carpeta externa simulada o destino adicional | Pendiente |

## Máquina prevista

| Campo | Valor |
|---|---|
| Hostname | piloto-lite |
| IP propuesta | 192.168.60.40 |
| Sistema operativo | Ubuntu Server |
| Perfil | 1 servidor + externo |
| Base de datos protegida | employees |
| Ruta backups locales | /home/dasc/backups |
| Ruta copia externa simulada | /home/dasc/external-backups |

## Alcance mínimo

| Área | Validación esperada | Estado |
|---|---|---|
| Instalación | DASC instalado en 1 servidor | Pendiente |
| Base de datos | MariaDB local funcional | Pendiente |
| Backups | Backup local funcional | Pendiente |
| Copia externa | Copia adicional simulada | Pendiente |
| Logs | Eventos registrados | Pendiente |
| Panel | Acceso web validado | Pendiente |
| Servicios | Listado o acción controlada | Pendiente |
| Terminal | Terminal local validada | Pendiente |
| Evidencias | Capturas y comandos guardados | Pendiente |
| Incidencias | Problemas registrados | Pendiente |

## Diferencia respecto al piloto 1

El piloto 1 validó una arquitectura de 2 servidores.

Este piloto valida una arquitectura más sencilla, donde DASC se ejecuta en una única máquina y la copia externa se simula mediante un destino separado.

## Condiciones del piloto

- No usar datos reales críticos.
- No exponer MariaDB a Internet.
- No vender este perfil como máxima seguridad.
- Indicar que la copia externa es obligatoria para que el perfil Lite sea aceptable.
- Registrar cualquier limitación frente al perfil de 2 servidores.

## Criterio de salida

R-043 se considera completada cuando:

- El panel está accesible.
- MariaDB funciona en la misma máquina.
- Se genera al menos un backup local.
- Existe una copia externa simulada.
- Los logs registran actividad.
- Se documentan limitaciones del perfil Lite.
- Se registran incidencias detectadas.

## Estado

Documentado: Sí  
Implementado: Pendiente  
Validado: Pendiente  
