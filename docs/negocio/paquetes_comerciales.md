# Paquetes comerciales - Vigex

## 1. Objetivo de los paquetes

Vigex se plantea como un producto adaptable a diferentes tipos de empresa. No todos los clientes tienen los mismos recursos, presupuesto o nivel de necesidad técnica, por eso el producto se divide inicialmente en tres paquetes comerciales:

- Vigex Lite.
- Vigex PyME.
- Vigex Pro.

La idea es que el mismo producto pueda instalarse en escenarios distintos, desde una empresa pequeña con un único servidor hasta una empresa que necesite separar responsabilidades entre panel, base de datos y backups.

---

## 2. Resumen general de paquetes

| Paquete | Cliente objetivo | Arquitectura recomendada | Nivel de protección | Precio orientativo |
|---|---|---|---|---|
| Vigex Lite | Autónomos, microempresas o pruebas internas | 1 servidor | Básico | 299 € - 499 € |
| Vigex PyME | Pequeñas empresas con datos importantes | 2 servidores | Medio | 799 € - 1.200 € |
| Vigex Pro | Empresas con mayor necesidad de control | 3 servidores | Alto | 1.500 € - 3.000 € |

Los precios son orientativos y pueden cambiar según el alcance real, horas de instalación, soporte contratado y personalizaciones necesarias.

---

## 3. Vigex Lite

### Descripción

Vigex Lite es la versión más sencilla del producto. Está pensada para clientes pequeños que quieren empezar a controlar sus copias de seguridad y operaciones básicas sin invertir en varios servidores.

En esta versión, el panel, la base de datos y las copias pueden convivir en una misma máquina. No es la opción más segura, pero permite ofrecer una entrada económica al producto.

### Cliente objetivo

Vigex Lite está pensado para:

- Autónomos.
- Microempresas.
- Pequeñas tiendas.
- Academias pequeñas.
- Despachos con pocos recursos técnicos.
- Clientes que quieren una primera instalación básica.
- Entornos de prueba o pilotos.

### Arquitectura recomendada

**Servidor único:**

- Panel Vigex.
- Base de datos MySQL/MariaDB.
- Backups locales.
- Logs.
- Servicios básicos.

### Funcionalidades incluidas

- Instalación del panel Vigex en un servidor.
- Panel web local.
- Login de administrador.
- Gestión básica de usuarios.
- Backups completos.
- Historial básico de acciones.
- Logs básicos del panel.
- Control básico de servicios.
- Configuración inicial.
- Documentación básica de uso.

### Funcionalidades no incluidas

- Separación física de backups.
- Alta disponibilidad.
- Monitorización avanzada.
- Alertas avanzadas.
- Soporte 24/7.
- Personalizaciones complejas.
- Restauración avanzada con múltiples puntos.
- Auditoría completa de seguridad.

### Ventajas

- Coste bajo.
- Instalación sencilla.
- Ideal para empezar.
- No requiere infraestructura compleja.
- Permite validar el producto en clientes pequeños.

### Limitaciones

- Si falla el único servidor, puede afectar al panel, la base de datos y los backups.
- Menor separación de responsabilidades.
- Menor seguridad que los paquetes superiores.
- No recomendado para empresas con datos muy críticos.

### Precio orientativo

299 € - 499 €.

Este precio puede incluir instalación inicial, configuración básica y una pequeña sesión de explicación al cliente.

---

## 4. Vigex PyME

### Descripción

Vigex PyME es el paquete recomendado para la mayoría de pequeñas empresas. Busca un equilibrio entre coste, seguridad y facilidad de implantación.

En este escenario se utilizan dos servidores. Uno ejecuta el panel y la base de datos principal, mientras que el segundo se encarga de almacenar backups y ejecutar servicios auxiliares.

Esta opción mejora mucho la seguridad respecto al paquete Lite, porque las copias no dependen completamente del mismo servidor donde está la base de datos.

### Cliente objetivo

Vigex PyME está pensado para:

- Pequeñas empresas.
- Gestorías.
- Despachos profesionales.
- Empresas con base de datos local.
- Negocios con información importante.
- Clientes que no pueden pagar una infraestructura grande, pero quieren más seguridad que una instalación simple.

