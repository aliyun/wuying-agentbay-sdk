#!/usr/bin/env python3
"""
AgentBay SDK - 自动化功能示例

本示例展示了如何使用AgentBay SDK的自动化功能，包括：
- 命令执行
- 代码执行
- UI自动化
- 工作流编排
"""

import os
import time
from agentbay import AgentBay
from agentbay.session_params import CreateSessionParams
from agentbay.ui.ui import KeyCode

def main():
    """主函数"""
    print("🚀 AgentBay 自动化功能示例")

    # 初始化AgentBay客户端
    api_key = os.environ.get("AGENTBAY_API_KEY") or "your_api_key_here"
    agent_bay = AgentBay(api_key=api_key)

    # 创建会话
    print("\n📱 创建会话...")
    session_params = CreateSessionParams()
    session_params.image_id = "code_latest"
    mobile_params = CreateSessionParams(image_id="mobile_latest")
    session_result = agent_bay.create(session_params)
    mobile_result = agent_bay.create(mobile_params)
    if not session_result.success:
        print(f"❌ 会话创建失败: {session_result.error_message}")
        return
    if not mobile_result.success:
        print(f"❌ 会话创建失败: {mobile_result.error_message}")
        return

    session = session_result.session
    mobile_session = mobile_result.session
    print(f"✅ 会话创建成功: {session.session_id}")

    try:
        # 1. 命令执行示例
        command_execution_example(session)

        # 2. 代码执行示例
        code_execution_example(session)

        # 3. UI自动化示例
        ui_automation_example(mobile_session)

        # 4. 工作流编排示例
        workflow_example(session)

    except Exception as e:
        print(f"❌ 示例执行失败: {e}")

    finally:
        # 清理会话
        print(f"\n🧹 清理会话: {session.session_id}")
        session_result = agent_bay.delete(session)
        if session_result.success:
            print("✅ 会话删除成功")
        mobile_result = agent_bay.delete(mobile_session)
        if mobile_result.success:
            print("✅ 会话删除成功")
        print("✅ 示例执行完成")

def command_execution_example(session):
    """命令执行示例"""
    print("\n💻 === 命令执行示例 ===")

    # 基本命令执行
    commands = [
        "whoami",
        "pwd",
        "ls -la /tmp",
        "df -h",
        "free -h"
    ]

    for cmd in commands:
        print(f"\n🔄 执行命令: {cmd}")
        result = session.command.execute_command(cmd)

        if result.success:
            print(f"✅ 输出: {result.output.strip()}")
        else:
            print(f"❌ 命令失败: {result.error}")

    # 带超时的命令执行
    print(f"\n🔄 执行带超时的命令...")
    result = session.command.execute_command("sleep 2", timeout_ms=5000)
    if result.success:
        print("✅ 超时命令执行成功")
    else:
        print(f"❌ 超时命令失败: {result.error_message}")

def code_execution_example(session):
    """代码执行示例"""
    print("\n🐍 === 代码执行示例 ===")

    # Python代码执行
    python_code = """
import sys
import os
import json
from datetime import datetime

# 系统信息
system_info = {
    "python_version": sys.version,
    "current_directory": os.getcwd(),
    "timestamp": datetime.now().isoformat(),
    "environment_vars": len(os.environ)
}

print("Python代码执行成功!")
print(f"系统信息: {json.dumps(system_info, indent=2)}")

# 简单计算
numbers = list(range(1, 11))
total = sum(numbers)
print(f"1到10的和: {total}")
"""

    print("🔄 执行Python代码...")
    result = session.code.run_code(python_code, "python")
    if result.success:
        print("✅ Python代码执行成功:")
        print(result.result)
    else:
        print(f"❌ Python代码执行失败: {result.error_message}")

    # JavaScript代码执行
    js_code = """
console.log("JavaScript代码执行成功!");

// 获取系统信息
const os = require('os');
const systemInfo = {
    platform: os.platform(),
    arch: os.arch(),
    nodeVersion: process.version,
    memory: Math.round(os.totalmem() / 1024 / 1024) + ' MB'
};

console.log("系统信息:", JSON.stringify(systemInfo, null, 2));

// 数组操作
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(n => n * 2);
console.log("原数组:", numbers);
console.log("翻倍后:", doubled);
"""

    print("\n🔄 执行JavaScript代码...")
    result = session.code.run_code(js_code, "javascript")
    if result.success:
        print("✅ JavaScript代码执行成功:")
        print(result.result)
    else:
        print(f"❌ JavaScript代码执行失败: {result.error}")

