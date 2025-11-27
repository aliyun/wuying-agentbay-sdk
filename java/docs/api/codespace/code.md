# Code Execution API Reference

## ⚡ Related Tutorial

- [Code Execution Guide](../../../../../docs/guides/codespace/code-execution.md) - Learn about executing code in cloud environments

## Overview

The Code module provides capabilities for executing Python and JavaScript code in isolated cloud environments. This is useful for running untrusted code, data processing, testing, and automation tasks.

## Code

```java
public class Code extends BaseService
```

Handles code execution operations in the AgentBay cloud environment.

### runCode

```java
public CodeExecutionResult runCode(String code, String language)
public CodeExecutionResult runCode(String code, String language, int timeoutS)
```

Execute code in the specified language with configurable timeout.

**Parameters:**
- `code` (String): The source code to execute
- `language` (String): Programming language - "python" or "javascript"
- `timeoutS` (int): Execution timeout in seconds (default: 300)

**Returns:**
- `CodeExecutionResult`: Result containing execution output and status

**Example:**

```java
Session session = agentBay.create().getSession();

// Execute Python code
String pythonCode = """
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n-1)
    
    print(f"Factorial of 5 is {factorial(5)}")
    """;

CodeExecutionResult result = session.getCode().runCode(pythonCode, "python");
if (result.isSuccess()) {
    System.out.println("Output: " + result.getResult());
}

// Execute JavaScript code
String jsCode = """
    function fibonacci(n) {
        if (n <= 1) return n;
        return fibonacci(n-1) + fibonacci(n-2);
    }
    
    console.log('Fibonacci of 10 is', fibonacci(10));
    """;

CodeExecutionResult jsResult = session.getCode().runCode(jsCode, "javascript");
if (jsResult.isSuccess()) {
    System.out.println("Output: " + jsResult.getResult());
}

// With custom timeout (60 seconds)
CodeExecutionResult longResult = session.getCode().runCode(pythonCode, "python", 60);

session.delete();
```

### execute

```java
public CodeExecutionResult execute(String code)
public CodeExecutionResult execute(String code, String language)
```

Execute code with default settings.

**Parameters:**
- `code` (String): The source code to execute
- `language` (String): Programming language (default: "python")

**Returns:**
- `CodeExecutionResult`: Result containing execution output and status

**Example:**

```java
// Execute Python code (default language)
CodeExecutionResult result = session.getCode().execute("print('Hello World')");

// Execute with explicit language
CodeExecutionResult jsResult = session.getCode().execute("console.log('Hello')", "javascript");
```

## CodeExecutionResult

```java
public class CodeExecutionResult extends ApiResponse
```

Result of code execution operations.

**Fields:**
- `success` (boolean): True if execution succeeded
- `result` (String): Execution output (stdout and stderr)
- `requestId` (String): Request identifier
- `errorMessage` (String): Error description if failed

**Methods:**
- `getResult()`: Get execution output
- `isSuccess()`: Check if execution succeeded
- `getErrorMessage()`: Get error message if failed

## Supported Languages

### Python

- **Version**: Python 3.x
- **Standard Library**: Full Python standard library available
- **Common Packages**: NumPy, Pandas, Requests, and other common packages
- **Installation**: Use pip within your code if needed

**Example:**

```java
String pythonCode = """
    import json
    import datetime
    
    data = {
        'timestamp': str(datetime.datetime.now()),
        'message': 'Hello from Python'
    }
    print(json.dumps(data, indent=2))
    """;

CodeExecutionResult result = session.getCode().runCode(pythonCode, "python");
```

### JavaScript

- **Runtime**: Node.js
- **Standard Library**: Full Node.js standard library
- **Common Packages**: Built-in Node.js modules
- **Installation**: Use npm within environment if needed

**Example:**

```java
String jsCode = """
    const data = {
        timestamp: new Date().toISOString(),
        message: 'Hello from JavaScript'
    };
    console.log(JSON.stringify(data, null, 2));
    """;

CodeExecutionResult result = session.getCode().runCode(jsCode, "javascript");
```

## Complete Example

