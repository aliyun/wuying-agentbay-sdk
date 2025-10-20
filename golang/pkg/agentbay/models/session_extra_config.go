package models

import (
	"encoding/json"
)

// AppManagerRule defines rules for managing app access on mobile devices
type AppManagerRule struct {
	// RuleType specifies the type of rule to apply
	// "White" for whitelist mode (only allow specified apps)
	// "Black" for blacklist mode (block specified apps)
	RuleType string `json:"rule_type"`

	// AppPackageNameList contains the list of Android package names to apply the rule to
	AppPackageNameList []string `json:"app_package_name_list"`
}

// MobileExtraConfig contains mobile-specific configuration settings
type MobileExtraConfig struct {
	// LockResolution determines whether to lock the screen resolution
	// true: Locks resolution for consistent mobile testing environments
	// false: Allows adaptive resolution for different device types
	LockResolution bool `json:"lock_resolution"`

	// AppManagerRule defines rules for managing app access on the mobile device
	AppManagerRule *AppManagerRule `json:"app_manager_rule,omitempty"`

	// HideNavigationBar determines whether to hide the system navigation bar
	// true: Hides the navigation bar by setting persist.wy.hasnavibar to false and restarting SystemUI
	// false: Shows the navigation bar (default behavior)
	HideNavigationBar bool `json:"hide_navigation_bar"`

	// UninstallBlacklist contains a list of package names that should be protected from uninstallation
	// These packages will be added to the system's uninstall protection list
	UninstallBlacklist []string `json:"uninstall_blacklist,omitempty"`
}

// ExtraConfigs contains extra configuration settings for different session types
type ExtraConfigs struct {
	// Mobile contains mobile-specific configuration settings
	Mobile *MobileExtraConfig `json:"mobile,omitempty"`
}

// ToJSON converts ExtraConfigs to JSON string
func (e *ExtraConfigs) ToJSON() (string, error) {
	if e == nil {
		return "", nil
	}

	data, err := json.Marshal(e)
	if err != nil {
		return "", err
	}

	return string(data), nil
}

// FromJSON creates ExtraConfigs from JSON string
func (e *ExtraConfigs) FromJSON(jsonStr string) error {
	if jsonStr == "" {
		return nil
	}

	return json.Unmarshal([]byte(jsonStr), e)
}
