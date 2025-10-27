/**
 * Command templates for various AgentBay operations.
 *
 * This module contains shell command templates used by different modules
 * to execute operations in remote environments.
 *
 * Template naming convention:
 * - Use descriptive names that clearly indicate the operation
 * - Group templates by functionality (mobile, desktop, network, etc.)
 * - Use consistent parameter naming across similar templates
 *
 * Parameter conventions:
 * - Use snake_case for parameter names
 * - Include descriptive parameter names (e.g., lock_switch, package_list)
 * - Document expected parameter types and values
 */

// ================================
// Mobile Device Command Templates
// ================================

/**
 * Resolution lock template
 * Parameters:
 *   lock_switch (string): "1" to enable lock, "0" to disable lock
 */
export const RESOLUTION_LOCK_TEMPLATE = "setprop sys.wuying.lockres {lock_switch}";

/**
 * Application whitelist template
 * Parameters:
 *   package_list (string): Newline-separated list of package names
 */
export const APP_WHITELIST_TEMPLATE = `cat > /data/system/pm_whitelist.txt << 'EOF'
{package_list}
EOF
chmod 644 /data/system/pm_whitelist.txt
setprop rw.wy.pm_whitelist.refresh 1
setprop persist.wy.pm_blacklist.switch 2`;

/**
 * Application blacklist template
 * Parameters:
 *   package_list (string): Newline-separated list of package names
 */
export const APP_BLACKLIST_TEMPLATE = `cat > /data/system/pm_blacklist.txt << 'EOF'
{package_list}
EOF
chmod 644 /data/system/pm_blacklist.txt
setprop rw.wy.pm_blacklist.refresh 1
setprop persist.wy.pm_blacklist.switch 1`;

/**
 * Hide navigation bar template
 * Hides the system navigation bar by setting system property and restarting SystemUI
 */
export const HIDE_NAVIGATION_BAR_TEMPLATE = "setprop persist.wy.hasnavibar false; killall com.android.systemui";

/**
 * Show navigation bar template
 * Shows the system navigation bar by setting system property and restarting SystemUI
 */
export const SHOW_NAVIGATION_BAR_TEMPLATE = "setprop persist.wy.hasnavibar true; killall com.android.systemui";

/**
 * Uninstall blacklist template
 * Parameters:
 *   package_list (string): Semicolon-separated list of package names
 */
export const UNINSTALL_BLACKLIST_TEMPLATE = "setprop persist.wy.pm_lock \"{package_list}\"";

/**
 * Mobile command templates mapping for easy access
 */
export const MOBILE_COMMAND_TEMPLATES: Record<string, string> = {
  "resolution_lock_enable": "setprop sys.wuying.lockres 1",
  "resolution_lock_disable": "setprop sys.wuying.lockres 0",
  "app_whitelist": APP_WHITELIST_TEMPLATE,
  "app_blacklist": APP_BLACKLIST_TEMPLATE,
  "hide_navigation_bar": HIDE_NAVIGATION_BAR_TEMPLATE,
  "show_navigation_bar": SHOW_NAVIGATION_BAR_TEMPLATE,
  "uninstall_blacklist": UNINSTALL_BLACKLIST_TEMPLATE,
};

/**
 * Get a mobile command template by name
 * 
 * @param templateName - The name of the template to retrieve
 * @returns The template string if found, undefined otherwise
 */
export function getMobileCommandTemplate(templateName: string): string | undefined {
  return MOBILE_COMMAND_TEMPLATES[templateName];
}

/**
 * Check if a mobile command template exists
 * 
 * @param templateName - The name of the template to check
 * @returns True if the template exists, false otherwise
 */
export function hasMobileCommandTemplate(templateName: string): boolean {
  return templateName in MOBILE_COMMAND_TEMPLATES;
}

/**
 * Replace placeholders in a template with actual values
 * 
 * @param template - The template string with placeholders
 * @param replacements - Object containing placeholder-value pairs
 * @returns The template with placeholders replaced
 */
export function replaceTemplatePlaceholders(
  template: string, 
  replacements: Record<string, string>
): string {
  let result = template;
  for (const [placeholder, value] of Object.entries(replacements)) {
    const placeholderPattern = new RegExp(`\\{${placeholder}\\}`, 'g');
    result = result.replace(placeholderPattern, value);
  }
  return result;
}
