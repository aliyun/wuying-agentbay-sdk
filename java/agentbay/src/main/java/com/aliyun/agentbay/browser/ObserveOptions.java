package com.aliyun.agentbay.browser;

import java.util.HashMap;
import java.util.Map;

/**
 * Options for browser observe operations - matches Python ObserveOptions
 */
public class ObserveOptions {
    private String instruction;
    private Boolean iframes;
    private Integer domSettleTimeoutMs;
    private Boolean useVision;

    public ObserveOptions(String instruction) {
        this.instruction = instruction;
    }

    public ObserveOptions(String instruction, Boolean iframes, Integer domSettleTimeoutMs, Boolean useVision) {
        this.instruction = instruction;
        this.iframes = iframes;
        this.domSettleTimeoutMs = domSettleTimeoutMs;
        this.useVision = useVision;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("instruction", instruction);
        if (iframes != null) map.put("iframes", iframes);
        if (domSettleTimeoutMs != null) map.put("dom_settle_timeout_ms", domSettleTimeoutMs);
        if (useVision != null) map.put("use_vision", useVision);
        return map;
    }

    // Getters and setters
    public String getInstruction() { return instruction; }
    public void setInstruction(String instruction) { this.instruction = instruction; }

    public Boolean getIframes() { return iframes; }
    public void setIframes(Boolean iframes) { this.iframes = iframes; }

    public Integer getDomSettleTimeoutMs() { return domSettleTimeoutMs; }
    public void setDomSettleTimeoutMs(Integer domSettleTimeoutMs) { this.domSettleTimeoutMs = domSettleTimeoutMs; }

    public Boolean getUseVision() { return useVision; }
    public void setUseVision(Boolean useVision) { this.useVision = useVision; }
}