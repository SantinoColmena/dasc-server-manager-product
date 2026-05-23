# R-035 - Base de conocimiento inicial

## Objetivo

Crear una base de conocimiento inicial para DASC Server Manager que sirva como referencia para soporte, mantenimiento, demostraciones, resolución de dudas y futuras integraciones con ayuda guiada o IA.

Esta base de conocimiento recoge preguntas frecuentes, errores habituales, procedimientos básicos y criterios de actuación.

## Uso previsto

Este documento puede usarse para:

- Resolver dudas básicas del cliente.
- Preparar respuestas de soporte.
- Documentar errores conocidos.
- Guiar a un técnico durante una instalación.
- Servir como fuente inicial para un asistente de ayuda.
- Mantener coherencia en futuras demos y pilotos.

## 1. Conceptos básicos

### ¿Qué es DASC Server Manager?

DASC Server Manager es un panel web orientado a pequeñas y medianas empresas que permite centralizar tareas relacionadas con copias de seguridad, logs, servicios, alertas y usuarios.

Su objetivo es facilitar el control del estado del sistema sin obligar al cliente a manejar directamente comandos complejos.

### ¿Qué problema resuelve?

DASC ayuda a resolver problemas habituales como:

- Backups realizados manualmente.
- Falta de comprobación de copias.
- Ausencia de logs claros.
- Dependencia de una persona concreta.
- Falta de alertas ante errores.
- Dificultad para saber si una restauración es posible.

### ¿DASC es solo un software?

No. La visión recomendada es ofrecer DASC como producto-servicio: instalación, configuración, revisión, soporte, alertas, pruebas de restauración e informes.

## 2. Módulos principales

### Panel principal

Muestra los accesos disponibles para el usuario autenticado.

### Copias de seguridad

Permite ejecutar y revisar backups.

Tipos principales:

- Completo.
- Incremental.
- Diferencial.

### Logs

Registra eventos importantes del sistema:

- Accesos.
- Acciones de usuarios.
- Operaciones de backup.
- Errores.
- Acciones sobre servicios.

### Servicios

Permite revisar o gestionar servicios del sistema, según permisos.

### Alertas

Permite avisar ante eventos importantes, como errores de backup o fallos críticos.

### Usuarios y permisos

Permite limitar qué puede ver o hacer cada usuario dentro del panel.

## 3. Preguntas frecuentes

### ¿Puedo usar DASC sin conocimientos técnicos?

Sí, el panel está pensado para simplificar tareas. Aun así, acciones delicadas como restauraciones o cambios de servicios deberían realizarse con soporte técnico.

### ¿Dónde se guardan las copias?

Depende de la instalación. En laboratorio pueden guardarse en una ruta local como `/home/dasc/backups`. En cliente real debe definirse una ubicación segura y, si es posible, una copia externa.

### ¿Qué tipo de backup debo usar?

- Completo: recomendado como base principal.
- Incremental: útil para guardar cambios desde la última copia.
- Diferencial: útil para guardar cambios desde la última copia completa.

### ¿Qué pasa si una copia falla?

El error debe quedar registrado en logs y, si las alertas están configuradas, debe enviarse un aviso.

### ¿Puede DASC restaurar datos?

Sí, pero la restauración debe hacerse con cuidado. En entornos reales se recomienda validar primero en un entorno seguro.

### ¿DASC sustituye a un administrador de sistemas?

No completamente. DASC ayuda a centralizar y automatizar tareas, pero no sustituye la revisión técnica en situaciones críticas.

### ¿Los datos salen a la nube?

No obligatoriamente. DASC está pensado para funcionar en local. Puede añadirse copia externa si el cliente lo necesita.

## 4. Errores habituales y actuación

### No puedo acceder al panel

Comprobar:

1. Que el servidor está encendido.
2. Que el servicio `dasc-api` está activo.
3. Que la URL es correcta.
4. Que el puerto 8000 está accesible.
5. Que el usuario y contraseña son correctos.

### El login falla

Posibles causas:

- Usuario incorrecto.
- Contraseña incorrecta.
- Usuario no creado.
- Problema con el archivo de usuarios.
- Configuración incorrecta en `config.env`.

Actuación:

