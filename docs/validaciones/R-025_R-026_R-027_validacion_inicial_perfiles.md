# R-025 / R-026 / R-027 - Validación inicial de perfiles

## Objetivo

Comprobar que la Fase 3 empieza con una base clara para los tres perfiles de despliegue:

- single / Lite
- dual / PyME
- distributed / Pro

## Archivos revisados

- config/perfiles/config.single.env.example
- config/perfiles/config.dual.env.example
- config/perfiles/config.distributed.env.example
- docs/tecnico/fase_3_despliegues_adaptables.md

## Validación de perfil single

El perfil single define todos los servicios en 127.0.0.1.

Este modo representa una instalación de bajo coste en un único servidor.

Resultado esperado:

- Panel local.
- Base de datos local.
- Logs locales.
- Backups locales.
- Copia externa obligatoria.

Estado: documentado.

## Validación de perfil dual

El perfil dual separa el servidor principal del nodo DASC.

Resultado esperado:

- Servidor principal con base de datos o servicios del cliente.
- Servidor DASC con backups, logs, alertas y panel.
- Mejor equilibrio entre coste y seguridad.

Estado: documentado.

## Validación de perfil distributed

El perfil distributed mantiene la arquitectura validada en laboratorio real.

Resultado esperado:

- API / Panel separado.
- Base de datos separada.
- Backups y servicios separados.

Estado: documentado.

## Pendiente de validación real

Queda pendiente probar cada perfil en laboratorio:

- Instalación single.
- Instalación dual.
- Instalación distributed tras los cambios.
- Copia externa mediante directorio montado, NAS o SFTP.
- Futuro asistente de instalación por perfil.

## Conclusión

La Fase 3 queda iniciada correctamente a nivel de estructura, perfiles y documentación base.

El siguiente paso técnico será adaptar el instalador para que pueda seleccionar o aplicar un perfil de instalación.
