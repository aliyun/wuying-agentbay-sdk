import {
  ContextSync,
  SyncPolicy,
  newSyncPolicy,
  newUploadPolicy,
  newDownloadPolicy,
  newDeletePolicy,
  UploadStrategy,
  DownloadStrategy
} from "../../src/context-sync";
import { log } from "../../src/utils/logger";

describe("ContextSync Unit Tests", () => {
  describe("SyncPolicy Default Construction", () => {
    it("should create default SyncPolicy with correct values", () => {
      const policy = newSyncPolicy();

      // Verify the policy is not null
      expect(policy).toBeDefined();

      // Verify uploadPolicy
      expect(policy.uploadPolicy).toBeDefined();
      if (policy.uploadPolicy) {
        expect(policy.uploadPolicy.autoUpload).toBe(true);
        expect(policy.uploadPolicy.uploadStrategy).toBe(UploadStrategy.UploadBeforeResourceRelease);
        expect(policy.uploadPolicy.period).toBe(30);
      }

      // Verify downloadPolicy
      expect(policy.downloadPolicy).toBeDefined();
      if (policy.downloadPolicy) {
        expect(policy.downloadPolicy.autoDownload).toBe(true);
        expect(policy.downloadPolicy.downloadStrategy).toBe(DownloadStrategy.DownloadAsync);
      }

      // Verify deletePolicy
      expect(policy.deletePolicy).toBeDefined();
      if (policy.deletePolicy) {
        expect(policy.deletePolicy.syncLocalFile).toBe(true);
      }

      // Verify bwList
      expect(policy.bwList).toBeDefined();
      if (policy.bwList && policy.bwList.whiteLists) {
        expect(policy.bwList.whiteLists).toBeDefined();
        expect(policy.bwList.whiteLists).toHaveLength(1);
        
        const firstWhiteList = policy.bwList.whiteLists[0];
        expect(firstWhiteList.path).toBe("");
        expect(firstWhiteList.excludePaths).toBeDefined();
        if (firstWhiteList.excludePaths) {
          expect(firstWhiteList.excludePaths).toHaveLength(0);
        }
      }
    });

    it("should create default SyncPolicy that matches JSON requirements", () => {
      const policy = newSyncPolicy();

      // Convert to JSON and verify structure
      const jsonString = JSON.stringify(policy);
      const jsonObject = JSON.parse(jsonString);

      // Verify uploadPolicy in JSON
      expect(jsonObject.uploadPolicy).toBeDefined();
      expect(jsonObject.uploadPolicy.autoUpload).toBe(true);
      expect(jsonObject.uploadPolicy.uploadStrategy).toBe("UploadBeforeResourceRelease");
      expect(jsonObject.uploadPolicy.period).toBe(30);

      // Verify downloadPolicy in JSON
      expect(jsonObject.downloadPolicy).toBeDefined();
      expect(jsonObject.downloadPolicy.autoDownload).toBe(true);
      expect(jsonObject.downloadPolicy.downloadStrategy).toBe("DownloadAsync");

      // Verify deletePolicy in JSON
      expect(jsonObject.deletePolicy).toBeDefined();
      expect(jsonObject.deletePolicy.syncLocalFile).toBe(true);

      // Verify bwList in JSON
      expect(jsonObject.bwList).toBeDefined();
      expect(jsonObject.bwList.whiteLists).toBeDefined();
      expect(jsonObject.bwList.whiteLists).toHaveLength(1);
      expect(jsonObject.bwList.whiteLists[0].path).toBe("");
      // excludePaths should be present in JSON since it's an empty array
      expect(jsonObject.bwList.whiteLists[0].excludePaths).toBeDefined();
      expect(jsonObject.bwList.whiteLists[0].excludePaths).toHaveLength(0);

      // Verify syncPaths should not exist in JSON
      expect(jsonObject.syncPaths).toBeUndefined();

      // Log the generated JSON for verification
      log("Generated JSON:", jsonString);
    });

    it("should create individual policy components with correct defaults", () => {
      // Test UploadPolicy defaults
      const uploadPolicy = newUploadPolicy();
      expect(uploadPolicy.autoUpload).toBe(true);
      expect(uploadPolicy.uploadStrategy).toBe(UploadStrategy.UploadBeforeResourceRelease);
      expect(uploadPolicy.period).toBe(30);

      // Test DownloadPolicy defaults
      const downloadPolicy = newDownloadPolicy();
      expect(downloadPolicy.autoDownload).toBe(true);
      expect(downloadPolicy.downloadStrategy).toBe(DownloadStrategy.DownloadAsync);

      // Test DeletePolicy defaults
      const deletePolicy = newDeletePolicy();
      expect(deletePolicy.syncLocalFile).toBe(true);
    });

    it("should create ContextSync with default policy", () => {
      const contextId = "test-context-123";
      const path = "/test/path";
      const policy = newSyncPolicy();

      const contextSync = new ContextSync(contextId, path, policy);

      expect(contextSync.contextId).toBe(contextId);
      expect(contextSync.path).toBe(path);
      expect(contextSync.policy).toBe(policy);
    });

    it("should allow chaining with withPolicy method", () => {
      const contextSync = new ContextSync("test-context", "/test/path");
      const policy = newSyncPolicy();

      const result = contextSync.withPolicy(policy);

      expect(result).toBe(contextSync);
      expect(contextSync.policy).toBe(policy);
    });
  });
});
