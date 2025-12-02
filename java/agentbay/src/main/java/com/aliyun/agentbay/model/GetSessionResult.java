package com.aliyun.agentbay.model;

/**
 * Result of GetSession operations
 */
public class GetSessionResult {
    private String requestId;
    private boolean success;
    private GetSessionData data;
    private String errorMessage;
    private Integer httpStatusCode;
    private String code;

    public GetSessionResult() {
    }

    public GetSessionResult(String requestId, boolean success, GetSessionData data, String errorMessage) {
        this.requestId = requestId;
        this.success = success;
        this.data = data;
        this.errorMessage = errorMessage;
    }

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public GetSessionData getData() {
        return data;
    }

    public void setData(GetSessionData data) {
        this.data = data;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    public Integer getHttpStatusCode() {
        return httpStatusCode;
    }

    public void setHttpStatusCode(Integer httpStatusCode) {
        this.httpStatusCode = httpStatusCode;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }
}

