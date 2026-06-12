package handlers

import (
	"encoding/json"
	"net/http"
)

const jsonContentType = "application/json; charset=utf-8"

func jsonOK(w http.ResponseWriter, data any) {
	w.Header().Set("Content-Type", jsonContentType)
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(data)
}

func jsonError(w http.ResponseWriter, status int, msg string) {
	w.Header().Set("Content-Type", jsonContentType)
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(map[string]string{"error": msg})
}
