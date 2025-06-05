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
    try {
      // Try to find the config file by traversing up from the current directory
      let dirPath = process.cwd();
      let found = false;
      
      // Start from current directory and traverse up to find config.json
      // This will check current dir, parent, grandparent, etc. up to filesystem root
      for (let i = 0; i < 10; i++) { // Limit search depth to prevent infinite loop
        const possibleConfigPath = path.join(dirPath, 'config.json');
        if (fs.existsSync(possibleConfigPath)) {
          configPath = possibleConfigPath;
          found = true;
          console.log(`Found config file at: ${possibleConfigPath}`);
          break;
        }
        
        // Move up one directory
        const parentDir = path.dirname(dirPath);
        if (parentDir === dirPath) {
          // We've reached the filesystem root
          break;
        }
        dirPath = parentDir;
      }
      
      if (!found) {
        // Config file not found, return default config
        console.log('Warning: Configuration file not found, using default values');
        return defaultConfig();
      }
    } catch (error) {
      console.log(`Warning: Failed to search for configuration file: ${error}, using default values`);
      return defaultConfig();
    }
  }

  try {
    // Make sure configPath is defined
    if (!configPath) {
      console.log('Warning: Configuration file path is undefined, using default values');
      return defaultConfig();
    }
    
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
