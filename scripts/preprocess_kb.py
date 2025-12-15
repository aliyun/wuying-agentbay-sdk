import os
import shutil

# 配置
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "tmp", "processed_kb")
GITHUB_BASE_URL = "https://github.com/aliyun/wuying-agentbay-sdk/blob/main"

# 需要包含的目录（相对于项目根目录）
INCLUDE_DIRS = [
    "docs",
    "cookbook",         # Cookbook 示例
    "python/docs",      # Python SDK 文档与示例
    "golang/docs",      # Go SDK 文档与示例
    "typescript/docs",  # TypeScript SDK 文档与示例
]

# 需要包含的文件扩展名
INCLUDE_EXTENSIONS = {".md", ".py", ".go", ".ts", ".tsx", ".js"}

def main():
    # 1. 清理并创建输出目录
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    
    print(f"Processing documentation to: {OUTPUT_DIR}")
    
    processed_files = []
    
    # 2. 遍历指定目录
    for rel_dir in INCLUDE_DIRS:
        src_dir = os.path.join(PROJECT_ROOT, rel_dir)
        if not os.path.exists(src_dir):
            print(f"Warning: Directory not found: {src_dir}")
            continue
            
        for root, _, files in os.walk(src_dir):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext not in INCLUDE_EXTENSIONS:
                    continue
                
                # 计算相对路径
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, PROJECT_ROOT)
                
                processed_files.append((abs_path, rel_path))
    
    # 3. 分批处理
    total_files = len(processed_files)
    batch_size = 100
    
    for i in range(0, total_files, batch_size):
        batch_num = (i // batch_size) + 1
        batch_dir = os.path.join(OUTPUT_DIR, f"batch_{batch_num}")
        os.makedirs(batch_dir, exist_ok=True)
        
        current_batch = processed_files[i : i + batch_size]
        
        for abs_path, rel_path in current_batch:
            # 在 batch 目录中保持原始目录结构
            # 也可以选择扁平化文件名，例如将 / 替换为 _，防止目录层级过深
            # 为了上传方便，这里采用"扁平化文件名"策略，
            # 文件名格式：docs_guides_README.md
            flat_name = rel_path.replace("/", "_").replace("\\", "_")
            process_file(abs_path, rel_path, batch_dir, flat_name)
            
    print(f"Successfully processed {total_files} files.")
    print(f"Split into {(total_files + batch_size - 1) // batch_size} batches in {OUTPUT_DIR}")


def process_file(file_path, relative_path, output_dir, output_filename):
    """读取文件，添加 GitHub 链接元数据，写入新位置"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 构建 GitHub 链接
        github_url = f"{GITHUB_BASE_URL}/{relative_path}"
        
        # 添加元数据头
        ext = os.path.splitext(file_path)[1]
        
        # 强制转换为 markdown
        if not output_filename.endswith(".md"):
            output_filename = output_filename + ".md"

        if ext == ".md":
            header = f"---\nsource_url: {github_url}\n---\n\n"
            new_content = header + content
        elif ext == ".py":
            header = f"# Source: {github_url}\n\n```python\n"
            footer = "\n```"
            new_content = header + content + footer
        elif ext == ".go":
            header = f"// Source: {github_url}\n\n```go\n"
            footer = "\n```"
            new_content = header + content + footer
        elif ext in {".ts", ".tsx", ".js"}:
            header = f"// Source: {github_url}\n\n```typescript\n"
            footer = "\n```"
            new_content = header + content + footer
        else:
            new_content = content

        # 输出路径
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


if __name__ == "__main__":
    main()
