#!/usr/bin/env python3
"""
批量文档验证脚本 (Doc-Evals Pipeline)
实现了提取、预检、补全、执行、归因、自愈的完整流程。
"""

import os
import sys
import argparse
import subprocess
import shutil
import json
import hashlib
import ast
import traceback
from typing import List, Dict, Any, Optional
from collections import defaultdict
from dataclasses import dataclass, asdict

# 尝试导入依赖
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from markdown_it import MarkdownIt
    print("✅ 依赖导入成功")
except ImportError as e:
    print(f"❌ 依赖导入失败: {e}")
    print("请确保安装了: langchain-openai, langchain-core, markdown-it-py")
    sys.exit(1)

# ================= Configuration =================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIRS = [
    os.path.join(PROJECT_ROOT, "python", "docs"),
    os.path.join(PROJECT_ROOT, "docs", "guides")
]
TMP_DIR = os.path.join(PROJECT_ROOT, "tmp", "doc_verification_batch")
CACHE_FILE = os.path.join(TMP_DIR, "verification_cache.json")
LLMS_FULL_PATH = os.path.join(PROJECT_ROOT, "llms-full.txt")

os.makedirs(TMP_DIR, exist_ok=True)

# ================= Data Structures =================

@dataclass
class Snippet:
    id: str
    file_path: str
    line_number: int
    content: str
    context: str = ""
    
    @property
    def content_hash(self) -> str:
        return hashlib.sha256(self.content.encode('utf-8')).hexdigest()

@dataclass
class VerificationResult:
    file_path: str
    success: bool
    output: str
    error_type: Optional[str] = None  # DOC_FAULT, ENV_FAULT, None
    snippets_count: int = 0
    snippets: List[Snippet] = None
    
    def __post_init__(self):
        if self.snippets is None:
            self.snippets = []
    
# ================= Core Modules =================

class CacheManager:
    def __init__(self, cache_path: str):
        self.cache_path = cache_path
        self.cache = self._load_cache()
        
    def _load_cache(self) -> Dict:
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
        
    def save_cache(self):
        with open(self.cache_path, 'w') as f:
            json.dump(self.cache, f, indent=2)
            
    def get_status(self, file_path: str, content_hash: str) -> Optional[str]:
        file_cache = self.cache.get(file_path, {})
        if file_cache.get('hash') == content_hash:
            return file_cache.get('status')
        return None
        
    def update_status(self, file_path: str, content_hash: str, status: str):
        self.cache[file_path] = {
            'hash': content_hash,
            'status': status,
            'timestamp': os.path.getmtime(file_path) if os.path.exists(file_path) else 0
        }

class CodeExtractor:
    def __init__(self):
        self.md = MarkdownIt()
        
    def extract(self, file_path: str) -> List[Snippet]:
        snippets = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            tokens = self.md.parse(content)
            
            # 简单的行号估算 (markdown-it-py token包含map属性 [start_line, end_line])
            lines = content.splitlines()
            
            for token in tokens:
                if token.type == 'fence' and token.info.lower() in ['python', 'py']:
                    code = token.content
                    start_line = token.map[0] if token.map else 0
                    
                    # 提取上下文 (前3行)
                    context_start = max(0, start_line - 3)
                    context = "\n".join(lines[context_start:start_line])
                    
                    snippets.append(Snippet(
                        id=f"{os.path.basename(file_path)}:{start_line}",
                        file_path=file_path,
                        line_number=start_line + 1,
                        content=code,
                        context=context
                    ))
        except Exception as e:
            print(f"⚠️ 解析失败 {file_path}: {e}")
            
        return snippets

    @staticmethod
    def pre_check(snippet: Snippet) -> bool:
        """AST 静态检查"""
        if not snippet.content.strip():
            return False
            
        # 过滤规则
        skip_patterns = [
            r'pip install',
            r'export\s+\w+=',
        ]
        import re
        for p in skip_patterns:
            if re.search(p, snippet.content, re.MULTILINE):
                return False

        try:
            ast.parse(snippet.content)
            return True
        except SyntaxError:
            # 允许一些常见的片段式错误（如缺少import），但在严格模式下这可能是一个信号
            # 这里我们只过滤掉极其明显的非代码文本
            return True 
        except Exception:
            return False

