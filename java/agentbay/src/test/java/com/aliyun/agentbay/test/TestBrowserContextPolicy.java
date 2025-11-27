package com.aliyun.agentbay.test;

import com.aliyun.agentbay.Config;
import com.aliyun.agentbay.browser.BrowserContext;
import com.aliyun.agentbay.browser.ExtensionOption;
import com.aliyun.agentbay.context.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

import static org.junit.Assert.*;

/**
 * Test browser context policy includes BWList with white lists.
 */
public class TestBrowserContextPolicy {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Test
    public void testBrowserContextPolicyIncludesBWList() throws Exception {
        // Create browser context
        String contextId = "test-browser-context";
        BrowserContext browserContext = new BrowserContext(contextId, true);

        // Create SyncPolicy for browser context (matching the logic in AgentBay.create)
        UploadPolicy uploadPolicy = new UploadPolicy(
            browserContext.isAutoUpload(),
            UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE,
            30
        );

        // Create BWList with white lists for browser data paths
        List<WhiteList> whiteLists = new ArrayList<>();
        whiteLists.add(new WhiteList("/Local State", new ArrayList<>()));
        whiteLists.add(new WhiteList("/Default/Cookies", new ArrayList<>()));
        whiteLists.add(new WhiteList("/Default/Cookies-journal", new ArrayList<>()));
        BWList bwList = new BWList(whiteLists);

        SyncPolicy syncPolicy = new SyncPolicy(
            uploadPolicy,
            DownloadPolicy.defaultPolicy(),
            DeletePolicy.defaultPolicy(),
            ExtractPolicy.defaultPolicy(),
            bwList
        );

        // Convert to map and serialize to JSON
        Map<String, Object> policyMap = syncPolicy.toMap();

        System.out.println("Generated policy JSON:");
        System.out.println(objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(policyMap));

        // Verify the policy contains the expected structure
        assertNotNull("Policy map should not be null", policyMap);
        assertTrue("bwList should be present in policy", policyMap.containsKey("bwList"));

        // Check that whiteLists exists in bwList
        @SuppressWarnings("unchecked")
        Map<String, Object> bwListMap = (Map<String, Object>) policyMap.get("bwList");
        assertNotNull("bwList should not be null", bwListMap);
        assertTrue("whiteLists should be present in bwList", bwListMap.containsKey("whiteLists"));

        // Check that we have 3 white lists
        @SuppressWarnings("unchecked")
        List<Map<String, Object>> whiteListsData = (List<Map<String, Object>>) bwListMap.get("whiteLists");
        assertNotNull("whiteLists should not be null", whiteListsData);
        assertEquals("Expected 3 white lists", 3, whiteListsData.size());

        // Check the specific paths
        List<String> paths = new ArrayList<>();
        for (Map<String, Object> wl : whiteListsData) {
            paths.add((String) wl.get("path"));
        }

        assertTrue("Expected path /Local State not found", paths.contains("/Local State"));
        assertTrue("Expected path /Default/Cookies not found", paths.contains("/Default/Cookies"));
        assertTrue("Expected path /Default/Cookies-journal not found", paths.contains("/Default/Cookies-journal"));

        System.out.println("✅ All tests passed! Browser context policy correctly includes BWList with white lists.");
    }

    @Test
    public void testExtensionContextSyncPolicy() throws Exception {
        // Test that extension context syncs have correct policy
        ExtensionOption extensionOption = new ExtensionOption(
            "ext-context",
            Arrays.asList("ext1.zip", "ext2.zip")
        );

        BrowserContext browserContext = new BrowserContext(
            "test-context",
            true,
            extensionOption,
            null
        );

        List<ContextSync> extensionSyncs = browserContext.getExtensionContextSyncs();
        assertNotNull("Extension syncs should not be null", extensionSyncs);
        assertFalse("Extension syncs should not be empty", extensionSyncs.isEmpty());

        // Get the first extension sync
        ContextSync extensionSync = extensionSyncs.get(0);
        assertNotNull("Extension sync should not be null", extensionSync);
        assertEquals("ext-context", extensionSync.getContextId());
        assertEquals("/tmp/extensions/", extensionSync.getPath());

        // Check policy
        SyncPolicy policy = extensionSync.getPolicy();
        assertNotNull("Extension sync policy should not be null", policy);

        // Convert to map
        Map<String, Object> policyMap = policy.toMap();
        assertNotNull("Policy map should not be null", policyMap);

        // Check upload policy
        assertTrue("uploadPolicy should be present", policyMap.containsKey("uploadPolicy"));
        @SuppressWarnings("unchecked")
        Map<String, Object> uploadPolicyMap = (Map<String, Object>) policyMap.get("uploadPolicy");
        assertEquals("Extension autoUpload should be false", false, uploadPolicyMap.get("autoUpload"));

        // Check delete policy
        assertTrue("deletePolicy should be present", policyMap.containsKey("deletePolicy"));
        @SuppressWarnings("unchecked")
        Map<String, Object> deletePolicyMap = (Map<String, Object>) policyMap.get("deletePolicy");
        assertEquals("Extension syncLocalFile should be false", false, deletePolicyMap.get("syncLocalFile"));

        // Check extract policy
        assertTrue("extractPolicy should be present", policyMap.containsKey("extractPolicy"));
        @SuppressWarnings("unchecked")
        Map<String, Object> extractPolicyMap = (Map<String, Object>) policyMap.get("extractPolicy");
        assertEquals("Extension extract should be true", true, extractPolicyMap.get("extract"));
        assertEquals("Extension deleteSrcFile should be true", true, extractPolicyMap.get("deleteSrcFile"));

        // Check BWList
        assertTrue("bwList should be present", policyMap.containsKey("bwList"));
        @SuppressWarnings("unchecked")
        Map<String, Object> bwListMap = (Map<String, Object>) policyMap.get("bwList");
        assertTrue("whiteLists should be present", bwListMap.containsKey("whiteLists"));

        @SuppressWarnings("unchecked")
        List<Map<String, Object>> whiteListsData = (List<Map<String, Object>>) bwListMap.get("whiteLists");
        assertEquals("Should have 2 extension whitelists", 2, whiteListsData.size());

        System.out.println("✅ Extension context sync policy is correct!");
    }

