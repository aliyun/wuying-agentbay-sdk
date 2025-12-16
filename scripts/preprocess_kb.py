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
        
        # 修复内容中的相对路径链接
        # 将 [Title](relative/path.md) 替换为 [Title](https://github.com/.../path.md)
        # 获取当前文件的目录在 github 上的 URL 前缀
        current_dir_rel = os.path.dirname(relative_path)
        # 如果是根目录，relpath 是空字符串，join 会处理好
        current_github_base = f"{GITHUB_BASE_URL}/{current_dir_rel}" if current_dir_rel else GITHUB_BASE_URL

        def replace_link(match):
            title = match.group(1)
            link = match.group(2)
            
            # 忽略绝对链接 (http, https, mailto, etc) 和锚点链接 (#)
            if link.startswith(("http://", "https://", "mailto:", "#")):
                return match.group(0)
            
            # 计算目标文件的相对项目根目录的路径
            # 这里的 link 是相对于当前处理文件的
            try:
                # 简单处理：移除 ? 和 # 后面的内容进行路径计算，然后再补回来
                clean_link = link.split('#')[0].split('?')[0]
                suffix = link[len(clean_link):]
                
                # 组合当前文件目录和链接路径
                # 注意：这里是在本地文件系统路径层面计算
                target_rel_path = os.path.normpath(os.path.join(current_dir_rel, clean_link))
                
                # 如果是 Windows 路径分隔符，转换为 /
                target_rel_path = target_rel_path.replace("\\", "/")

                # 判断目标是文件还是目录（虽然我们只能通过扩展名猜测，或者假设都是文件）
                # GitHub blob 用于文件，tree 用于目录
                # 简单的启发式：没有扩展名或者是目录常见名 -> tree，否则 -> blob
                # 实际上 SDK 文档里大部分是文件引用。为了稳妥，统一用 blob 可能会有少部分错，
                # 但 GitHub 会自动重定向 blob 到 tree 如果是目录，反之亦然。
                # 更精确的做法是检查本地是否存在该目录。
                
                target_local_path = os.path.join(PROJECT_ROOT, target_rel_path)
                url_type = "tree" if os.path.isdir(target_local_path) else "blob"
                
                # 重新构建 GitHub URL，注意基础 URL 是 https://github.com/aliyun/wuying-agentbay-sdk
                # GITHUB_BASE_URL 是 .../blob/main，所以我们需要拆分一下
                repo_root = "https://github.com/aliyun/wuying-agentbay-sdk"
                final_url = f"{repo_root}/{url_type}/main/{target_rel_path}{suffix}"
                
                return f"[{title}]({final_url})"
            except Exception:
                # 解析失败则保留原样
                return match.group(0)

        # 使用正则替换 Markdown 链接
        import re
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, content)
        
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
