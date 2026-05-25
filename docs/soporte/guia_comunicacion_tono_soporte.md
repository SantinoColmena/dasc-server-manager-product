# Guía de comunicación y tono de soporte - DASC Server Manager

## Objetivo

Definir cómo debe comunicarse el equipo DASC con clientes PyME durante incidencias, consultas, mantenimientos y solicitudes de soporte.

El objetivo es mantener una comunicación profesional, clara y cercana, sin obligar al cliente a entender detalles técnicos internos.

## Principios generales

La comunicación de soporte DASC debe ser:

- Clara.
- Profesional.
- Tranquila.
- Respetuosa.
- Orientada a solución.
- Sin culpar al cliente.
- Sin exceso de tecnicismos.
- Con próximos pasos concretos.
- Con evidencias cuando se cierre un caso.

## Tono recomendado

El tono debe ser cercano pero profesional.

Ejemplo recomendado:

~~~text
Hemos revisado el servicio y actualmente responde correctamente. Vamos a seguir comprobando los logs para confirmar si hubo algún fallo puntual.
~~~

Evitar:

~~~text
Eso no es un fallo, es normal.
~~~

Mejor:

~~~text
La redirección al login es el comportamiento esperado cuando no hay una sesión iniciada.
~~~

## Qué debe incluir una buena respuesta

Siempre que sea posible, una respuesta debe incluir:

| Elemento | Descripción |
|---|---|
| Confirmación | Indicar que se ha recibido o revisado la solicitud |
| Estado | Explicar si está en análisis, resuelta o pendiente |
| Acción | Decir qué se ha hecho o qué se hará |
| Próximo paso | Indicar qué ocurrirá después |
| Evidencia | Añadir resultado verificable cuando se cierre |

## Qué evitar

El equipo DASC debe evitar:

- Respuestas demasiado técnicas.
- Culpabilizar al cliente.
- Decir solo “funciona” sin evidencia.
- Usar frases ambiguas.
- Prometer tiempos imposibles.
- Pedir al cliente que use GitHub.
- Pedir al cliente que edite scripts.
- Pedir al cliente que toque `config.env`.
- Pedir al cliente que ejecute restauraciones solo.

## Cómo explicar incidencias técnicas

Cuando exista un problema técnico, se debe traducir a lenguaje comprensible.

Ejemplo técnico interno:

~~~text
Access denied for user 'dasc_logs'@'192.168.60.10'
~~~

Comunicación al cliente:

~~~text
Hemos detectado un problema de permisos en el registro de eventos. El panel seguía funcionando, pero algunos eventos no se estaban guardando correctamente. Ya hemos ajustado la configuración y confirmado que los eventos vuelven a registrarse.
~~~

## Cómo explicar una caída

Evitar:

~~~text
El servicio estaba caído por un problema en systemd.
~~~

Mejor:

~~~text
Hemos detectado que el servicio del panel no estaba respondiendo correctamente. Lo hemos reiniciado, comprobado y ahora vuelve a estar operativo.
~~~

## Cómo explicar una restauración

Las restauraciones deben comunicarse con especial cuidado.

Debe indicarse:

- Qué se va a restaurar.
- Desde qué fecha aproximada.
- Si puede sobrescribir datos actuales.
- Cuándo se realizará.
- Cómo se validará después.

Ejemplo:

~~~text
Antes de iniciar la restauración necesitamos confirmar que queréis recuperar los datos desde la copia del día indicado. Esta acción puede sustituir datos actuales, por lo que no la ejecutaremos hasta recibir confirmación.
~~~

## Cómo responder por prioridad

### Prioridad crítica

Tono:

- Directo.
- Rápido.
- Tranquilo.
- Sin promesas exageradas.

Ejemplo:

~~~text
Hemos recibido la incidencia crítica y la estamos revisando con prioridad. Vamos a comprobar el estado de los servicios principales y os informaremos con el diagnóstico inicial lo antes posible.
~~~

### Prioridad alta

Ejemplo:

~~~text
Hemos registrado la incidencia con prioridad alta. Estamos revisando el servicio afectado y os actualizaremos cuando tengamos el primer diagnóstico.
~~~

### Prioridad media

Ejemplo:

~~~text
Hemos registrado la solicitud y la revisaremos dentro del flujo habitual de soporte. Si necesitamos más información, os la pediremos por este mismo canal.
~~~

### Prioridad baja

Ejemplo:

~~~text
Hemos recibido la consulta. La revisaremos y os responderemos con la información o recomendación correspondiente.
~~~

## Comunicación por canal

### Email

Debe ser el canal principal.

Permite:

- Respuestas completas.
- Evidencias.
- Resumen de acciones.
- Historial claro.

### Formulario

Debe generar una respuesta de confirmación.

Ejemplo:

~~~text
Hemos recibido la solicitud enviada por formulario y la registraremos internamente para su revisión.
~~~

### WhatsApp

Debe usarse para mensajes breves.

No debe usarse para explicar diagnósticos largos.

Ejemplo:

~~~text
Recibido. Lo registramos internamente y revisamos el caso. Te actualizamos cuando tengamos novedades.
~~~

### Teléfono

Debe usarse para urgencias o coordinación.

Después de una llamada debe quedar resumen escrito.

### Jira o Zammad

Son herramientas internas.

El cliente puede recibir referencias, pero no debe depender de conocer la herramienta.

## Comunicación de cierre

Todo cierre debe indicar:

- Qué se revisó.
- Qué se corrigió.
- Qué evidencia confirma el resultado.
- Qué hacer si vuelve a ocurrir.

Ejemplo:

~~~text
La incidencia queda resuelta. Hemos revisado el servicio, aplicado la corrección necesaria y validado que vuelve a responder correctamente. Si vuelve a ocurrir, podéis responder a este mismo hilo indicando la hora exacta y una captura del error.
~~~

## Frases recomendadas

~~~text
Hemos recibido la solicitud.
Estamos revisando el caso.
Necesitamos confirmar algunos datos antes de actuar.
El servicio se encuentra operativo.
La incidencia queda resuelta.
Hemos validado el resultado.
Registramos el caso internamente.
Os informaremos del siguiente paso.
~~~

## Frases a evitar

~~~text
Eso no es nuestro problema.
No sabemos qué ha pasado.
Tienes que tocar la configuración.
Mira GitHub.
Ejecuta este script como root.
Eso es normal, no pasa nada.
No podemos hacer nada.
~~~

## Regla final

El cliente debe sentir que DASC controla la situación.

Aunque internamente haya errores técnicos, la comunicación externa debe ser ordenada, clara y orientada a resolver.

## Conclusión

Una buena comunicación forma parte del producto.

DASC Server Manager no solo debe funcionar técnicamente, también debe dar confianza al cliente durante incidencias, cambios y mantenimientos.