class LLMGenerator:
    def __init__(self):
        api_key = os.environ.get("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY not found")
            
        self.model = ChatOpenAI(
            model="qwen-max",
            openai_api_key=api_key,
            openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
            temperature=0.1
        )
        self.sdk_context = self._load_context()
        
    def _load_context(self) -> str:
        if os.path.exists(LLMS_FULL_PATH):
            try:
                with open(LLMS_FULL_PATH, 'r') as f:
                    return f.read()[:30000] # Limit context
            except:
                pass
        return ""

    def generate_script(self, file_path: str, snippets: List[Snippet], last_error: str = "") -> str:
        snippets_text = ""
        for i, s in enumerate(snippets):
            snippets_text += f"\n--- SNIPPET {i+1} (Line {s.line_number}) ---\n{s.content}\n"
            
        prompt = """
你是一个 Python 代码验证专家。你的任务是将文档中的 Python 代码片段转换为可执行的测试脚本，以验证其正确性。

### SDK Context
{sdk_context}

### 目标文件: {file_path}

### 待验证代码片段:
{snippets_text}

### 上一次报错 (如果是重试):
{last_error}

### 要求:
1. **全量覆盖**: 必须验证上述**所有**代码片段。
2. **逻辑封装**: 将每个片段封装为独立的函数 `def snippet_N():` (N=1,2,...)。
   - 如果片段之间有明显的依赖关系（如片段1初始化变量，片段2使用），你可以将它们合并在一个流程中，或者在 `snippet_N` 中重新初始化。
   - 优先假设片段是独立的，除非它们明显属于同一个步骤。
3. **环境补全**: 
   - 补充所有必要的 `import`。
   - 使用 `unittest.mock` 或 `tempfile` 模拟文件/网络操作，禁止真实外网请求。
4. **错误处理 (关键)**:
   - **不要** 自动为用户的代码添加 `try...except` 或 `pytest.raises` 来掩盖错误，除非用户代码本身包含异常捕获逻辑。
   - 我们的目标是**发现**文档中不能运行的错误代码。如果用户代码执行时报错，那就是测试不通过。
   - 例外：如果代码注释中明确写了 `# Expect Error` 或 `# Should raise`，则允许你添加捕获逻辑。
5. **执行入口**:
   - 生成 `if __name__ == "__main__":` 块，按顺序调用所有 `snippet_N` 函数。
   - 使用 `try...except` 包裹每个函数调用。
   - 如果是文档代码本身的错误（如API不存在），打印 `[DOC_FAULT] snippet_N` 并退出(1)。
   - 如果是环境/Mock缺失导致的错误，打印 `[ENV_FAULT] snippet_N` 并退出(2)。
   - 打印详细的堆栈信息以便调试。

### 输出格式:
只返回 Python 代码，不要包含 Markdown 标记。
"""
        chain = ChatPromptTemplate.from_template(prompt) | self.model
        resp = chain.invoke({
            "sdk_context": self.sdk_context,
            "file_path": file_path,
            "snippets_text": snippets_text,
            "last_error": last_error
        })
        
        content = resp.content.strip()
        if content.startswith("```python"):
            content = content.split("```python")[1]
        if content.endswith("```"):
            content = content[:-3]
        return content.strip()

