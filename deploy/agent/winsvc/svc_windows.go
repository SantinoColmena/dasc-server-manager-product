//go:build windows

package winsvc

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"time"

	"golang.org/x/sys/windows/svc"
	"golang.org/x/sys/windows/svc/mgr"
)

const ServiceName = "VigexAgent"
const ServiceDisplayName = "Vigex Agent"
const ServiceDesc = "Agente Vigex para la gestion remota del servidor Windows"

// IsWindowsService devuelve true si el proceso esta corriendo como servicio Windows.
func IsWindowsService() bool {
	ok, err := svc.IsWindowsService()
	return err == nil && ok
}

// Run ejecuta el agente como servicio Windows.
// startHTTP es la funcion que arranca el servidor HTTP; stopHTTP lo detiene.
func Run(startHTTP func(), stopHTTP func()) error {
	return svc.Run(ServiceName, &agentSvc{startHTTP: startHTTP, stopHTTP: stopHTTP})
}

type agentSvc struct {
	startHTTP func()
	stopHTTP  func()
}

func (s *agentSvc) Execute(_ []string, r <-chan svc.ChangeRequest, changes chan<- svc.Status) (bool, uint32) {
	changes <- svc.Status{State: svc.StartPending}
	go s.startHTTP()
	changes <- svc.Status{State: svc.Running, Accepts: svc.AcceptStop | svc.AcceptShutdown}

	for c := range r {
		switch c.Cmd {
		case svc.Stop, svc.Shutdown:
			changes <- svc.Status{State: svc.StopPending}
			s.stopHTTP()
			return false, 0
		case svc.Interrogate:
			changes <- c.CurrentStatus
		}
	}
	return false, 0
}

// Install registra el agente como servicio Windows de inicio automatico.
func Install() error {
	exePath, err := os.Executable()
	if err != nil {
		return fmt.Errorf("obteniendo ruta del ejecutable: %w", err)
	}
	exePath, err = filepath.Abs(exePath)
	if err != nil {
		return err
	}

	m, err := mgr.Connect()
	if err != nil {
		return fmt.Errorf("conectando al Service Manager: %w", err)
	}
	defer m.Disconnect()

	// Verificar si ya existe
	s, err := m.OpenService(ServiceName)
	if err == nil {
		s.Close()
		return fmt.Errorf("el servicio %s ya esta instalado", ServiceName)
	}

	s, err = m.CreateService(ServiceName, exePath, mgr.Config{
		DisplayName:  ServiceDisplayName,
		Description:  ServiceDesc,
		StartType:    mgr.StartAutomatic,
		ErrorControl: mgr.ErrorNormal,
	}, "run")
	if err != nil {
		return fmt.Errorf("creando servicio: %w", err)
	}
	defer s.Close()

	log.Printf("[svc] servicio %s instalado correctamente", ServiceName)
	return nil
}

// Uninstall elimina el servicio Windows.
func Uninstall() error {
	m, err := mgr.Connect()
	if err != nil {
		return fmt.Errorf("conectando al Service Manager: %w", err)
	}
	defer m.Disconnect()

	s, err := m.OpenService(ServiceName)
	if err != nil {
		return fmt.Errorf("servicio %s no encontrado: %w", ServiceName, err)
	}
	defer s.Close()

	// Detener antes de eliminar
	status, err := s.Query()
	if err == nil && status.State == svc.Running {
		s.Control(svc.Stop)
		time.Sleep(2 * time.Second)
	}

	if err := s.Delete(); err != nil {
		return fmt.Errorf("eliminando servicio: %w", err)
	}
	log.Printf("[svc] servicio %s eliminado", ServiceName)
	return nil
}

// StartService arranca el servicio instalado.
func StartService() error {
	m, err := mgr.Connect()
	if err != nil {
		return err
	}
	defer m.Disconnect()
	s, err := m.OpenService(ServiceName)
	if err != nil {
		return fmt.Errorf("servicio %s no encontrado", ServiceName)
	}
	defer s.Close()
	return s.Start()
}

// StopService detiene el servicio instalado.
func StopService() error {
	m, err := mgr.Connect()
	if err != nil {
		return err
	}
	defer m.Disconnect()
	s, err := m.OpenService(ServiceName)
	if err != nil {
		return fmt.Errorf("servicio %s no encontrado", ServiceName)
	}
	defer s.Close()
	_, err = s.Control(svc.Stop)
	return err
}
