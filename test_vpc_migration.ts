#!/usr/bin/env node
/**
 * Simple test script to verify VPC functionality migration works correctly.
 */

import { AgentBay, CreateSessionParams } from './typescript/src';

async function testVpcSessionCreation(): Promise<boolean> {
    /**Test VPC session creation and tool listing.*/
    // Get API key from environment
    const apiKey = process.env.AGENTBAY_API_KEY;
    if (!apiKey) {
        console.log("Error: AGENTBAY_API_KEY environment variable not set");
        return false;
    }
    
    try {
        // Initialize AgentBay client
        const config = {
            region_id: 'cn-hangzhou',
            endpoint: 'wuyingai-pre.cn-hangzhou.aliyuncs.com',
            timeout_ms: 60000
        };
        const agentBay = new AgentBay({ apiKey, config });
        console.log("✓ AgentBay client initialized successfully");
        
        // Create VPC session parameters
        const params: CreateSessionParams = {
            imageId: "imgc-07eksy57nw6r759fb",
            isVpc: true,
            labels: {
                "test-type": "vpc-migration-test",
                "purpose": "verify-implementation"
            }
        };
        console.log("✓ VPC session parameters created");
        
        // Create VPC session
        console.log("Creating VPC session...");
        const sessionResult = await agentBay.create(params);
        
        if (!sessionResult.success) {
            console.log(`Error creating session: ${sessionResult.errorMessage}`);
            return false;
        }
            
        const session = sessionResult.session!;
        console.log(`✓ VPC session created successfully: ${session.getSessionId()}`);
        
        // Verify VPC properties
        console.log(`✓ Is VPC enabled: ${session.isVpcEnabled()}`);
        console.log(`✓ Network Interface IP: ${session.getNetworkInterfaceIp()}`);
        console.log(`✓ HTTP Port: ${session.getHttpPort()}`);
        
        // Test MCP tools listing
        console.log("Testing MCP tools listing...");
        const toolsResult = await session.listMcpTools();
        console.log(`✓ Found ${toolsResult.tools.length} MCP tools`);
        
        // Display first few tools
        for (let i = 0; i < Math.min(3, toolsResult.tools.length); i++) {
            const tool = toolsResult.tools[i];
            console.log(`  Tool ${i+1}: ${tool.name} (server: ${tool.server})`);
        }
        
        // Test find_server_for_tool functionality
        if (toolsResult.tools.length > 0) {
            const firstTool = toolsResult.tools[0];
            const foundServer = session.findServerForTool(firstTool.name);
            console.log(`✓ Found server for '${firstTool.name}': ${foundServer}`);
        }
        
        // Clean up
        const deleteResult = await session.delete();
        if (deleteResult.success) {
            console.log("✓ Session deleted successfully");
        } else {
            console.log(`Warning: Error deleting session: ${deleteResult.errorMessage}`);
        }
        
        console.log("\n🎉 VPC migration test completed successfully!");
        return true;
        
    } catch (error) {
        console.log(`Error during VPC test: ${error}`);
        return false;
    }
}

async function main() {
    console.log("Testing VPC functionality migration...");
    const success = await testVpcSessionCreation();
    process.exit(success ? 0 : 1);
}

if (require.main === module) {
    main();
} 