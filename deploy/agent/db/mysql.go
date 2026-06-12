package db

import (
	"compress/gzip"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strings"
	"time"
)

// MySQLBackend soporta MySQL 5.7/8.x y MariaDB 10.x para Windows.
type MySQLBackend struct {
	Host      string
	Port      int
	User      string
	Pass      string
	BackupDir string
	Retention int
}

func (b *MySQLBackend) Name() string { return "mysql" }

func (b *MySQLBackend) CreateBackup() (*BackupResult, error) {
	if err := os.MkdirAll(b.BackupDir, 0750); err != nil {
		return nil, fmt.Errorf("creando directorio de backups: %w", err)
	}

	mysqldump, err := findMySQLDump()
	if err != nil {
		return nil, err
	}

	ts := time.Now().UTC().Format("2006-01-02T15-04-05")
	filename := fmt.Sprintf("vigex_backup_%s.sql.gz", ts)
	outPath := filepath.Join(b.BackupDir, filename)

	args := b.buildArgs("--all-databases", "--single-transaction", "--routines", "--events")
	cmd := exec.Command(mysqldump, args...)

	// Comprimir el output directamente con gzip
	outFile, err := os.Create(outPath)
	if err != nil {
		return nil, fmt.Errorf("creando fichero de backup: %w", err)
	}
	defer outFile.Close()

	gz := gzip.NewWriter(outFile)
	defer gz.Close()

	cmd.Stdout = gz
	var stderrBuf strings.Builder
	cmd.Stderr = &stderrBuf

	if err := cmd.Run(); err != nil {
		os.Remove(outPath)
		return nil, fmt.Errorf("mysqldump: %w\n%s", err, stderrBuf.String())
	}
	gz.Close()

	info, _ := os.Stat(outPath)
	sizeMB := 0.0
	if info != nil {
		sizeMB = float64(info.Size()) / (1024 * 1024)
	}

	b.pruneOldBackups()

	return &BackupResult{
		Filename:  filename,
		SizeMB:    sizeMB,
		CreatedAt: time.Now().UTC().Format(time.RFC3339),
		DBBackend: "mysql",
		Ok:        true,
	}, nil
}

func (b *MySQLBackend) RestoreBackup(filename string) (*RestoreResult, error) {
	backupPath := filepath.Join(b.BackupDir, filepath.Base(filename))
	if _, err := os.Stat(backupPath); err != nil {
		return nil, fmt.Errorf("fichero de backup no encontrado: %s", filename)
	}

	mysql, err := findMySQL()
	if err != nil {
		return nil, err
	}

	f, err := os.Open(backupPath)
	if err != nil {
		return nil, fmt.Errorf("abriendo backup: %w", err)
	}
	defer f.Close()

	var reader io.Reader = f
	if strings.HasSuffix(filename, ".gz") {
		gz, err := gzip.NewReader(f)
		if err != nil {
			return nil, fmt.Errorf("descomprimiendo backup: %w", err)
		}
		defer gz.Close()
		reader = gz
	}

	args := b.buildArgs()
	cmd := exec.Command(mysql, args...)
	cmd.Stdin = reader

	if out, err := cmd.CombinedOutput(); err != nil {
		return nil, fmt.Errorf("mysql restore: %w\n%s", err, string(out))
	}

	return &RestoreResult{
		Filename:  filename,
		Database:  "all",
		DBBackend: "mysql",
		Ok:        true,
	}, nil
}

func (b *MySQLBackend) ListBackups() ([]BackupFile, error) {
	return listBackupFiles(b.BackupDir, ".sql.gz", "mysql", "sql.gz")
}

func (b *MySQLBackend) buildArgs(extra ...string) []string {
	args := []string{
		fmt.Sprintf("--host=%s", b.Host),
		fmt.Sprintf("--user=%s", b.User),
		fmt.Sprintf("--password=%s", b.Pass),
	}
	if b.Port > 0 {
		args = append(args, fmt.Sprintf("--port=%d", b.Port))
	}
	return append(args, extra...)
}

func (b *MySQLBackend) pruneOldBackups() {
	if b.Retention <= 0 {
		return
	}
	files, err := filepath.Glob(filepath.Join(b.BackupDir, "vigex_backup_*.sql.gz"))
	if err != nil || len(files) <= b.Retention {
		return
	}
	sort.Strings(files)
	for _, f := range files[:len(files)-b.Retention] {
		os.Remove(f)
	}
}

// findMySQLDump busca mysqldump.exe en los paths habituales de MySQL y MariaDB.
func findMySQLDump() (string, error) {
	return findMySQLBin("mysqldump")
}

func findMySQL() (string, error) {
	return findMySQLBin("mysql")
}

func findMySQLBin(name string) (string, error) {
	// Primero intentar desde el PATH
	if p, err := exec.LookPath(name + ".exe"); err == nil {
		return p, nil
	}
	// Buscar en ubicaciones tipicas de MySQL y MariaDB en Windows
	candidates := []string{
		`C:\Program Files\MySQL\MySQL Server 8.4\bin\` + name + `.exe`,
		`C:\Program Files\MySQL\MySQL Server 8.0\bin\` + name + `.exe`,
		`C:\Program Files\MySQL\MySQL Server 5.7\bin\` + name + `.exe`,
		`C:\Program Files\MariaDB 11.4\bin\` + name + `.exe`,
		`C:\Program Files\MariaDB 10.11\bin\` + name + `.exe`,
		`C:\Program Files\MariaDB 10.6\bin\` + name + `.exe`,
	}
	for _, c := range candidates {
		if _, err := os.Stat(c); err == nil {
			return c, nil
		}
	}
	return "", fmt.Errorf("%s.exe no encontrado; asegurate de que MySQL o MariaDB esta instalado y en el PATH", name)
}
