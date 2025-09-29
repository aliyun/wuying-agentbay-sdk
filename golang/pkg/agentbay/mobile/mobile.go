package mobile

import (
	"fmt"
	"strings"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/command"
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay/models"
)

// Mobile handles mobile environment configuration operations
type Mobile struct {
	command *command.Command
}

// NewMobile creates a new Mobile instance
func NewMobile(cmd *command.Command) *Mobile {
	return &Mobile{
		command: cmd,
	}
}

// Configure configures mobile settings from MobileExtraConfig
func (m *Mobile) Configure(mobileConfig *models.MobileExtraConfig) error {
	if mobileConfig == nil {
		return fmt.Errorf("no mobile configuration provided")
	}

	// Configure resolution lock
	if err := m.setResolutionLock(mobileConfig.LockResolution); err != nil {
		return fmt.Errorf("failed to set resolution lock: %v", err)
	}

	// Configure app management rules
	if mobileConfig.AppManagerRule != nil && mobileConfig.AppManagerRule.RuleType != "" {
		appRule := mobileConfig.AppManagerRule
		packageNames := appRule.AppPackageNameList

		if len(packageNames) > 0 && (appRule.RuleType == "White" || appRule.RuleType == "Black") {
			if appRule.RuleType == "White" {
				if err := m.setAppWhitelist(packageNames); err != nil {
					return fmt.Errorf("failed to set app whitelist: %v", err)
				}
			} else {
				if err := m.setAppBlacklist(packageNames); err != nil {
					return fmt.Errorf("failed to set app blacklist: %v", err)
				}
			}
		} else if len(packageNames) == 0 {
			return fmt.Errorf("no package names provided for %s list", appRule.RuleType)
		}
	}

	return nil
}

// SetResolutionLock sets display resolution lock for mobile devices
func (m *Mobile) SetResolutionLock(enable bool) error {
	return m.setResolutionLock(enable)
}

// setResolutionLock internal method to set resolution lock
func (m *Mobile) setResolutionLock(enable bool) error {
	var templateName string
	if enable {
		templateName = "resolution_lock_enable"
	} else {
		templateName = "resolution_lock_disable"
	}

	template, exists := command.GetMobileCommandTemplate(templateName)
	if !exists {
		return fmt.Errorf("resolution lock template not found: %s", templateName)
	}

	return m.executeTemplateCommand(template, templateName)
}

// setAppWhitelist sets app whitelist configuration
func (m *Mobile) setAppWhitelist(packageNames []string) error {
	template, exists := command.GetMobileCommandTemplate("app_whitelist")
	if !exists {
		return fmt.Errorf("app whitelist template not found")
	}

	// Replace placeholder with actual package names (newline-separated for file content)
	packageList := strings.Join(packageNames, "\n")
	command := strings.ReplaceAll(template, "{package_list}", packageList)

	return m.executeTemplateCommand(command, fmt.Sprintf("App whitelist configuration (%d packages)", len(packageNames)))
}

// setAppBlacklist sets app blacklist configuration
func (m *Mobile) setAppBlacklist(packageNames []string) error {
	template, exists := command.GetMobileCommandTemplate("app_blacklist")
	if !exists {
		return fmt.Errorf("app blacklist template not found")
	}

	// Replace placeholder with actual package names (newline-separated for file content)
	packageList := strings.Join(packageNames, "\n")
	command := strings.ReplaceAll(template, "{package_list}", packageList)

	return m.executeTemplateCommand(command, fmt.Sprintf("App blacklist configuration (%d packages)", len(packageNames)))
}

// executeTemplateCommand executes a mobile command template
func (m *Mobile) executeTemplateCommand(commandTemplate, description string) error {
	if m.command == nil {
		return fmt.Errorf("command service not available")
	}

	fmt.Printf("Executing %s\n", description)

	result, err := m.command.ExecuteCommand(commandTemplate)
	if err != nil {
		return fmt.Errorf("failed to execute %s: %v", description, err)
	}

	if result != nil && result.Output != "" {
		fmt.Printf("✅ %s completed successfully\n", description)
	}

	return nil
}
