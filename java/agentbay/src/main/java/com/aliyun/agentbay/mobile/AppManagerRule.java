package com.aliyun.agentbay.mobile;

import java.util.List;

/**
 * App manager rule for whitelist/blacklist configuration.
 */
public class AppManagerRule {
    private String ruleType; // "White" or "Black"
    private List<String> appPackageNameList;

    public AppManagerRule() {
    }

    public AppManagerRule(String ruleType, List<String> appPackageNameList) {
        this.ruleType = ruleType;
        this.appPackageNameList = appPackageNameList;
    }

    public String getRuleType() {
        return ruleType;
    }

    public void setRuleType(String ruleType) {
        this.ruleType = ruleType;
    }

    public List<String> getAppPackageNameList() {
        return appPackageNameList;
    }

    public void setAppPackageNameList(List<String> appPackageNameList) {
        this.appPackageNameList = appPackageNameList;
    }
}
