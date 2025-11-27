package com.aliyun.agentbay.test;

import com.aliyun.agentbay.Config;
import com.aliyun.agentbay.browser.BrowserContext;
import com.aliyun.agentbay.browser.BrowserFingerprintContext;
import com.aliyun.agentbay.browser.ExtensionOption;
import com.aliyun.agentbay.session.CreateSessionParams;
import org.junit.Test;

import java.util.Arrays;

import static org.junit.Assert.*;

/**
 * Test browser context configuration and constant usage.
 */
public class TestBrowserContextConfig {

    @Test
    public void testBrowserDataPathConstant() {
        // Test that BROWSER_DATA_PATH constant is correctly defined
        assertEquals("/tmp/agentbay_browser", Config.BROWSER_DATA_PATH);
        assertNotNull(Config.BROWSER_DATA_PATH);
        assertTrue(Config.BROWSER_DATA_PATH.startsWith("/"));
    }

    @Test
    public void testBrowserFingerprintPathConstant() {
        // Test that BROWSER_FINGERPRINT_PERSIST_PATH constant is correctly defined
        assertEquals("/tmp/browser_fingerprint", Config.BROWSER_FINGERPRINT_PERSIST_PATH);
        assertNotNull(Config.BROWSER_FINGERPRINT_PERSIST_PATH);
        assertTrue(Config.BROWSER_FINGERPRINT_PERSIST_PATH.startsWith("/"));
    }

    @Test
    public void testBrowserContextCreation() {
        // Test BrowserContext creation with correct attributes
        String contextId = "test-context-123";
        boolean autoUpload = true;

        BrowserContext browserContext = new BrowserContext(contextId, autoUpload);

        assertEquals(contextId, browserContext.getContextId());
        assertTrue(browserContext.isAutoUpload());
    }

    @Test
    public void testBrowserContextDefaultAutoUpload() {
        // Test BrowserContext creation with default auto_upload value
        String contextId = "test-context-456";

        BrowserContext browserContext = new BrowserContext(contextId);

        assertEquals(contextId, browserContext.getContextId());
        assertTrue(browserContext.isAutoUpload()); // Default should be true
    }

    @Test
    public void testBrowserContextWithExtensions() {
        // Test BrowserContext creation with extensions
        String contextId = "test-context-with-extensions";
        ExtensionOption extensionOption = new ExtensionOption(
            "ext-context",
            Arrays.asList("ext1.zip", "ext2.zip")
        );

        BrowserContext browserContext = new BrowserContext(
            contextId,
            true,
            extensionOption,
            null
        );

        assertEquals(contextId, browserContext.getContextId());
        assertTrue(browserContext.isAutoUpload());
        assertNotNull(browserContext.getExtensionOption());
        assertEquals("ext-context", browserContext.getExtensionContextId());
        assertEquals(2, browserContext.getExtensionIds().size());
        assertFalse(browserContext.getExtensionContextSyncs().isEmpty());
    }

    @Test
    public void testBrowserContextWithFingerprint() {
        // Test BrowserContext creation with fingerprint
        String contextId = "test-context-with-fingerprint";
        BrowserFingerprintContext fingerprintContext = new BrowserFingerprintContext(
            "fingerprint-context-id"
        );

        BrowserContext browserContext = new BrowserContext(
            contextId,
            true,
            null,
            fingerprintContext
        );

        assertEquals(contextId, browserContext.getContextId());
        assertTrue(browserContext.isAutoUpload());
        assertNotNull(browserContext.getFingerprintContext());
        assertEquals("fingerprint-context-id", browserContext.getFingerprintContextId());
        assertNotNull(browserContext.getFingerprintContextSync());
    }

    @Test
    public void testBrowserContextWithExtensionsAndFingerprint() {
        // Test BrowserContext creation with both extensions and fingerprint
        String contextId = "test-context-full";
        ExtensionOption extensionOption = new ExtensionOption(
            "ext-context",
            Arrays.asList("ext1.zip", "ext2.zip")
        );
        BrowserFingerprintContext fingerprintContext = new BrowserFingerprintContext(
            "fingerprint-context-id"
        );

        BrowserContext browserContext = new BrowserContext(
            contextId,
            true,
            extensionOption,
            fingerprintContext
        );

        assertEquals(contextId, browserContext.getContextId());
        assertTrue(browserContext.isAutoUpload());
        assertNotNull(browserContext.getExtensionOption());
        assertNotNull(browserContext.getFingerprintContext());
        assertEquals(2, browserContext.getExtensionIds().size());
        assertFalse(browserContext.getExtensionContextSyncs().isEmpty());
        assertNotNull(browserContext.getFingerprintContextSync());
    }

