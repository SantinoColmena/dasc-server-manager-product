# R-055A — Acceso al panel desde un navegador Windows

> **Destinatario:** usuario final de la PyME (el cliente, no el técnico).
> Para la guía de instalación y despliegue, ver [`R-055B`](R-055B_despliegue_desde_windows.md).

---

## ¿Qué necesitas?

Un ordenador con Windows y cualquier navegador moderno (Chrome, Edge, Firefox).
No se requiere instalar ningún programa adicional.

---

## 1. Dirección de acceso (URL)

El técnico que instaló Vigex te habrá indicado una URL de acceso. Las formas habituales son:

| Tipo de instalación | URL de ejemplo |
|---|---|
| Panel en Windows local (Docker) | `http://localhost:8000` |
| Solo IP, HTTP (lab/pruebas) | `http://192.168.1.50:8000` |
| Solo IP, HTTPS (producción) | `https://192.168.1.50` |
| Con nombre de dominio | `https://vigex.tuempresa.com` |

> Si no sabes la URL, contacta con el responsable técnico.

---

## 2. El aviso del navegador sobre el certificado

Si el técnico configuró HTTPS con un **certificado autofirmado** (la opción habitual en redes internas sin dominio público), el navegador mostrará un aviso de seguridad la primera vez:

**En Chrome / Edge:**
1. El navegador muestra "Tu conexión no es privada" o similar.
2. Haz clic en **Avanzado** (o "Más información").
3. Haz clic en **Continuar hacia [IP] (no seguro)**.

**En Firefox:**
1. El navegador muestra "Aviso: riesgo potencial de seguridad".
2. Haz clic en **Avanzado…**
3. Haz clic en **Aceptar el riesgo y continuar**.

> Este aviso aparece porque el certificado no está firmado por una autoridad reconocida públicamente.
> En una red interna de confianza es seguro proceder. Si la URL es pública con un dominio real,
> el aviso no debería aparecer (certificado Let's Encrypt).

---

## 3. Pantalla de inicio de sesión

Al acceder al panel verás una pantalla de login. Introduce:

- **Usuario:** el que te facilitó el responsable técnico.
- **Contraseña:** la contraseña asignada.

Pulsa **Entrar**. Si los datos son correctos, entrarás al panel principal.

> Si el sistema bloquea el acceso tras varios intentos fallidos, espera 15 minutos
> antes de volver a intentarlo. Esto es una protección normal del sistema.

---

## 4. Qué puedes hacer desde el panel

Una vez dentro, el menú lateral muestra las secciones a las que tienes acceso.
Un usuario estándar puede ver:

| Sección | Para qué sirve |
|---|---|
| **Copias** | Ver el historial de backups, lanzar una copia manual, comprobar el resultado |
| **Recuperación** | Recuperar datos de una copia anterior (acción delicada, consultar al técnico) |
| **Logs** | Ver eventos del sistema: quién accedió, qué acciones se ejecutaron, si hubo errores |
| **Alertas** | Configurar notificaciones por Telegram (@VigexPanelBot) o email |
| **Servicios** | Ver y controlar el estado de servicios del servidor (si tienes permiso) |
| **Cumplimiento** | Panel de cobertura NIS2/ENS/ISO 27001, evidencias datadas y dossier para auditor |
| **Incidentes** | Registrar y gestionar incidentes de seguridad con cuenta atrás NIS2 (24 h/72 h) |
| **Asistente IA** | Chat inteligente sobre el sistema: consulta backups, logs y estado sin navegar |

Los administradores además ven la sección **Administración** (usuarios, logs de acceso).

---

## 5. Qué NO puedes hacer desde el navegador

El panel web cubre el uso diario. Hay acciones que requieren intervención técnica (SSH al servidor):

- Modificar la configuración del sistema (`config.env`).
- Actualizar Vigex a una nueva versión.
- Cambiar la arquitectura de servidores (Lite / Standard / Pro).
- Acceder directamente a los archivos de backup en el servidor.
- Configurar UFW, fail2ban o el certificado HTTPS.

Para estas acciones, contacta con el responsable técnico.

---

## 6. Buenas prácticas de uso

- **No compartas tu contraseña** con nadie, ni por correo ni por chat.
- **Comprueba semanalmente** que existan copias recientes en la sección *Copias*.
- **Revisa los logs** si sospechas que algo ha fallado.
- **No repitas muchas veces** la misma acción si da error — anota el mensaje y avisa al técnico.
- **Cierra sesión** cuando termines, especialmente si usas un ordenador compartido.

---

## 7. Qué hacer si hay un error

1. Anota la hora exacta del error.
2. Haz captura de pantalla del mensaje.
3. Revisa la sección **Logs** — el evento puede aparecer ahí con más detalle.
4. Contacta con soporte indicando: usuario, acción realizada, hora y el mensaje de error.

---

## Referencia relacionada

- Manual de usuario completo: [`docs/cliente/R-034_manual_rapido_cliente.md`](../cliente/R-034_manual_rapido_cliente.md)
- Guía de instalación para técnicos: [`R-055B_despliegue_desde_windows.md`](R-055B_despliegue_desde_windows.md)
