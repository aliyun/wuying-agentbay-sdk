import { loadConfig, Config } from "../../src/config";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import { log } from "../../src/utils/logger";

describe("Config", () => {
  let originalEnv: NodeJS.ProcessEnv;

  beforeEach(() => {
    originalEnv = process.env;
    // 清除所有环境变量
    process.env = {};

    // 创建临时目录
    const testDir = fs.mkdtempSync(path.join(os.tmpdir(), "config-test-"));
    process.chdir(testDir);
  });

  afterEach(() => {
    // 恢复原始环境变量
    process.env = originalEnv;
  });

  describe("test_load_from_passed_config", () => {
    it("should load configuration from passed Config object", () => {
      const customCfg: Config = {
        region_id: "custom-region",
        endpoint: "custom-endpoint",
        timeout_ms: 5000,
      };

      const result = loadConfig(customCfg);

      expect(result.region_id).toBe("custom-region");
      expect(result.endpoint).toBe("custom-endpoint");
      expect(result.timeout_ms).toBe(5000);
    });
  });

  describe("test_load_from_env_file", () => {
    it("should load configuration from .env file", () => {
      // 创建 .env 文件并写入测试内容
      const envFilePath = path.resolve(process.cwd(), ".env");
      fs.writeFileSync(
        envFilePath,
        "AGENTBAY_REGION_ID=env-region\n" +
          "AGENTBAY_ENDPOINT=env-endpoint\n" +
          "AGENTBAY_TIMEOUT_MS=10000\n"
      );

      // 验证文件确实存在
      expect(fs.existsSync(envFilePath)).toBe(true);

      // 清除环境变量
      process.env = {};

      // 调用 loadConfig
      const result = loadConfig(undefined);

      // 验证结果
      expect(result.region_id).toBe("env-region");
      expect(result.endpoint).toBe("env-endpoint");
      expect(result.timeout_ms).toBe(10000);
    });
  });

  describe("test_load_from_system_env_vars", () => {
    it("should load configuration from system environment variables", () => {
      // 设置环境变量
      process.env.AGENTBAY_REGION_ID = "sys-region";
      process.env.AGENTBAY_ENDPOINT = "sys-endpoint";
      process.env.AGENTBAY_TIMEOUT_MS = "15000";

      // 确保没有 .env 文件
      const envFilePath = path.resolve(process.cwd(), ".env");
      if (fs.existsSync(envFilePath)) {
        fs.unlinkSync(envFilePath);
      }

      // 调用 loadConfig
      const result = loadConfig(undefined);

      // 验证结果
      expect(result.region_id).toBe("sys-region");
      expect(result.endpoint).toBe("sys-endpoint");
      expect(result.timeout_ms).toBe(15000);
    });
  });

  describe("test_use_default_config_when_no_source_provided", () => {
    it("should use default configuration when no source is provided", () => {
      // 清除环境变量
      process.env = {};

      // 确保没有 .env 文件
      const envFilePath = path.resolve(process.cwd(), ".env");
      if (fs.existsSync(envFilePath)) {
        fs.unlinkSync(envFilePath);
      }

      // 调用 loadConfig
      const result = loadConfig(undefined);

      // 获取默认配置
      const defaultCfg = {
        region_id: "cn-shanghai",
        endpoint: "wuyingai.cn-shanghai.aliyuncs.com",
        timeout_ms: 60000,
      };

      // 验证结果
      expect(result.region_id).toBe(defaultCfg.region_id);
      expect(result.endpoint).toBe(defaultCfg.endpoint);
      expect(result.timeout_ms).toBe(defaultCfg.timeout_ms);
    });
  });

  describe("test_config_precedence_order", () => {
    it("should follow the correct precedence order for configuration sources", () => {
      // 创建 .env 文件并写入测试内容
      const envFilePath = path.resolve(process.cwd(), ".env");
      fs.writeFileSync(
        envFilePath,
        "AGENTBAY_REGION_ID=env-region\n" +
          "AGENTBAY_ENDPOINT=env-endpoint\n" +
          "AGENTBAY_TIMEOUT_MS=10000\n"
      );

      // 验证文件确实存在
      expect(fs.existsSync(envFilePath)).toBe(true);

      // 设置环境变量
      process.env.AGENTBAY_REGION_ID = "sys-region";
      process.env.AGENTBAY_ENDPOINT = "sys-endpoint";
      process.env.AGENTBAY_TIMEOUT_MS = "15000";

      // 获取默认配置
      const defaultCfg = {
        region_id: "cn-shanghai",
        endpoint: "wuyingai.cn-shanghai.aliyuncs.com",
        timeout_ms: 60000,
      };

      // 1. 显式传入的配置应具有最高优先级
      const customCfg: Config = {
        region_id: "explicit-region",
        endpoint: "explicit-endpoint",
        timeout_ms: 2000,
      };
      let result = loadConfig(customCfg);
      expect(result.region_id).toBe("explicit-region");
      expect(result.endpoint).toBe("explicit-endpoint");
      expect(result.timeout_ms).toBe(2000);

      // 2. 当显式配置为 undefined 时，应使用环境变量
      result = loadConfig(undefined);
      expect(result.region_id).toBe("sys-region");
      expect(result.endpoint).toBe("sys-endpoint");
      expect(result.timeout_ms).toBe(15000);

      // 3. 清除环境变量后，应使用 .env 文件
      process.env = {};
      result = loadConfig(undefined);
      expect(result.region_id).toBe("env-region");
      expect(result.endpoint).toBe("env-endpoint");
      expect(result.timeout_ms).toBe(10000);

      // 4. 所有其他来源都不存在时，应使用默认配置
      fs.unlinkSync(envFilePath);
      result = loadConfig(undefined);
      expect(result.region_id).toBe(defaultCfg.region_id);
      expect(result.endpoint).toBe(defaultCfg.endpoint);
      expect(result.timeout_ms).toBe(defaultCfg.timeout_ms);
    });
  });
});