    @Test
    public void testCreateSessionParamsWithBrowserContext() {
        // Test CreateSessionParams with browser context
        String contextId = "test-context-789";
        BrowserContext browserContext = new BrowserContext(contextId, false);

        CreateSessionParams params = new CreateSessionParams();
        params.setBrowserContext(browserContext);

        assertNotNull(params.getBrowserContext());
        assertEquals(contextId, params.getBrowserContext().getContextId());
        assertFalse(params.getBrowserContext().isAutoUpload());
    }

    @Test
    public void testCreateSessionParamsAutoMergeExtensionSyncs() {
        // Test that extension context syncs are automatically merged
        String contextId = "test-context-merge";
        ExtensionOption extensionOption = new ExtensionOption(
            "ext-context",
            Arrays.asList("ext1.zip", "ext2.zip")
        );
        BrowserContext browserContext = new BrowserContext(
            contextId,
            true,
            extensionOption,
            null
        );

        CreateSessionParams params = new CreateSessionParams();
        params.setBrowserContext(browserContext);

        assertNotNull(params.getBrowserContext());
        assertNotNull(params.getContextSyncs());
        // Should have extension context syncs merged
        assertTrue(params.getContextSyncs().size() > 0);
    }

    @Test
    public void testCreateSessionParamsAutoMergeFingerprintSync() {
        // Test that fingerprint context sync is automatically merged
        String contextId = "test-context-fingerprint-merge";
        BrowserFingerprintContext fingerprintContext = new BrowserFingerprintContext(
            "fingerprint-context-id"
        );
        BrowserContext browserContext = new BrowserContext(
            contextId,
            true,
            null,
            fingerprintContext
        );

        CreateSessionParams params = new CreateSessionParams();
        params.setBrowserContext(browserContext);

        assertNotNull(params.getBrowserContext());
        assertNotNull(params.getContextSyncs());
        // Should have fingerprint context sync merged
        assertTrue(params.getContextSyncs().size() > 0);
    }

    @Test
    public void testExtensionOptionValidation() {
        // Test ExtensionOption validation
        ExtensionOption extensionOption = new ExtensionOption(
            "ext-context",
            Arrays.asList("ext1.zip", "ext2.zip")
        );

        assertTrue(extensionOption.validate());
        assertEquals("ext-context", extensionOption.getContextId());
        assertEquals(2, extensionOption.getExtensionIds().size());
    }

    @Test
    public void testExtensionOptionEmptyContextId() {
        // Test ExtensionOption throws exception with empty context ID
        assertThrows(IllegalArgumentException.class, () -> {
            new ExtensionOption("", Arrays.asList("ext1.zip"));
        });
    }

    @Test
    public void testExtensionOptionEmptyExtensionIds() {
        // Test ExtensionOption throws exception with empty extension IDs
        assertThrows(IllegalArgumentException.class, () -> {
            new ExtensionOption("ext-context", Arrays.asList());
        });
    }

    @Test
    public void testBrowserFingerprintContextValidation() {
        // Test BrowserFingerprintContext validation
        BrowserFingerprintContext fingerprintContext = new BrowserFingerprintContext(
            "fingerprint-id"
        );

        assertEquals("fingerprint-id", fingerprintContext.getFingerprintContextId());
    }

    @Test
    public void testBrowserFingerprintContextEmptyId() {
        // Test BrowserFingerprintContext throws exception with empty ID
        assertThrows(IllegalArgumentException.class, () -> {
            new BrowserFingerprintContext("");
        });
    }

    @Test
    public void testBrowserContextToString() {
        // Test BrowserContext toString method
        String contextId = "test-context-string";
        BrowserContext browserContext = new BrowserContext(contextId, true);

        String str = browserContext.toString();
        assertNotNull(str);
        assertTrue(str.contains(contextId));
        assertTrue(str.contains("autoUpload"));
    }

    @Test
    public void testExtensionOptionToString() {
        // Test ExtensionOption toString method
        ExtensionOption extensionOption = new ExtensionOption(
            "ext-context",
            Arrays.asList("ext1.zip", "ext2.zip")
        );

        String str = extensionOption.toString();
        assertNotNull(str);
        assertTrue(str.contains("2"));
        assertTrue(str.contains("ext-context"));
    }

    @Test
    public void testBrowserFingerprintContextToString() {
        // Test BrowserFingerprintContext toString method
        BrowserFingerprintContext fingerprintContext = new BrowserFingerprintContext(
            "fingerprint-id"
        );

        String str = fingerprintContext.toString();
        assertNotNull(str);
        assertTrue(str.contains("fingerprint-id"));
    }
}