1. Probar con usuario administrador.
2. Revisar usuarios creados.
3. Revisar logs del panel.
4. No mostrar contraseñas en capturas.

### No se ejecuta un backup

Posibles causas:

- Fallo de conexión con la base de datos.
- Credenciales incorrectas.
- Usuario de backup sin permisos.
- Ruta de destino inexistente.
- Falta de espacio en disco.
- Error en el script `backups_api.sh`.

Actuación:

1. Revisar mensaje de error.
2. Validar conexión a base de datos.
3. Probar `mysqldump`.
4. Revisar permisos de carpeta destino.
5. Revisar logs.

### No aparecen logs

Posibles causas:

- Base de datos de logs no disponible.
- Credenciales incorrectas.
- Tabla de eventos no creada.
- Problema de red entre panel y servidor de logs.
- Error en la función de registro.

Actuación:

1. Comprobar servicio de base de datos.
2. Validar conexión a `dasc_logs`.
3. Revisar configuración `LOGS_DB_HOST`.
4. Comprobar tabla `eventos`.

### No funcionan las acciones de servicios

Posibles causas:

- SSH no configurado.
- Clave SSH no copiada.
- Usuario sin permisos sudo.
- Script `servicios_api.sh` no instalado.
- Servicio solicitado inexistente.

Actuación:

1. Probar conexión SSH.
2. Validar existencia del script remoto.
3. Revisar sudoers.
4. Probar acción manual controlada.

### No llegan alertas

Posibles causas:

- Token incorrecto.
- Chat ID incorrecto.
- Bot no iniciado por el usuario.
- Sin conexión a Internet.
- Canal de alertas desactivado.

Actuación:

1. Revisar configuración.
2. Probar envío manual.
3. Comprobar destinatarios.
4. No publicar tokens en capturas ni repositorios.

## 5. Buenas prácticas de soporte

### Antes de tocar el sistema

- Preguntar qué acción se realizó.
- Pedir hora aproximada del fallo.
- Revisar logs.
- Confirmar si hay backup reciente.
- No ejecutar restauraciones sin autorización.
- No borrar copias sin confirmar alternativas.

### Durante una incidencia

Registrar:

- Fecha y hora.
- Usuario afectado.
- Módulo afectado.
- Acción realizada.
- Mensaje de error.
- Solución aplicada.

### Después de resolver

- Documentar causa.
- Documentar solución.
- Añadir el caso a esta base de conocimiento si puede repetirse.
- Validar que el sistema vuelve a funcionar.
- Informar al cliente con lenguaje sencillo.

## 6. Criterios de prioridad

| Prioridad | Caso | Actuación |
|---|---|---|
| Alta | No hay backups recientes | Revisar inmediatamente |
| Alta | Restauración necesaria | Validar con soporte técnico |
| Alta | Error crítico de base de datos | Escalar a técnico |
| Media | Error puntual de alerta | Revisar configuración |
| Media | Usuario no puede acceder | Revisar credenciales/permisos |
| Baja | Duda de uso | Responder con manual rápido |

## 7. Respuestas tipo para soporte

### Respuesta ante fallo de backup

Hemos detectado que la copia no se ha completado correctamente. Vamos a revisar la conexión con la base de datos, los permisos del usuario de backup y el espacio disponible en el servidor de destino.

### Respuesta ante duda de restauración

La restauración puede sobrescribir datos actuales, por eso recomendamos validarla primero en un entorno seguro o realizarla con supervisión técnica.

### Respuesta ante duda sobre copias externas

La copia externa sirve para proteger los datos si el servidor principal falla. Puede configurarse en un NAS, servidor SFTP o almacenamiento externo cifrado.

### Respuesta ante error de acceso

Vamos a revisar si el usuario existe, si tiene permisos correctos y si el panel está registrando el intento en logs.

## 8. Relación con otros documentos

Esta base de conocimiento se relaciona con:

- `docs/cliente/R-034_manual_rapido_cliente.md`
- `docs/cliente/R-038_checklist_instalacion_cliente.md`
- `docs/comercial/R-037_guion_llamada_demo.md`
- `docs/demo/R-032_modo_demo_sin_datos_sensibles.md`

## Estado

Documentado: Sí  
Implementado: No aplica  
Validado: Pendiente de revisión durante una demo o piloto
