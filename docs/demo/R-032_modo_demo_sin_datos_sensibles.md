# R-032 - Modo demo sin datos sensibles

## Objetivo

Preparar un modo de demostración seguro para enseñar DASC Server Manager sin exponer datos reales, credenciales, tokens, rutas internas sensibles ni información de clientes.

## Contexto

La Fase 4 se centra en preparar el proyecto para demostraciones, validaciones externas y posibles pilotos. El modo demo debe permitir enseñar el funcionamiento principal del sistema sin riesgo de modificar datos importantes ni enseñar secretos.

## Alcance del modo demo

El modo demo debe permitir enseñar:

- Acceso al panel.
- Gestión visual de backups.
- Historial de copias.
- Logs de actividad.
- Alertas simuladas o controladas.
- Estado de servicios.
- Flujo general de restauración, si aplica.
- Arquitecturas Lite, PyME y Pro a nivel explicativo.

## Datos que NO deben aparecer en la demo

No deben mostrarse:

- Contraseñas reales.
- Tokens de Telegram.
- Claves SSH privadas.
- IPs públicas reales de clientes.
- Datos personales reales.
- Bases de datos reales de clientes.
- Rutas internas sensibles.
- Ficheros config.env reales.
- Capturas con secretos visibles.

## Datos permitidos en demo

Se permite usar:

- Usuarios ficticios.
- Base de datos de prueba.
- Nombres de empresa inventados.
- Backups generados en laboratorio.
- Eventos de logs simulados o procedentes del entorno de pruebas.
- IPs privadas de laboratorio.
- Capturas del panel sin secretos.

## Usuario demo recomendado

Usuario: demo  
Rol: usuario limitado  
Permisos recomendados:

- Logs: lectura.
- Backups: ejecución controlada.
- Servicios: solo visualización o acciones preparadas.
- Administración: no permitido.

## Escenario de demo recomendado

El escenario recomendado para enseñar el sistema es:

1. Entrar al panel con usuario demo.
2. Mostrar el dashboard principal.
3. Ir a copias de seguridad.
4. Ejecutar una copia manual de prueba.
5. Ver el resultado en el historial.
6. Ir a logs.
7. Confirmar que la acción queda registrada.
8. Mostrar alertas o explicar el flujo de avisos.
9. Mostrar servicios.
10. Explicar que en cliente real se validaría restauración y copia externa.

## Riesgos evitados

Con este modo demo se evitan:

- Enseñar secretos durante la presentación.
- Romper datos reales durante una demostración.
- Ejecutar restauraciones peligrosas.
- Usar credenciales administrativas innecesarias.
- Mezclar entorno de pruebas con entorno de cliente.

## Estado

Documentado: Sí  
Implementado: Pendiente de aplicar en entorno si se desea usuario demo real  
Validado: Pendiente
