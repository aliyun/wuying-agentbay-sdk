## Natural Language Mobile Control (Cookbook)

This cookbook example provides two ways to control a cloud phone with natural language:

- **CLI / LangChain agent (async)**: generic mobile tools + optional app presets
- **Web UI (FastAPI)**: create a session, preview the cloud phone (iframe), type instructions, and watch results live

### Prerequisites

- `AGENTBAY_API_KEY`
- `DASHSCOPE_API_KEY` (DashScope OpenAI-compatible)

Optional:

- `MOBILE_IMAGE_ID` (defaults to a demo image id)

### Run (Web UI)

From repo root:

```bash
source agentbay_example_env/bin/activate
python cookbook/mobile/nl-mobile-control/server.py
```

Open:

- `http://127.0.0.1:8000`

### Run (CLI)

From repo root:

```bash
cd cookbook/mobile/nl-mobile-control/langchain
python src/nl_mobile_agent_example.py
```


