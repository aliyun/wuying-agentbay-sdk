# Session Metrics Example

This example demonstrates how to retrieve **runtime metrics** for a session using `getMetrics()`.

## Overview

The `getMetrics()` method retrieves real-time metrics from a session including:

- CPU usage and core count
- Memory usage (total and used)
- Disk usage (total and used)
- Network statistics (RX/TX rate and total usage)
- Timestamp of the metrics snapshot

## Running the Example

```bash
mvn exec:java -Dexec.mainClass="com.aliyun.agentbay.examples.SessionMetricsExample"
```

Or compile and run directly:

```bash
mvn clean package
java -cp target/agentbay-sdk-0.14.0.jar com.aliyun.agentbay.examples.SessionMetricsExample
```

## Code Example

```java
import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.model.SessionMetrics;
import com.aliyun.agentbay.model.SessionMetricsResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;

public class SessionMetricsExample {
    public static void main(String[] args) throws Exception {
        AgentBay agentBay = new AgentBay();

        // Create session with linux_latest image
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("linux_latest");
        SessionResult result = agentBay.create(params);

        if (!result.isSuccess()) {
            System.err.println("Failed to create session");
            return;
        }

        // Get metrics
        SessionMetricsResult metricsResult = result.getSession().getMetrics();

        if (metricsResult.isSuccess()) {
            SessionMetrics metrics = metricsResult.getMetrics();

            System.out.println("CPU Count: " + metrics.getCpuCount());
            System.out.println("CPU Usage: " + metrics.getCpuUsedPct() + "%");
            System.out.println("Memory: " + metrics.getMemUsed() + " / " + metrics.getMemTotal());
            System.out.println("Disk: " + metrics.getDiskUsed() + " / " + metrics.getDiskTotal());
            System.out.println("Network RX Rate: " + metrics.getRxRateKBps() + " KB/s");
            System.out.println("Network TX Rate: " + metrics.getTxRateKBps() + " KB/s");
        }

        result.getSession().delete();
    }
}
```

## Expected Output

```
Creating session with linux_latest image...
Session created: mcp-xxxxx

Retrieving session metrics...

=== Session Metrics ===
Timestamp: 2025-12-29T20:00:00+08:00

CPU:
  CPU Count: 4
  CPU Used: 1.23%

Memory:
  Total: 7.38 GB
  Used: 1.99 GB
  Usage: 26.97%

Disk:
  Total: 98.07 GB
  Used: 28.19 GB
  Usage: 28.74%

Network:
  RX Rate: 0.22 KB/s
  TX Rate: 0.38 KB/s
  RX Total: 1247.27 KB
  TX Total: 120.13 KB
```

## Notes

- The `get_metrics` MCP tool is available on `linux_latest` and future images
- Metrics are returned as a snapshot at the time of the call
- All sizes are in bytes (memory and disk) or KB (network)
- Network rates are in KB/s
