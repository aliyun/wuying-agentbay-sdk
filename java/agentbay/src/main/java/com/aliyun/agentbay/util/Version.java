package com.aliyun.agentbay.util;

import java.io.BufferedReader;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Enumeration;
import java.util.Properties;
import java.util.jar.Manifest;
import java.util.jar.Attributes;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Version information for the AgentBay SDK.
 * 
 * This class provides SDK version information for tracking and statistics purposes.
 * The version is read from multiple sources in order of preference:
 * 1. Maven-generated pom.properties file (META-INF/maven/{groupId}/{artifactId}/pom.properties)
 * 2. MANIFEST.MF Implementation-Version attribute (from SDK's own JAR)
 * 3. pom.xml file (for development mode)
 * 4. Default version constant
 */
public class Version {
    private static final Logger logger = LoggerFactory.getLogger(Version.class);
    
    private static final String DEFAULT_VERSION = "0.0.3";
    private static final String VERSION_PROPERTIES_FILE = "/META-INF/maven/com.aliyun/agentbay-sdk/pom.properties";
    
    private static final String VERSION = getVersion();
    private static final boolean IS_RELEASE = isReleaseBuild();
    
    /**
     * Get the SDK version.
     * 
     * This method tries multiple sources in order:
     * 1. Maven-generated pom.properties file
     * 2. MANIFEST.MF Implementation-Version (from SDK's own JAR)
     * 3. pom.xml file (for development mode)
     * 4. Default version constant
     * 
     * @return SDK version string
     */
    private static String getVersion() {
        // Try 1: Read from Maven-generated pom.properties file
        String version = readVersionFromPomProperties();
        if (version != null && !version.isEmpty()) {
            logger.debug("SDK version {} read from pom.properties: {}", version, VERSION_PROPERTIES_FILE);
            return version;
        }
        
        // Try 2: Read from MANIFEST.MF (from SDK's own JAR, not other JARs)
        version = readVersionFromManifest();
        if (version != null && !version.isEmpty()) {
            logger.debug("SDK version {} read from MANIFEST.MF", version);
            return version;
        }
        
        // Try 3: Read from pom.xml (for development mode)
        version = readVersionFromPomXml();
        if (version != null && !version.isEmpty()) {
            logger.debug("SDK version {} read from pom.xml", version);
            return version;
        }
        
        // Fallback: Use default version (this should match pom.xml version)
        logger.debug("SDK version {} read from DEFAULT_VERSION constant", DEFAULT_VERSION);
        return DEFAULT_VERSION;
    }
    
    /**
     * Read version from Maven-generated pom.properties file.
     * 
     * @return version string, or null if not found
     */
    private static String readVersionFromPomProperties() {
        InputStream is = null;
        try {
            is = Version.class.getResourceAsStream(VERSION_PROPERTIES_FILE);
            if (is != null) {
                Properties props = new Properties();
                props.load(is);
                String version = props.getProperty("version");
                if (version != null && !version.isEmpty()) {
                    return version;
                }
            }
        } catch (Exception e) {
            // Ignore exceptions and try next method
        } finally {
            if (is != null) {
                try {
                    is.close();
                } catch (Exception e) {
                    // Ignore close exceptions
                }
            }
        }
        return null;
    }
    
    /**
     * Read version from pom.xml file (for development mode).
     * Similar to Python SDK's approach of reading from pyproject.toml.
     * 
     * This method tries to find pom.xml in multiple locations:
     * 1. java/agentbay/pom.xml (most likely location when running tests)
     * 2. Current working directory/pom.xml
     * 3. Relative paths from class location
     * 
     * @return version string, or null if not found
     */
    private static String readVersionFromPomXml() {
        try {
            Path currentPath = Paths.get("").toAbsolutePath();
            
            // Try multiple possible locations
            Path[] possiblePaths = {
                // Most common: java/agentbay/pom.xml (when running from project root)
                currentPath.resolve("java").resolve("agentbay").resolve("pom.xml"),
                // Current directory (when running from java/agentbay)
                currentPath.resolve("pom.xml"),
                // Parent directory (when running from java/agentbay/target)
                currentPath.getParent().resolve("pom.xml"),
            };
            
            for (Path pomPath : possiblePaths) {
                if (Files.exists(pomPath) && Files.isRegularFile(pomPath)) {
                    try (BufferedReader reader = Files.newBufferedReader(pomPath)) {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            // Look for: <version>0.0.3</version>
                            // Handle both single-line and multi-line formats
                            line = line.trim();
                            
                            // Single line format: <version>0.0.3</version>
                            if (line.startsWith("<version>") && line.contains("</version>")) {
                                int start = line.indexOf("<version>") + "<version>".length();
                                int end = line.indexOf("</version>");
                                if (end > start) {
                                    String version = line.substring(start, end).trim();
                                    if (!version.isEmpty()) {
                                        return version;
                                    }
                                }
                            }
                            // Multi-line format: <version>\n  0.0.3\n</version>
                            else if (line.startsWith("<version>") && !line.contains("</version>")) {
                                // Read next line for version value
                                String nextLine = reader.readLine();
                                if (nextLine != null) {
                                    String version = nextLine.trim();
                                    if (!version.isEmpty() && !version.startsWith("<")) {
                                        return version;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        } catch (Exception e) {
            // Ignore exceptions and try next method
            logger.debug("Failed to read version from pom.xml: {}", e.getMessage());
        }
        return null;
    }
    
    /**
     * Read version from MANIFEST.MF Implementation-Version attribute.
     * 
     * This method searches through all MANIFEST.MF files in the classpath
     * and finds the one that belongs to our SDK (by checking Implementation-Title).
     * 
     * @return version string, or null if not found
     */
    private static String readVersionFromManifest() {
        try {
            // Search through all MANIFEST.MF files in classpath to find our SDK's manifest
            Enumeration<URL> resources = Version.class.getClassLoader().getResources("META-INF/MANIFEST.MF");
            while (resources.hasMoreElements()) {
                URL url = resources.nextElement();
                InputStream is = null;
                try {
                    is = url.openStream();
                    Manifest manifest = new Manifest(is);
                    Attributes attributes = manifest.getMainAttributes();
                    
                    // Check if this is our SDK's manifest by looking at Implementation-Title
                    String title = attributes.getValue("Implementation-Title");
                    String bundleName = attributes.getValue("Bundle-SymbolicName");
                    
                    // Only accept manifest from our SDK
                    boolean isOurSdk = (title != null && (title.contains("agentbay") || title.contains("AgentBay"))) ||
                                      (bundleName != null && bundleName.contains("agentbay"));
                    
                    if (isOurSdk) {
                        String version = attributes.getValue("Implementation-Version");
                        if (version != null && !version.isEmpty()) {
                            return version;
                        }
                        
                        // Try Specification-Version as fallback
                        version = attributes.getValue("Specification-Version");
                        if (version != null && !version.isEmpty()) {
                            return version;
                        }
                    }
                } catch (Exception e) {
                    // Continue to next manifest
                } finally {
                    if (is != null) {
                        try {
                            is.close();
                        } catch (Exception e) {
                            // Ignore close exceptions
                        }
                    }
                }
            }
        } catch (Exception e) {
            // Ignore exceptions and try next method
        }
        return null;
    }
    
    /**
     * Check if this is a release build.
     * 
     * The release flag is determined in the following order:
     * 1. MANIFEST.MF AgentBay-Is-Release attribute (injected at build time)
     * 2. System property: agentbay.is.release.build
     * 3. Environment variable: AGENTBAY_IS_RELEASE_BUILD
     * 4. Default: false
     * 
     * For release builds, use: mvn deploy -Dagentbay.is.release.build=true
     * 
     * @return true if this is a release build, false otherwise
     */
    private static boolean isReleaseBuild() {
        // Try 1: Read from MANIFEST.MF (injected at build time, most reliable for packaged SDK)
        String manifestRelease = readReleaseFromManifest();
        if (manifestRelease != null) {
            return Boolean.parseBoolean(manifestRelease);
        }
        
        // Try 2: Check system property
        String isRelease = System.getProperty("agentbay.is.release.build");
        if (isRelease != null) {
            return Boolean.parseBoolean(isRelease);
        }
        
        // Try 3: Check environment variable
        String envRelease = System.getenv("AGENTBAY_IS_RELEASE_BUILD");
        if (envRelease != null) {
            return Boolean.parseBoolean(envRelease);
        }
        
        // Default: false for development builds
        return false;
    }
    
    /**
     * Read release flag from MANIFEST.MF AgentBay-Is-Release attribute.
     * This is injected at build time via maven-jar-plugin.
     * 
     * @return "true" or "false" string, or null if not found
     */
    private static String readReleaseFromManifest() {
        try {
            // Search through all MANIFEST.MF files to find our SDK's manifest
            Enumeration<URL> resources = Version.class.getClassLoader().getResources("META-INF/MANIFEST.MF");
            while (resources.hasMoreElements()) {
                URL url = resources.nextElement();
                InputStream is = null;
                try {
                    is = url.openStream();
                    Manifest manifest = new Manifest(is);
                    Attributes attributes = manifest.getMainAttributes();
                    
                    // Check if this is our SDK's manifest
                    String title = attributes.getValue("Implementation-Title");
                    boolean isOurSdk = title != null && (title.contains("agentbay") || title.contains("AgentBay"));
                    
                    if (isOurSdk) {
                        String releaseFlag = attributes.getValue("AgentBay-Is-Release");
                        if (releaseFlag != null && !releaseFlag.isEmpty()) {
                            return releaseFlag;
                        }
                    }
                } catch (Exception e) {
                    // Continue to next manifest
                } finally {
                    if (is != null) {
                        try {
                            is.close();
                        } catch (Exception e) {
                            // Ignore
                        }
                    }
                }
            }
        } catch (Exception e) {
            // Ignore and fall back to other methods
        }
        return null;
    }
    
    /**
     * Get the SDK version string.
     * 
     * @return SDK version string
     */
    public static String getVersionString() {
        return VERSION;
    }
    
    /**
     * Check if this is a release build.
     * 
     * @return true if this is a release build, false otherwise
     */
    public static boolean isRelease() {
        return IS_RELEASE;
    }
    
    /**
     * Get SDK language identifier.
     * 
     * @return "java"
     */
    public static String getSdkLanguage() {
        return "java";
    }
}