### Arquitectura recomendada

**Servidor 1 - Principal:**

- Panel Vigex.
- Base de datos MySQL/MariaDB.
- Logs.
- Aplicación principal.

**Servidor 2 - Backups y servicios auxiliares:**

- Backups.
- Scripts de mantenimiento.
- Control de servicios.
- Posible monitorización básica.

### Funcionalidades incluidas

- Instalación del panel Vigex.
- Configuración de conexión con servidor de backups.
- Backups completos.
- Backups incrementales.
- Backups diferenciales.
- Historial de backups.
- Logs de actividad del panel.
- Gestión de usuarios y permisos.
- Control de servicios.
- Alertas básicas.
- Configuración inicial de retención.
- Validación inicial del sistema.
- Documentación técnica básica.
- Prueba de backup y restauración básica.

### Funcionalidades no incluidas

- Alta disponibilidad completa.
- Soporte 24/7.
- Monitorización avanzada con informes periódicos.
- Infraestructura de tres servidores.
- Desarrollo a medida ilimitado.
- Auditoría legal o de ciberseguridad completa.

### Ventajas

- Mejor equilibrio entre precio y seguridad.
- Backups separados del servidor principal.
- Adecuado para la mayoría de PyMEs.
- Permite crecimiento futuro hacia Vigex Pro.
- Reduce el riesgo de perder los backups si falla el servidor principal.

### Limitaciones

- El panel y la base de datos pueden seguir compartiendo máquina.
- No existe separación total de responsabilidades.
- La monitorización puede ser básica.
- Requiere al menos dos máquinas o dos servidores virtuales.

### Precio orientativo

799 € - 1.200 €.

Este precio puede incluir instalación, configuración, pruebas iniciales, documentación básica y soporte inicial limitado.

---

## 5. Vigex Pro

### Descripción

Vigex Pro es la versión más completa del producto. Está pensada para empresas que necesitan mayor separación, más seguridad y mejor trazabilidad.

En este escenario se utilizan tres servidores, separando claramente el panel, la base de datos y el servidor de backups, servicios auxiliares y monitorización.

Es la arquitectura más parecida a la planteada en el entorno técnico original del proyecto.

### Cliente objetivo

Vigex Pro está pensado para:

- Empresas con datos críticos.
- Empresas con mayor volumen de información.
- Clientes que necesitan mayor separación de responsabilidades.
- Empresas que quieren monitorización y alertas.
- Clientes que necesitan una instalación más profesional.
- Negocios que quieren reducir riesgos operativos.

### Arquitectura recomendada

**Servidor 1 - Panel/API:**

- Panel Vigex.
- Backend FastAPI.
- Gestión de usuarios.
- Interfaz web.

**Servidor 2 - Base de datos:**

- MySQL/MariaDB.
- Datos principales.
- Logs centralizados.
- Configuración de acceso controlado.

**Servidor 3 - Backups, servicios y monitorización:**

- Backups completos.
- Backups incrementales.
- Backups diferenciales.
- Scripts de mantenimiento.
- Control de servicios.
- Alertas.
- Monitorización con Cacti.

### Funcionalidades incluidas

- Instalación completa en tres servidores.
- Panel web local.
- Gestión de usuarios y permisos.
- Backups completos.
- Backups incrementales.
- Backups diferenciales.
- Historial completo de backups.
- Restauración controlada.
- Descarga de backups.
- Eliminación controlada de backups antiguos.
- Logs avanzados.
- Filtros y búsqueda en logs.
- Control de servicios.
- Alertas por Telegram o canal equivalente.
- Monitorización con Cacti.
- Configuración de retención.
- Documentación técnica.
- Prueba de backup.
- Prueba de restauración.
- Soporte inicial ampliado.

### Funcionalidades no incluidas

- Soporte 24/7 salvo contratación específica.
- Sustitución de una auditoría completa de ciberseguridad.
- Reparación de hardware del cliente.
- Administración completa de todos los sistemas externos al producto.
- Garantía absoluta frente a ataques externos.
- Migraciones complejas no acordadas previamente.

### Ventajas

