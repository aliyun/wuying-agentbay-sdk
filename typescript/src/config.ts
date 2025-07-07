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

  // Try to load .env file
  const envPath = path.resolve(process.cwd(), ".env");

  // 显式加载 .env 文件内容到 process.env
  if (fs.existsSync(envPath)) {
    const envConfig = dotenv.parse(fs.readFileSync(envPath));
    for (const k in envConfig) {
      // 仅当环境变量未设置时才使用 .env 文件中的值
      if (!process.env.hasOwnProperty(k)) {
        // 更新 config 对象以反映 .env 文件的值
        if (k === "AGENTBAY_REGION_ID") config.region_id = envConfig[k];
        else if (k === "AGENTBAY_ENDPOINT") config.endpoint = envConfig[k];
        else if (k === "AGENTBAY_TIMEOUT_MS") {
          const timeout = parseInt(envConfig[k], 10);
          if (!isNaN(timeout) && timeout > 0) {
            config.timeout_ms = timeout;
          }
        }
      }
    }
    log(`Loaded .env file at: ${envPath}`);
  }
  return config;
}

export { Config };
