import * as fs from 'fs';
import * as path from 'path';
import 'dotenv/config';
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
      region_id: 'cn-shanghai',
      endpoint: 'wuyingai.cn-shanghai.aliyuncs.com',
    timeout_ms: 60000
  };
}

/**
 * Loads configuration from file
 */
export function loadConfig(): Config {
  // First check if the config file path is specified in environment variables
  let configPath = process.env.AGENTBAY_CONFIG_PATH;
  if (!configPath) {
    // Try to find the config file in the project root directory
    // First try the current directory
    configPath = 'config.json';
    if (!fs.existsSync(configPath)) {
      // Then try the parent directory
      configPath = path.join('..', 'config.json');
      if (!fs.existsSync(configPath)) {
        // Then try the grandparent directory
        configPath = path.join('..', '..', 'config.json');
        if (!fs.existsSync(configPath)) {
          // Config file not found, return default config
          console.log('Warning: Configuration file not found, using default values');
          return defaultConfig();
        }
      }
    }
  }

  try {
    // Read the config file
    const data = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(data) as Config;

    // Allow environment variables to override config file values
    if (process.env.AGENTBAY_REGION_ID) {
      config.region_id = process.env.AGENTBAY_REGION_ID;
    }
    if (process.env.AGENTBAY_ENDPOINT) {
      config.endpoint = process.env.AGENTBAY_ENDPOINT;
    }

    return config;
  } catch (error) {
    console.log(`Warning: Failed to read configuration file: ${error}, using default values`);
    return defaultConfig();
  }
}
