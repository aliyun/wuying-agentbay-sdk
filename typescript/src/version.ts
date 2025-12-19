/**
 * Version information for the AgentBay SDK
 * Automatically read from package.json
 */

import * as fs from "fs";
import * as path from "path";

function getVersionFromPackageJson(): string {
  try {
    // Get the path to package.json (relative to this file)
    // When compiled, this will be in dist/, so we need to go up to find package.json
    const packageJsonPath = path.join(__dirname, "..", "package.json");
    
    if (fs.existsSync(packageJsonPath)) {
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf-8"));
      return packageJson.version || "0.0.0";
    }
  } catch (error) {
    // Fallback to default version if reading fails
  }
  
  // Fallback version if package.json cannot be read
  return "0.13.0";
}

/**
 * Check if this is a release build.
 *
 * This value can be overridden at build time by replacing the placeholder below.
 * The CI/CD workflow will replace __AGENTBAY_IS_RELEASE_BUILD__ with true for release builds.
 */
function isReleaseBuild(): boolean {
  // This placeholder will be replaced by the build process
  // For release builds: sed -i 's/__AGENTBAY_IS_RELEASE_BUILD__/true/g' src/version.ts
  return __AGENTBAY_IS_RELEASE_BUILD__;  // Default: false for development builds
}

// For release builds, the CI/CD will replace __AGENTBAY_IS_RELEASE_BUILD__ with true
const __AGENTBAY_IS_RELEASE_BUILD__ = false;

export const VERSION = getVersionFromPackageJson();
export const IS_RELEASE = isReleaseBuild();

