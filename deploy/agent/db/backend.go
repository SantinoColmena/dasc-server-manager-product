package db

// BackupResult representa el resultado de una operacion de backup o restauracion.
type BackupResult struct {
	Filename  string  `json:"filename"`
	SizeMB    float64 `json:"size_mb"`
	CreatedAt string  `json:"created_at"`
	DBBackend string  `json:"db_backend"`
	Ok        bool    `json:"ok"`
}

// BackupFile es la informacion de un fichero de backup existente.
type BackupFile struct {
	Filename  string  `json:"filename"`
	SizeMB    float64 `json:"size_mb"`
	CreatedAt string  `json:"created_at"`
	Format    string  `json:"format"` // "sql.gz" | "bak"
	DBBackend string  `json:"db_backend"`
}

// RestoreResult representa el resultado de una restauracion.
type RestoreResult struct {
	Filename string `json:"filename"`
	Database string `json:"database"`
	DBBackend string `json:"db_backend"`
	Ok        bool   `json:"ok"`
}

// Backend define la interfaz que deben implementar todos los motores de BD.
type Backend interface {
	// Name devuelve el identificador del backend: "mysql", "sqlserver", "none"
	Name() string
	// CreateBackup crea un backup completo y devuelve metadata del fichero.
	CreateBackup() (*BackupResult, error)
	// RestoreBackup restaura desde un fichero de backup.
	RestoreBackup(filename string) (*RestoreResult, error)
	// ListBackups lista los backups disponibles en el directorio configurado.
	ListBackups() ([]BackupFile, error)
}
