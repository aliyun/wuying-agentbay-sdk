/**
 * Base exception for all AgentBay errors.
 */
export class AgentBayError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "AgentBayError";
    Object.setPrototypeOf(this, AgentBayError.prototype);
  }
}

/**
 * Raised when there is an authentication error.
 */
export class AuthenticationError extends AgentBayError {
  constructor(message: string) {
    super(message);
    this.name = "AuthenticationError";
    Object.setPrototypeOf(this, AuthenticationError.prototype);
  }
}

/**
 * Raised when there is an error with the API.
 */
export class APIError extends AgentBayError {
  constructor(message: string) {
    super(message);
    this.name = "APIError";
    Object.setPrototypeOf(this, APIError.prototype);
  }
}

/**
 * Raised when there is an error with file operations.
 */
export class FileError extends AgentBayError {
  constructor(message: string) {
    super(message);
    this.name = "FileError";
    Object.setPrototypeOf(this, FileError.prototype);
  }
}

/**
 * Raised when there is an error with command execution.
 */
export class CommandError extends AgentBayError {
  constructor(message: string) {
    super(message);
    this.name = "CommandError";
    Object.setPrototypeOf(this, CommandError.prototype);
  }
}
