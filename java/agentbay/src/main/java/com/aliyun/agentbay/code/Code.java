package com.aliyun.agentbay.code;

import com.aliyun.agentbay.model.code.*;
import com.aliyun.agentbay.model.OperationResult;
import com.aliyun.agentbay.service.BaseService;
import com.aliyun.agentbay.session.Session;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;

public class Code extends BaseService {
    private static final Logger logger = LoggerFactory.getLogger(Code.class);
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public Code(Session session) {
        super(session);
    }

    private EnhancedCodeExecutionResult parseResponseBody(Map<String, Object> responseData) {
        try {
            if (responseData == null || responseData.isEmpty()) {
                throw new RuntimeException("No data field in response");
            }

            Object contentObj = responseData.get("content");
            if (contentObj instanceof List) {
                List<?> content = (List<?>) contentObj;
                if (!content.isEmpty() && content.get(0) instanceof Map) {
                    Map<?, ?> contentItem = (Map<?, ?>) content.get(0);
                    Object textObj = contentItem.get("text");
                    if (textObj != null) {
                        try {
                            String textString = textObj.toString();
                            Map<String, Object> parsedJson = objectMapper.readValue(textString, Map.class);
                            if (parsedJson.containsKey("result") || parsedJson.containsKey("executionError")) {
                                responseData = parsedJson;
                            }
                        } catch (Exception e) {
                        }
                    }
                }
            }

            if (responseData.containsKey("result") && responseData.get("result") instanceof List) {
                return parseNewJsonFormat(responseData);
            }

            boolean isRich = responseData.containsKey("logs") || responseData.containsKey("results");
            if (isRich) {
                return parseRichFormat(responseData);
            }

            Boolean isError = (Boolean) responseData.get("isError");
            if (isError != null && isError) {
                return parseLegacyErrorFormat(responseData);
            }

            return parseLegacyFormat(responseData);

        } catch (Exception e) {
            logger.error("Error parsing response body", e);
            throw new RuntimeException("Error parsing response body: " + e.getMessage());
        }
    }

    private EnhancedCodeExecutionResult parseNewJsonFormat(Map<String, Object> responseData) {
        try {
            CodeExecutionLogs logs = new CodeExecutionLogs();
            if (responseData.get("stdout") instanceof List) {
                logs.setStdout((List<String>) responseData.get("stdout"));
            }
            if (responseData.get("stderr") instanceof List) {
                logs.setStderr((List<String>) responseData.get("stderr"));
            }

            List<CodeResult> results = new ArrayList<>();
            Object resultObj = responseData.get("result");
            if (resultObj instanceof List) {
                for (Object resItem : (List<?>) resultObj) {
                    Map<String, Object> parsedItem = null;

                    if (resItem instanceof String) {
                        try {
                            Object parsed = objectMapper.readValue((String) resItem, Object.class);
                            if (parsed instanceof String) {
                                try {
                                    parsedItem = objectMapper.readValue((String) parsed, Map.class);
                                } catch (Exception e) {
                                }
                            } else if (parsed instanceof Map) {
                                parsedItem = (Map<String, Object>) parsed;
                            }
                        } catch (Exception e) {
                            CodeResult result = new CodeResult();
                            result.setText(resItem.toString());
                            results.add(result);
                            continue;
                        }
                    } else if (resItem instanceof Map) {
                        parsedItem = (Map<String, Object>) resItem;
                    }

                    if (parsedItem != null) {
                        CodeResult result = new CodeResult();
                        result.setText(getStringValue(parsedItem, "text/plain", "text"));
                        result.setHtml(getStringValue(parsedItem, "text/html", "html"));
                        result.setMarkdown(getStringValue(parsedItem, "text/markdown", "markdown"));
                        result.setPng(getStringValue(parsedItem, "image/png", "png"));
                        result.setJpeg(getStringValue(parsedItem, "image/jpeg", "jpeg"));
                        result.setSvg(getStringValue(parsedItem, "image/svg+xml", "svg"));
                        result.setJson(parsedItem.get("application/json") != null ? parsedItem.get("application/json") : parsedItem.get("json"));
                        result.setLatex(getStringValue(parsedItem, "text/latex", "latex"));

                        Object chartObj = parsedItem.get("application/vnd.vegalite.v4+json");
                        if (chartObj == null) chartObj = parsedItem.get("application/vnd.vegalite.v5+json");
                        if (chartObj == null) chartObj = parsedItem.get("chart");
                        result.setChart(chartObj);

                        Boolean isMain = (Boolean) parsedItem.get("isMainResult");
                        if (isMain == null) isMain = (Boolean) parsedItem.get("is_main_result");
                        result.setMainResult(isMain != null && isMain);

                        results.add(result);
                    }
                }
            }

            CodeExecutionError error = null;
            Object executionError = responseData.get("executionError");
            if (executionError != null && !executionError.toString().isEmpty()) {
                error = new CodeExecutionError("ExecutionError", executionError.toString(), "");
            }

            EnhancedCodeExecutionResult enhancedResult = new EnhancedCodeExecutionResult();
            enhancedResult.setExecutionCount((Integer) responseData.get("execution_count"));

            Object execTime = responseData.get("execution_time");
            if (execTime instanceof Number) {
                enhancedResult.setExecutionTime(((Number) execTime).doubleValue());
            }

            enhancedResult.setLogs(logs);
            enhancedResult.setResults(results);
            enhancedResult.setError(error);

            Boolean isError = (Boolean) responseData.get("isError");
            enhancedResult.setSuccess(error == null && (isError == null || !isError));

            return enhancedResult;

        } catch (Exception e) {
            logger.error("Error parsing new JSON format", e);
            throw new RuntimeException("Error parsing new JSON format: " + e.getMessage());
        }
    }

