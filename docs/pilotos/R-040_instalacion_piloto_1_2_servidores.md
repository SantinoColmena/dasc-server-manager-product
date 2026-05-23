# R-040 - Instalación piloto 1 en perfil 2 servidores

## Objetivo

Ejecutar el primer piloto técnico de DASC Server Manager usando el perfil PyME de 2 servidores.

El objetivo no es vender todavía el producto como definitivo, sino validar que DASC puede instalarse, configurarse y probarse fuera del laboratorio académico principal de forma controlada.

## Tipo de piloto

Piloto técnico controlado.

## Arquitectura prevista

Perfil: DASC PyME - 2 servidores.

| Servidor | Función | Estado |
|---|---|---|
| Servidor cliente | Base de datos o servicio a proteger | Pendiente |
| Servidor DASC | Panel, backups, logs y validación | Pendiente |

## Condiciones del piloto

- No usar datos críticos reales sin autorización.
- No prometer soporte 24/7.
- No usar contraseñas por defecto.
- No exponer MySQL a Internet.
- Guardar evidencias técnicas.
- Validar backup y restauración en entorno seguro.
- Registrar incidencias y tiempos reales.

## Alcance mínimo

| Área | Validación esperada | Estado |
|---|---|---|
| Instalación | DASC instalado en perfil 2 servidores | Pendiente |
| Acceso | Login correcto e incorrecto probado | Pendiente |
| Usuarios | Admin y usuario limitado creados | Pendiente |
| Backups | Backup completo funcional | Pendiente |
| Logs | Eventos registrados en el panel | Pendiente |
| Servicios | Servicio visualizado o acción controlada | Pendiente |
| Alertas | Alerta real o simulada probada | Pendiente |
| Restauración | Restauración segura o validación equivalente | Pendiente |
| Evidencias | Capturas y comandos guardados | Pendiente |
| Feedback | Dudas, errores y mejoras registradas | Pendiente |

## Criterio de salida

R-040 se considera completada cuando:

- El panel está accesible.
- Existe al menos un backup válido.
- Los logs registran actividad.
- Existe una prueba de restauración o validación equivalente.
- Se han configurado permisos básicos.
- Se han guardado evidencias.
- Se ha documentado cualquier incidencia detectada.

## Estado

Documentado: Sí  
Implementado: Pendiente  
Validado: Pendiente  
