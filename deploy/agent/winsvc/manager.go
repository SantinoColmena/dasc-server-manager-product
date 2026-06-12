package winsvc

import (
	"fmt"
	"os/exec"
	"strings"
)

type Service struct {
	Name        string
	DisplayName string
	Status      string
}

// Status devuelve el estado de un servicio Windows ("running", "stopped", "unknown").
func Status(name string) (string, error) {
	out, err := exec.Command("sc", "query", name).Output()
	if err != nil {
		return "unknown", fmt.Errorf("sc query %s: %w", name, err)
	}
	s := string(out)
	switch {
	case strings.Contains(s, "RUNNING"):
		return "running", nil
	case strings.Contains(s, "STOPPED"):
		return "stopped", nil
	case strings.Contains(s, "PAUSED"):
		return "paused", nil
	case strings.Contains(s, "START_PENDING"):
		return "starting", nil
	case strings.Contains(s, "STOP_PENDING"):
		return "stopping", nil
	default:
		return "unknown", nil
	}
}

// Start arranca un servicio Windows.
func Start(name string) error {
	out, err := exec.Command("sc", "start", name).CombinedOutput()
	if err != nil {
		// "ya en ejecucion" no es un error real
		if strings.Contains(string(out), "1056") || strings.Contains(string(out), "already running") {
			return nil
		}
		return fmt.Errorf("sc start %s: %w — %s", name, err, string(out))
	}
	return nil
}

// Stop detiene un servicio Windows.
func Stop(name string) error {
	out, err := exec.Command("sc", "stop", name).CombinedOutput()
	if err != nil {
		// "ya detenido" no es un error real
		if strings.Contains(string(out), "1062") || strings.Contains(string(out), "not started") {
			return nil
		}
		return fmt.Errorf("sc stop %s: %w — %s", name, err, string(out))
	}
	return nil
}

// Restart detiene y arranca un servicio.
func Restart(name string) error {
	_ = Stop(name)
	return Start(name)
}

// List devuelve informacion de los servicios indicados.
// Si names esta vacio, devuelve todos los servicios en ejecucion.
func List(names []string) ([]Service, error) {
	if len(names) > 0 {
		return listNamed(names)
	}
	return listRunning()
}

func listNamed(names []string) ([]Service, error) {
	var services []Service
	for _, name := range names {
		status, _ := Status(name)
		displayName := getDisplayName(name)
		services = append(services, Service{
			Name:        name,
			DisplayName: displayName,
			Status:      status,
		})
	}
	return services, nil
}

func listRunning() ([]Service, error) {
	out, err := exec.Command("sc", "query", "type=", "all", "state=", "running").Output()
	if err != nil {
		return nil, fmt.Errorf("sc query all running: %w", err)
	}
	return parseSCOutput(string(out)), nil
}

func getDisplayName(name string) string {
	out, err := exec.Command("sc", "qc", name).Output()
	if err != nil {
		return name
	}
	for _, line := range strings.Split(string(out), "\n") {
		if strings.Contains(line, "DISPLAY_NAME") {
			parts := strings.SplitN(line, ":", 2)
			if len(parts) == 2 {
				return strings.TrimSpace(parts[1])
			}
		}
	}
	return name
}

func parseSCOutput(output string) []Service {
	var services []Service
	var current Service
	for _, line := range strings.Split(output, "\n") {
		line = strings.TrimSpace(line)
		if strings.HasPrefix(line, "SERVICE_NAME:") {
			if current.Name != "" {
				services = append(services, current)
			}
			current = Service{
				Name:   strings.TrimSpace(strings.TrimPrefix(line, "SERVICE_NAME:")),
				Status: "running",
			}
		} else if strings.HasPrefix(line, "DISPLAY_NAME:") {
			current.DisplayName = strings.TrimSpace(strings.TrimPrefix(line, "DISPLAY_NAME:"))
		}
	}
	if current.Name != "" {
		services = append(services, current)
	}
	return services
}
