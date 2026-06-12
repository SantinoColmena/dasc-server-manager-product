package db

import (
	"fmt"
	"log"
	"os/exec"
	"strings"
)

type Config struct {
	Backend   string
	Host      string
	Port      int
	User      string
	Pass      string
	BackupDir string
	Retention int
}

// Detect devuelve el backend correcto segun la configuracion y lo que este instalado.
func Detect(cfg Config) Backend {
	backend := strings.ToLower(cfg.Backend)

	switch backend {
	case "mysql":
		log.Println("[db] backend forzado: mysql")
		return newMySQL(cfg)
	case "sqlserver", "mssql":
		log.Println("[db] backend forzado: sqlserver")
		return newSQLServer(cfg)
	case "none":
		log.Println("[db] backend forzado: none")
		return &NoBackend{}
	default:
		// auto-deteccion
		return autoDetect(cfg)
	}
}

func autoDetect(cfg Config) Backend {
	// Detectar SQL Server: buscar servicios MSSQLSERVER o MSSQL$<instancia>
	if hasSQLServer() {
		log.Println("[db] auto-detectado: sqlserver")
		return newSQLServer(cfg)
	}
	// Detectar MySQL / MariaDB
	if hasMySQL() {
		log.Println("[db] auto-detectado: mysql")
		return newMySQL(cfg)
	}
	log.Println("[db] no se detecto ningun motor de base de datos")
	return &NoBackend{}
}

func hasSQLServer() bool {
	out, err := exec.Command("sc", "query", "type=", "all", "state=", "all").Output()
	if err != nil {
		return false
	}
	s := string(out)
	return strings.Contains(s, "MSSQLSERVER") || strings.Contains(s, "MSSQL$")
}

func hasMySQL() bool {
	for _, svc := range []string{"MySQL84", "MySQL80", "MySQL57", "MySQL", "MariaDB"} {
		out, err := exec.Command("sc", "query", svc).Output()
		if err == nil && strings.Contains(string(out), svc) {
			return true
		}
	}
	return false
}

func newMySQL(cfg Config) Backend {
	port := cfg.Port
	if port == 0 {
		port = 3306
	}
	return &MySQLBackend{
		Host:      cfg.Host,
		Port:      port,
		User:      cfg.User,
		Pass:      cfg.Pass,
		BackupDir: cfg.BackupDir,
		Retention: cfg.Retention,
	}
}

func newSQLServer(cfg Config) Backend {
	port := cfg.Port
	// Puerto 0 = instancia default, no especificar
	return &SqlServerBackend{
		Host:      cfg.Host,
		Port:      port,
		User:      cfg.User,
		Pass:      cfg.Pass,
		BackupDir: cfg.BackupDir,
		Retention: cfg.Retention,
	}
}

// listBackupFiles es una utilidad compartida por ambos backends.
func listBackupFiles(dir, ext, backendName, format string) ([]BackupFile, error) {
	pattern := fmt.Sprintf("%s/vigex_backup_*%s", dir, ext)
	matches, err := listGlob(pattern)
	if err != nil {
		return nil, err
	}

	var files []BackupFile
	for _, m := range matches {
		info, err := statFile(m)
		if err != nil {
			continue
		}
		files = append(files, BackupFile{
			Filename:  info.Name,
			SizeMB:    info.SizeMB,
			CreatedAt: info.ModTime,
			Format:    format,
			DBBackend: backendName,
		})
	}
	return files, nil
}
