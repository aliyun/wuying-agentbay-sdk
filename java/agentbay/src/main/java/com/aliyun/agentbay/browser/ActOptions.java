package com.aliyun.agentbay.browser;

import java.util.HashMap;
import java.util.Map;

/**
 * Options for browser act operations - matches Python ActOptions
 */
public class ActOptions {
    private String action;
    private Integer timeoutMS;
    private Boolean iframes;
    private Integer domSettleTimeoutMs;
    private Map<String, String> variables;
    private Boolean useVision;

    public ActOptions(String action) {
        this.action = action;
    }

    public ActOptions(String action, Integer timeoutMS, Boolean iframes, Integer domSettleTimeoutMs, Map<String, String> variables, Boolean useVision) {
        this.action = action;
        this.timeoutMS = timeoutMS;
        this.iframes = iframes;
        this.domSettleTimeoutMs = domSettleTimeoutMs;
        this.variables = variables;
        this.useVision = useVision;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("action", action);
        if (timeoutMS != null) map.put("timeoutMS", timeoutMS);
        if (iframes != null) map.put("iframes", iframes);
        if (domSettleTimeoutMs != null) map.put("dom_settle_timeout_ms", domSettleTimeoutMs);
        if (variables != null) map.put("variables", variables);
        if (useVision != null) map.put("use_vision", useVision);
        return map;
    }

    // Getters and setters
    public String getAction() { return action; }
    public void setAction(String action) { this.action = action; }

    public Integer getTimeoutMS() { return timeoutMS; }
    public void setTimeoutMS(Integer timeoutMS) { this.timeoutMS = timeoutMS; }

    public Boolean getIframes() { return iframes; }
    public void setIframes(Boolean iframes) { this.iframes = iframes; }

    public Integer getDomSettleTimeoutMs() { return domSettleTimeoutMs; }
    public void setDomSettleTimeoutMs(Integer domSettleTimeoutMs) { this.domSettleTimeoutMs = domSettleTimeoutMs; }

    public Map<String, String> getVariables() { return variables; }
    public void setVariables(Map<String, String> variables) { this.variables = variables; }

    public Boolean getUseVision() { return useVision; }
    public void setUseVision(Boolean useVision) { this.useVision = useVision; }
}