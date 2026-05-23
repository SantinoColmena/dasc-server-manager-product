# R-037 - Guion de llamada y demo comercial

## Objetivo

Preparar un guion sencillo para presentar DASC Server Manager a un posible cliente, explicar el problema que resuelve y enseñar una demo breve del producto.

Este guion está pensado para una PyME que no tiene personal técnico especializado y necesita controlar mejor sus copias de seguridad, logs, servicios y alertas.

## Duración recomendada

Duración total recomendada: 10 a 15 minutos.

Distribución:

| Parte | Tiempo aproximado |
|---|---|
| Presentación inicial | 1 minuto |
| Problema del cliente | 2 minutos |
| Propuesta de DASC | 2 minutos |
| Demo del panel | 5 a 7 minutos |
| Cierre y siguientes pasos | 2 minutos |

## 1. Inicio de la llamada

Texto recomendado:

Buenos días, soy del equipo de DASC Server Manager. La idea de esta llamada es enseñarte una solución pensada para pequeñas y medianas empresas que necesitan controlar sus copias de seguridad, revisar logs y tener una visión sencilla del estado de sus servicios sin depender de procesos manuales.

No queremos venderte una herramienta complicada, sino enseñarte cómo podrías tener más control sobre tus datos y saber si tus backups realmente se están realizando.

## 2. Preguntas iniciales al cliente

Antes de enseñar la demo, hacer preguntas sencillas:

- ¿Actualmente hacéis copias de seguridad?
- ¿Cada cuánto se realizan?
- ¿Sabéis si las copias se pueden restaurar correctamente?
- ¿Quién revisa si una copia ha fallado?
- ¿Tenéis algún sistema de alertas?
- ¿Guardáis logs de acciones importantes?
- ¿Dependéis de una persona concreta para revisar todo esto?

## 3. Problema que resuelve DASC

Explicación recomendada:

Muchas empresas pequeñas tienen copias de seguridad, pero no siempre saben si están funcionando correctamente. A veces los backups existen, pero nadie revisa si se han generado bien o si se pueden restaurar.

También es habitual que las acciones se hagan manualmente, que no quede registro claro de quién hizo cada operación y que los errores se detecten tarde.

DASC Server Manager intenta resolver ese problema centralizando en un panel las copias, los logs, los servicios y las alertas.

## 4. Propuesta de valor

Texto recomendado:

DASC no busca sustituir a herramientas empresariales muy grandes. Su objetivo es ser una solución sencilla, local y mantenida para PYMES.

La propuesta es:

- Backups controlados desde panel.
- Historial de copias.
- Logs de actividad.
- Alertas ante errores.
- Gestión básica de servicios.
- Usuarios con permisos.
- Instalación y mantenimiento por parte del proveedor.
- Posibilidad de copia externa para mayor seguridad.

El cliente no paga solo por el software, sino por tener una instalación revisada, documentada y con soporte.

## 5. Demo del panel

### Paso 1 - Login

Mostrar la pantalla de login.

Explicación:

Aquí el usuario accede con sus credenciales. Cada usuario puede tener permisos diferentes, así evitamos que todos tengan acceso a funciones administrativas.

### Paso 2 - Panel principal

Mostrar el dashboard.

Explicación:

Desde esta pantalla se ven los módulos disponibles: copias, logs, servicios y administración. Cada usuario ve únicamente lo que tiene permitido.

### Paso 3 - Copias de seguridad

Entrar en Copias.

Explicación:

Desde aquí se puede lanzar una copia manual. El sistema permite trabajar con copias completas, incrementales y diferenciales, según la configuración del entorno.

Durante la demo se puede lanzar una copia de prueba sobre una base de datos de laboratorio.

### Paso 4 - Resultado del backup

Mostrar el mensaje de resultado.

Explicación:

El objetivo no es solo lanzar una copia, sino comprobar que existe un resultado claro y que la acción queda registrada.

### Paso 5 - Logs

Entrar en Logs.

Explicación:

Aquí se muestra la trazabilidad del sistema. Podemos ver accesos, acciones realizadas, resultados correctos o errores, usuario, recurso afectado y fecha.

Esto ayuda a saber qué ha pasado y cuándo.

### Paso 6 - Servicios

Entrar en Servicios.

Explicación:

Desde esta sección se puede revisar el estado de servicios y, según permisos, realizar acciones como iniciar, detener o reiniciar.

En un cliente real, estas acciones deben limitarse a usuarios autorizados.

### Paso 7 - Alertas

Explicar el módulo de alertas.

Texto recomendado:

El sistema puede enviar avisos cuando se produce un evento importante, por ejemplo un error de backup o una incidencia crítica. La idea es que el cliente no tenga que entrar todos los días al panel para descubrir que algo ha fallado.

## 6. Arquitecturas que se pueden ofrecer

Explicar las tres opciones:

| Opción | Descripción | Cliente recomendado |
|---|---|---|
| DASC Lite | 1 servidor con copia externa obligatoria | Microempresa o prueba inicial |
| DASC PyME | 2 servidores o servidor + nodo de backups | Opción recomendada para PyME |
| DASC Pro | 3 servidores separados | Empresa con más necesidad de separación |

Texto recomendado:

Para una PyME, la opción más equilibrada suele ser la de 2 servidores: un servidor principal y otro nodo para DASC, backups o logs. Así las copias no dependen totalmente del mismo equipo donde están los datos principales.

## 7. Cierre de la demo

Texto recomendado:

La idea de DASC Server Manager es dar tranquilidad. No se trata solo de hacer backups, sino de saber si existen, si han funcionado, si se pueden revisar y si hay alertas cuando algo falla.

El siguiente paso sería revisar vuestro entorno real, ver qué base de datos o servicios queréis proteger y preparar una instalación piloto controlada.

## 8. Posibles preguntas del cliente

### ¿Esto sustituye a un técnico?

No. DASC ayuda a reducir tareas manuales y a centralizar información, pero no sustituye totalmente a un responsable técnico. La ventaja es que facilita el mantenimiento y permite que el proveedor revise el sistema de forma más clara.

### ¿Mis datos salen a la nube?

No obligatoriamente. DASC está pensado para funcionar en local. Se puede añadir copia externa si el cliente lo necesita, por ejemplo en NAS, SFTP o almacenamiento externo cifrado.

### ¿Qué pasa si falla un backup?

El error queda registrado en logs y puede generar una alerta. Después se revisa la causa y se corrige.

### ¿Puedo restaurar una copia?

Sí, pero la restauración debe hacerse con cuidado. En entornos reales se recomienda validarla con soporte técnico para evitar sobrescribir datos importantes.

### ¿Es una herramienta para empresas grandes?

No es el objetivo inicial. DASC está pensado especialmente para microempresas y PYMES que necesitan una solución más sencilla y acompañada.

## 9. Siguientes pasos después de la llamada

Después de una llamada/demo, se recomienda:

1. Enviar resumen al cliente.
2. Pedir información técnica mínima.
3. Elegir arquitectura: Lite, PyME o Pro.
4. Preparar checklist de instalación.
5. Definir alcance del piloto.
6. Acordar fecha de instalación.
7. Validar backup y restauración de prueba.
8. Entregar manual rápido.

## Estado

Documentado: Sí  
Implementado: No aplica  
Validado: Pendiente de usar en una demo real o simulada
