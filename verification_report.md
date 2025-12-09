# 文档示例代码自动化巡检报告

## 1. 概览

- **总计文件**: 1
- **✅ 通过**: 0
- **❌ 失败**: 1

## 2. 🔴 失败文件详情

| 文件路径 | 错误类型 | 详情 |
| :--- | :--- | :--- |
| `python/docs/guides/async-programming/migration-guide.md` | **DOC_FAULT** | `SyntaxError: 'async with' outside async function` |

### 错误堆栈与分析

#### 📄 python/docs/guides/async-programming/migration-guide.md
- **错误类型**: DOC_FAULT
- **代码片段数**: 15

**运行日志 (部分)**:
```text
File "/Users/liyuebing/Projects/wuying-agentbay-sdk/tmp/doc_verification_batch/run_9c8a7e1a/runner.py", line 25
    async with AgentBay() as agent_bay:
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: 'async with' outside async function
```

