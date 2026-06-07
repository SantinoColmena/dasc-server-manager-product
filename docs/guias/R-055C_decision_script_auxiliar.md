# R-055C — Decisión sobre script auxiliar Windows

> **Conclusión:** No se crea un script PowerShell de despliegue.
> La guía [`R-055B`](R-055B_despliegue_desde_windows.md) + SSH nativo de Windows es suficiente
> para el perfil de técnico objetivo. Se describe aquí el razonamiento.

---

## Opciones evaluadas

| Opción | Descripción | Pros | Contras |
|---|---|---|---|
| **A — Solo documentación** (elegida) | Guía Markdown con comandos exactos copy-paste | Sin código a mantener; funciona con cualquier herramienta SSH | El técnico debe ejecutar los comandos manualmente |
| **B — Script PowerShell interactivo** | Asistente PS que pregunta IPs, perfil y ejecuta SSH/SCP | Experiencia guiada | Complejidad alta: gestionar SSH desde PowerShell, encodings, errores remotos |
| **C — Script PowerShell + OpenSSH** | Script que usa `ssh.exe` como subproceso | Reutiliza SSH nativo | Salida remota difícil de parsear; sin ventaja real sobre ejecutar los comandos a mano |

---

## Criterio de decisión

**El técnico objetivo** (reseller o administrador de sistemas PyME) ya sabe usar SSH.
El despliegue de DASC requiere tomar decisiones contextuales durante la instalación
(IPs, contraseñas, perfil), que un script debe hardcodear o preguntar interactivamente.

Un script PowerShell de despliegue:
- Tendría que replicar la lógica de `prompt_config_key()` de los instaladores bash.
- Sería más frágil que los propios scripts bash (encodings, gestión de errores remotos).
- Añadiría una capa de mantenimiento paralela sin aumentar fiabilidad.

**La alternativa correcta** para usuarios no técnicos es un instalador con interfaz web
o un appliance (fuera del alcance de la Fase 6).

---

## Lo que ya existe y es suficiente

| Recurso | Utilidad |
|---|---|
| `R-055A` — Guía de acceso por navegador | Usuario final PyME |
| `R-055B` — Guía de despliegue desde Windows | Técnico/reseller |
| `R-053D` — Checklist reproducible por perfil | Comandos exactos de instalación |
| `R-038` — Checklist de instalación en cliente | Lista de verificación pre/post |
| `tools/windows/check_api_package_installable.ps1` | Valida el paquete antes de desplegar |
| `tools/windows/check_repo_clean.ps1` | Audita el repo antes de distribuirlo |

Los scripts PowerShell existentes en `tools/windows/` cubren la parte de validación
desde Windows; el despliegue real requiere SSH al servidor Linux, que es lo que
documentan R-055A/B y R-053D.

---

## Posibles mejoras futuras (no en Fase 6)

- **Fase 7+:** Script PowerShell que automatice la transferencia del repo y la ejecución
  remota vía SSH (`ssh user@host 'bash -s' < install_db.sh`) para entornos conocidos.
- **Fase 8+:** Appliance OVA o imagen Docker para despliegue sin conocimientos de Linux.
