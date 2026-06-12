//go:build !windows

// Stubs para compilar en Linux/macOS durante desarrollo.
package winsvc

import "fmt"

const ServiceName = "VigexAgent"

func IsWindowsService() bool  { return false }
func Run(_, _ func()) error   { return fmt.Errorf("Windows service solo disponible en Windows") }
func Install() error          { return fmt.Errorf("solo disponible en Windows") }
func Uninstall() error        { return fmt.Errorf("solo disponible en Windows") }
func StartService() error     { return fmt.Errorf("solo disponible en Windows") }
func StopService() error      { return fmt.Errorf("solo disponible en Windows") }
