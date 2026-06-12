package handlers

import (
	"net/http"
	"os"
	"time"
	"vigex/agent/db"
)

var startTime = time.Now()

type HealthResponse struct {
	Status        string `json:"status"`
	Version       string `json:"version"`
	Hostname      string `json:"hostname"`
	DBBackend     string `json:"db_backend"`
	UptimeSeconds int64  `json:"uptime_seconds"`
}

func Health(backend db.Backend) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		host, _ := os.Hostname()
		resp := HealthResponse{
			Status:        "ok",
			Version:       "1.0.0",
			Hostname:      host,
			DBBackend:     backend.Name(),
			UptimeSeconds: int64(time.Since(startTime).Seconds()),
		}
		jsonOK(w, resp)
	}
}
