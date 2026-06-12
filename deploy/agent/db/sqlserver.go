package db

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strings"
	"time"
)

// SqlServerBackend soporta SQL Server 2016/2019/2022 (Express, Standard, Enterprise).
type SqlServerBackend struct {
	Host      string
	Port      int
	User      string
	Pass      string
	BackupDir string
	Retention int
	// Instance es el nombre de la instancia (vacio = instancia por defecto MSSQLSERVER)
	Instance string
}

func (b *SqlServerBackend) Name() string { return "sqlserver" }

func (b *SqlServerBackend) CreateBackup() (*BackupResult, error) {
	if err := os.MkdirAll(b.BackupDir, 0750); err != nil {
		return nil, fmt.Errorf("creando directorio de backups: %w", err)
	}

	dbs, err := b.listDatabases()
	if err != nil {
		return nil, fmt.Errorf("listando bases de datos: %w", err)
	}

	ts := time.Now().UTC().Format("2006-01-02T15-04-05")
	var totalSize float64

	for _, dbName := range dbs {
		filename := fmt.Sprintf("vigex_backup_%s_%s.bak", dbName, ts)
		outPath := filepath.Join(b.BackupDir, filename)

		sql := fmt.Sprintf(
			`BACKUP DATABASE [%s] TO DISK = N'%s' WITH NOFORMAT, NOINIT, COMPRESSION, STATS = 10`,
			dbName, outPath,
		)
		if err := b.runSQL(sql); err != nil {
			return nil, fmt.Errorf("backup de %s: %w", dbName, err)
		}

		if info, err := os.Stat(outPath); err == nil {
			totalSize += float64(info.Size()) / (1024 * 1024)
		}
	}

	b.pruneOldBackups()

	return &BackupResult{
		Filename:  fmt.Sprintf("vigex_backup_%s_*.bak (%d bases de datos)", ts, len(dbs)),
		SizeMB:    totalSize,
		CreatedAt: time.Now().UTC().Format(time.RFC3339),
		DBBackend: "sqlserver",
		Ok:        true,
	}, nil
}

func (b *SqlServerBackend) RestoreBackup(filename string) (*RestoreResult, error) {
	backupPath := filepath.Join(b.BackupDir, filepath.Base(filename))
	if _, err := os.Stat(backupPath); err != nil {
		return nil, fmt.Errorf("fichero de backup no encontrado: %s", filename)
	}

	// Extraer nombre de BD del nombre de fichero: vigex_backup_<DB>_<TS>.bak
	base := strings.TrimSuffix(filepath.Base(filename), ".bak")
	parts := strings.Split(base, "_")
	if len(parts) < 3 {
		return nil, fmt.Errorf("nombre de fichero de backup no reconocido: %s", filename)
	}
	// formato: vigex_backup_DBNAME_TS
	// partes: ["vigex", "backup", "DBNAME", "TS"]
	dbName := parts[2]

	sql := fmt.Sprintf(
		`RESTORE DATABASE [%s] FROM DISK = N'%s' WITH REPLACE, STATS = 10`,
		dbName, backupPath,
	)
	if err := b.runSQL(sql); err != nil {
		return nil, fmt.Errorf("restore de %s: %w", dbName, err)
	}

	return &RestoreResult{
		Filename:  filename,
		Database:  dbName,
		DBBackend: "sqlserver",
		Ok:        true,
	}, nil
}

func (b *SqlServerBackend) ListBackups() ([]BackupFile, error) {
	return listBackupFiles(b.BackupDir, ".bak", "sqlserver", "bak")
}

// listDatabases devuelve las bases de datos de usuario (excluye las del sistema).
func (b *SqlServerBackend) listDatabases() ([]string, error) {
	sql := `SET NOCOUNT ON; SELECT name FROM sys.databases WHERE database_id > 4 AND state_desc = 'ONLINE'`
	out, err := b.runSQLOutput(sql)
	if err != nil {
		return nil, err
	}
	var dbs []string
	for _, line := range strings.Split(strings.TrimSpace(out), "\n") {
		if t := strings.TrimSpace(line); t != "" {
			dbs = append(dbs, t)
		}
	}
	return dbs, nil
}

func (b *SqlServerBackend) runSQL(sql string) error {
	_, err := b.runSQLOutput(sql)
	return err
}

func (b *SqlServerBackend) runSQLOutput(sql string) (string, error) {
	sqlcmd, err := findSqlCmd()
	if err != nil {
		return "", err
	}

	args := []string{
		"-S", b.serverArg(),
		"-U", b.User,
		"-P", b.Pass,
		"-Q", sql,
		"-W",  // quita espacios de relleno
		"-h", "-1", // sin cabecera
	}

	cmd := exec.Command(sqlcmd, args...)
	out, err := cmd.Output()
	if err != nil {
		return "", fmt.Errorf("sqlcmd: %w", err)
	}
	return strings.TrimSpace(string(out)), nil
}

func (b *SqlServerBackend) serverArg() string {
	host := b.Host
	if b.Instance != "" {
		host = host + `\` + b.Instance
	}
	if b.Port > 0 {
		host = fmt.Sprintf("%s,%d", host, b.Port)
	}
	return host
}

func (b *SqlServerBackend) pruneOldBackups() {
	if b.Retention <= 0 {
		return
	}
	files, err := filepath.Glob(filepath.Join(b.BackupDir, "vigex_backup_*.bak"))
	if err != nil || len(files) <= b.Retention {
		return
	}
	sort.Strings(files)
	for _, f := range files[:len(files)-b.Retention] {
		os.Remove(f)
	}
}

func findSqlCmd() (string, error) {
	if p, err := exec.LookPath("sqlcmd.exe"); err == nil {
		return p, nil
	}
	// Buscar en ubicaciones tipicas de SQL Server
	bases := []string{
		`C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn`,
		`C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\130\Tools\Binn`,
		`C:\Program Files\Microsoft SQL Server\110\Tools\Binn`,
	}
	for _, base := range bases {
		p := filepath.Join(base, "sqlcmd.exe")
		if _, err := os.Stat(p); err == nil {
			return p, nil
		}
	}
	return "", fmt.Errorf("sqlcmd.exe no encontrado; instala SQL Server Management Studio o las SQL Server Command Line Utilities")
}