    private EnhancedCodeExecutionResult parseRichFormat(Map<String, Object> responseData) {
        try {
            CodeExecutionLogs logs = new CodeExecutionLogs();
            Object logsObj = responseData.get("logs");
            if (logsObj instanceof Map) {
                Map<?, ?> logsData = (Map<?, ?>) logsObj;
                if (logsData.get("stdout") instanceof List) {
                    logs.setStdout((List<String>) logsData.get("stdout"));
                }
                if (logsData.get("stderr") instanceof List) {
                    logs.setStderr((List<String>) logsData.get("stderr"));
                }
            }

            List<CodeResult> results = new ArrayList<>();
            Object resultsObj = responseData.get("results");
            if (resultsObj instanceof List) {
                for (Object resItem : (List<?>) resultsObj) {
                    if (resItem instanceof Map) {
                        Map<?, ?> resData = (Map<?, ?>) resItem;
                        CodeResult result = new CodeResult();
                        result.setText((String) resData.get("text"));
                        result.setHtml((String) resData.get("html"));
                        result.setMarkdown((String) resData.get("markdown"));
                        result.setPng((String) resData.get("png"));
                        result.setJpeg((String) resData.get("jpeg"));
                        result.setSvg((String) resData.get("svg"));
                        result.setJson(resData.get("json"));
                        result.setLatex((String) resData.get("latex"));
                        result.setChart(resData.get("chart"));

                        Boolean isMain = (Boolean) resData.get("is_main_result");
                        result.setMainResult(isMain != null && isMain);

                        results.add(result);
                    }
                }
            }

            CodeExecutionError error = null;
            Object errorObj = responseData.get("error");
            if (errorObj instanceof Map) {
                Map<?, ?> errorData = (Map<?, ?>) errorObj;
                error = new CodeExecutionError(
                    errorData.get("name") != null ? errorData.get("name").toString() : "UnknownError",
                    errorData.get("value") != null ? errorData.get("value").toString() : "",
                    errorData.get("traceback") != null ? errorData.get("traceback").toString() : ""
                );
            }

            EnhancedCodeExecutionResult enhancedResult = new EnhancedCodeExecutionResult();
            enhancedResult.setExecutionCount((Integer) responseData.get("execution_count"));

            Object execTime = responseData.get("execution_time");
            if (execTime instanceof Number) {
                enhancedResult.setExecutionTime(((Number) execTime).doubleValue());
            }

            enhancedResult.setLogs(logs);
            enhancedResult.setResults(results);
            enhancedResult.setError(error);

            Boolean isError = (Boolean) responseData.get("isError");
            enhancedResult.setSuccess(isError == null || !isError);

            return enhancedResult;

        } catch (Exception e) {
            logger.error("Error parsing rich format", e);
            throw new RuntimeException("Error parsing rich format: " + e.getMessage());
        }
    }

