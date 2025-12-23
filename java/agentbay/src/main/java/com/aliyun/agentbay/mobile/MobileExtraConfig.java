package com.aliyun.agentbay.mobile;

import java.util.List;

/**
 * Configuration for mobile environment settings.
 */
public class MobileExtraConfig {
    private Boolean lockResolution;
    private AppManagerRule appManagerRule;
    private Boolean hideNavigationBar;
    private List<String> uninstallBlacklist;

    public MobileExtraConfig() {
    }

    public MobileExtraConfig(Boolean lockResolution, AppManagerRule appManagerRule, 
                            Boolean hideNavigationBar, List<String> uninstallBlacklist) {
        this.lockResolution = lockResolution;
        this.appManagerRule = appManagerRule;
        this.hideNavigationBar = hideNavigationBar;
        this.uninstallBlacklist = uninstallBlacklist;
    }

    public Boolean getLockResolution() {
        return lockResolution;
    }

    public void setLockResolution(Boolean lockResolution) {
        this.lockResolution = lockResolution;
    }

    public AppManagerRule getAppManagerRule() {
        return appManagerRule;
    }

    public void setAppManagerRule(AppManagerRule appManagerRule) {
        this.appManagerRule = appManagerRule;
    }

    public Boolean getHideNavigationBar() {
        return hideNavigationBar;
    }

    public void setHideNavigationBar(Boolean hideNavigationBar) {
        this.hideNavigationBar = hideNavigationBar;
    }

    public List<String> getUninstallBlacklist() {
        return uninstallBlacklist;
    }

    public void setUninstallBlacklist(List<String> uninstallBlacklist) {
        this.uninstallBlacklist = uninstallBlacklist;
    }
}
