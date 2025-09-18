// Copyright 2025 Alibaba Cloud
// SPDX-License-Identifier: Apache-2.0

package main

import (
	"context"
	"fmt"
	"io"
	"os"
	"os/signal"
	"path/filepath"
	"syscall"
	"time"

	golog "log"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/agent"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/application"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/code"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/command"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/filesystem"
	"github.com/joho/godotenv"

	"github.com/rs/zerolog"
	zlog "github.com/rs/zerolog/log"

	log "github.com/sirupsen/logrus"
)

// AgentBayServer represents the main server instance
type AgentBayServer struct {
	agentBay        *agentbay.AgentBay
	contextManager  *agentbay.ContextManager
	sessionManager  *SessionManager
	agentService    *agent.Agent
	applicationSvc  *application.ApplicationManager
	codeService     *code.Code
	commandService  *command.Command
	filesystemSvc   *filesystem.FileSystem
	ctx             context.Context
	cancel          context.CancelFunc
}

// SessionManager manages active sessions
type SessionManager struct {
	sessions map[string]*agentbay.Session
}

// NewSessionManager creates a new session manager
func NewSessionManager() *SessionManager {
	return &SessionManager{
		sessions: make(map[string]*agentbay.Session),
	}
}

func main() {
	// Load configuration
	cfg := agentbay.LoadConfig(nil)

	log.Infof("Starting AgentBay Server with config: RegionID=%s, Endpoint=%s", cfg.RegionID, cfg.Endpoint)

	// Get API key from environment
	apiKey := os.Getenv("AGENTBAY_API_KEY")
	if apiKey == "" {
		log.Errorf("AGENTBAY_API_KEY environment variable is required")
		return
	}

	// Create AgentBay client
	agentBayClient, err := agentbay.NewAgentBay(apiKey, agentbay.WithConfig(&cfg))
	if err != nil {
		log.Errorf("Failed to create AgentBay client: %v", err)
		return
	}

	log.Info("AgentBay client initialized successfully")

	// Create context with cancellation
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Initialize session manager
	sessionManager := NewSessionManager()

	// Create a demo session for service initialization
	// In a real application, you would create sessions as needed
	sessionResult, err := agentBayClient.Create(nil)
	if err != nil {
		log.Warnf("Failed to create demo session for service initialization: %v", err)
		// Continue without services that require a session
	}

	var demoSession *agentbay.Session
	var contextManager *agentbay.ContextManager
	if sessionResult != nil {
		demoSession = sessionResult.Session
		// Initialize context manager with the session (not the AgentBay client)
		contextManager = agentbay.NewContextManager(demoSession)
	}

	// Initialize services (these require a session)
	var agentService *agent.Agent
	var applicationSvc *application.ApplicationManager
	var codeService *code.Code
	var commandService *command.Command
	var filesystemSvc *filesystem.FileSystem

	if demoSession != nil {
		agentService = agent.NewAgent(demoSession)
		applicationSvc = application.NewApplicationManager(demoSession)
		codeService = code.NewCode(demoSession)
		commandService = command.NewCommand(demoSession)
		filesystemSvc = filesystem.NewFileSystem(demoSession)
		log.Info("All services initialized successfully")
	} else {
		log.Warn("Services requiring session not initialized due to session creation failure")
	}

	// Create server instance
	server := &AgentBayServer{
		agentBay:       agentBayClient,
		contextManager: contextManager,
		sessionManager: sessionManager,
		agentService:   agentService,
		applicationSvc: applicationSvc,
		codeService:    codeService,
		commandService: commandService,
		filesystemSvc:  filesystemSvc,
		ctx:            ctx,
		cancel:         cancel,
	}

	// Start background services
	go server.startBackgroundServices()

	// Start session cleanup routine
	go server.startSessionCleanup()

	// Start context synchronization service
	go server.startContextSync()

	log.Info("AgentBay Server started successfully")

	// Set up signal handling
	interruptChannel := make(chan os.Signal, 1)
	signal.Notify(interruptChannel, os.Interrupt, syscall.SIGTERM)

	// Wait for interrupt signal
	<-interruptChannel
	log.Info("Received interrupt signal, shutting down gracefully...")

	// Graceful shutdown
	server.shutdown()
	log.Info("AgentBay Server shutdown complete")
}

// startBackgroundServices starts various background services
func (s *AgentBayServer) startBackgroundServices() {
	ticker := time.NewTicker(30 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-s.ctx.Done():
			log.Info("Background services stopped")
			return
		case <-ticker.C:
			// Perform periodic health checks
			s.performHealthCheck()
		}
	}
}

// startSessionCleanup starts the session cleanup routine
func (s *AgentBayServer) startSessionCleanup() {
	ticker := time.NewTicker(5 * time.Minute)
	defer ticker.Stop()

	for {
		select {
		case <-s.ctx.Done():
			log.Info("Session cleanup stopped")
			return
		case <-ticker.C:
			s.cleanupInactiveSessions()
		}
	}
}

// startContextSync starts the context synchronization service
func (s *AgentBayServer) startContextSync() {
	ticker := time.NewTicker(1 * time.Minute)
	defer ticker.Stop()

	for {
		select {
		case <-s.ctx.Done():
			log.Info("Context sync service stopped")
			return
		case <-ticker.C:
			s.syncContexts()
		}
	}
}

