"""
Command templates for various AgentBay operations.

This module contains shell command templates used by different modules
to execute operations in remote environments.

Template naming convention:
- Use descriptive names that clearly indicate the operation
- Group templates by functionality (mobile, desktop, network, etc.)
- Use consistent parameter naming across similar templates

Parameter conventions:
- Use snake_case for parameter names
- Include descriptive parameter names (e.g., lock_switch, package_list)
- Document expected parameter types and values
"""

# ================================
# Mobile Device Command Templates
# ================================

# Resolution lock template
# Parameters:
#   lock_switch (int): 1 to enable lock, 0 to disable lock
RESOLUTION_LOCK_TEMPLATE = "setprop sys.wuying.lockres {lock_switch}"

# Application whitelist template
# Parameters:
#   package_list (str): Newline-separated list of package names
APP_WHITELIST_TEMPLATE = """cat > /data/system/pm_whitelist.txt << 'EOF'
{package_list}
EOF
chmod 644 /data/system/pm_whitelist.txt
setprop rw.wy.pm_whitelist.refresh 1
setprop persist.wy.pm_blacklist.switch 2
"""

# Application blacklist template
# Parameters:
#   package_list (str): Newline-separated list of package names
APP_BLACKLIST_TEMPLATE = """cat > /data/system/pm_blacklist.txt << 'EOF'
{package_list}
EOF
chmod 644 /data/system/pm_blacklist.txt
setprop rw.wy.pm_blacklist.refresh 1
setprop persist.wy.pm_blacklist.switch 1
"""

# Hide navigation bar template
# Hides the system navigation bar by setting system property and restarting SystemUI
HIDE_NAVIGATION_BAR_TEMPLATE = "setprop persist.wy.hasnavibar false; killall com.android.systemui"

# Show navigation bar template
# Shows the system navigation bar by setting system property and restarting SystemUI
SHOW_NAVIGATION_BAR_TEMPLATE = "setprop persist.wy.hasnavibar true; killall com.android.systemui"

# Uninstall blacklist template
# Parameters:
#   package_list (str): Semicolon-separated list of package names
UNINSTALL_BLACKLIST_TEMPLATE = "setprop persist.wy.pm_lock \"{package_list}\""

# Mobile command templates dictionary for easy access
MOBILE_COMMAND_TEMPLATES = {
    "resolution_lock": RESOLUTION_LOCK_TEMPLATE,
    "app_whitelist": APP_WHITELIST_TEMPLATE,
    "app_blacklist": APP_BLACKLIST_TEMPLATE,
    "hide_navigation_bar": HIDE_NAVIGATION_BAR_TEMPLATE,
    "show_navigation_bar": SHOW_NAVIGATION_BAR_TEMPLATE,
    "uninstall_blacklist": UNINSTALL_BLACKLIST_TEMPLATE,
}
