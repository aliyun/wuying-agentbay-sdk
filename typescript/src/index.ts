// IMPORTANT: Load config first to ensure .env file is loaded before logger initialization
export { loadConfig, loadDotEnv, type Config } from "./config";

// Export all public classes and interfaces
export { AgentBay, type CreateSessionParams} from "./agent-bay";
export * from "./agent";
export * from "./api";
export * from "./application";
export * from "./browser";
export * from "./command";
export { Context, ContextService } from "./context";
export * from "./exceptions";
export * from "./extension";
export * from "./filesystem";
export * from "./oss";
export { Session } from "./session";
export { type ListSessionParams } from "./types";
export * from "./types";
export * from "./ui";
export * from './context-sync'
export * from './context-manager'
export * from './session-params'
// Export utility functions
export {
  log,
  logDebug,
  logInfo,
  logWarn,
  logError,
  setLogLevel,
  getLogLevel,
  maskSensitiveData,
  setupLogger,
  type LogLevel,
  type LoggerConfig
} from "./utils/logger";
