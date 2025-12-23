package com.aliyun.agentbay.mobile;

/**
 * Configuration for mobile simulation.
 */
public class MobileSimulateConfig {
    private boolean simulate;
    private String simulatePath;
    private MobileSimulateMode simulateMode;
    private String simulatedContextId;

    public MobileSimulateConfig() {
        this.simulate = false;
        this.simulateMode = MobileSimulateMode.PROPERTIES_ONLY;
    }

    public MobileSimulateConfig(boolean simulate, String simulatePath, 
                               MobileSimulateMode simulateMode, String simulatedContextId) {
        this.simulate = simulate;
        this.simulatePath = simulatePath;
        this.simulateMode = simulateMode;
        this.simulatedContextId = simulatedContextId;
    }

    public boolean isSimulate() {
        return simulate;
    }

    public void setSimulate(boolean simulate) {
        this.simulate = simulate;
    }

    public String getSimulatePath() {
        return simulatePath;
    }

    public void setSimulatePath(String simulatePath) {
        this.simulatePath = simulatePath;
    }

    public MobileSimulateMode getSimulateMode() {
        return simulateMode;
    }

    public void setSimulateMode(MobileSimulateMode simulateMode) {
        this.simulateMode = simulateMode;
    }

    public String getSimulatedContextId() {
        return simulatedContextId;
    }

    public void setSimulatedContextId(String simulatedContextId) {
        this.simulatedContextId = simulatedContextId;
    }
}
