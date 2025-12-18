# Mobile App Login Persistence Examples

This directory contains examples demonstrating how to maintain the login state of various mobile applications across different sessions using AgentBay's persistent Context feature.

## Important Notes & Disclaimers

> **⚠️ Custom Image**: The image ID `imgc-0aae4rgl3u35xrhoe` used in the example code is a **temporary custom image** created specifically for demonstration. It consists of the base system image with the target applications installed. For your own use, you should create a custom image containing the applications you intend to automate.

> **⚠️ Risk Control & Validity**: While these examples were verified at the time of writing, mobile applications frequently update their security mechanisms and risk control strategies. The persistence methods described here (based on file system synchronization) **may not guarantee** login persistence indefinitely or across all application versions. These examples are provided for reference purposes to demonstrate the Context persistence capability.

## General Approach

The core idea is to mount a persistent `Context` to the application's data directory on the Android file system. When the session ends, changes in this directory are saved to the Context. When a new session starts with the same Context mounted, the data is restored, preserving the login state.

### Key Steps

1.  **Identify Data Path**: Determine the data storage path for the target application. Usually, this is `/data/data/<package_name>/` or specific subdirectories like `shared_prefs`, `files`, `mmkv`, etc.
2.  **Create Context**: Use `agent_bay.context.get(name="...", create=True)` to get or create a named Context.
3.  **Define ContextSync**: Create a `ContextSync` object mapping the Context ID to the application's data path.
4.  **Create Session**: Pass the `ContextSync` object in the `context_syncs` list when creating a session.

### Common App Data Paths

| App Name | Package Name | Data Path (Example) |
| :--- | :--- | :--- |
| **Xiaohongshu (Red)** | `com.xingin.xhs` | `/data/data/com.xingin.xhs/files/mmkv` |
| **Pinduoduo** | `com.xunmeng.pinduoduo` | `/data/data/com.xunmeng.pinduoduo/files/mmkv` |
| **Weibo** | `com.sina.weibo` | `/data/data/com.sina.weibo/` |
| **Ele.me** | `me.ele` | `/data/data/me.ele/` |

> **Note**: The exact path required for persistence might vary by app version. Sometimes syncing the entire `/data/data/<package_name>/` is easiest, but syncing specific subdirectories (like `mmkv` or `shared_prefs`) can be more efficient if you know where the auth tokens are stored.

## Examples

*   [Xiaohongshu (Red)](./xiaohongshu)
*   [Pinduoduo](./pinduoduo)
*   [Weibo](./weibo)
*   [Ele.me](./eleme)

## Usage

Navigate to the specific example directory and run `main.py`.

```bash
cd xiaohongshu
python main.py
```

Ensure you have:
1.  `AGENTBAY_API_KEY` set in your environment.
2.  The required mobile image available in your AgentBay environment (see Important Notes above).
