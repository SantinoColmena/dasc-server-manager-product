package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
	"vigex/agent/db"
	"vigex/agent/handlers"
	"vigex/agent/winsvc"

	"github.com/go-chi/chi/v5"
	chimw "github.com/go-chi/chi/v5/middleware"
)

const version = "1.0.0"

func main() {
	log.SetFlags(log.Ldate | log.Ltime | log.Lmsgprefix)
	log.SetPrefix("[vigex-agent] ")

	// Subcomandos de gestion del servicio Windows
	if len(os.Args) > 1 {
		handleSubcommand(os.Args[1])
		return
	}

	// Sin argumentos: ejecutar como servicio si aplica, o en primer plano
	cfg, err := loadConfig()
	if err != nil {
		log.Fatalf("configuracion invalida: %v", err)
	}

	backend := db.Detect(db.Config{
		Backend:   cfg.DBBackend,
		Host:      cfg.DBHost,
		Port:      cfg.DBPort,
		User:      cfg.DBUser,
		Pass:      cfg.DBPass,
		BackupDir: cfg.BackupDir,
		Retention: cfg.BackupRetention,
	})

	srv := buildServer(cfg, backend)

	if winsvc.IsWindowsService() {
		// Modo servicio Windows
		log.Println("iniciando como servicio Windows")
		err = winsvc.Run(
			func() {
				if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
					log.Printf("error en servidor HTTP: %v", err)
				}
			},
			func() {
				ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
				defer cancel()
				srv.Shutdown(ctx)
			},
		)
		if err != nil {
			log.Fatalf("error en servicio Windows: %v", err)
		}
		return
	}

	// Modo primer plano (desarrollo / manual)
	runForeground(srv, cfg.Port)
}

func buildServer(cfg *Config, backend db.Backend) *http.Server {
	r := chi.NewRouter()
	r.Use(chimw.Logger)
	r.Use(chimw.Recoverer)
	r.Use(chimw.RealIP)

	// /health es publico (para healthchecks del panel sin token)
	r.Get("/health", handlers.Health(backend))

	// Todas las demas rutas requieren autenticacion
	r.Group(func(r chi.Router) {
		r.Use(authMiddleware(cfg.Token))

		r.Get("/api/v1/system", handlers.System())
		r.Get("/api/v1/disk", handlers.Disk())

		r.Get("/api/v1/services", handlers.ListServices(cfg.MonitoredServices))
		r.Post("/api/v1/services/{name}/{action}", handlers.ServiceAction())

		r.Get("/api/v1/backups", handlers.ListBackups(backend))
		r.Post("/api/v1/backups/create", handlers.CreateBackup(backend))
		r.Post("/api/v1/backups/restore", handlers.RestoreBackup(backend))

		r.Get("/api/v1/logs", handlers.Logs())
	})

	return &http.Server{
		Addr:         fmt.Sprintf(":%d", cfg.Port),
		Handler:      r,
		ReadTimeout:  30 * time.Second,
		WriteTimeout: 300 * time.Second, // backups pueden tardar
		IdleTimeout:  60 * time.Second,
	}
}

func runForeground(srv *http.Server, port int) {
	log.Printf("Vigex Agent v%s escuchando en :%d", version, port)
	log.Println("CTRL+C para detener")

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt, syscall.SIGTERM)

	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("error fatal: %v", err)
		}
	}()

	<-stop
	log.Println("deteniendo agente...")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	srv.Shutdown(ctx)
	log.Println("agente detenido")
}

func handleSubcommand(cmd string) {
	switch cmd {
	case "install":
		if err := winsvc.Install(); err != nil {
			log.Fatalf("error instalando servicio: %v", err)
		}
		fmt.Println("Servicio VigexAgent instalado. Usa 'VigexAgent.exe start' para arrancarlo.")
	case "uninstall":
		if err := winsvc.Uninstall(); err != nil {
			log.Fatalf("error desinstalando servicio: %v", err)
		}
		fmt.Println("Servicio VigexAgent eliminado.")
	case "start":
		if err := winsvc.StartService(); err != nil {
			log.Fatalf("error arrancando servicio: %v", err)
		}
		fmt.Println("Servicio VigexAgent arrancado.")
	case "stop":
		if err := winsvc.StopService(); err != nil {
			log.Fatalf("error deteniendo servicio: %v", err)
		}
		fmt.Println("Servicio VigexAgent detenido.")
	case "run":
		// Forzar modo primer plano aunque se llame desde un servicio
		cfg, err := loadConfig()
		if err != nil {
			log.Fatalf("configuracion invalida: %v", err)
		}
		backend := db.Detect(db.Config{
			Backend: cfg.DBBackend, Host: cfg.DBHost, Port: cfg.DBPort,
			User: cfg.DBUser, Pass: cfg.DBPass,
			BackupDir: cfg.BackupDir, Retention: cfg.BackupRetention,
		})
		runForeground(buildServer(cfg, backend), cfg.Port)
	case "version":
		fmt.Printf("Vigex Agent v%s\n", version)
	default:
		fmt.Fprintf(os.Stderr, "Uso: VigexAgent.exe [install|uninstall|start|stop|run|version]\n")
		os.Exit(1)
	}
}