    private EnhancedCodeExecutionResult parseLegacyErrorFormat(Map<String, Object> responseData) {
        StringBuilder errorMessage = new StringBuilder();
        Object contentObj = responseData.get("content");
        if (contentObj instanceof List) {
            for (Object item : (List<?>) contentObj) {
                if (item instanceof Map) {
                    Object text = ((Map<?, ?>) item).get("text");
                    if (text != null) {
                        if (errorMessage.length() > 0) errorMessage.append("; ");
                        errorMessage.append(text.toString());
                    }
                }
            }
        }

        EnhancedCodeExecutionResult result = new EnhancedCodeExecutionResult();
        result.setSuccess(false);
        result.setErrorMessage("Error in response: " + errorMessage.toString());
        return result;
    }

    private EnhancedCodeExecutionResult parseLegacyFormat(Map<String, Object> responseData) {
        Object contentObj = responseData.get("content");
        if (contentObj instanceof List) {
            List<?> content = (List<?>) contentObj;
            if (!content.isEmpty() && content.get(0) instanceof Map) {
                Map<?, ?> contentItem = (Map<?, ?>) content.get(0);
                Object textObj = contentItem.get("text");
                if (textObj != null) {
                    String textString = textObj.toString();

                    EnhancedCodeExecutionResult result = new EnhancedCodeExecutionResult();
                    result.setSuccess(true);

                    CodeExecutionLogs logs = new CodeExecutionLogs();
                    logs.getStdout().add(textString);
                    result.setLogs(logs);

                    CodeResult codeResult = new CodeResult();
                    codeResult.setText(textString);
                    codeResult.setMainResult(true);
                    result.getResults().add(codeResult);

                    return result;
                }
            }
        }

        throw new RuntimeException("Unknown response format");
    }

    private String getStringValue(Map<String, Object> map, String key1, String key2) {
        Object value = map.get(key1);
        if (value == null) value = map.get(key2);
        return value != null ? value.toString() : null;
    }

    public EnhancedCodeExecutionResult runCode(String code, String language, int timeoutS) {
        try {
            if (!language.equals("python") && !language.equals("javascript")) {
                return new EnhancedCodeExecutionResult("", false,
                    "Unsupported language: " + language + ". Supported languages are 'python' and 'javascript'");
            }

            Map<String, Object> args = new HashMap<>();
            args.put("code", code);
            args.put("language", language);
            args.put("timeout_s", timeoutS);

            logger.debug("Executing {} code: {}", language, code.substring(0, Math.min(100, code.length())));

            OperationResult result = callMcpTool("run_code", args);
            logger.debug("Run code response: {}", result);

            if (result.isSuccess()) {
                try {
                    Map<String, Object> responseData = objectMapper.readValue(result.getData(), Map.class);
                    EnhancedCodeExecutionResult enhancedResult = parseResponseBody(responseData);
                    enhancedResult.setRequestId(result.getRequestId());
                    return enhancedResult;
                } catch (Exception e) {
                    EnhancedCodeExecutionResult enhancedResult = new EnhancedCodeExecutionResult();
                    enhancedResult.setRequestId(result.getRequestId());
                    enhancedResult.setSuccess(true);

                    CodeResult codeResult = new CodeResult();
                    codeResult.setText(result.getData());
                    codeResult.setMainResult(true);
                    enhancedResult.getResults().add(codeResult);

                    CodeExecutionLogs logs = new CodeExecutionLogs();
                    logs.getStdout().add(result.getData());
                    enhancedResult.setLogs(logs);

                    return enhancedResult;
                }
            } else {
                return new EnhancedCodeExecutionResult(result.getRequestId(), false,
                    result.getErrorMessage() != null && !result.getErrorMessage().isEmpty()
                        ? result.getErrorMessage() : "Failed to run code");
            }

        } catch (Exception e) {
            logger.error("Error executing code", e);
            return new EnhancedCodeExecutionResult("", false, "Failed to run code: " + e.getMessage());
        }
    }

    public EnhancedCodeExecutionResult execute(String code, String language) {
        return runCode(code, language, 60);
    }

    public EnhancedCodeExecutionResult execute(String code) {
        return execute(code, "python");
    }

    public EnhancedCodeExecutionResult runCode(String code, String language) {
        return runCode(code, language, 60);
    }
}
