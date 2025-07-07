import * as fs from "fs";
import * as path from "path";
import "dotenv/config";
import { log } from "./utils/logger";
interface Config {
  region_id: string;
  endpoint: string;
  timeout_ms: number;
}

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
 * Loads configuration from file
 */
export function loadConfig(customConfig?: Config): Config {
  // If custom config is provided, use it directly
  if (customConfig) {
    return { ...defaultConfig(), ...customConfig };
  }

  // Create base config from default values
  const config = defaultConfig();
  
  // Try to load .env file
  const envPath = path.resolve(process.cwd(), '.env');
  if (fs.existsSync(envPath)) {
    // dotenv is imported in the top of the file with "dotenv/config"
    log(`Loaded .env file at: ${envPath}`);
  }
  
  // Override with environment variables if they exist
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
