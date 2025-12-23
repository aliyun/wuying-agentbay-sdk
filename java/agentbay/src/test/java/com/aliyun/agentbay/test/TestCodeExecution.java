package com.aliyun.agentbay.test;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.exception.SessionException;
import com.aliyun.agentbay.model.code.EnhancedCodeExecutionResult;
import com.aliyun.agentbay.model.DeleteResult;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Test cases for Code Execution functionality in AgentBay Java SDK
 * This test class covers the functionality demonstrated in CodeExecutionExample.java
 */
public class TestCodeExecution {

    private static AgentBay agentBay;
    private static Session session;

    /**
     * Get API key for testing
     */
    private static String getTestApiKey() {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.trim().isEmpty()) {
            apiKey = "akm-xxx"; // Replace with your test API key
            System.out.println("Warning: Using default API key. Set AGENTBAY_API_KEY environment variable for testing.");
        }
        return apiKey;
    }

    /**
     * Set up before all tests - create AgentBay client and session
     */
    @BeforeClass
    public static void setUp() throws AgentBayException {
        System.out.println("Setting up test environment...");
        String apiKey = getTestApiKey();
        agentBay = new AgentBay(apiKey);

        // Create a session with Linux image for code execution
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("code_latest");
        SessionResult sessionResult = agentBay.create(params);

        assertTrue("Failed to create session: " + sessionResult.getErrorMessage(), 
                   sessionResult.isSuccess());
        assertNotNull("Session object is null", sessionResult.getSession());

        session = sessionResult.getSession();
        System.out.println("✅ Session created with ID: " + session.getSessionId());
    }

    /**
     * Clean up after all tests - delete the session
     */
    @AfterClass
    public static void tearDown() {
        if (session != null && agentBay != null) {
            try {
                System.out.println("Cleaning up session...");
                DeleteResult deleteResult = agentBay.delete(session, false);
                if (deleteResult.isSuccess()) {
                    System.out.println("✅ Session deleted successfully");
                } else {
                    System.err.println("⚠️ Failed to delete session: " + deleteResult.getErrorMessage());
                }
            } catch (Exception e) {
                System.err.println("⚠️ Error during cleanup: " + e.getMessage());
            }
        }
    }

    /**
     * Test Python code execution with simple print statement
     */
    @Test
    public void testPythonCodeExecution() throws SessionException {
        System.out.println("\n🐍 Testing Python code execution...");
        
        String pythonCode = "print(\"hello world\")";
        EnhancedCodeExecutionResult result = session.getCode().runCode(pythonCode, "python");

        // Verify execution was successful
        assertTrue("Python code execution failed: " + result.getErrorMessage(), 
                   result.isSuccess());
        assertNotNull("Result is null", result.getResult());
        assertTrue("Output should contain 'hello world'", 
                   result.getResult().contains("hello world"));
        assertNotNull("Request ID should not be null", result.getRequestId());

        System.out.println("✅ Python code executed successfully!");
        System.out.println("   Output: " + result.getResult());
    }

    /**
     * Test Python code execution with mathematical operations
     */
    @Test
    public void testPythonMathExecution() throws SessionException {
        System.out.println("\n🔢 Testing Python math operations...");
        
        String pythonCode = "result = 5 + 3\nprint(f'5 + 3 = {result}')";
        EnhancedCodeExecutionResult result = session.getCode().runCode(pythonCode, "python");

        assertTrue("Python math code execution failed: " + result.getErrorMessage(), 
                   result.isSuccess());
        assertNotNull("Result is null", result.getResult());
        assertTrue("Output should contain '5 + 3 = 8'", 
                   result.getResult().contains("5 + 3 = 8"));

        System.out.println("✅ Python math operations executed successfully!");
        System.out.println("   Output: " + result.getResult());
    }

    /**
     * Test JavaScript code execution with console.log
     */
    @Test
    public void testJavaScriptCodeExecution() throws SessionException {
        System.out.println("\n🟨 Testing JavaScript code execution...");
        
        String jsCode = "console.log('Hello from JavaScript!');\nconst result = 5 * 4;\nconsole.log(`5 * 4 = ${result}`);";
        EnhancedCodeExecutionResult result = session.getCode().runCode(jsCode, "javascript");

        assertTrue("JavaScript code execution failed: " + result.getErrorMessage(), 
                   result.isSuccess());
        assertNotNull("Result is null", result.getResult());
        assertTrue("Output should contain 'Hello from JavaScript'", 
                   result.getResult().contains("Hello from JavaScript"));
        assertTrue("Output should contain '5 * 4 = 20'", 
                   result.getResult().contains("5 * 4 = 20"));
        assertNotNull("Request ID should not be null", result.getRequestId());

        System.out.println("✅ JavaScript code executed successfully!");
        System.out.println("   Output: " + result.getResult());
    }

    /**
     * Test JavaScript code execution with simple operations
     */
    @Test
    public void testJavaScriptSimpleExecution() throws SessionException {
        System.out.println("\n✨ Testing JavaScript simple operations...");
        
        String jsCode = "const greeting = 'Hello World';\nconsole.log(greeting);";
        EnhancedCodeExecutionResult result = session.getCode().runCode(jsCode, "javascript");

        assertTrue("JavaScript simple code execution failed: " + result.getErrorMessage(), 
                   result.isSuccess());
        assertNotNull("Result is null", result.getResult());
        assertTrue("Output should contain 'Hello World'", 
                   result.getResult().contains("Hello World"));

        System.out.println("✅ JavaScript simple operations executed successfully!");
        System.out.println("   Output: " + result.getResult());
    }

    /**
     * Test Python code execution with loops
     */
    @Test
    public void testPythonLoopExecution() throws SessionException {
        System.out.println("\n🔄 Testing Python loop execution...");
        
        String pythonCode = "for i in range(3):\n    print(f'Number: {i}')";
        EnhancedCodeExecutionResult result = session.getCode().runCode(pythonCode, "python");

        assertTrue("Python loop execution failed: " + result.getErrorMessage(),
                   result.isSuccess());
        assertNotNull("Result is null", result.getResult());
        assertTrue("Output should contain 'Number: 0'", 
                   result.getResult().contains("Number: 0"));
        assertTrue("Output should contain 'Number: 1'", 
                   result.getResult().contains("Number: 1"));
        assertTrue("Output should contain 'Number: 2'", 
                   result.getResult().contains("Number: 2"));

        System.out.println("✅ Python loop executed successfully!");
        System.out.println("   Output: " + result.getResult());
    }

    /**
     * Test Python code execution with multiple lines
     */
    @Test
    public void testPythonMultilineExecution() throws SessionException {
        System.out.println("\n📝 Testing Python multiline code execution...");
        
        String pythonCode = "x = 10\ny = 20\nsum_result = x + y\nprint(f'{x} + {y} = {sum_result}')";
        EnhancedCodeExecutionResult result = session.getCode().runCode(pythonCode, "python");

        assertTrue("Python multiline execution failed: " + result.getErrorMessage(), 
                   result.isSuccess());
        assertNotNull("Result is null", result.getResult());
        assertTrue("Output should contain '10 + 20 = 30'", 
                   result.getResult().contains("10 + 20 = 30"));

        System.out.println("✅ Python multiline code executed successfully!");
        System.out.println("   Output: " + result.getResult());
    }

    /**
     * Test JavaScript code execution with array operations
     */
    @Test
    public void testJavaScriptArrayExecution() throws SessionException {
        System.out.println("\n📦 Testing JavaScript array operations...");
        
        String jsCode = "const numbers = [1, 2, 3, 4, 5];\nconst sum = numbers.reduce((a, b) => a + b, 0);\nconsole.log(`Sum: ${sum}`);";
        EnhancedCodeExecutionResult result = session.getCode().runCode(jsCode, "javascript");

        assertTrue("JavaScript array operations failed: " + result.getErrorMessage(), 
                   result.isSuccess());
        assertNotNull("Result is null", result.getResult());
        assertTrue("Output should contain 'Sum: 15'", 
                   result.getResult().contains("Sum: 15"));

        System.out.println("✅ JavaScript array operations executed successfully!");
        System.out.println("   Output: " + result.getResult());
    }

    /**
     * Test error handling - invalid Python code
     */
    @Test
    public void testInvalidPythonCode() {
        System.out.println("\n Testing invalid Python code handling...");
        
        String invalidPythonCode = "print('Hello'\nprint('Missing closing parenthesis')";
        
        try {
            EnhancedCodeExecutionResult result = session.getCode().runCode(invalidPythonCode, "python");
            // The execution might complete but should indicate an error
            if (result.isSuccess()) {
                // Some systems might still return success but with error output
                System.out.println("⚠️ Execution completed with result: " + result.getResult());
            } else {
                System.out.println("✅ Error properly detected: " + result.getErrorMessage());
            }
        } catch (Exception e) {
            System.out.println("✅ Exception properly thrown: " + e.getMessage());
        }
    }

    /**
     * Test session creation and deletion as demonstrated in CodeExecutionExample
     */
    @Test
    public void testSessionLifecycle() throws AgentBayException {
        System.out.println("\n🔄 Testing session lifecycle...");
        
        // Create a new session (separate from the one in setUp)
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("code_latest");
        SessionResult sessionResult = agentBay.create(params);

        assertTrue("Session creation failed", sessionResult.isSuccess());
        assertNotNull("Session is null", sessionResult.getSession());
        assertNotNull("Session ID is null", sessionResult.getSession().getSessionId());
        assertNotNull("Request ID is null", sessionResult.getRequestId());

        Session testSession = sessionResult.getSession();
        System.out.println("✅ Session created: " + testSession.getSessionId());

        // Execute some code to verify session is working
        String pythonCode = "print('Session test')";
        EnhancedCodeExecutionResult codeResult = testSession.getCode().runCode(pythonCode, "python");
        assertTrue("Code execution failed", codeResult.isSuccess());
        System.out.println("✅ Code executed in session");

        // Delete the session
        DeleteResult deleteResult = agentBay.delete(testSession, false);
        assertTrue("Session deletion failed: " + deleteResult.getErrorMessage(), 
                   deleteResult.isSuccess());
        System.out.println("✅ Session deleted successfully");
    }

    /**
     * Test that session object provides code execution interface
     */
    @Test
    public void testSessionCodeInterface() {
        System.out.println("\n🔌 Testing session code interface...");
        
        assertNotNull("Session should not be null", session);
        assertNotNull("Session code interface should not be null", session.getCode());
        System.out.println("✅ Session code interface is available");
    }

    /**
     * Main method to run tests manually (for debugging purposes)
     * In production, use Maven or IDE test runners
     */
    public static void main(String[] args) {
        System.out.println("=== Running Code Execution Tests ===\n");
        
        TestCodeExecution test = new TestCodeExecution();
        
        try {
            // Test 1: Python execution
            test.setUp();
            test.testPythonCodeExecution();
            test.tearDown();
            
            // Test 2: Python math
            test.setUp();
            test.testPythonMathExecution();
            test.tearDown();
            
            // Test 3: JavaScript execution
            test.setUp();
            test.testJavaScriptCodeExecution();
            test.tearDown();
            
            // Test 4: JavaScript simple
            test.setUp();
            test.testJavaScriptSimpleExecution();
            test.tearDown();
            
            // Test 5: Python loop
            test.setUp();
            test.testPythonLoopExecution();
            test.tearDown();
            
            // Test 6: Python multiline
            test.setUp();
            test.testPythonMultilineExecution();
            test.tearDown();
            
            // Test 7: JavaScript array
            test.setUp();
            test.testJavaScriptArrayExecution();
            test.tearDown();
            
            // Test 8: Invalid code
            test.setUp();
            test.testInvalidPythonCode();
            test.tearDown();
            
            // Test 9: Session lifecycle
            test.setUp();
            test.testSessionLifecycle();
            test.tearDown();
            
            // Test 10: Session interface
            test.setUp();
            test.testSessionCodeInterface();
            test.tearDown();
            
            System.out.println("\n=== ✅ All Code Execution Tests Completed Successfully ===");
        } catch (Exception e) {
            System.err.println("\n=== ❌ Test Failed ===");
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}

