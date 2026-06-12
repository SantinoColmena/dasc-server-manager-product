package db

import (
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"time"
)

type fileInfo struct {
	Name    string
	SizeMB  float64
	ModTime string
}

func statFile(path string) (*fileInfo, error) {
	info, err := os.Stat(path)
	if err != nil {
		return nil, err
	}
	return &fileInfo{
		Name:    filepath.Base(path),
		SizeMB:  float64(info.Size()) / (1024 * 1024),
		ModTime: info.ModTime().UTC().Format(time.RFC3339),
	}, nil
}

func listGlob(pattern string) ([]string, error) {
	// Normalizar separadores
	pattern = filepath.FromSlash(pattern)
	matches, err := filepath.Glob(pattern)
	if err != nil {
		return nil, fmt.Errorf("listando backups: %w", err)
	}
	// Ordenar por nombre descendente (mas recientes primero)
	sort.Sort(sort.Reverse(sort.StringSlice(matches)))
	return matches, nil
}
