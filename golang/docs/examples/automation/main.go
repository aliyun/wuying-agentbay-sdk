package main

import (
	"fmt"
	"log"

	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

// AgentBay SDK - 自动化功能示例 (Golang)
//
// 本示例展示了如何使用AgentBay SDK的自动化功能，包括：
// - 命令执行
// - 代码执行
// - UI自动化
// - 工作流编排

func main() {
	fmt.Println("🚀 AgentBay 自动化功能示例 (Golang)")

	// 初始化AgentBay客户端
	client, err := agentbay.NewAgentBay("", nil)
	if err != nil {
		log.Fatalf("❌ 客户端初始化失败: %v", err)
	}

	// 创建会话
	fmt.Println("\n📱 创建会话...")
	sessionResult, err := client.Create(agentbay.NewCreateSessionParams())
	if err != nil || sessionResult.IsError {
		fmt.Printf("❌ 会话创建失败: %v\n", err)
		return
	}

	session := sessionResult.Session
	fmt.Printf("✅ 会话创建成功: %s\n", session.SessionID)

	defer func() {
		// 清理会话
		fmt.Printf("\n🧹 清理会话: %s\n", session.SessionID)
		client.Destroy(session.SessionID)
		fmt.Println("✅ 示例执行完成")
	}()

	// 1. 命令执行示例
	commandExecutionExample(session)

	// 2. 代码执行示例
	codeExecutionExample(session)

	// 3. UI自动化示例
	uiAutomationExample(session)

	// 4. 工作流编排示例
	workflowExample(session)
}

func commandExecutionExample(session *agentbay.Session) {
	fmt.Println("\n💻 === 命令执行示例 ===")

	// 基本命令执行
	commands := []string{
		"whoami",
		"pwd",
		"ls -la /tmp",
		"df -h",
		"free -h",
	}

	for _, cmd := range commands {
		fmt.Printf("\n🔄 执行命令: %s\n", cmd)
		result, err := session.Command.ExecuteCommand(cmd)

		if err == nil && !result.IsError {
			fmt.Printf("✅ 输出: %s\n", result.Data.Stdout)
			if result.Data.Stderr != "" {
				fmt.Printf("⚠️ 错误: %s\n", result.Data.Stderr)
			}
		} else {
			fmt.Printf("❌ 命令失败: %v\n", err)
		}
	}

	// 带超时的命令执行
	fmt.Println("\n🔄 执行带超时的命令...")
	options := &agentbay.CommandOptions{Timeout: 5}
	result, err := session.Command.ExecuteCommandWithOptions("sleep 2", options)
	if err == nil && !result.IsError {
		fmt.Println("✅ 超时命令执行成功")
	} else {
		fmt.Printf("❌ 超时命令失败: %v\n", err)
	}
}

func codeExecutionExample(session *agentbay.Session) {
	fmt.Println("\n🐍 === 代码执行示例 ===")

	// Python代码执行
	pythonCode := `
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
`

	fmt.Println("🔄 执行Python代码...")
	pythonResult, err := session.Code.RunCode(pythonCode, "python")
	if err == nil && !pythonResult.IsError {
		fmt.Println("✅ Python代码执行成功:")
		fmt.Println(pythonResult.Data.Stdout)
	} else {
		fmt.Printf("❌ Python代码执行失败: %v\n", err)
	}

	// JavaScript代码执行
	jsCode := `
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
`

	fmt.Println("\n🔄 执行JavaScript代码...")
	jsResult, err := session.Code.RunCode(jsCode, "javascript")
	if err == nil && !jsResult.IsError {
		fmt.Println("✅ JavaScript代码执行成功:")
		fmt.Println(jsResult.Data.Stdout)
	} else {
		fmt.Printf("❌ JavaScript代码执行失败: %v\n", err)
	}
}

func uiAutomationExample(session *agentbay.Session) {
	fmt.Println("\n🖱️ === UI自动化示例 ===")

	// 截图
	fmt.Println("🔄 获取屏幕截图...")
	screenshot, err := session.UI.Screenshot()
	if err == nil && !screenshot.IsError {
		// 保存截图
		session.FileSystem.WriteFile("/tmp/screenshot.png", screenshot.Data)
		fmt.Println("✅ 截图保存成功: /tmp/screenshot.png")
	} else {
		fmt.Printf("❌ 截图失败: %v\n", err)
	}

	// 模拟键盘输入
	fmt.Println("🔄 模拟键盘输入...")
	session.UI.Type("Hello AgentBay!")
	session.UI.Key("Enter")
	fmt.Println("✅ 键盘输入完成")

	// 模拟鼠标操作
	fmt.Println("🔄 模拟鼠标操作...")
	session.UI.Click(100, 100)
	fmt.Println("✅ 鼠标点击完成")
}

func workflowExample(session *agentbay.Session) {
	fmt.Println("\n🔄 === 工作流编排示例 ===")

	fmt.Println("🔄 执行数据处理工作流...")

	// 步骤1: 创建测试数据
	fmt.Println("步骤1: 创建测试数据...")
	createDataCode := `
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
`

	createResult, err := session.Code.RunCode(createDataCode, "python")
	if err != nil || createResult.IsError {
		fmt.Printf("❌ 数据创建失败: %v\n", err)
		return
	}
	fmt.Println("✅ 测试数据创建完成")

	// 步骤2: 数据分析 (使用Go代码)
	fmt.Println("步骤2: 数据分析...")
	analysisCode := `
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
)

type Record struct {
	ID       int    ` + "`json:\"id\"`" + `
	Name     string ` + "`json:\"name\"`" + `
	Score    int    ` + "`json:\"score\"`" + `
	Date     string ` + "`json:\"date\"`" + `
	Category string ` + "`json:\"category\"`" + `
}

type AnalysisResult struct {
	TotalRecords         int            ` + "`json:\"total_records\"`" + `
	AverageScore         float64        ` + "`json:\"average_score\"`" + `
	MaxScore             int            ` + "`json:\"max_score\"`" + `
	MinScore             int            ` + "`json:\"min_score\"`" + `
	CategoryDistribution map[string]int ` + "`json:\"category_distribution\"`" + `
}

func main() {
	// 读取数据
	data, err := ioutil.ReadFile("/tmp/test_data.json")
	if err != nil {
		fmt.Printf("读取文件失败: %v\n", err)
		return
	}

	var records []Record
	if err := json.Unmarshal(data, &records); err != nil {
		fmt.Printf("解析JSON失败: %v\n", err)
		return
	}

	// 分析数据
	var totalScore int
	maxScore := math.MinInt32
	minScore := math.MaxInt32
	categories := make(map[string]int)

	for _, record := range records {
		totalScore += record.Score
		if record.Score > maxScore {
			maxScore = record.Score
		}
		if record.Score < minScore {
			minScore = record.Score
		}
		categories[record.Category]++
	}

	result := AnalysisResult{
		TotalRecords:         len(records),
		AverageScore:         float64(totalScore) / float64(len(records)),
		MaxScore:             maxScore,
		MinScore:             minScore,
		CategoryDistribution: categories,
	}

	// 保存分析结果
	resultData, _ := json.MarshalIndent(result, "", "  ")
	ioutil.WriteFile("/tmp/analysis_result.json", resultData, 0644)

	fmt.Println("数据分析完成:")
	fmt.Printf("  总记录数: %d\n", result.TotalRecords)
	fmt.Printf("  平均分数: %.2f\n", result.AverageScore)
	fmt.Printf("  最高分数: %d\n", result.MaxScore)
	fmt.Printf("  最低分数: %d\n", result.MinScore)
	fmt.Printf("  分类分布: %+v\n", result.CategoryDistribution)
}
`

	analysisResult, err := session.Code.RunCode(analysisCode, "go")
	if err != nil || analysisResult.IsError {
		fmt.Printf("❌ 数据分析失败: %v\n", err)
		return
	}
	fmt.Println("✅ 数据分析完成")

	// 步骤3: 生成报告
	fmt.Println("步骤3: 生成报告...")
	reportCode := `
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
        <h1>数据分析报告 (Golang示例)</h1>
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
`

	reportResult, err := session.Code.RunCode(reportCode, "python")
	if err != nil || reportResult.IsError {
		fmt.Printf("❌ 报告生成失败: %v\n", err)
		return
	}
	fmt.Println("✅ 报告生成完成")

	// 步骤4: 验证结果
	fmt.Println("步骤4: 验证结果...")
	filesToCheck := []string{"/tmp/test_data.json", "/tmp/analysis_result.json", "/tmp/report.html"}

	for _, filePath := range filesToCheck {
		result, err := session.FileSystem.ReadFile(filePath)
		if err == nil && !result.IsError {
			fmt.Printf("✅ 文件存在: %s (%d 字节)\n", filePath, len(result.Data))
		} else {
			fmt.Printf("❌ 文件不存在: %s\n", filePath)
		}
	}

	fmt.Println("🎉 工作流执行完成!")
}
