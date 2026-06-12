package handlers

import (
	"fmt"
	"net/http"
	"vigex/agent/db"
)

func ListBackups(backend db.Backend) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		backups, err := backend.ListBackups()
		if err != nil {
			jsonError(w, http.StatusInternalServerError, fmt.Sprintf("error listando backups: %v", err))
			return
		}
		jsonOK(w, backups)
	}
}

func CreateBackup(backend db.Backend) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		result, err := backend.CreateBackup()
		if err != nil {
			jsonError(w, http.StatusInternalServerError, fmt.Sprintf("error creando backup: %v", err))
			return
		}
		jsonOK(w, result)
	}
}

func RestoreBackup(backend db.Backend) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		filename := r.URL.Query().Get("filename")
		if filename == "" {
			jsonError(w, http.StatusBadRequest, "parametro 'filename' requerido")
			return
		}
		result, err := backend.RestoreBackup(filename)
		if err != nil {
			jsonError(w, http.StatusInternalServerError, fmt.Sprintf("error restaurando backup: %v", err))
			return
		}
		jsonOK(w, result)
	}
}
