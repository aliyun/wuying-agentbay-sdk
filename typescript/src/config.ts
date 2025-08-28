import * as fs from "fs";
import * as path from "path";
import * as dotenv from "dotenv";
import { log } from "./utils/logger";
interface Config {
  region_id: string;
  endpoint: string;
  timeout_ms: number;
}

/**
 * Browser data path constant
 */
export const BROWSER_DATA_PATH = "/tmp/agentbay_browser";

/**
 * Returns the default configuration
 */
export function defaultConfig(): Config {
  return {
    region_id: "cn-shanghai",
    endpoint: "wuyingai.cn-shanghai.aliyuncs.com",
    timeout_ms: 60000,
  };
}

/**
 * Load .env file into process.env if it exists
 * This function should be called early to ensure .env variables are available
 */
export function loadDotEnv(): void {
  try {
    const envPath = path.resolve(process.cwd(), ".env");
    if (fs.existsSync(envPath)) {
      const envConfig = dotenv.parse(fs.readFileSync(envPath));
      for (const k in envConfig) {
        // only load env variables that are not already set in process.env
        if (!process.env.hasOwnProperty(k)) {
          process.env[k] = envConfig[k];
        }
      }
      log(`Loaded .env file at: ${envPath}`);
    }
  } catch (error) {
    log(`Warning: Failed to load .env file: ${error}`);
  }
}

/**
 * The SDK uses the following precedence order for configuration (highest to lowest):
 * 1. Explicitly passed configuration in code.
 * 2. Environment variables.
 * 3. .env file.
 * 4. Default configuration.
 */
export function loadConfig(customConfig?: Config): Config {
  // If custom config is provided, use it directly
  if (customConfig) {
    return customConfig;
  }

  // Create base config from default values
  const config = defaultConfig();

  // Override with environment variables if they exist
  // Note: .env file should already be loaded by loadDotEnv() before this function is called
  if (process.env.AGENTBAY_REGION_ID) {
    config.region_id = process.env.AGENTBAY_REGION_ID;
  }

  if (process.env.AGENTBAY_ENDPOINT) {
    config.endpoint = process.env.AGENTBAY_ENDPOINT;
  }

  if (process.env.AGENTBAY_TIMEOUT_MS) {
    const timeout = parseInt(process.env.AGENTBAY_TIMEOUT_MS, 10);
    if (!isNaN(timeout) && timeout > 0) {
      config.timeout_ms = timeout;
    }
  }

  return config;
}

export { Config };