- Separación clara de responsabilidades.
- Mayor seguridad.
- Mejor trazabilidad.
- Mejor escalabilidad.
- Más fácil de mantener.
- Más defendible para clientes con datos importantes.
- Permite añadir servicios gestionados en el futuro.

### Limitaciones

- Mayor coste inicial.
- Requiere más infraestructura.
- Requiere más tiempo de instalación.
- Puede ser excesivo para clientes muy pequeños.

### Precio orientativo

1.500 € - 3.000 €.

Este precio puede incluir instalación completa, configuración, pruebas, documentación, formación inicial y soporte durante el arranque.

---

## 6. Comparativa funcional

| Funcionalidad | Lite | PyME | Pro |
|---|---|---|---|
| Panel web local | Sí | Sí | Sí |
| Login administrador | Sí | Sí | Sí |
| Gestión de usuarios | Básica | Sí | Sí |
| Backups completos | Sí | Sí | Sí |
| Backups incrementales | No / opcional | Sí | Sí |
| Backups diferenciales | No / opcional | Sí | Sí |
| Historial de backups | Básico | Sí | Avanzado |
| Restauración desde panel | No / opcional | Básica | Sí |
| Descarga de backups | No / opcional | Sí | Sí |
| Eliminación de backups | Básica | Sí | Sí |
| Logs del panel | Básicos | Sí | Avanzados |
| Filtros en logs | No | Básicos | Avanzados |
| Control de servicios | Básico | Sí | Sí |
| Alertas | No / opcional | Básicas | Sí |
| Cacti / monitorización | No | Opcional | Sí |
| Separación de servidores | No | Parcial | Completa |
| Soporte inicial | Básico | Medio | Ampliado |

---

## 7. Adaptación por número de servidores

Uno de los puntos clave del producto es que puede adaptarse a los recursos del cliente.

### Instalación en 1 servidor

Adecuada para Vigex Lite.

Ventajas:

- Menor coste.
- Instalación más rápida.
- Menos complejidad.

Desventajas:

- Menor separación.
- Más riesgo si falla el servidor.
- Backups menos protegidos.

### Instalación en 2 servidores

Adecuada para Vigex PyME.

Ventajas:

- Mejor equilibrio.
- Backups separados.
- Coste asumible para una PyME.
- Menor riesgo que en un único servidor.

Desventajas:

- No separa completamente panel y base de datos.
- Requiere una segunda máquina física o virtual.

### Instalación en 3 servidores

Adecuada para Vigex Pro.

Ventajas:

- Separación completa.
- Mejor seguridad.
- Mejor mantenimiento.
- Arquitectura más profesional.
- Más preparada para crecimiento.

Desventajas:

- Mayor coste.
- Más infraestructura.
- Más tiempo de despliegue.

---

## 8. Recomendación comercial inicial

La opción recomendada para vender primero sería Vigex PyME.

Motivos:

- Es más realista para una pequeña empresa.
- No exige tres servidores.
- Es más segura que una instalación en un único servidor.
- Permite justificar mejor el valor del producto.
- Tiene margen para ofrecer mantenimiento posterior.
- Puede evolucionar a Pro si el cliente crece.

Vigex Lite puede usarse como entrada económica o piloto.

Vigex Pro puede reservarse para clientes con mayor presupuesto o mayor necesidad de seguridad.

---

## 9. Posibles servicios adicionales

Además de la instalación inicial, se pueden ofrecer servicios adicionales:

- Mantenimiento mensual.
- Revisión periódica de backups.
- Pruebas de restauración.
- Actualizaciones del panel.
- Configuración de nuevas alertas.
- Revisión de logs.
- Informes mensuales.
- Soporte técnico.
- Migración de instalación Lite a PyME.
- Migración de PyME a Pro.

Estos servicios permitirían pasar de una venta única a un modelo con ingresos recurrentes.

---

## 10. Conclusión

Los paquetes Lite, PyME y Pro permiten convertir Vigex en un producto más flexible y comercial.

La división por paquetes facilita adaptar la solución al presupuesto y necesidades de cada cliente, evitando ofrecer una única instalación demasiado grande o demasiado cara.

La estrategia inicial recomendada es centrar el producto en el paquete PyME, manteniendo Lite como opción de entrada y Pro como opción avanzada.