def ui_automation_example(session):
    """UI自动化示例"""
    print("\n🖱️ === UI自动化示例 ===")

    try:
        # 截图
        print("🔄 获取屏幕截图...")
        screenshot = session.ui.screenshot()
        if screenshot.success:
            # 保存截图
            result = session.file_system.write_file("/tmp/screenshot.png", screenshot.data)
            if result.success:
                print("✅ 写入文件成功: /tmp/screenshot.png")
            else:
                print(f"❌ 写入文件失败: {result.error_message}")
        else:
            print(f"❌ 截图失败: {screenshot.error_message}")

        # 模拟键盘输入
        print("🔄 模拟键盘输入...")
        result = session.ui.send_key(KeyCode.MENU)
        if result.success:
            print("✅ 键盘输入完成")
        else:
            print(f"❌ 键盘输入失败: {result.error_message}")

        # 模拟鼠标操作
        print("🔄 模拟鼠标操作...")
        result = session.ui.click(x=100, y=100, button="left")
        if result.success:
            print("✅ 鼠标点击完成")
        else:
            print(f"❌ 鼠标点击失败: {result.error_message}")

    except Exception as e:
        print(f"⚠️ UI自动化功能可能不可用: {e}")

def workflow_example(session):
    """工作流编排示例"""
    print("\n🔄 === 工作流编排示例 ===")

    print("🔄 执行数据处理工作流...")

    # 步骤1: 创建测试数据
    print("步骤1: 创建测试数据...")
    create_data_code = """
import json
import random
from datetime import datetime, timedelta

# 生成测试数据
data = []
base_date = datetime.now()

for i in range(50):
    record = {
        "id": i + 1,
        "name": f"用户{i+1}",
        "score": random.randint(60, 100),
        "date": (base_date - timedelta(days=random.randint(0, 30))).isoformat(),
        "category": random.choice(["A", "B", "C"])
    }
    data.append(record)

# 保存数据
with open('/tmp/test_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"生成了 {len(data)} 条测试数据")
"""

    result = session.code.run_code(create_data_code, "python")
    if result.success:
        print("✅ 测试数据创建完成")
    else:
        print(f"❌ 测试数据创建失败: {result.error_message}")


    # 步骤2: 数据分析
    print("步骤2: 数据分析...")
    analysis_code = """
import json
import statistics

# 读取数据
with open('/tmp/test_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 分析数据
scores = [record['score'] for record in data]
categories = {}
for record in data:
    cat = record['category']
    categories[cat] = categories.get(cat, 0) + 1

analysis_result = {
    "total_records": len(data),
    "average_score": statistics.mean(scores),
    "max_score": max(scores),
    "min_score": min(scores),
    "category_distribution": categories
}

# 保存分析结果
with open('/tmp/analysis_result.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_result, f, ensure_ascii=False, indent=2)

print("数据分析完成:")
for key, value in analysis_result.items():
    print(f"  {key}: {value}")
"""

    result = session.code.run_code(analysis_code, "python")
    if not result.success:
        print(f"❌ 数据分析失败: {result.error_message}")
        return
    print("✅ 数据分析完成")

    # 步骤3: 生成报告
    print("步骤3: 生成报告...")
    report_code = """
import json
from datetime import datetime

# 读取分析结果
with open('/tmp/analysis_result.json', 'r', encoding='utf-8') as f:
    analysis = json.load(f)

# 生成HTML报告
html_report = f'''
<!DOCTYPE html>
<html>
<head>
    <title>数据分析报告</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background-color: #f0f8ff; padding: 20px; border-radius: 8px; }}
        .metric {{ margin: 10px 0; padding: 10px; background-color: #f9f9f9; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>数据分析报告</h1>
        <p>生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>

    <div class="metric">
        <h3>基本统计</h3>
        <p>总记录数: {analysis['total_records']}</p>
        <p>平均分数: {analysis['average_score']:.2f}</p>
        <p>最高分数: {analysis['max_score']}</p>
        <p>最低分数: {analysis['min_score']}</p>
    </div>

    <div class="metric">
        <h3>分类分布</h3>
'''

for category, count in analysis['category_distribution'].items():
    html_report += f'        <p>类别 {category}: {count} 条记录</p>\\n'

html_report += '''
    </div>
</body>
</html>
'''

# 保存报告
with open('/tmp/report.html', 'w', encoding='utf-8') as f:
    f.write(html_report)

print("HTML报告生成完成: /tmp/report.html")
"""

    result = session.code.run_code(report_code, "python")
    if not result.success:
        print(f"❌ 报告生成失败: {result.error_message}")
        return
    print("✅ 报告生成完成")

    # 步骤4: 验证结果
    print("步骤4: 验证结果...")
    files_to_check = ["/tmp/test_data.json", "/tmp/analysis_result.json", "/tmp/report.html"]

    for file_path in files_to_check:
        result = session.file_system.read_file(file_path)
        if result.success:
            print(f"✅ 文件存在: {file_path} ({len(result.content)} 字节)")
        else:
            print(f"❌ 文件不存在: {file_path}")

    print("🎉 工作流执行完成!")

if __name__ == "__main__":
    main()
