package handlers

import (
	"fmt"
	"net/http"
	"vigex/agent/winsvc"

	"github.com/go-chi/chi/v5"
)

type ServiceInfo struct {
	Name        string `json:"name"`
	DisplayName string `json:"display_name"`
	Status      string `json:"status"`
}

func ListServices(monitored []string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// Si hay lista configurada, usar esa; si no, listar todos los servicios en ejecucion
		var names []string
		if len(monitored) > 0 {
			names = monitored
		}
		services, err := winsvc.List(names)
		if err != nil {
			jsonError(w, http.StatusInternalServerError, fmt.Sprintf("error listando servicios: %v", err))
			return
		}
		result := make([]ServiceInfo, len(services))
		for i, s := range services {
			result[i] = ServiceInfo{Name: s.Name, DisplayName: s.DisplayName, Status: s.Status}
		}
		jsonOK(w, result)
	}
}

func ServiceAction() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		name := chi.URLParam(r, "name")
		action := chi.URLParam(r, "action")

		var err error
		switch action {
		case "start":
			err = winsvc.Start(name)
		case "stop":
			err = winsvc.Stop(name)
		case "restart":
			err = winsvc.Restart(name)
		default:
			jsonError(w, http.StatusBadRequest, fmt.Sprintf("accion desconocida: %s (start|stop|restart)", action))
			return
		}

		if err != nil {
			jsonError(w, http.StatusInternalServerError, fmt.Sprintf("error ejecutando %s en %s: %v", action, name, err))
			return
		}

		status, _ := winsvc.Status(name)
		jsonOK(w, map[string]any{
			"name":   name,
			"action": action,
			"status": status,
			"ok":     true,
		})
	}
}