class SandboxRunner:
    def run(self, script: str, file_path: str) -> Dict:
        # Generate unique run directory
        run_id = hashlib.md5(f"{file_path}{script}".encode()).hexdigest()[:8]
        run_dir = os.path.join(TMP_DIR, f"run_{run_id}")
        
        if os.path.exists(run_dir):
            shutil.rmtree(run_dir)
        os.makedirs(run_dir)
        
        script_path = os.path.join(run_dir, "runner.py")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script)
            
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.join(PROJECT_ROOT, "python") + os.pathsep + env.get("PYTHONPATH", "")
        
        try:
            result = subprocess.run(
                [sys.executable, "runner.py"],
                cwd=run_dir,
                capture_output=True,
                text=True,
                env=env,
                timeout=180
            )
            
            output = result.stdout + "\n" + result.stderr
            
            # 优化输出格式，方便后续提取
            final_output = output
            if result.returncode != 0:
                # 尝试从输出中提取 Exception 信息
                lines = output.strip().splitlines()
                # 查找类似 [DOC_FAULT] 的行
                fault_lines = [l for l in lines if "[DOC_FAULT]" in l or "[ENV_FAULT]" in l]
                if fault_lines:
                    # 如果有明确的FAULT标记，尝试把它放在最后一行
                    pass
                else:
                    # 如果没有，可能是在 print 之前就崩溃了，保留原样
                    pass

            if result.returncode == 0:
                return {"status": "SUCCESS", "output": final_output}
            elif result.returncode == 1 or "DOC_FAULT" in final_output:
                return {"status": "DOC_FAULT", "output": final_output}
            else:
                return {"status": "ENV_FAULT", "output": final_output}

                
        except subprocess.TimeoutExpired:
             return {"status": "ENV_FAULT", "output": "Timeout"}
        except Exception as e:
             return {"status": "ENV_FAULT", "output": str(e)}

# ================= Main Pipeline =================

def process_file(file_path: str, 
                 extractor: CodeExtractor, 
                 generator: LLMGenerator, 
                 runner: SandboxRunner,
                 cache: CacheManager) -> VerificationResult:
    
    print(f"\n📄 Processing: {file_path}")
    
    # 1. Extraction
    snippets = extractor.extract(file_path)
    snippets = [s for s in snippets if extractor.pre_check(s)]
    
    if not snippets:
        print("   ⏩ No executable snippets found.")
        return VerificationResult(file_path, True, "No snippets", None, 0, [])
        
    # 2. Cache Check (Combined hash of all snippets)
    combined_hash = hashlib.sha256("".join(s.content for s in snippets).encode()).hexdigest()
    cached_status = cache.get_status(file_path, combined_hash)
    
    if cached_status == "SUCCESS":
        print("   ✅ Cache hit (SUCCESS)")
        return VerificationResult(file_path, True, "Cached", None, len(snippets), snippets)
        
    # 3. Augmentation & Execution (with Retry)
    max_retries = 2
    last_error = ""
    
    for attempt in range(max_retries + 1):
        if attempt > 0:
            print(f"   🔄 Retry {attempt}/{max_retries} due to ENV_FAULT...")
            
        # Generate
        try:
            script = generator.generate_script(file_path, snippets, last_error)
        except Exception as e:
            print(f"   ❌ LLM Generation failed: {e}")
            return VerificationResult(file_path, False, str(e), "LLM_ERROR", len(snippets), snippets)
            
        # Execute
        res = runner.run(script, file_path)
        
        if res['status'] == 'SUCCESS':
            print("   ✅ Verification Passed")
            cache.update_status(file_path, combined_hash, "SUCCESS")
            cache.save_cache()
            return VerificationResult(file_path, True, res['output'], None, len(snippets), snippets)
            
        elif res['status'] == 'DOC_FAULT':
            print("   ❌ Document Fault Detected")
            return VerificationResult(file_path, False, res['output'], "DOC_FAULT", len(snippets), snippets)
            
        else: # ENV_FAULT
            last_error = res['output'][-2000:] # Capture last part of error for retry
            
    print("   ⚠️ Environment Setup Failed after retries")
    return VerificationResult(file_path, False, last_error, "ENV_FAULT", len(snippets), snippets)

