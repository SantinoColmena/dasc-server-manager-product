package db

import "fmt"

// NoBackend se usa cuando no se detecta ningun motor de base de datos.
type NoBackend struct{}

func (b *NoBackend) Name() string { return "none" }

func (b *NoBackend) CreateBackup() (*BackupResult, error) {
	return nil, fmt.Errorf("no hay motor de base de datos configurado en este servidor")
}

func (b *NoBackend) RestoreBackup(_ string) (*RestoreResult, error) {
	return nil, fmt.Errorf("no hay motor de base de datos configurado en este servidor")
}

func (b *NoBackend) ListBackups() ([]BackupFile, error) {
	return []BackupFile{}, nil
}
