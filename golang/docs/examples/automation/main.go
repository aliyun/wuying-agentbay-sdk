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

func main() {
	fmt.Println("🚀 AgentBay 自动化功能示例 (Golang)")

	// 初始化AgentBay客户端
	client, err := agentbay.NewAgentBay("", nil)
	if err != nil {
		log.Fatalf("❌ 客户端初始化失败: %v", err)
	}

	// 创建会话
	fmt.Println("\n📱 创建会话...")
	sessionResult, err := client.Create(agentbay.NewCreateSessionParams().WithImageId("code_latest"))
	if err != nil {
		fmt.Printf("❌ 会话创建失败: %v\n", err)
		return
	}

	session := sessionResult.Session
	fmt.Printf("✅ 会话创建成功: %s\n", session.SessionID)

	defer func() {
		// 清理会话
		fmt.Printf("\n🧹 清理会话: %s\n", session.SessionID)
		client.Delete(session)
		fmt.Println("✅ 示例执行完成")
	}()

	// 1. 命令执行示例
	commandExecutionExample(session)

	// 2. 代码执行示例
	codeExecutionExample(session)
}

func commandExecutionExample(session *agentbay.Session) {
	fmt.Println("\n💻 === 命令执行示例 ===")

	// 基本命令执行
	commands := []string{
		"whoami",
		"pwd",
		"ls -la /tmp",
		"echo 'Hello AgentBay!'",
	}

	for _, cmd := range commands {
		fmt.Printf("\n🔄 执行命令: %s\n", cmd)
		result, err := session.Command.ExecuteCommand(cmd)

		if err == nil {
			fmt.Printf("✅ 输出: %s\n", result.Output)
		} else {
			fmt.Printf("❌ 命令失败: %v\n", err)
		}
	}

	// 带超时的命令执行
	fmt.Println("\n🔄 执行带超时的命令...")
	timeoutResult, err := session.Command.ExecuteCommand("sleep 2", 5000) // 5秒超时，单位毫秒
	if err == nil {
		fmt.Println("✅ 超时命令执行成功")
		fmt.Printf("输出: %s\n", timeoutResult.Output)
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
	if err == nil {
		fmt.Println("✅ Python代码执行成功:")
		fmt.Println(pythonResult.Output)
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
	if err == nil {
		fmt.Println("✅ JavaScript代码执行成功:")
		fmt.Println(jsResult.Output)
	} else {
		fmt.Printf("❌ JavaScript代码执行失败: %v\n", err)
	}
}
