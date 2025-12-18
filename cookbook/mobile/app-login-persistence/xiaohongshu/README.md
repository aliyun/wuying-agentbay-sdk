# Mobile App Login Persistence Example

This example demonstrates how to maintain the login state of a mobile application across different sessions using AgentBay's persistent Context feature.

## Scenario

We want to run a mobile agent that uses the "Xiaohongshu" (Red) app. To avoid logging in every time a new session starts, we use a `Context` to persist the application's data files.

## Prerequisites

- Python 3.8+
- AgentBay SDK (`pip install agentbay`)
- A custom AgentBay image with the target app installed (Example uses `imgc-0aae4rgl3u35xrhoe`).
- `AGENTBAY_API_KEY` set in your environment.

## How it works

1. **Context Creation**: We create a named Context (`xhs-login-persistence-ctx`). If it already exists, we reuse it.
2. **Mounting**: We define a `ContextSync` that maps the Context to the app's data directory on the mobile device. 
   - For Xiaohongshu, the key data path is `/data/data/com.xingin.xhs/files/mmkv`.
3. **Session 1 (Login)**: 
   - We create a session with the Context mounted.
   - You manually login to the app via the browser interface.
   - When the session ends, the changes in the mounted path are synced back to the Context.
4. **Session 2 (Persistence)**:
   - We create a new session with the *same* Context.
   - The files are restored to the path.
   - The app should recognize the previous login state.

## Usage

1. Set your API Key:
   ```bash
   export AGENTBAY_API_KEY=your_api_key_here
   ```

2. Run the example:
   ```bash
   python main.py
   ```

3. Follow the on-screen instructions to login and verify.

