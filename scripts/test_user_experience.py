#!/usr/bin/env python3
"""
用户体验测试脚本
模拟不同类型用户的文档使用路径
"""

import os
import sys
from pathlib import Path

def test_newbie_user_path():
    """测试新手用户路径"""
    print("🆕 测试新手用户路径...")
    
    required_files = [
        "README.md",  # 主入口
        "docs/README.md",  # 文档入口
        "docs/quickstart/README.md",  # 新手导航
        "docs/quickstart/installation.md",  # 安装指南
        "docs/quickstart/basic-concepts.md",  # 基础概念
        "docs/quickstart/first-session.md",  # 第一个会话
        "docs/quickstart/best-practices.md",  # 最佳实践
        "docs/quickstart/faq.md",  # 常见问题
        "docs/quickstart/troubleshooting.md",  # 故障排除
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"  ❌ 缺少文件: {missing_files}")
        return False
    else:
        print("  ✅ 新手用户路径完整")
        return True

def test_experienced_user_path():
    """测试有经验用户路径"""
    print("🚀 测试有经验用户路径...")
    
    required_files = [
        "README.md",  # 主入口
        "docs/guides/README.md",  # 功能导航
        "docs/guides/session-management.md",  # 会话管理
        "docs/guides/file-operations.md",  # 文件操作
        "docs/guides/automation.md",  # 自动化功能
        "docs/guides/data-persistence.md",  # 数据持久化
        "docs/guides/advanced-features.md",  # 高级功能
        "docs/api-reference.md",  # API速查表
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"  ❌ 缺少文件: {missing_files}")
        return False
    else:
        print("  ✅ 有经验用户路径完整")
        return True

def test_package_user_path():
    """测试包安装用户路径"""
    print("📦 测试包安装用户路径...")
    
    languages = ["python", "typescript", "golang"]
    all_good = True
    
    for lang in languages:
        print(f"  测试 {lang.upper()} 用户路径...")
        
        required_files = [
            f"{lang}/README.md",  # 语言特定README
            f"{lang}/docs/api/README.md",  # API文档
        ]
        
        # 检查示例代码
        examples_dir = f"{lang}/docs/examples"
        if os.path.exists(examples_dir):
            example_count = len([f for f in os.listdir(examples_dir) 
                               if os.path.isdir(os.path.join(examples_dir, f))])
            if example_count > 0:
                print(f"    ✅ 发现 {example_count} 个示例")
            else:
                print(f"    ⚠️  示例目录为空")
        else:
            print(f"    ❌ 缺少示例目录: {examples_dir}")
            all_good = False
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            print(f"    ❌ 缺少文件: {missing_files}")
            all_good = False
        else:
            print(f"    ✅ {lang.upper()} 路径完整")
    
    return all_good

def test_content_quality():
    """测试内容质量"""
    print("📝 测试内容质量...")
    
    # 检查核心文档的内容长度
    core_docs = {
        "docs/quickstart/first-session.md": 1000,  # 至少1000字符
        "docs/guides/session-management.md": 2000,  # 至少2000字符
        "docs/guides/automation.md": 1500,  # 至少1500字符
        "docs/guides/data-persistence.md": 2000,  # 至少2000字符
        "docs/guides/advanced-features.md": 2000,  # 至少2000字符
    }
    
    all_good = True
    for doc_path, min_length in core_docs.items():
        if os.path.exists(doc_path):
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) >= min_length:
                    print(f"  ✅ {doc_path} 内容充实 ({len(content)} 字符)")
                else:
                    print(f"  ⚠️  {doc_path} 内容较少 ({len(content)} 字符，建议至少 {min_length})")
        else:
            print(f"  ❌ 文档不存在: {doc_path}")
            all_good = False
    
    return all_good

def test_navigation_consistency():
    """测试导航一致性"""
    print("🧭 测试导航一致性...")
    
    # 检查主要README文件是否都有用户分流
    readme_files = [
        "README.md",
        "python/README.md", 
        "typescript/README.md",
        "golang/README.md"
    ]
    
    all_good = True
    for readme in readme_files:
        if os.path.exists(readme):
            with open(readme, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查是否包含用户分流关键词
            user_flow_keywords = ["新手用户", "有经验的用户", "选择你的学习路径"]
            has_user_flow = any(keyword in content for keyword in user_flow_keywords)
            
            if has_user_flow:
                print(f"  ✅ {readme} 包含用户分流")
            else:
                print(f"  ⚠️  {readme} 缺少用户分流")
                all_good = False
        else:
            print(f"  ❌ README不存在: {readme}")
            all_good = False
    
    return all_good

def main():
    """主函数"""
    print("🧪 开始用户体验测试...")
    print(f"项目根目录: {os.getcwd()}")
    print()
    
    # 执行各项测试
    tests = [
        ("新手用户路径", test_newbie_user_path),
        ("有经验用户路径", test_experienced_user_path),
        ("包安装用户路径", test_package_user_path),
        ("内容质量", test_content_quality),
        ("导航一致性", test_navigation_consistency),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # 汇总结果
    print("="*50)
    print("📊 测试结果汇总:")
    print()
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print()
    print(f"总体通过率: {passed}/{len(results)} ({passed/len(results)*100:.1f}%)")
    
    if passed == len(results):
        print("\n🎉 所有测试通过！文档用户体验良好。")
        return 0
    else:
        print(f"\n⚠️  有 {len(results)-passed} 项测试未通过，需要改进。")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 