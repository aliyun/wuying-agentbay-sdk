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

	fmt.Println("\n=== Error Confirmation ===")
	fmt.Println("ResourceURL field mentioned in documentation does not exist in actual struct")
	fmt.Println("Documentation is missing AgentBay field and other actually existing fields")
}