    @Test
    public void testFingerprintContextSyncPolicy() throws Exception {
        // Test that fingerprint context sync has correct policy
        com.aliyun.agentbay.browser.BrowserFingerprintContext fingerprintContext =
            new com.aliyun.agentbay.browser.BrowserFingerprintContext("fingerprint-id");

        BrowserContext browserContext = new BrowserContext(
            "test-context",
            true,
            null,
            fingerprintContext
        );

        ContextSync fingerprintSync = browserContext.getFingerprintContextSync();
        assertNotNull("Fingerprint sync should not be null", fingerprintSync);
        assertEquals("fingerprint-id", fingerprintSync.getContextId());
        assertEquals(Config.BROWSER_FINGERPRINT_PERSIST_PATH, fingerprintSync.getPath());

        // Check policy
        SyncPolicy policy = fingerprintSync.getPolicy();
        assertNotNull("Fingerprint sync policy should not be null", policy);

        // Convert to map
        Map<String, Object> policyMap = policy.toMap();
        assertNotNull("Policy map should not be null", policyMap);

        // Check upload policy
        assertTrue("uploadPolicy should be present", policyMap.containsKey("uploadPolicy"));
        @SuppressWarnings("unchecked")
        Map<String, Object> uploadPolicyMap = (Map<String, Object>) policyMap.get("uploadPolicy");
        assertEquals("Fingerprint autoUpload should be false", false, uploadPolicyMap.get("autoUpload"));

        // Check extract policy
        assertTrue("extractPolicy should be present", policyMap.containsKey("extractPolicy"));
        @SuppressWarnings("unchecked")
        Map<String, Object> extractPolicyMap = (Map<String, Object>) policyMap.get("extractPolicy");
        assertEquals("Fingerprint extract should be true", true, extractPolicyMap.get("extract"));
        assertEquals("Fingerprint deleteSrcFile should be true", true, extractPolicyMap.get("deleteSrcFile"));

        System.out.println("✅ Fingerprint context sync policy is correct!");
    }

    @Test
    public void testBrowserContextAutoUploadTrue() throws Exception {
        // Test browser context with auto_upload=true
        BrowserContext browserContext = new BrowserContext("test-context", true);

        assertTrue(browserContext.isAutoUpload());

        // Create upload policy
        UploadPolicy uploadPolicy = new UploadPolicy(
            browserContext.isAutoUpload(),
            UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE,
            30
        );

        Map<String, Object> uploadPolicyMap = uploadPolicy.toMap();
        assertEquals("autoUpload should be true", true, uploadPolicyMap.get("autoUpload"));
    }

    @Test
    public void testBrowserContextAutoUploadFalse() throws Exception {
        // Test browser context with auto_upload=false
        BrowserContext browserContext = new BrowserContext("test-context", false);

        assertFalse(browserContext.isAutoUpload());

        // Create upload policy
        UploadPolicy uploadPolicy = new UploadPolicy(
            browserContext.isAutoUpload(),
            UploadStrategy.UPLOAD_BEFORE_RESOURCE_RELEASE,
            30
        );

        Map<String, Object> uploadPolicyMap = uploadPolicy.toMap();
        assertEquals("autoUpload should be false", false, uploadPolicyMap.get("autoUpload"));
    }
}

