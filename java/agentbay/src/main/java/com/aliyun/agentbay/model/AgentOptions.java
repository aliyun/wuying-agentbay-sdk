package com.aliyun.agentbay.model;

public class AgentOptions {
    private boolean useVision;
    private String outputSchema;

    public AgentOptions() {
        this.useVision = false;
        this.outputSchema = "";
    }

    public AgentOptions(boolean useVision, String outputSchema) {
        this.useVision = useVision;
        this.outputSchema = outputSchema;
    }

    public boolean isUseVision() {
        return useVision;
    }

    public void setUseVision(boolean useVision) {
        this.useVision = useVision;
    }

    public String getOutputSchema() {
        return outputSchema;
    }

    public void setOutputSchema(String outputSchema) {
        this.outputSchema = outputSchema;
    }
}
