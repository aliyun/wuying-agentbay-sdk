## Natural Language Mobile Control (LangChain, Async)

This example shows how to use **LangChain (LangGraph ReAct agent)** to control an **AgentBay mobile session** with natural language.

It is **app-agnostic** (generic tools like tap/swipe/input/tap_text/get_visible_texts), and this directory also provides a **Xiaohongshu preset** (`imgc-0aae4rgl3u35xrhoe`, `com.xingin.xhs`) for a stable demo.

### Prerequisites

- `AGENTBAY_API_KEY` is set in your environment
- `DASHSCOPE_API_KEY` is set in your environment (Bailian / DashScope OpenAI-compatible mode)

Optional:

- `DASHSCOPE_MODEL` (default: `qwen3-max`)

### Run

From repo root:

```bash
cd cookbook/mobile/xiaohongshu-nl-control/async/langchain
python src/nl_mobile_agent_example.py
```

Optional overrides:

- `MOBILE_IMAGE_ID` (default: Xiaohongshu preset image)
- `MOBILE_APP_PACKAGE` (default: `com.xingin.xhs`)
- `MOBILE_QUERY` (default: `少女高颜值穿搭`)

### Prompt evaluation (success rate + smoothness)

Run the same task under different prompt styles and get a report:

```bash
cd cookbook/mobile/xiaohongshu-nl-control/async/langchain
python src/nl_mobile_prompt_eval.py --runs 1
```

### Outputs

The scripts will download screenshots into `./tmp/` so you can review what happened.


