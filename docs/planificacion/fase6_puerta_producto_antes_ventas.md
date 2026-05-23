# Fase 6 - Puerta de producto antes de ventas

## Objetivo

Definir qué debe estar preparado antes de retomar ventas reales, primer cliente de pago o pilotos de pago.

## Estado

En curso.

## Motivo

La Fase 6 incluye tareas comerciales, pero antes de vender a una PyME el producto debe estar más pulido.

No basta con tener herramientas funcionando en GitHub.

## Checklist mínimo antes de R-048 y R-051

### 1. Repositorio y release

- [x] Release candidate creada.
- [x] Tag `v1.0-rc1` creado.
- [x] Auditoría clean inicial creada.
- [x] Artefactos sensibles eliminados del paquete API.
- [ ] Auditoría clean final repetida antes de nueva release.
- [ ] Nueva release candidate si hay cambios importantes.

### 2. Instalación

- [ ] Instalador API revisado.
- [ ] Instalador DB revisado.
- [ ] Instalador backups/servicios revisado.
- [ ] Uninstallers revisados.
- [ ] Instalación probada desde cero.
- [ ] Actualización probada desde una versión anterior.
- [ ] `config.env.example` validado.
- [ ] Perfiles Lite, PyME y Pro claros.

### 3. Windows y experiencia de uso

- [ ] Guía de uso desde Windows.
- [ ] Diferencia clara entre PC del usuario y servidores Ubuntu.
- [ ] Acceso al panel desde navegador explicado.
- [ ] Comandos Windows solo para equipo técnico.
- [ ] Nada de exigir GitHub a la PyME.

### 4. Soporte

- [x] GitHub Issues definido como herramienta interna.
- [ ] Canal real de cliente definido.
- [ ] Email o formulario de soporte definido.
- [ ] Flujo cliente -> equipo -> ticket interno definido.
- [ ] Prioridades y límites claros.
- [ ] SLA realista conectado con soporte real.

### 5. Informe mensual

- [x] Informe mensual v1 interno generado.
- [ ] Informe con datos reales de backups.
- [ ] Informe con restauración de prueba.
- [ ] Informe con alertas.
- [ ] Informe entendible para cliente no técnico.
- [ ] Exportación o entrega simple definida.

### 6. Producto frente a documentación

- [ ] Separar qué está implementado.
- [ ] Separar qué está documentado.
- [ ] Separar qué es futuro.
- [ ] Revisar que no se prometan funciones no listas.
- [ ] Revisar README y documentos comerciales.

## Criterio para abrir ventas

Se podrá retomar R-048 o R-051 cuando:

- El producto esté limpio.
- El despliegue sea repetible.
- El cliente no dependa de GitHub.
- El soporte tenga canal real.
- El informe mensual sea útil o se venda como revisión manual incluida.
- Exista una demo clara.
- Existan límites comerciales claros.

## Conclusión

La Fase 6 sigue en marcha, pero antes de ventas se añade una puerta de producto.

Esta puerta evita vender documentación en lugar de vender una solución real.