// performHealthCheck performs periodic health checks
func (s *AgentBayServer) performHealthCheck() {
	log.Debug("Performing health check...")

	// Check if AgentBay client is still healthy
	if s.agentBay == nil {
		log.Warn("AgentBay client is nil")
		return
	}

	// Check active sessions count
	activeSessionsCount := len(s.sessionManager.sessions)
	log.Debugf("Active sessions: %d", activeSessionsCount)

	// Check service availability
	servicesAvailable := 0
	if s.agentService != nil {
		servicesAvailable++
	}
	if s.applicationSvc != nil {
		servicesAvailable++
	}
	if s.codeService != nil {
		servicesAvailable++
	}
	if s.commandService != nil {
		servicesAvailable++
	}
	if s.filesystemSvc != nil {
		servicesAvailable++
	}

	log.Debugf("Services available: %d/5", servicesAvailable)
	log.Debug("Health check completed")
}

// cleanupInactiveSessions cleans up inactive sessions
func (s *AgentBayServer) cleanupInactiveSessions() {
	log.Debug("Cleaning up inactive sessions...")

	for sessionID, session := range s.sessionManager.sessions {
		// Check if session is still active (this is a placeholder logic)
		if session == nil {
			delete(s.sessionManager.sessions, sessionID)
			log.Infof("Cleaned up inactive session: %s", sessionID)
		}
	}

	log.Debug("Session cleanup completed")
}

// syncContexts synchronizes contexts
func (s *AgentBayServer) syncContexts() {
	log.Debug("Synchronizing contexts...")

	if s.contextManager != nil {
		// Perform context synchronization
		_, err := s.contextManager.Sync()
		if err != nil {
			log.Errorf("Context synchronization failed: %v", err)
		} else {
			log.Debug("Context synchronization completed")
		}
	}
}

// shutdown performs graceful shutdown
func (s *AgentBayServer) shutdown() {
	log.Info("Starting graceful shutdown...")

	// Cancel context to stop all background services
	s.cancel()

	// Clean up all active sessions
	for sessionID, session := range s.sessionManager.sessions {
		if session != nil {
			log.Infof("Cleaning up session: %s", sessionID)
			_, err := s.agentBay.Delete(session, false)
			if err != nil {
				log.Errorf("Failed to delete session %s: %v", sessionID, err)
			}
		}
	}

	// Additional cleanup can be added here
	log.Info("Graceful shutdown completed")
}

func init() {
	// Load .env file
	err := godotenv.Load()
	if err != nil {
		log.Printf("Warning: Error loading .env file: %v", err)
		// Continue anyway, as environment variables might be set directly
	}

	// Set up logging
	logLevel := log.InfoLevel

	logLevelEnv, logLevelSet := os.LookupEnv("LOG_LEVEL")
	if logLevelSet {
		var err error
		logLevel, err = log.ParseLevel(logLevelEnv)
		if err != nil {
			log.Warnf("Failed to parse log level '%s', using InfoLevel: %v", logLevelEnv, err)
			logLevel = log.InfoLevel
		}
	}

	log.SetLevel(logLevel)
	log.SetOutput(os.Stdout)
	log.SetFormatter(&log.TextFormatter{
		FullTimestamp: true,
		TimestampFormat: time.RFC3339,
	})

	// Set up log file if specified
	logFilePath, logFilePathSet := os.LookupEnv("LOG_FILE_PATH")
	if logFilePathSet {
		logDir := filepath.Dir(logFilePath)

		if err := os.MkdirAll(logDir, 0755); err != nil {
			log.Errorf("Failed to create log directory: %v", err)
			os.Exit(1)
		}

		file, err := os.OpenFile(logFilePath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
		if err != nil {
			log.Errorf("Failed to open log file: %v", err)
			os.Exit(1)
		}

		log.SetOutput(io.MultiWriter(os.Stdout, file))
	}

	// Set up zerolog
	zerologLevel, err := zerolog.ParseLevel(logLevel.String())
	if err != nil {
		log.Warnf("Failed to parse zerolog level, using InfoLevel: %v", err)
		zerologLevel = zerolog.InfoLevel
	}

	zerolog.SetGlobalLevel(zerologLevel)
	zerolog.TimeFieldFormat = zerolog.TimeFormatUnix

	zlog.Logger = zlog.Output(zerolog.ConsoleWriter{
		Out:        os.Stdout,
		TimeFormat: time.RFC3339,
	})

	// Set standard log output to use our custom writer
	golog.SetOutput(os.Stdout)
	golog.SetFlags(golog.LstdFlags | golog.Lshortfile)

	// Print startup banner
	fmt.Println("╔══════════════════════════════════════════════════════════════╗")
	fmt.Println("║                        AgentBay Server                       ║")
	fmt.Println("║                   Alibaba Cloud AgentBay SDK                 ║")
	fmt.Println("║              https://agentbay.console.aliyun.com             ║")
	fmt.Println("╚══════════════════════════════════════════════════════════════╝")
	fmt.Println()
}
