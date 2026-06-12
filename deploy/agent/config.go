package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
)

type Config struct {
	Token             string
	Port              int
	DBBackend         string
	DBHost            string
	DBPort            int
	DBUser            string
	DBPass            string
	BackupDir         string
	BackupRetention   int
	MonitoredServices []string
}

func loadConfig() (*Config, error) {
	// Buscar agent.env junto al ejecutable
	execPath, err := os.Executable()
	if err != nil {
		return nil, fmt.Errorf("no se pudo obtener la ruta del ejecutable: %w", err)
	}
	envPath := filepath.Join(filepath.Dir(execPath), "agent.env")

	// Fallback al directorio de trabajo (util en desarrollo)
	if _, err := os.Stat(envPath); os.IsNotExist(err) {
		envPath = "agent.env"
	}

	env, err := parseEnvFile(envPath)
	if err != nil {
		return nil, fmt.Errorf("error leyendo %s: %w", envPath, err)
	}

	cfg := &Config{
		Token:           env["VIGEX_AGENT_TOKEN"],
		Port:            8050,
		DBBackend:       getEnvDefault(env, "VIGEX_DB_BACKEND", "auto"),
		DBHost:          getEnvDefault(env, "VIGEX_DB_HOST", "localhost"),
		DBPort:          0,
		DBUser:          getEnvDefault(env, "VIGEX_DB_USER", "vigex_backup"),
		DBPass:          env["VIGEX_DB_PASS"],
		BackupRetention: 10,
	}

	if p := env["VIGEX_AGENT_PORT"]; p != "" {
		if n, err := strconv.Atoi(p); err == nil {
			cfg.Port = n
		}
	}

	if p := env["VIGEX_DB_PORT"]; p != "" {
		if n, err := strconv.Atoi(p); err == nil {
			cfg.DBPort = n
		}
	}

	if r := env["VIGEX_BACKUP_RETENTION"]; r != "" {
		if n, err := strconv.Atoi(r); err == nil {
			cfg.BackupRetention = n
		}
	}

	// Directorio de backups con default por plataforma
	if d := env["VIGEX_BACKUP_DIR"]; d != "" {
		cfg.BackupDir = d
	} else if runtime.GOOS == "windows" {
		cfg.BackupDir = `C:\Vigex\backups`
	} else {
		cfg.BackupDir = "/var/backups/vigex"
	}

	if s := env["VIGEX_MONITORED_SERVICES"]; s != "" {
		for _, svc := range strings.Split(s, ",") {
			if t := strings.TrimSpace(svc); t != "" {
				cfg.MonitoredServices = append(cfg.MonitoredServices, t)
			}
		}
	}

	if cfg.Token == "" || cfg.Token == "CAMBIAR_POR_TOKEN_ALEATORIO_64_CHARS" {
		return nil, fmt.Errorf("VIGEX_AGENT_TOKEN no configurado en %s", envPath)
	}

	return cfg, nil
}

func parseEnvFile(path string) (map[string]string, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	env := make(map[string]string)
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		idx := strings.IndexByte(line, '=')
		if idx < 0 {
			continue
		}
		key := strings.TrimSpace(line[:idx])
		val := strings.TrimSpace(line[idx+1:])
		// Eliminar comillas opcionales
		if len(val) >= 2 && val[0] == '"' && val[len(val)-1] == '"' {
			val = val[1 : len(val)-1]
		}
		env[key] = val
	}
	return env, scanner.Err()
}

func getEnvDefault(env map[string]string, key, def string) string {
	if v, ok := env[key]; ok && v != "" {
		return v
	}
	return def
}