def generate_report(results: List[VerificationResult], output_path: str):
    total = len(results)
    success = len([r for r in results if r.success])
    failed = total - success
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 文档示例代码自动化巡检报告\n\n")
        
        # 1. 概览
        f.write("## 1. 概览\n\n")
        f.write(f"- **总计文件**: {total}\n")
        f.write(f"- **✅ 通过**: {success}\n")
        f.write(f"- **❌ 失败**: {failed}\n")
        
        # 2. 失败详情
        if failed > 0:
            f.write("\n## 2. 🔴 失败文件详情\n\n")
            f.write("| 文件路径 | 错误类型 | 详情 |\n")
            f.write("| :--- | :--- | :--- |\n")
            
            for r in results:
                if not r.success:
                    # 尝试提取最后一行错误信息
                    error_lines = r.output.strip().splitlines()
                    last_error = error_lines[-1] if error_lines else "Unknown Error"
                    
                    # 简化文件路径
                    rel_path = os.path.relpath(r.file_path, PROJECT_ROOT)
                    
                    f.write(f"| `{rel_path}` | **{r.error_type}** | `{last_error}` |\n")
            
            f.write("\n### 错误堆栈与分析\n\n")
            for r in results:
                if not r.success:
                    rel_path = os.path.relpath(r.file_path, PROJECT_ROOT)
                    f.write(f"#### 📄 {rel_path}\n")
                    f.write(f"- **错误类型**: {r.error_type}\n")
                    f.write(f"- **代码片段数**: {r.snippets_count}\n")
                    
                    # 尝试定位出错的 snippet
                    import re
                    fault_match = re.search(r"\[(DOC|ENV)_FAULT\] snippet_(\d+)", r.output)
                    if fault_match:
                        snippet_idx = int(fault_match.group(2)) - 1
                        if 0 <= snippet_idx < len(r.snippets):
                            fault_snippet = r.snippets[snippet_idx]
                            f.write(f"\n**出错代码片段 (第 {snippet_idx+1} 段, 行 {fault_snippet.line_number})**:\n")
                            f.write("```python\n")
                            f.write(fault_snippet.content)
                            f.write("\n```\n")
                    
                    # 提取关键报错信息 (过滤掉部分无用的堆栈)
                    f.write("\n**运行日志 (部分)**:\n")
                    f.write("```text\n")
                    # 只保留最后20行
                    log_content = "\n".join(r.output.strip().splitlines()[-20:])
                    f.write(log_content)
                    f.write("\n```\n\n")
                    
        # 3. 通过列表
        if success > 0:
            f.write("\n## 3. ✅ 通过文件列表\n\n")
            for r in results:
                if r.success:
                    rel_path = os.path.relpath(r.file_path, PROJECT_ROOT)
                    f.write(f"- `{rel_path}`\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", help="Filter files by pattern")
    parser.add_argument("--report", default="verification_report.md")
    args = parser.parse_args()
    
    # Init components
    try:
        extractor = CodeExtractor()
        generator = LLMGenerator()
        runner = SandboxRunner()
        cache = CacheManager(CACHE_FILE)
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        sys.exit(1)
        
    results = []
    
    # Scan files
    files_to_process = []
    for doc_dir in DOCS_DIRS:
        for root, _, files in os.walk(doc_dir):
            for file in files:
                if file.endswith(".md"):
                    path = os.path.join(root, file)
                    rel_path = os.path.relpath(path, PROJECT_ROOT)
                    if args.pattern and args.pattern not in rel_path:
                        continue
                    files_to_process.append(path)
                    
    print(f"🚀 Starting verification for {len(files_to_process)} files...")
    
    for file_path in files_to_process:
        res = process_file(file_path, extractor, generator, runner, cache)
        results.append(res)
        
    generate_report(results, args.report)
    print(f"\n📝 Report generated: {args.report}")
    
    if any(not r.success for r in results):
        sys.exit(1)

if __name__ == "__main__":
    main()
