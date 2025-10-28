import { expect } from "chai";
import * as sinon from "sinon";
import {
  log,
  logError,
  logDebug,
  logWarn,
  logInfo,
  logAPICall,
  logAPIResponseWithDetails,
  maskSensitiveData,
  getRequestId,
  setRequestId,
  clearRequestId,
} from "../../src/utils/logger";

describe("Logger", () => {
  let stdoutWriteStub: sinon.SinonStub;
  let stderrWriteStub: sinon.SinonStub;

  beforeEach(() => {
    stdoutWriteStub = sinon.stub(process.stdout, "write");
    stderrWriteStub = sinon.stub(process.stderr, "write");
  });

  afterEach(() => {
    sinon.restore();
    clearRequestId();
  });

  describe("Basic Logging Functions", () => {
    it("should log message to stdout", () => {
      log("test message");
      expect(stdoutWriteStub.called).to.be.true;
      expect(stdoutWriteStub.firstCall.args[0]).to.include("test message");
    });

    it("should log info message with INFO prefix", () => {
      logInfo("info message");
      expect(stdoutWriteStub.called).to.be.true;
      const output = stdoutWriteStub.firstCall.args[0];
      expect(output).to.include("ℹ️  INFO");
      expect(output).to.include("info message");
    });

    it("should log debug message with DEBUG prefix", () => {
      logDebug("debug message");
      expect(stdoutWriteStub.called).to.be.true;
      const output = stdoutWriteStub.firstCall.args[0];
      expect(output).to.include("🐛 DEBUG");
      expect(output).to.include("debug message");
    });

    it("should log warning message with WARN prefix", () => {
      logWarn("warning message");
      expect(stdoutWriteStub.called).to.be.true;
      const output = stdoutWriteStub.firstCall.args[0];
      expect(output).to.include("⚠️  WARN");
      expect(output).to.include("warning message");
    });

    it("should log error message to stderr with ERROR prefix", () => {
      logError("error message");
      expect(stderrWriteStub.called).to.be.true;
      const output = stderrWriteStub.firstCall.args[0];
      expect(output).to.include("❌ ERROR");
      expect(output).to.include("error message");
    });

    it("should log error with Error object stack trace", () => {
      const error = new Error("test error");
      logError("operation failed", error);
      expect(stderrWriteStub.called).to.be.true;
      const fullOutput = stderrWriteStub.getCalls().map(c => c.args[0]).join("");
      expect(fullOutput).to.include("test error");
      expect(fullOutput).to.include("Stack");
    });
  });

  describe("API Logging Functions", () => {
    it("should log API call with API name", () => {
      logAPICall("CreateSession");
      expect(stdoutWriteStub.called).to.be.true;
      const output = stdoutWriteStub.firstCall.args[0];
      expect(output).to.include("🔗 API Call");
      expect(output).to.include("CreateSession");
    });

    it("should log API response with success status", () => {
      setRequestId("req-123");
      logAPIResponseWithDetails("CreateSession", "req-123", true, {
        session_id: "sess-456",
        resource_url: "https://example.com",
      });
      expect(stdoutWriteStub.called).to.be.true;
      const output = stdoutWriteStub.getCalls().map(c => c.args[0]).join("");
      expect(output).to.include("✅ API Response");
      expect(output).to.include("CreateSession");
      expect(output).to.include("req-123");
      expect(output).to.include("session_id=sess-456");
      expect(output).to.include("resource_url=https://example.com");
    });

    it("should log API response with error status", () => {
      logAPIResponseWithDetails("DeleteSession", "req-789", false, {}, "Not found");
      expect(stderrWriteStub.called).to.be.true;
      const output = stderrWriteStub.getCalls().map(c => c.args[0]).join("");
      expect(output).to.include("❌ API Response Failed");
      expect(output).to.include("DeleteSession");
    });
  });

  describe("Sensitive Data Masking", () => {
    it("should mask API keys in objects", () => {
      const data = {
        api_key: "sk-1234567890abcdef",
        username: "testuser",
      };
      const masked = maskSensitiveData(data);
      expect(masked.api_key).to.equal("sk****ef");
      expect(masked.username).to.equal("testuser");
    });

    it("should mask tokens in objects", () => {
      const data = {
        access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        user_id: "12345",
      };
      const masked = maskSensitiveData(data);
      expect(masked.access_token).to.equal("ey****J9");
      expect(masked.user_id).to.equal("12345");
    });

    it("should mask passwords in objects", () => {
      const data = {
        password: "mySecurePassword123",
        email: "user@example.com",
      };
      const masked = maskSensitiveData(data);
      expect(masked.password).to.equal("my****23");
      expect(masked.email).to.equal("user@example.com");
    });

    it("should recursively mask nested objects", () => {
      const data = {
        user: {
          name: "John",
          api_key: "secret123",
        },
        credentials: {
          password: "pass456",
        },
      };
      const masked = maskSensitiveData(data);
      expect(masked.user.api_key).to.equal("se****23");
      expect(masked.credentials.password).to.equal("pa****56");
      expect(masked.user.name).to.equal("John");
    });

    it("should mask arrays of objects", () => {
      const data = [
        { api_key: "key123", name: "item1" },
        { api_key: "key456", name: "item2" },
      ];
      const masked = maskSensitiveData(data);
      expect(masked[0].api_key).to.equal("ke****23");
      expect(masked[1].api_key).to.equal("ke****56");
    });

    it("should handle custom sensitive fields", () => {
      const data = {
        custom_secret: "mysecretvalue",
        public_field: "publicvalue",
      };
      const masked = maskSensitiveData(data, ["custom_secret"]);
      expect(masked.custom_secret).to.equal("my****ue");
      expect(masked.public_field).to.equal("publicvalue");
    });
  });

  describe("RequestID Management", () => {
    it("should set and get RequestID", () => {
      setRequestId("req-12345");
      expect(getRequestId()).to.equal("req-12345");
    });

    it("should include RequestID in API call logs", () => {
      setRequestId("req-xyz");
      logAPICall("TestAPI");
      const output = stdoutWriteStub.getCalls().map(c => c.args[0]).join("");
      expect(output).to.include("req-xyz");
    });

    it("should clear RequestID", () => {
      setRequestId("req-abc");
      clearRequestId();
      expect(getRequestId()).to.equal("");
    });

    it("should handle empty RequestID gracefully", () => {
      expect(getRequestId()).to.equal("");
      logAPICall("TestAPI");
      expect(stdoutWriteStub.called).to.be.true;
    });
  });

  describe("Multiple Arguments Logging", () => {
    it("should log message with multiple arguments", () => {
      log("test message", { key: "value" }, "additional");
      expect(stdoutWriteStub.called).to.be.true;
      expect(stdoutWriteStub.callCount).to.be.greaterThan(1);
    });

    it("should format objects with proper indentation", () => {
      log("message", { nested: { field: "value" } });
      const calls = stdoutWriteStub.getCalls();
      expect(calls.some(c => c.args[0].includes(JSON.stringify({ nested: { field: "value" } }, null, 2)))).to.be.true;
    });
  });

  describe("Edge Cases", () => {
    it("should handle null values gracefully", () => {
      expect(() => log("message", null)).to.not.throw();
    });

    it("should handle undefined values gracefully", () => {
      expect(() => log("message", undefined)).to.not.throw();
    });

    it("should handle circular references in masking", () => {
      const data: any = { api_key: "secret", ref: null };
      data.ref = data;
      expect(() => maskSensitiveData(data)).to.not.throw();
    });

    it("should handle very long strings", () => {
      const longString = "a".repeat(10000);
      expect(() => log(longString)).to.not.throw();
    });
  });
});
