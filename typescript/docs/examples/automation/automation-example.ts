/**
 * AgentBay SDK - 自动化功能示例 (TypeScript)
 *
 * 本示例展示了如何使用AgentBay SDK的自动化功能，包括：
 * - 命令执行
 * - 代码执行
 * - UI自动化
 * - 工作流编排
 */

import { AgentBay,KeyCode } from 'wuying-agentbay-sdk';

async function main(): Promise<void> {
    console.log('🚀 AgentBay 自动化功能示例 (TypeScript)');

    // 初始化AgentBay客户端
    const agentBay = new AgentBay();

    // 创建会话
    console.log('\n📱 创建会话...');
    const sessionResult = await agentBay.create({imageId:'code_latest'});
    const mobileResult = await agentBay.create({imageId:'mobile_latest'})
    if (!sessionResult.success) {
        console.log(`❌ 会话创建失败: ${sessionResult.errorMessage}`);
        return;
    }
    if (!mobileResult.success) {
        console.log(`❌ 会话创建失败: ${mobileResult.errorMessage}`);
        return;
    }

    const session = sessionResult.session;
    const mobileSession = mobileResult.session;
    console.log(`✅ 会话创建成功: ${session.sessionId}`);

    try {
        // 1. 命令执行示例
        await commandExecutionExample(session);

        // 2. 代码执行示例
        await codeExecutionExample(session);

        // 3. UI自动化示例
        await uiAutomationExample(mobileSession);

        // 4. 工作流编排示例
        await workflowExample(mobileSession);

    } catch (error) {
        console.log(`❌ 示例执行失败: ${error}`);
    } finally {
        // 清理会话
        console.log(`\n🧹 清理会话: ${session.sessionId}`);
        await agentBay.delete(session);
        await agentBay.delete(mobileSession);
        console.log('✅ 示例执行完成');
    }
}

async function commandExecutionExample(session: any): Promise<void> {
    console.log('\n💻 === 命令执行示例 ===');

    // 基本命令执行
    const commands = [
        'whoami',
        'pwd',
        'ls -la /tmp',
        'df -h',
        'free -h'
    ];

    for (const cmd of commands) {
        console.log(`\n🔄 执行命令: ${cmd}`);
        const result = await session.command.executeCommand(cmd);

        if (!result.isError) {
            console.log(`✅ 输出: ${result.output.trim()}`);
        } else {
            console.log(`❌ 命令失败: ${result.error}`);
        }
    }

    // 带超时的命令执行
    console.log('\n🔄 执行带超时的命令...');
    const timeoutResult = await session.command.executeCommand('sleep 2', { timeout: 5000 });
    if (!timeoutResult.isError) {
        console.log('✅ 超时命令执行成功');
    } else {
        console.log(`❌ 超时命令失败: ${timeoutResult.error}`);
    }
}

async function codeExecutionExample(session: any): Promise<void> {
    console.log('\n🐍 === 代码执行示例 ===');

    // Python代码执行
    const pythonCode = `
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
`;

    console.log('🔄 执行Python代码...');
    const pythonResult = await session.code.runCode(pythonCode, 'python');
    if (!pythonResult.isError) {
        console.log('✅ Python代码执行成功:');
        console.log(pythonResult.result);
    } else {
        console.log(`❌ Python代码执行失败: ${pythonResult.error}`);
    }

    // JavaScript代码执行
    const jsCode = `
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
`;

    console.log('\n🔄 执行JavaScript代码...');
    const jsResult = await session.code.runCode(jsCode, 'javascript');
    if (!jsResult.isError) {
        console.log('✅ JavaScript代码执行成功:');
        console.log(jsResult.result);
    } else {
        console.log(`❌ JavaScript代码执行失败: ${jsResult.error}`);
    }
}

async function uiAutomationExample(session: any): Promise<void> {
    console.log('\n🖱️ === UI自动化示例 ===');

    try {
        // 截图
        console.log('🔄 获取屏幕截图...');
        const screenshot = await session.ui.screenshot();
        if (!screenshot.isError) {
            // 保存截图
            await session.fileSystem.writeFile('/tmp/screenshot.png', screenshot.data);
            console.log('✅ 截图保存成功: /tmp/screenshot.png');
        } else {
            console.log(`❌ 截图失败: ${screenshot.error}`);
        }

        // 模拟键盘输入
        console.log('🔄 模拟键盘输入...');
        await session.ui.sendKey(KeyCode.HOME);
        console.log('✅ 键盘输入完成');

        // 模拟鼠标操作
        console.log('🔄 模拟鼠标操作...');
        await session.ui.click({ x: 100, y: 100 });
        console.log('✅ 鼠标点击完成');

    } catch (error) {
        console.log(`⚠️ UI自动化功能可能不可用: ${error}`);
    }
}

async function workflowExample(session: any): Promise<void> {
    console.log('\n🔄 === 工作流编排示例 ===');

    console.log('🔄 执行数据处理工作流...');

    // 步骤1: 创建测试数据
    console.log('步骤1: 创建测试数据...');
    const createDataCode = `
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
`;

    const createResult = await session.code.runCode(createDataCode, 'python');
    if (createResult.isError) {
        console.log(`❌ 数据创建失败: ${createResult.error}`);
        return;
    }
    console.log('✅ 测试数据创建完成');

    // 步骤2: 数据分析 (使用JavaScript)
    console.log('步骤2: 数据分析...');
    const analysisCode = `
const fs = require('fs');

// 读取数据
const rawData = fs.readFileSync('/tmp/test_data.json', 'utf8');
const data = JSON.parse(rawData);

// 分析数据
const scores = data.map(record => record.score);
const categories = {};
data.forEach(record => {
    const cat = record.category;
    categories[cat] = (categories[cat] || 0) + 1;
});

const analysisResult = {
    total_records: data.length,
    average_score: scores.reduce((a, b) => a + b, 0) / scores.length,
    max_score: Math.max(...scores),
    min_score: Math.min(...scores),
    category_distribution: categories
};

// 保存分析结果
fs.writeFileSync('/tmp/analysis_result.json', JSON.stringify(analysisResult, null, 2));

console.log("数据分析完成:");
Object.entries(analysisResult).forEach(([key, value]) => {
    console.log(\`  \${key}: \${JSON.stringify(value)}\`);
});
`;

    const analysisResult = await session.code.runCode(analysisCode, 'javascript');
    if (analysisResult.isError) {
        console.log(`❌ 数据分析失败: ${analysisResult.error}`);
        return;
    }
    console.log('✅ 数据分析完成');

    // 步骤3: 生成报告
    console.log('步骤3: 生成报告...');
    const reportCode = `
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
        <h1>数据分析报告 (TypeScript示例)</h1>
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
`;

    const reportResult = await session.code.runCode(reportCode, 'python');
    if (reportResult.isError) {
        console.log(`❌ 报告生成失败: ${reportResult.error}`);
        return;
    }
    console.log('✅ 报告生成完成');

    // 步骤4: 验证结果
    console.log('步骤4: 验证结果...');
    const filesToCheck = ['/tmp/test_data.json', '/tmp/analysis_result.json', '/tmp/report.html'];

    for (const filePath of filesToCheck) {
        const result = await session.fileSystem.readFile(filePath);
        if (!result.isError) {
            console.log(`✅ 文件存在: ${filePath} (${result.content.length} 字节)`);
        } else {
            console.log(`❌ 文件不存在: ${filePath}`);
        }
    }

    console.log('🎉 工作流执行完成!');
}

// 运行示例
if (require.main === module) {
    main().catch(console.error);
}

export { main };
