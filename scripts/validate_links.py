#!/usr/bin/env python3
"""
文档链接验证脚本
检查所有markdown文件中的内部链接是否有效
"""

import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urljoin

def find_markdown_files(base_path):
    """查找所有markdown文件"""
    markdown_files = []
    for root, dirs, files in os.walk(base_path):
        # 跳过隐藏目录和node_modules等
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                markdown_files.append(filepath)
    
    return markdown_files

def extract_links(content):
    """提取markdown文件中的所有链接"""
    # 匹配 [text](link) 格式的链接
    link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
    links = re.findall(link_pattern, content)
    return [(text, link) for text, link in links]

def is_internal_link(link):
    """判断是否为内部链接"""
    parsed = urlparse(link)
    # 如果有scheme（http/https）则为外部链接
    if parsed.scheme:
        return False
    # 如果以#开头则为锚点链接
    if link.startswith('#'):
        return False
    return True

def resolve_link_path(base_file, link):
    """解析链接的绝对路径"""
    base_dir = os.path.dirname(base_file)
    
    # 处理锚点
    if '#' in link:
        link = link.split('#')[0]
    
    # 如果链接为空（纯锚点），则指向当前文件
    if not link:
        return base_file
    
    # 解析相对路径
    if link.startswith('/'):
        # 绝对路径（相对于项目根目录）
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        target_path = os.path.join(project_root, link.lstrip('/'))
    else:
        # 相对路径
        target_path = os.path.join(base_dir, link)
    
    # 规范化路径
    target_path = os.path.normpath(target_path)
    
    # 如果是目录，尝试找README.md
    if os.path.isdir(target_path):
        readme_path = os.path.join(target_path, 'README.md')
        if os.path.exists(readme_path):
            return readme_path
    
    return target_path

def validate_internal_links(base_path):
    """验证内部链接"""
    errors = []
    markdown_files = find_markdown_files(base_path)
    
    print(f"检查 {len(markdown_files)} 个markdown文件...")
    
    for filepath in markdown_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            errors.append(f"{filepath}: 无法读取文件 - {e}")
            continue
        
        links = extract_links(content)
        
        for text, link in links:
            if is_internal_link(link):
                target_path = resolve_link_path(filepath, link)
                
                if not os.path.exists(target_path):
                    relative_filepath = os.path.relpath(filepath, base_path)
                    errors.append(f"{relative_filepath}: 链接不存在 [{text}]({link}) -> {target_path}")
    
    return errors

def check_github_links():
    """检查GitHub链接的格式是否正确"""
    errors = []
    expected_repo = "https://github.com/aliyun/wuying-agentbay-sdk"
    
    # 检查主要README文件中的GitHub链接
    readme_files = [
        "README.md",
        "python/README.md", 
        "typescript/README.md",
        "golang/README.md"
    ]
    
    for readme_file in readme_files:
        if os.path.exists(readme_file):
            try:
                with open(readme_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 查找GitHub链接
                github_links = re.findall(r'https://github\.com/[^)\s]+', content)
                
                for link in github_links:
                    if not link.startswith(expected_repo):
                        errors.append(f"{readme_file}: GitHub链接可能不正确 - {link}")
                        
            except Exception as e:
                errors.append(f"{readme_file}: 无法检查GitHub链接 - {e}")
    
    return errors

def main():
    """主函数"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("🔍 开始验证文档链接...")
    print(f"项目根目录: {base_path}")
    print()
    
    # 验证内部链接
    print("📋 验证内部链接...")
    internal_errors = validate_internal_links(base_path)
    
    # 验证GitHub链接
    print("🔗 验证GitHub链接...")
    github_errors = check_github_links()
    
    # 汇总结果
    all_errors = internal_errors + github_errors
    
    if all_errors:
        print(f"\n❌ 发现 {len(all_errors)} 个链接问题:")
        for error in all_errors:
            print(f"  - {error}")
        return 1
    else:
        print("\n✅ 所有链接验证通过!")
        return 0

if __name__ == "__main__":
    sys.exit(main()) 