#!/usr/bin/env python3
"""
批量文档验证脚本 - 按文件分组处理代码片段以减少AI调用次数
"""

import os
import sys
import argparse
import subprocess
import shutil
import json
from typing import List, Dict, Any, Optional
from collections import defaultdict

# 导入依赖
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    print("✅ AI依赖导入成功")
except ImportError as e:
    print(f"❌ AI依赖导入失败: {e}")
    sys.exit(1)

# 配置
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIRS = [
    os.path.join(PROJECT_ROOT, "python", "docs"),
    os.path.join(PROJECT_ROOT, "docs", "guides")
]
TMP_DIR = os.path.join(PROJECT_ROOT, "tmp", "doc_verification_batch")
LLMS_FULL_PATH = os.path.join(PROJECT_ROOT, "llms-full.txt")

os.makedirs(TMP_DIR, exist_ok=True)

def get_model():
    """初始化Qwen模型"""
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("⚠️ 未找到DASHSCOPE_API_KEY")
        return None
    
    return ChatOpenAI(
        model="qwen-max", 
        openai_api_key=api_key,
        openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature=0.1
    )

def load_sdk_context():
    """加载SDK上下文"""
    if os.path.exists(LLMS_FULL_PATH):
        try:
            with open(LLMS_FULL_PATH, "r", encoding="utf-8") as f:
                content = f.read()
                # 限制上下文大小以避免token超限
                return content[:30000] + "..." if len(content) > 30000 else content
        except Exception as e:
            print(f"⚠️ 读取llms-full.txt失败: {e}")
    return ""

def extract_snippets_from_md(file_path: str) -> List[Dict]:
    """从markdown文件提取代码片段"""
    snippets = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        in_code_block = False
        code_lines = []
        start_line = 0
        lang = ""
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("```"):
                if in_code_block:
                    in_code_block = False
                    if lang in ["python", "py"]:
                        content = "".join(code_lines)
                        if content.strip():
                            context_start = max(0, start_line - 3)
                            context = "".join(lines[context_start:start_line])
                            
                            snippets.append({
                                "id": f"{os.path.basename(file_path)}:{start_line}",
                                "line_number": start_line + 1,
                                "content": content,
                                "context": context
                            })
                    code_lines = []
                    lang = ""
                else:
                    lang = stripped.lstrip("`").strip().lower()
                    if lang in ["python", "py"]:
                        in_code_block = True
                        start_line = i
            elif in_code_block:
                code_lines.append(line)
                
    except Exception as e:
        print(f"⚠️ 解析文件失败 {file_path}: {e}")
        
    return snippets

def group_snippets_by_file():
    """按文件分组收集所有代码片段"""
    file_groups = defaultdict(list)
    
    for doc_dir in DOCS_DIRS:
        if not os.path.exists(doc_dir):
            continue
            
        for root, _, files in os.walk(doc_dir):
            for file in files:
                if file.endswith(".md"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, PROJECT_ROOT)
                    snippets = extract_snippets_from_md(full_path)
                    
                    if snippets:
                        file_groups[rel_path] = snippets
    
    return file_groups

def generate_batch_verification_script(file_path: str, snippets: List[Dict], sdk_context: str) -> Optional[str]:
    """为一个文件中的所有代码片段生成批量验证脚本"""
    model = get_model()
    if not model:
        return None

    # 构建批量prompt
    snippets_text = ""
    for i, snippet in enumerate(snippets):
        snippets_text += f"""
### 代码片段 {i+1} (Line {snippet['line_number']}):
```python
{snippet['content']}
```
上下文: {snippet['context'][:200]}...

"""

    prompt_template = """
你是Python SDK专家。请为文档文件中的多个代码片段生成一个统一的验证脚本。

### SDK Context (前30000字符)
{sdk_context}

### 文档文件: {file_path}

### 需要验证的代码片段:
{snippets_text}

### 任务要求:
1. **判断每个代码片段**是否是可运行的示例代码:
   - 跳过: 函数定义、类定义、API接口描述、pip install命令
   - 验证: 包含具体逻辑、函数调用、print语句的示例代码

2. **生成一个完整的Python脚本**:
   - 包含所有必要的import语句
   - 初始化AgentBay客户端: `AsyncAgentBay(api_key=os.getenv("AGENTBAY_API_KEY"))`
   - 为每个需要验证的片段创建独立的测试函数
   - 使用try/except包装每个测试，打印结果
   - 在main()函数中依次调用所有测试

### 输出格式:
如果所有片段都应跳过:
SKIP_ALL: <原因>

否则输出完整脚本:
```python
import os
import asyncio
from agentbay import AsyncAgentBay

async def test_snippet_1():
    \"\"\"测试代码片段1 (Line X)\"\"\"
    try:
        # 这里放验证代码
        print("✅ 片段1验证通过")
        return True
    except Exception as e:
        print(f"❌ 片段1验证失败: {{e}}")
        return False

# ... 更多测试函数

async def main():
    results = []
    results.append(await test_snippet_1())
    # ... 调用所有测试
    
    passed = sum(results)
    total = len(results)
    print(f"批量验证结果: {{passed}}/{{total}} 通过")

if __name__ == "__main__":
    asyncio.run(main())
```
"""

    try:
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | model
        response = chain.invoke({
            "sdk_context": sdk_context,
            "file_path": file_path,
            "snippets_text": snippets_text
        })
        
        text = response.content.strip()
        
        if text.startswith("SKIP_ALL:"):
            return None
            
        if "```python" in text:
            script = text.split("```python")[1].split("```")[0].strip()
        else:
            script = text
            
        return script
        
    except Exception as e:
        print(f"❌ 生成批量脚本失败: {e}")
        return None

