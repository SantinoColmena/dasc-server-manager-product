# R-055B — Despliegue de Vigex desde un PC Windows

> **Destinatario:** técnico o reseller que instala Vigex desde un PC Windows 10/11.
>
> Para la guía del usuario final, ver [`R-055A`](R-055A_acceso_navegador_windows.md).

---

## ¿Qué escenario necesitas?

Vigex soporta tres topologías. Elige la que corresponda al cliente:

| Escenario | Descripción | Guía |
|---|---|---|
| **A — Panel en Windows** | El panel Vigex corre en un PC/servidor Windows usando Docker. Los servidores gestionados son Linux. | [Sección A](#escenario-a--panel-vigex-en-windows-con-docker) |
| **B — Todo Linux** | Panel y servidores gestionados son Linux. Tú instalas desde tu PC Windows. | [Sección B](#escenario-b--panel-en-linux-instalacion-remota-desde-windows) |
| **C — Topología mixta** | El panel está en Linux o Docker, pero algún servidor gestionado es Windows. | [Sección C](#escenario-c--servidores-gestionados-windows-vigex-agent) |

---

## Escenario A — Panel Vigex en Windows con Docker

El cliente tiene un PC o servidor Windows y quiere que el panel Vigex corra ahí.

### Instalación con VigexSetup.exe (R-099)

1. Descarga `VigexSetup.exe` de la [distribución Vigex](https://vigex.es/descargar).
2. Ejecútalo como **Administrador** en el PC del cliente.
3. El instalador:
   - Verifica requisitos (RAM ≥ 4 GB, disco ≥ 6 GB libres).
   - Descarga e instala Docker Desktop si no está presente.
   - Descarga la imagen `scolmena/vigex-panel:latest` de Docker Hub.
   - Crea `C:\ProgramData\Vigex\config.env` con los valores del cliente.
   - Registra una tarea de inicio automático en Windows.
   - Despliega el contenedor en `localhost:8000`.
4. Accede al panel en `http://localhost:8000` o `https://localhost:8000`.

**Actualizar a una nueva versión:**
```powershell
# Opción 1 — doble clic en:
C:\ProgramData\Vigex\vigex-update.bat

# Opción 2 — PowerShell como Administrador:
.\VigexSetup.ps1 -Update
```

**Desinstalar:**
```powershell
.\VigexSetup.ps1 -Uninstall
```

> Los servidores Linux gestionados se configuran igual que siempre (SSH).
> El panel en Docker se conecta a ellos exactamente igual que el panel en Linux.

---

## Escenario B — Panel en Linux, instalación remota desde Windows

---

## Herramientas necesarias en Windows

No hace falta instalar nada especial. Windows 10 (versión 1809 o posterior) y
Windows 11 incluyen de serie todo lo necesario:

| Herramienta | Dónde está | Para qué |
|---|---|---|
| **SSH client** | Activado por defecto en W10/W11 | Conectarse a los servidores Linux |
| **SCP** | Incluido con el cliente SSH | Copiar ficheros al servidor |
| **Windows Terminal** | Microsoft Store (recomendado) o `cmd.exe` / PowerShell | Ejecutar los comandos |

> Si SSH no está disponible: *Configuración → Aplicaciones → Características opcionales → Añadir → "Servidor OpenSSH cliente"*. Reinicia si es necesario.

**Herramientas opcionales (GUI):**
- **WinSCP** — gestor de ficheros gráfico para transferir archivos al servidor.
- **PuTTY** — cliente SSH con interfaz gráfica, útil para sesiones largas.

---

## Qué ocurre en cada servidor

Vigex se instala íntegramente en el/los servidores Linux mediante scripts bash.
Desde Windows solo necesitas:

1. **Conectarte por SSH** a cada servidor.
2. **Copiar el repositorio** Vigex al servidor (una sola vez).
3. **Ejecutar los instaladores** con los parámetros del entorno.

Todo el software (Python, MariaDB, nginx, fail2ban, etc.) lo instalan los propios
scripts de Vigex en el servidor Linux. El PC Windows solo actúa de terminal remota.

---

## 1. Preparar el PC Windows

Abre **Windows Terminal** (o PowerShell / cmd) y comprueba que SSH funciona:

```powershell
ssh -V
# OpenSSH_for_Windows_9.x, LibreSSL ...  ← correcto
```

Si el servidor Linux usa autenticación por clave (recomendado), genera un par de claves
si aún no tienes:

```powershell
ssh-keygen -t ed25519 -C "tecnico-vigex"
# Guarda la clave en la ruta por defecto (Enter) y define una passphrase
```

Copia la clave pública al servidor:

```powershell
# Reemplaza con el usuario y la IP del servidor
ssh-copy-id ubuntu@192.168.1.50
# Si ssh-copy-id no está disponible en tu versión:
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh ubuntu@192.168.1.50 "cat >> ~/.ssh/authorized_keys"
```

---

## 2. Descargar / obtener el repositorio Vigex

Tienes dos opciones para llevar el código al servidor:

### Opción A — Clonar directamente en el servidor (si tiene acceso a Internet)

```powershell
# Conéctate al servidor
ssh ubuntu@192.168.1.50

# En el servidor Linux:
git clone https://github.com/<tu-org>/vigex-server-manager-product.git ~/vigex
# O usa el tag/commit específico de la release:
git -C ~/vigex checkout v1.1-rc1
```

### Opción B — Transferir el archivo desde Windows con SCP (red sin acceso a Internet)

En Windows, desde el directorio local del repo:

```powershell
# Crear un tarball del repo (sin git archive para incluir ficheros no commiteados si fuera necesario):
git archive --format=tar.gz -o C:\Temp\vigex-src.tgz HEAD

# Copiar al servidor
scp C:\Temp\vigex-src.tgz ubuntu@192.168.1.50:/home/ubuntu/vigex-src.tgz

# En el servidor (via SSH):
ssh ubuntu@192.168.1.50 "mkdir -p ~/vigex && tar xzf ~/vigex-src.tgz -C ~/vigex"
```

---

## 3. Instalación por perfil

La instalación se ejecuta **en el servidor Linux** via SSH. Usa la guía de referencia:

> **[`docs/validaciones/R-053D_checklist_instalacion_desde_cero.md`](../validaciones/R-053D_checklist_instalacion_desde_cero.md)**
>
> Este documento contiene los comandos exactos para los 3 perfiles (Lite, Standard, Pro),
> el orden correcto de los instaladores, y las variables de entorno necesarias.

### Flujo típico para un perfil Standard (2 servidores)

Desde Windows Terminal, abres **dos pestañas SSH** — una por servidor:

**Pestaña 1 — servidor DB (`192.168.1.51`):**
```bash
ssh ubuntu@192.168.1.51
cd ~/vigex/deploy/db
sudo -E VIGEX_PROFILE=standard APP_PASSWORD='<pass-vigex>' \
    BACKUP_ALLOWED_HOST=192.168.1.50 LOGS_ALLOWED_HOST=192.168.1.50 \
    bash install_db.sh
# Cuando termine: anota las credenciales de /root/vigex-db-install-secrets.env
```

**Pestaña 2 — servidor panel+backup (`192.168.1.50`):**
```bash
ssh ubuntu@192.168.1.50
cd ~/vigex/deploy/backup-services
sudo -E VIGEX_PROFILE=standard APP_PASSWORD='<pass-vigex>' \
    DB_HOST=192.168.1.51 ... bash install_backup_services.sh

cd ~/vigex/deploy/api
sudo -E VIGEX_PROFILE=standard ... bash install_vigex_api.sh </dev/null
```

---

## 4. Transferir secretos entre servidores (si necesario)

En despliegues Standard y Pro, el instalador de DB genera un fichero de secretos
`/root/vigex-db-install-secrets.env` que los otros instaladores necesitan.
Para copiarlo entre servidores **desde Windows** como intermediario:

```powershell
# 1. En el servidor DB: copiar el fichero a /home/ubuntu/ (accesible por SCP)
ssh ubuntu@192.168.1.51 "sudo cp /root/vigex-db-install-secrets.env /home/ubuntu/ && sudo chown ubuntu: /home/ubuntu/vigex-db-install-secrets.env"

# 2. Desde Windows: descargarlo
scp ubuntu@192.168.1.51:/home/ubuntu/vigex-db-install-secrets.env C:\Temp\vigex-db-secrets.env

# 3. Subirlo al servidor de panel/backup
scp C:\Temp\vigex-db-secrets.env ubuntu@192.168.1.50:/home/ubuntu/vigex-db-install-secrets.env

# 4. En el servidor de panel: moverlo a /root/ para que el instalador lo encuentre
ssh ubuntu@192.168.1.50 "sudo mv /home/ubuntu/vigex-db-install-secrets.env /root/"

# 5. Eliminar la copia local (contiene credenciales)
Remove-Item C:\Temp\vigex-db-secrets.env
```

---

## 5. Endurecimiento post-instalación (R-054)

Una vez instalado Vigex, aplica los scripts de hardening desde cada servidor:

```bash
# En el servidor del panel (API host):
cd ~/vigex/deploy/proxy
sudo bash install_reverse_proxy.sh          # HTTPS + activa HTTPS_ONLY

cd ~/vigex/deploy/api
sudo bash harden_ufw_api.sh                 # UFW: 22/80/443
sudo bash harden_fail2ban_api.sh            # fail2ban: sshd + vigex-auth

# En el servidor DB:
cd ~/vigex/deploy/db
sudo MARIADB_ALLOWED_HOSTS="192.168.1.50" bash harden_ufw_db.sh

# En el servidor de backup (si es separado — perfil Pro):
cd ~/vigex/deploy/backup-services
sudo bash harden_ufw_backup.sh
```

---

## 6. Verificar desde el navegador Windows

Tras instalar, comprueba que el panel responde:

1. Abre Chrome, Edge o Firefox en Windows.
2. Accede a `https://192.168.1.50` (o el dominio si tienes uno).
3. Si aparece el aviso de certificado autofirmado → sigue los pasos de [`R-055A §2`](R-055A_acceso_navegador_windows.md#2-el-aviso-del-navegador-sobre-el-certificado).
4. Inicia sesión con el usuario admin y la contraseña configurada.
5. Lanza un backup de prueba para confirmar que el circuito completo funciona.

---

## 7. Actualizaciones futuras

Para actualizar Vigex a una nueva versión desde Windows:

```powershell
# 1. Crear tarball del nuevo código:
git archive --format=tar.gz -o C:\Temp\vigex-src-nuevo.tgz HEAD

# 2. Subir al servidor:
scp C:\Temp\vigex-src-nuevo.tgz ubuntu@192.168.1.50:/home/ubuntu/

# 3. En el servidor: extraer, hacer backup de config.env, re-ejecutar instalador
ssh ubuntu@192.168.1.50
#   cp /opt/vigex/api/config.env ~/config.env.bak
#   mkdir -p ~/vigex-nuevo && tar xzf ~/vigex-src-nuevo.tgz -C ~/vigex-nuevo
#   cd ~/vigex-nuevo/deploy/api && sudo bash install_vigex_api.sh </dev/null
```

> El instalador es idempotente: conserva `config.env`, `SECRET_KEY` y
> `known_hosts` en re-ejecuciones.

---

## Resumen rápido

| Paso | Dónde | Herramienta Windows |
|---|---|---|
| Generar clave SSH | PC Windows | `ssh-keygen` en Terminal |
| Copiar repo al servidor | Windows → servidor | `scp` o WinSCP |
| Ejecutar instaladores | En el servidor Linux | `ssh` + sesión interactiva |
| Transferir secretos entre servidores | Windows como intermediario | `scp` doble |
| Hardening (UFW, nginx, fail2ban) | En cada servidor Linux | `ssh` |
| Verificar el panel | PC Windows | Navegador (Chrome/Edge/Firefox) |

---

## Escenario C — Servidores gestionados Windows (Vigex Agent)

Si uno o más servidores que Vigex debe monitorizar/gestionar corren **Windows Server**
(no el panel — el servidor gestionado), se usa **Vigex Agent** en lugar de SSH.

### Instalar VigexAgent.exe en el servidor Windows gestionado (R-100)

1. Copia `deploy/agent/VigexAgent.exe` al servidor Windows (via red compartida o SCP).
2. En el servidor Windows, crea el archivo de configuración:

```powershell
# C:\ProgramData\VigexAgent\agent.env
VIGEX_AGENT_TOKEN=TOKEN_SECRETO_LARGO_Y_UNICO
VIGEX_AGENT_PORT=8050
VIGEX_MONITORED_SERVICES=NombreServicio1,NombreServicio2
VIGEX_BACKUP_DIR=C:\Vigex\backups
VIGEX_BACKUP_RETENTION=7
```

3. Ejecuta el agente (en producción, regístralo como servicio de Windows):

```powershell
# Prueba manual:
.\VigexAgent.exe

# Como servicio (recomendado):
sc.exe create VigexAgent binPath= "C:\ProgramData\VigexAgent\VigexAgent.exe" start= auto
sc.exe start VigexAgent
```

4. Abre el puerto 8050 en el firewall de Windows:

```powershell
netsh advfirewall firewall add rule name="VigexAgent" dir=in action=allow protocol=TCP localport=8050
```

### Configurar el panel para usar el agente

En `config.env` del panel Vigex (Linux o Docker), añade:

```env
VIGEX_AGENT_PORT=8050
# Formato: IP_SERVIDOR:TOKEN (separados por coma si hay varios)
VIGEX_AGENT_TOKEN_MAP=192.168.1.60:TOKEN_SECRETO_LARGO_Y_UNICO
```

A partir de ese momento, el panel enruta automáticamente las operaciones de ese host
por HTTP al agente en lugar de por SSH. El resto de hosts Linux no cambian.
