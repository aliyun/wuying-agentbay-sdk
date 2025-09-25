from typing import List, Dict, Any
from agentbay.api.base_service import BaseService
from agentbay.logger import get_logger
from agentbay.command import MOBILE_COMMAND_TEMPLATES

# Initialize logger for this module
logger = get_logger("mobile")


class Mobile(BaseService):
    """
    Handles mobile environment configuration operations.
    
    Provides methods for session-level and runtime mobile configurations.
    """

    def configure(self, mobile_config):
        """
        Configure mobile settings from MobileExtraConfig.
        
        Args:
            mobile_config: MobileExtraConfig object containing mobile configuration.
        """
        if not mobile_config:
            logger.warning("No mobile configuration provided")
            return
        
        # Configure resolution lock
        if mobile_config.lock_resolution is not None:
            self._set_resolution_lock(mobile_config.lock_resolution)
        
        # Configure app management rules
        if mobile_config.app_manager_rule and mobile_config.app_manager_rule.rule_type:
            app_rule = mobile_config.app_manager_rule
            package_names = app_rule.app_package_name_list or []
            
            if package_names and app_rule.rule_type in ["White", "Black"]:
                if app_rule.rule_type == "White":
                    self._set_app_whitelist(package_names)
                else:
                    self._set_app_blacklist(package_names)
            elif not package_names:
                logger.warning(f"No package names provided for {app_rule.rule_type} list")

    def set_resolution_lock(self, enable: bool):
        """
        Set display resolution lock for mobile devices.
        
        Args:
            enable (bool): True to enable, False to disable.
        """
        self._set_resolution_lock(enable)

    def set_app_whitelist(self, package_names: List[str]):
        """
        Set application whitelist.
        
        Args:
            package_names (List[str]): List of Android package names to whitelist.
        """
        if not package_names:
            logger.warning("Empty package names list for whitelist")
            return
        self._set_app_whitelist(package_names)

    def set_app_blacklist(self, package_names: List[str]):
        """
        Set application blacklist.
        
        Args:
            package_names (List[str]): List of Android package names to blacklist.
        """
        if not package_names:
            logger.warning("Empty package names list for blacklist")
            return
        self._set_app_blacklist(package_names)

    def _execute_template_command(self, template_name: str, params: Dict[str, Any], operation_name: str):
        """Execute a command using template and parameters."""
        template = MOBILE_COMMAND_TEMPLATES.get(template_name)
        if not template:
            logger.error(f"Template '{template_name}' not found")
            return
            
        command = template.format(**params)
        
        logger.info(f"Executing {operation_name}")
        result = self.session.command.execute_command(command)
        
        if result.success:
            logger.info(f"✅ {operation_name} completed successfully")
        else:
            logger.error(f"❌ {operation_name} failed: {result.error_message}")

    def _set_resolution_lock(self, enable: bool):
        """Execute resolution lock command."""
        params = {"lock_switch": 1 if enable else 0}
        operation_name = f"Resolution lock {'enable' if enable else 'disable'}"
        self._execute_template_command("resolution_lock", params, operation_name)

    def _set_app_whitelist(self, package_names: List[str]):
        """Execute app whitelist command."""
        params = {
            "package_list": '\n'.join(package_names),
            "package_count": len(package_names)
        }
        operation_name = f"App whitelist configuration ({len(package_names)} packages)"
        self._execute_template_command("app_whitelist", params, operation_name)

    def _set_app_blacklist(self, package_names: List[str]):
        """Execute app blacklist command."""
        params = {
            "package_list": '\n'.join(package_names),
            "package_count": len(package_names)
        }
        operation_name = f"App blacklist configuration ({len(package_names)} packages)"
        self._execute_template_command("app_blacklist", params, operation_name)