def execute_batch_script(file_path: str, script: str) -> Dict[str, Any]:
    """执行批量验证脚本"""
    run_dir = os.path.join(TMP_DIR, f"batch_{hash(file_path) % 10000}")
    if os.path.exists(run_dir):
        shutil.rmtree(run_dir)
    os.makedirs(run_dir)
    
    script_path = os.path.join(run_dir, "batch_verify.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)
        
    print(f"▶️ 执行批量验证: {file_path}")
    
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(PROJECT_ROOT, "python") + os.pathsep + env.get("PYTHONPATH", "")
    
    try:
        result = subprocess.run(
            [sys.executable, "batch_verify.py"],
            cwd=run_dir,
            capture_output=True,
            text=True,
            env=env,
            timeout=180  # 3分钟超时
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout + "\n" + result.stderr,
            "script": script
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "批量执行超时 (180s)",
            "script": script
        }
    except Exception as e:
        return {
            "success": False,
            "output": f"执行异常: {e}",
            "script": script
        }

def generate_report(results: Dict[str, Dict]) -> str:
    """生成最终报告"""
    total_files = len(results)
    successful_files = len([r for r in results.values() if r["success"]])
    
    content = f"# 批量文档验证报告\n\n"
    content += f"**总结**: {total_files} 文件 | ✅ {successful_files} 成功 | ❌ {total_files - successful_files} 失败\n\n"
    
    if successful_files == total_files:
        content += "🎉 **所有文件验证通过!**\n\n"
    else:
        content += "## 🚨 验证失败的文件\n\n"
        for file_path, result in results.items():
            if not result["success"]:
                content += f"### 📄 {file_path}\n\n"
                content += f"**错误输出**:\n```\n{result['output'][-1000:]}\n```\n\n"
    
    content += "## 📊 详细结果\n\n"
    for file_path, result in results.items():
        status = "✅ 成功" if result["success"] else "❌ 失败"
        content += f"- `{file_path}`: {status}\n"
    
    return content

def main():
    parser = argparse.ArgumentParser(description="批量文档验证脚本")
    parser.add_argument("--limit", type=int, help="限制处理文件数量")
    parser.add_argument("--pattern", type=str, help="文件路径过滤模式")
    parser.add_argument("--report", type=str, default="batch_verification_report.md", help="报告文件路径")
    args = parser.parse_args()
    
    print("🚀 开始批量文档验证...")
    
    # 收集所有代码片段，按文件分组
    file_groups = group_snippets_by_file()
    
    # 应用过滤器
    if args.pattern:
        file_groups = {k: v for k, v in file_groups.items() if args.pattern in k}
        
    if args.limit:
        file_groups = dict(list(file_groups.items())[:args.limit])
    
    print(f"📚 找到 {len(file_groups)} 个包含Python代码的文档文件")
    
    # 加载SDK上下文
    sdk_context = load_sdk_context()
    
    # 批量处理每个文件
    results = {}
    
    for i, (file_path, snippets) in enumerate(file_groups.items(), 1):
        print(f"\n📖 处理文件 ({i}/{len(file_groups)}): {file_path}")
        print(f"   包含 {len(snippets)} 个代码片段")
        
        # 生成批量验证脚本
        script = generate_batch_verification_script(file_path, snippets, sdk_context)
        
        if script is None:
            print(f"   ⏩ 跳过 (无需验证的代码)")
            results[file_path] = {"success": True, "output": "所有片段已跳过", "skipped": True}
            continue
        
        # 执行批量验证
        result = execute_batch_script(file_path, script)
        results[file_path] = result
        
        status = "✅ 成功" if result["success"] else "❌ 失败"
        print(f"   结果: {status}")
    
    # 生成报告
    report_content = generate_report(results)
    
    with open(args.report, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"\n📝 报告已生成: {args.report}")
    
    # 统计结果
    total = len(results)
    successful = len([r for r in results.values() if r.get("success", False)])
    
    print(f"🎯 批量验证完成: {successful}/{total} 文件成功")
    
    # 如果有失败，返回非零退出码
    if successful < total:
        sys.exit(1)

if __name__ == "__main__":
    main()