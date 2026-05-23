# R-039 - Selección del primer piloto técnico

## Objetivo

Definir el perfil recomendado para el primer piloto técnico de DASC Server Manager y dejar documentados los criterios para seleccionarlo.

El objetivo no es elegir todavía una empresa real con datos privados, sino establecer qué tipo de cliente o entorno sería adecuado para probar DASC fuera del laboratorio académico.

## Enfoque

El primer piloto técnico debe ser controlado, sencillo y seguro.

No se recomienda empezar con un cliente crítico ni con una empresa que dependa totalmente del sistema desde el primer día.

La finalidad del piloto es validar:

- Instalación.
- Backups.
- Logs.
- Permisos.
- Alertas.
- Restauración de prueba.
- Manual de cliente.
- Checklist de instalación.
- Guion de demo.
- Soporte básico.

## Perfil recomendado para el primer piloto

El primer piloto debería ser una empresa pequeña o entorno conocido con estas características:

- Entre 1 y 10 usuarios.
- Infraestructura sencilla.
- Base de datos local o servicio de prueba.
- Persona de contacto accesible.
- Posibilidad de realizar pruebas sin afectar producción.
- Acepta una instalación controlada.
- Acepta que el producto está en fase inicial.
- Permite guardar evidencias técnicas.
- No exige soporte 24/7.
- No maneja datos extremadamente críticos durante la prueba.

## Tipo de cliente recomendado

Perfiles más adecuados:

1. Taller pequeño.
2. Academia pequeña.
3. Tienda con TPV o base de datos local.
4. Empresa conocida de entorno cercano.
5. Proveedor IT pequeño que quiera probar el sistema.
6. Laboratorio interno simulando cliente real.

## Opción recomendada para el primer piloto

La opción más segura para el primer piloto es:

**Piloto técnico controlado en entorno conocido o simulado como cliente real.**

Motivo:

Permite validar el proceso completo sin poner en riesgo datos reales de una empresa.

## Arquitectura recomendada del piloto

Para el primer piloto se recomienda usar arquitectura tipo DASC PyME simplificada:

- Servidor principal: base de datos o servicio a proteger.
- Servidor DASC/backups/logs: panel, backups y registros.

Si no se dispone de dos servidores, se puede usar una instalación Lite:

- 1 servidor.
- Copia externa obligatoria.
- Datos de prueba.
- Restauración validada en entorno seguro.

## Alcance mínimo del piloto

El piloto debe validar como mínimo:

| Área | Validación |
|---|---|
| Acceso | Login correcto e incorrecto |
| Usuarios | Usuario admin y usuario limitado |
| Backups | Copia completa funcional |
| Logs | Registro de acciones |
| Servicios | Visualización o acción controlada |
| Alertas | Envío o simulación de alerta |
| Restauración | Prueba segura o explicación documentada |
| Documentación | Manual rápido entregado |
| Instalación | Checklist seguido |
| Demo | Guion usado o adaptado |

## Criterios para aceptar un piloto

Un piloto se considera aceptable si cumple:

- No compromete datos reales.
- Tiene autorización del responsable.
- Permite pruebas de backup.
- Permite revisar logs.
- Permite probar restauración en entorno seguro.
- Tiene un contacto disponible.
- Tiene expectativas realistas.
- Acepta limitaciones de fase inicial.

## Criterios para rechazar un piloto

No se recomienda aceptar como primer piloto:

- Empresa con datos críticos sin entorno de prueba.
- Cliente que exige garantía absoluta.
- Cliente que exige soporte 24/7.
- Infraestructura demasiado compleja.
- Entorno sin acceso SSH o sin permisos mínimos.
- Cliente que no permite evidencias.
- Cliente que no acepta pruebas controladas.
- Sistemas sanitarios o legales críticos sin supervisión profesional.

## Plan de ejecución del piloto

### Fase 1 - Preparación

1. Confirmar tipo de cliente.
2. Confirmar arquitectura.
3. Recopilar información técnica.
4. Revisar checklist de instalación.
5. Definir datos de prueba.
6. Acordar ventana de instalación.

### Fase 2 - Instalación

1. Instalar base de datos o usar entorno existente de prueba.
2. Instalar servidor de backups/servicios.
3. Instalar panel DASC.
4. Configurar usuarios.
5. Configurar backups.
6. Configurar logs.
7. Configurar alertas si aplica.

### Fase 3 - Validación

1. Probar login.
2. Ejecutar backup.
3. Revisar archivo generado.
4. Revisar logs.
5. Probar permisos de usuario.
6. Probar alerta.
7. Probar restauración en entorno seguro.
8. Guardar evidencias.

### Fase 4 - Cierre

1. Entregar manual rápido.
2. Explicar funcionamiento.
3. Registrar incidencias.
4. Recoger feedback.
5. Definir mejoras.
6. Decidir si el piloto continúa.

## Métricas del piloto

Durante el piloto se recomienda medir:

| Métrica | Objetivo |
|---|---|
| Tiempo de instalación | Saber si el proceso es repetible |
| Número de errores | Detectar puntos débiles |
| Backup correcto | Validar función principal |
| Restauración validada | Confirmar utilidad real |
| Logs generados | Confirmar trazabilidad |
| Alertas generadas | Confirmar aviso de incidencias |
| Comprensión del cliente | Validar facilidad de uso |
| Feedback recibido | Detectar mejoras |

## Resultado esperado

El primer piloto técnico debe demostrar que DASC Server Manager puede instalarse, configurarse y validarse en un entorno controlado, con backups funcionales, logs activos, permisos definidos y documentación mínima entregada.

## Decisión inicial

Para la fase actual, se selecciona como primer piloto recomendado:

**Piloto técnico controlado con datos de prueba en entorno conocido, simulando una PyME con arquitectura Lite o PyME simplificada.**

Esta decisión evita riesgos innecesarios y permite validar el producto antes de ofrecerlo a una empresa real.

## Estado

Documentado: Sí  
Implementado: Pendiente de ejecutar piloto real  
Validado: Pendiente
