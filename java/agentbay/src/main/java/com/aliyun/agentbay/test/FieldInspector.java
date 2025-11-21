package com.aliyun.agentbay.test;

import com.aliyun.wuyingai20250506.models.CallMcpToolRequest;
import java.lang.reflect.Field;

public class FieldInspector {
    public static void main(String[] args) {
        CallMcpToolRequest request = new CallMcpToolRequest();

        System.out.println("CallMcpToolRequest available fields:");
        Field[] fields = request.getClass().getFields();
        for (Field field : fields) {
            System.out.println("- " + field.getName() + " (" + field.getType().getSimpleName() + ")");
        }

        // Test setting different field names
        try {
            // Test if 'name' field exists
            Field nameField = request.getClass().getField("name");
            System.out.println("✅ 'name' field found: " + nameField.getType());
        } catch (NoSuchFieldException e) {
            System.out.println("❌ 'name' field not found");
        }

        try {
            // Test if 'tool' field exists
            Field toolField = request.getClass().getField("tool");
            System.out.println("✅ 'tool' field found: " + toolField.getType());
        } catch (NoSuchFieldException e) {
            System.out.println("❌ 'tool' field not found");
        }
    }
}