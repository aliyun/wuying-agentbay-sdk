package main

import (
	"fmt"
	"reflect"
	
	"github.com/aliyun/wuying-agentbay-sdk/golang/pkg/agentbay"
)

func main() {
	// Test to verify Session struct properties
	sessionType := reflect.TypeOf(agentbay.Session{})
	
	fmt.Println("=== Golang Session struct fields ===")
	for i := 0; i < sessionType.NumField(); i++ {
		field := sessionType.Field(i)
		fmt.Printf("Field: %s, Type: %s\n", field.Name, field.Type)
	}
	
	fmt.Println("\n=== 错误确认 ===")
	fmt.Println("文档中提到的ResourceURL字段在实际struct中不存在")
	fmt.Println("文档中缺少了AgentBay字段等实际存在的字段")
}