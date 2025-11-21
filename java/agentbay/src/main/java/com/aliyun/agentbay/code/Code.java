package com.aliyun.agentbay.code;

import com.aliyun.agentbay.model.CodeExecutionResult;
import com.aliyun.agentbay.model.OperationResult;
import com.aliyun.agentbay.service.BaseService;
import com.aliyun.agentbay.session.Session;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.HashMap;
import java.util.Map;
import java.util.List;

public class Code extends BaseService {
    private static final Logger logger = LoggerFactory.getLogger(Code.class);

    public Code(Session session) {
        super(session);
    }

    public CodeExecutionResult execute(String code, String language) {
        return runCode(code, language, 300); // Default timeout 300 seconds
    }

    public CodeExecutionResult runCode(String code, String language, int timeoutS) {
        try {
            // Validate language
            if (!language.equals("python") && !language.equals("javascript")) {
                return new CodeExecutionResult("", false, "",
                    "Unsupported language: " + language + ". Supported languages are 'python' and 'javascript'");
            }

            // Prepare arguments for MCP tool call
            Map<String, Object> args = new HashMap<>();
            args.put("code", code);
            args.put("language", language);
            args.put("timeout_s", timeoutS);

            logger.debug("Executing {} code: {}", language, code.substring(0, Math.min(100, code.length())));

            OperationResult result = callMcpTool("run_code", args);

            if (result.isSuccess()) {
                return new CodeExecutionResult(result.getRequestId(), true, result.getData(), "");
            } else {
                return new CodeExecutionResult(result.getRequestId(), false, "", result.getErrorMessage());
            }

        } catch (Exception e) {
            logger.error("Error executing code", e);
            return new CodeExecutionResult("", false, "", e.getMessage());
        }
    }

    public CodeExecutionResult execute(String code) {
        return execute(code, "python");
    }

    public CodeExecutionResult runCode(String code, String language) {
        return runCode(code, language, 300);
    }
}
