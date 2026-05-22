# R-030 - Asistente de instalación por perfil

## Objetivo

Crear una primera herramienta que permita seleccionar un perfil de despliegue y generar un archivo `config.env` base a partir de las plantillas existentes.

## Archivo creado

- scripts/generar_config_perfil.sh

## Perfiles soportados

| Opción | Perfil | Archivo origen |
|---|---|---|
| 1 | single / Lite | config/perfiles/config.single.env.example |
| 2 | dual / PyME | config/perfiles/config.dual.env.example |
| 3 | distributed / Pro | config/perfiles/config.distributed.env.example |

## Funcionamiento esperado

El script puede ejecutarse de forma interactiva:

~~~bash
bash scripts/generar_config_perfil.sh
~~~

O indicando el perfil directamente:

~~~bash
bash scripts/generar_config_perfil.sh single
bash scripts/generar_config_perfil.sh dual
bash scripts/generar_config_perfil.sh distributed
~~~

## Resultado esperado

El script genera un archivo:

~~~text
config.env
~~~

Si ya existe un `config.env`, crea antes una copia de seguridad con fecha y hora.

## Decisión técnica

En esta fase no se modifica todavía el instalador real de API, DB o Backups.

Primero se crea un asistente independiente para reducir riesgo y validar la lógica de perfiles antes de integrarla en los instaladores definitivos.

## Estado

R-030 queda implementada como primera versión funcional del asistente de perfil.

Queda pendiente probarlo en una máquina Ubuntu y después integrarlo en el flujo real de instalación.