```java
import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.session.Session;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.model.CodeExecutionResult;

public class CodeExecutionExample {
    public static void main(String[] args) throws Exception {
        AgentBay agentBay = new AgentBay(System.getenv("AGENTBAY_API_KEY"));
        
        // Create session (code_latest image recommended for code execution)
        CreateSessionParams params = new CreateSessionParams();
        params.setImageId("code_latest");
        Session session = agentBay.create(params).getSession();
        
        // Python: Data processing example
        String pythonCode = """
            import statistics
            
            data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            mean = statistics.mean(data)
            median = statistics.median(data)
            stdev = statistics.stdev(data)
            
            print(f"Mean: {mean}")
            print(f"Median: {median}")
            print(f"Standard Deviation: {stdev:.2f}")
            """;
        
        CodeExecutionResult pythonResult = session.getCode().runCode(pythonCode, "python");
        if (pythonResult.isSuccess()) {
            System.out.println("Python Output:");
            System.out.println(pythonResult.getResult());
        } else {
            System.err.println("Python Error: " + pythonResult.getErrorMessage());
        }
        
        // JavaScript: API data processing example
        String jsCode = """
            const users = [
                { name: 'Alice', age: 30 },
                { name: 'Bob', age: 25 },
                { name: 'Charlie', age: 35 }
            ];
            
            const avgAge = users.reduce((sum, u) => sum + u.age, 0) / users.length;
            const names = users.map(u => u.name).join(', ');
            
            console.log(`Users: ${names}`);
            console.log(`Average age: ${avgAge}`);
            """;
        
        CodeExecutionResult jsResult = session.getCode().runCode(jsCode, "javascript");
        if (jsResult.isSuccess()) {
            System.out.println("\nJavaScript Output:");
            System.out.println(jsResult.getResult());
        } else {
            System.err.println("JavaScript Error: " + jsResult.getErrorMessage());
        }
        
        // Clean up
        session.delete();
    }
}
```

## Use Cases

### Data Processing

```java
String code = """
    import pandas as pd
    import json
    
    # Process data
    data = [
        {'product': 'A', 'sales': 100},
        {'product': 'B', 'sales': 150},
        {'product': 'C', 'sales': 200}
    ]
    
    df = pd.DataFrame(data)
    total = df['sales'].sum()
    avg = df['sales'].mean()
    
    result = {
        'total_sales': total,
        'average_sales': avg,
        'product_count': len(df)
    }
    
    print(json.dumps(result))
    """;

CodeExecutionResult result = session.getCode().runCode(code, "python");
```

### API Integration

```java
String code = """
    const https = require('https');
    
    // Simulated API call
    const data = {
        status: 'success',
        timestamp: new Date().toISOString()
    };
    
    console.log(JSON.stringify(data));
    """;

CodeExecutionResult result = session.getCode().runCode(code, "javascript");
```

### Testing and Validation

```java
String testCode = """
    def validate_email(email):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    test_emails = [
        'valid@example.com',
        'invalid@',
        'another.valid@test.org'
    ]
    
    for email in test_emails:
        result = validate_email(email)
        print(f"{email}: {'Valid' if result else 'Invalid'}")
    """;

CodeExecutionResult result = session.getCode().runCode(testCode, "python");
```

## Best Practices

1. **Error Handling**: Always check `result.isSuccess()` before using output
2. **Timeouts**: Set appropriate timeouts based on expected execution time
3. **Resource Management**: Clean up resources and delete sessions when done
4. **Security**: Code executes in isolated environment - safe for untrusted code
5. **Output**: Capture both stdout and stderr in the result
6. **Dependencies**: Install required packages within your code if needed
7. **Image Selection**: Use `code_latest` image for optimal code execution environment

## Limitations

- **Execution Time**: Default timeout is 300 seconds (5 minutes)
- **Memory**: Limited by session environment (contact support for higher limits)
- **Network Access**: Available within the cloud environment
- **File System**: Full access to session file system
- **Supported Languages**: Currently Python and JavaScript only

## Integration with File System

Code execution can work with the file system:

```java
// Write a Python script to file
String script = """
    import sys
    print('Arguments:', sys.argv)
    with open('/tmp/output.txt', 'w') as f:
        f.write('Script executed successfully')
    """;
session.getFileSystem().writeFile("/tmp/script.py", script);

// Execute the script
CodeExecutionResult result = session.getCode().runCode(
    "exec(open('/tmp/script.py').read())",
    "python"
);

// Read the output file
FileContentResult fileResult = session.getFileSystem().readFile("/tmp/output.txt");
```

## Error Handling

```java
CodeExecutionResult result = session.getCode().runCode(code, language);

if (result.isSuccess()) {
    // Process successful execution
    String output = result.getResult();
    System.out.println("Output: " + output);
} else {
    // Handle execution error
    String error = result.getErrorMessage();
    System.err.println("Execution failed: " + error);
    
    // Common errors:
    // - Syntax errors in code
    // - Timeout exceeded
    // - Runtime exceptions
    // - Unsupported language
}
```

## Related Resources

- [Code Execution Example](../../../agentbay/src/main/java/com/aliyun/agentbay/examples/CodeExecutionExample.java)
- [FileSystem API Reference](../common-features/basics/filesystem.md)
- [Session API Reference](../common-features/basics/session.md)

---

*Documentation for AgentBay Java SDK*

