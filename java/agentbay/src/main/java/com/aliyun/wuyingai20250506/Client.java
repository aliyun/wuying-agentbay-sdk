// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506;

import com.aliyun.tea.*;
import com.aliyun.wuyingai20250506.models.*;

public class Client extends com.aliyun.teaopenapi.Client {

    public Client(com.aliyun.teaopenapi.models.Config config) throws Exception {
        super(config);
        this._endpointRule = "";
        this.checkConfig(config);
        this._endpoint = this.getEndpoint("wuyingai", _regionId, _endpointRule, _network, _suffix, _endpointMap, _endpoint);
    }


    public String getEndpoint(String productId, String regionId, String endpointRule, String network, String suffix, java.util.Map<String, String> endpointMap, String endpoint) throws Exception {
        if (!com.aliyun.teautil.Common.empty(endpoint)) {
            return endpoint;
        }

        if (!com.aliyun.teautil.Common.isUnset(endpointMap) && !com.aliyun.teautil.Common.empty(endpointMap.get(regionId))) {
            return endpointMap.get(regionId);
        }

        return com.aliyun.endpointutil.Client.getEndpointRules(productId, regionId, endpointRule, network, suffix);
    }

    /**
     * <b>summary</b> : 
     * <p>调用mcp工具</p>
     * 
     * @param request CallMcpToolRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return CallMcpToolResponse
     */
    public CallMcpToolResponse callMcpToolWithOptions(CallMcpToolRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.args)) {
            body.put("Args", request.args);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.autoGenSession)) {
            body.put("AutoGenSession", request.autoGenSession);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.externalUserId)) {
            body.put("ExternalUserId", request.externalUserId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.imageId)) {
            body.put("ImageId", request.imageId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.name)) {
            body.put("Name", request.name);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.server)) {
            body.put("Server", request.server);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.tool)) {
            body.put("Tool", request.tool);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "CallMcpTool"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new CallMcpToolResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>调用mcp工具</p>
     * 
     * @param request CallMcpToolRequest
     * @return CallMcpToolResponse
     */
    public CallMcpToolResponse callMcpTool(CallMcpToolRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.callMcpToolWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>删除持久化上下文</p>
     * 
     * @param request ClearContextRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return ClearContextResponse
     */
    public ClearContextResponse clearContextWithOptions(ClearContextRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.id)) {
            body.put("Id", request.id);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "ClearContext"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new ClearContextResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>删除持久化上下文</p>
     * 
     * @param request ClearContextRequest
     * @return ClearContextResponse
     */
    public ClearContextResponse clearContext(ClearContextRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.clearContextWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>创建 mcp session</p>
     * 
     * @param tmpReq CreateMcpSessionRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return CreateMcpSessionResponse
     */
    public CreateMcpSessionResponse createMcpSessionWithOptions(CreateMcpSessionRequest tmpReq, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(tmpReq);
        CreateMcpSessionShrinkRequest request = new CreateMcpSessionShrinkRequest();
        com.aliyun.openapiutil.Client.convert(tmpReq, request);
        if (!com.aliyun.teautil.Common.isUnset(tmpReq.persistenceDataList)) {
            request.persistenceDataListShrink = com.aliyun.openapiutil.Client.arrayToStringWithSpecifiedStyle(tmpReq.persistenceDataList, "PersistenceDataList", "json");
        }

        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.contextId)) {
            body.put("ContextId", request.contextId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.directLink)) {
            body.put("DirectLink", request.directLink);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.enableRecord)) {
            body.put("EnableRecord", request.enableRecord);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.externalUserId)) {
            body.put("ExternalUserId", request.externalUserId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.imageId)) {
            body.put("ImageId", request.imageId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.labels)) {
            body.put("Labels", request.labels);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.loginRegionId)) {
            body.put("LoginRegionId", request.loginRegionId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.mcpPolicyId)) {
            body.put("McpPolicyId", request.mcpPolicyId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.networkId)) {
            body.put("NetworkId", request.networkId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.persistenceDataListShrink)) {
            body.put("PersistenceDataList", request.persistenceDataListShrink);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sdkStats)) {
            body.put("SdkStats", request.sdkStats);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.vpcResource)) {
            body.put("VpcResource", request.vpcResource);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "CreateMcpSession"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new CreateMcpSessionResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>创建 mcp session</p>
     * 
     * @param request CreateMcpSessionRequest
     * @return CreateMcpSessionResponse
     */
    public CreateMcpSessionResponse createMcpSession(CreateMcpSessionRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.createMcpSessionWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>创建网络</p>
     * 
     * @param request CreateNetworkRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return CreateNetworkResponse
     */
    public CreateNetworkResponse createNetworkWithOptions(CreateNetworkRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.networkId)) {
            body.put("NetworkId", request.networkId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "CreateNetwork"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new CreateNetworkResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>创建网络</p>
     * 
     * @param request CreateNetworkRequest
     * @return CreateNetworkResponse
     */
    public CreateNetworkResponse createNetwork(CreateNetworkRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.createNetworkWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>删除持久化上下文</p>
     * 
     * @param request DeleteContextRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return DeleteContextResponse
     */
    public DeleteContextResponse deleteContextWithOptions(DeleteContextRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.id)) {
            body.put("Id", request.id);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "DeleteContext"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new DeleteContextResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>删除持久化上下文</p>
     * 
     * @param request DeleteContextRequest
     * @return DeleteContextResponse
     */
    public DeleteContextResponse deleteContext(DeleteContextRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.deleteContextWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>获取上传context文件url</p>
     * 
     * @param request DeleteContextFileRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return DeleteContextFileResponse
     */
    public DeleteContextFileResponse deleteContextFileWithOptions(DeleteContextFileRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.contextId)) {
            body.put("ContextId", request.contextId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.filePath)) {
            body.put("FilePath", request.filePath);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "DeleteContextFile"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new DeleteContextFileResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>获取上传context文件url</p>
     * 
     * @param request DeleteContextFileRequest
     * @return DeleteContextFileResponse
     */
    public DeleteContextFileResponse deleteContextFile(DeleteContextFileRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.deleteContextFileWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>休眠</p>
     * 
     * @param request DeleteSessionAsyncRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return DeleteSessionAsyncResponse
     */
    public DeleteSessionAsyncResponse deleteSessionAsyncWithOptions(DeleteSessionAsyncRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "DeleteSessionAsync"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new DeleteSessionAsyncResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>休眠</p>
     * 
     * @param request DeleteSessionAsyncRequest
     * @return DeleteSessionAsyncResponse
     */
    public DeleteSessionAsyncResponse deleteSessionAsync(DeleteSessionAsyncRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.deleteSessionAsyncWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>查询context特定目录文件</p>
     * 
     * @param request DescribeContextFilesRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return DescribeContextFilesResponse
     */
    public DescribeContextFilesResponse describeContextFilesWithOptions(DescribeContextFilesRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> query = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.maxResults)) {
            query.put("MaxResults", request.maxResults);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.nextToken)) {
            query.put("NextToken", request.nextToken);
        }

        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.contextId)) {
            body.put("ContextId", request.contextId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.pageNumber)) {
            body.put("PageNumber", request.pageNumber);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.pageSize)) {
            body.put("PageSize", request.pageSize);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.parentFolderPath)) {
            body.put("ParentFolderPath", request.parentFolderPath);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("query", com.aliyun.openapiutil.Client.query(query)),
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "DescribeContextFiles"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new DescribeContextFilesResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>查询context特定目录文件</p>
     * 
     * @param request DescribeContextFilesRequest
     * @return DescribeContextFilesResponse
     */
    public DescribeContextFilesResponse describeContextFiles(DescribeContextFilesRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.describeContextFilesWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>查询网络信息</p>
     * 
     * @param request DescribeNetworkRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return DescribeNetworkResponse
     */
    public DescribeNetworkResponse describeNetworkWithOptions(DescribeNetworkRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.networkId)) {
            body.put("NetworkId", request.networkId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "DescribeNetwork"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new DescribeNetworkResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>查询网络信息</p>
     * 
     * @param request DescribeNetworkRequest
     * @return DescribeNetworkResponse
     */
    public DescribeNetworkResponse describeNetwork(DescribeNetworkRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.describeNetworkWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>获取ADB链接</p>
     * 
     * @param request GetAdbLinkRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return GetAdbLinkResponse
     */
    public GetAdbLinkResponse getAdbLinkWithOptions(GetAdbLinkRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.option)) {
            body.put("Option", request.option);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "GetAdbLink"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new GetAdbLinkResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>获取ADB链接</p>
     * 
     * @param request GetAdbLinkRequest
     * @return GetAdbLinkResponse
     */
    public GetAdbLinkResponse getAdbLink(GetAdbLinkRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.getAdbLinkWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>获取并加载内部Context</p>
     * 
     * @param request GetAndLoadInternalContextRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return GetAndLoadInternalContextResponse
     */
    public GetAndLoadInternalContextResponse getAndLoadInternalContextWithOptions(GetAndLoadInternalContextRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.contextTypes)) {
            body.put("ContextTypes", request.contextTypes);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "GetAndLoadInternalContext"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new GetAndLoadInternalContextResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>获取并加载内部Context</p>
     * 
     * @param request GetAndLoadInternalContextRequest
     * @return GetAndLoadInternalContextResponse
     */
    public GetAndLoadInternalContextResponse getAndLoadInternalContext(GetAndLoadInternalContextRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.getAndLoadInternalContextWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>获取CDP链接</p>
     * 
     * @param request GetCdpLinkRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return GetCdpLinkResponse
     */
    public GetCdpLinkResponse getCdpLinkWithOptions(GetCdpLinkRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "GetCdpLink"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new GetCdpLinkResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>获取CDP链接</p>
     * 
     * @param request GetCdpLinkRequest
     * @return GetCdpLinkResponse
     */
    public GetCdpLinkResponse getCdpLink(GetCdpLinkRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.getCdpLinkWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>获取上下文</p>
     * 
     * @param request GetContextRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return GetContextResponse
     */
    public GetContextResponse getContextWithOptions(GetContextRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.allowCreate)) {
            body.put("AllowCreate", request.allowCreate);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.contextId)) {
            body.put("ContextId", request.contextId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.loginRegionId)) {
            body.put("LoginRegionId", request.loginRegionId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.name)) {
            body.put("Name", request.name);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "GetContext"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new GetContextResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>获取上下文</p>
     * 
     * @param request GetContextRequest
     * @return GetContextResponse
     */
    public GetContextResponse getContext(GetContextRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.getContextWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>获取上传context文件url</p>
     * 
     * @param request GetContextFileDownloadUrlRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return GetContextFileDownloadUrlResponse
     */
    public GetContextFileDownloadUrlResponse getContextFileDownloadUrlWithOptions(GetContextFileDownloadUrlRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.contextId)) {
            body.put("ContextId", request.contextId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.filePath)) {
            body.put("FilePath", request.filePath);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "GetContextFileDownloadUrl"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new GetContextFileDownloadUrlResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>获取上传context文件url</p>
     * 
     * @param request GetContextFileDownloadUrlRequest
     * @return GetContextFileDownloadUrlResponse
     */
    public GetContextFileDownloadUrlResponse getContextFileDownloadUrl(GetContextFileDownloadUrlRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.getContextFileDownloadUrlWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>获取上传context文件url</p>
     * 
     * @param request GetContextFileUploadUrlRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return GetContextFileUploadUrlResponse
     */
    public GetContextFileUploadUrlResponse getContextFileUploadUrlWithOptions(GetContextFileUploadUrlRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.contextId)) {
            body.put("ContextId", request.contextId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.filePath)) {
            body.put("FilePath", request.filePath);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "GetContextFileUploadUrl"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new GetContextFileUploadUrlResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>获取上传context文件url</p>
     * 
     * @param request GetContextFileUploadUrlRequest
     * @return GetContextFileUploadUrlResponse
     */
    public GetContextFileUploadUrlResponse getContextFileUploadUrl(GetContextFileUploadUrlRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.getContextFileUploadUrlWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>获取上下文信息</p>
     * 
     * @param request GetContextInfoRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return GetContextInfoResponse
     */
    public GetContextInfoResponse getContextInfoWithOptions(GetContextInfoRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.contextId)) {
            body.put("ContextId", request.contextId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.path)) {
            body.put("Path", request.path);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.taskType)) {
            body.put("TaskType", request.taskType);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "GetContextInfo"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new GetContextInfoResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>获取上下文信息</p>
     * 
     * @param request GetContextInfoRequest
     * @return GetContextInfoResponse
     */
    public GetContextInfoResponse getContextInfo(GetContextInfoRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.getContextInfoWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>获取标签</p>
     * 
     * @param request GetLabelRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return GetLabelResponse
     */
    public GetLabelResponse getLabelWithOptions(GetLabelRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.maxResults)) {
            body.put("MaxResults", request.maxResults);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.nextToken)) {
            body.put("NextToken", request.nextToken);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "GetLabel"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new GetLabelResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>获取标签</p>
     * 
     * @param request GetLabelRequest
     * @return GetLabelResponse
     */
    public GetLabelResponse getLabel(GetLabelRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.getLabelWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>获取特定端口的转发链接</p>
     * 
     * @param request GetLinkRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return GetLinkResponse
     */
    public GetLinkResponse getLinkWithOptions(GetLinkRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.option)) {
            body.put("Option", request.option);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.port)) {
            body.put("Port", request.port);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.protocolType)) {
            body.put("ProtocolType", request.protocolType);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "GetLink"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new GetLinkResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>获取特定端口的转发链接</p>
     * 
     * @param request GetLinkRequest
     * @return GetLinkResponse
     */
    public GetLinkResponse getLink(GetLinkRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.getLinkWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>获取mcp资源信息</p>
     * 
     * @param request GetMcpResourceRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return GetMcpResourceResponse
     */
    public GetMcpResourceResponse getMcpResourceWithOptions(GetMcpResourceRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "GetMcpResource"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new GetMcpResourceResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>获取mcp资源信息</p>
     * 
     * @param request GetMcpResourceRequest
     * @return GetMcpResourceResponse
     */
    public GetMcpResourceResponse getMcpResource(GetMcpResourceRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.getMcpResourceWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>GetSession</p>
     * 
     * @param request GetSessionRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return GetSessionResponse
     */
    public GetSessionResponse getSessionWithOptions(GetSessionRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "GetSession"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new GetSessionResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>GetSession</p>
     * 
     * @param request GetSessionRequest
     * @return GetSessionResponse
     */
    public GetSessionResponse getSession(GetSessionRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.getSessionWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>初始化AI浏览器</p>
     * 
     * @param request InitBrowserRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return InitBrowserResponse
     */
    public InitBrowserResponse initBrowserWithOptions(InitBrowserRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.browserOption)) {
            body.put("BrowserOption", request.browserOption);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.persistentPath)) {
            body.put("PersistentPath", request.persistentPath);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "InitBrowser"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new InitBrowserResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>初始化AI浏览器</p>
     * 
     * @param request InitBrowserRequest
     * @return InitBrowserResponse
     */
    public InitBrowserResponse initBrowser(InitBrowserRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.initBrowserWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>获取上下文列表</p>
     * 
     * @param request ListContextsRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return ListContextsResponse
     */
    public ListContextsResponse listContextsWithOptions(ListContextsRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.contextType)) {
            body.put("ContextType", request.contextType);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.maxResults)) {
            body.put("MaxResults", request.maxResults);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.nextToken)) {
            body.put("NextToken", request.nextToken);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "ListContexts"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new ListContextsResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>获取上下文列表</p>
     * 
     * @param request ListContextsRequest
     * @return ListContextsResponse
     */
    public ListContextsResponse listContexts(ListContextsRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.listContextsWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>ListMcpTools</p>
     * 
     * @param request ListMcpToolsRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return ListMcpToolsResponse
     */
    public ListMcpToolsResponse listMcpToolsWithOptions(ListMcpToolsRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.imageId)) {
            body.put("ImageId", request.imageId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "ListMcpTools"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new ListMcpToolsResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>ListMcpTools</p>
     * 
     * @param request ListMcpToolsRequest
     * @return ListMcpToolsResponse
     */
    public ListMcpToolsResponse listMcpTools(ListMcpToolsRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.listMcpToolsWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>根据Lable查询Session列表</p>
     * 
     * @param request ListSessionRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return ListSessionResponse
     */
    public ListSessionResponse listSessionWithOptions(ListSessionRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.isAll)) {
            body.put("IsAll", request.isAll);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.labels)) {
            body.put("Labels", request.labels);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.maxResults)) {
            body.put("MaxResults", request.maxResults);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.nextToken)) {
            body.put("NextToken", request.nextToken);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "ListSession"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new ListSessionResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>根据Lable查询Session列表</p>
     * 
     * @param request ListSessionRequest
     * @return ListSessionResponse
     */
    public ListSessionResponse listSession(ListSessionRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.listSessionWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>修改上下文</p>
     * 
     * @param request ModifyContextRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return ModifyContextResponse
     */
    public ModifyContextResponse modifyContextWithOptions(ModifyContextRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.id)) {
            body.put("Id", request.id);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.name)) {
            body.put("Name", request.name);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "ModifyContext"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new ModifyContextResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>修改上下文</p>
     * 
     * @param request ModifyContextRequest
     * @return ModifyContextResponse
     */
    public ModifyContextResponse modifyContext(ModifyContextRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.modifyContextWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>休眠</p>
     * 
     * @param request PauseSessionAsyncRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return PauseSessionAsyncResponse
     */
    public PauseSessionAsyncResponse pauseSessionAsyncWithOptions(PauseSessionAsyncRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "PauseSessionAsync"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new PauseSessionAsyncResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>休眠</p>
     * 
     * @param request PauseSessionAsyncRequest
     * @return PauseSessionAsyncResponse
     */
    public PauseSessionAsyncResponse pauseSessionAsync(PauseSessionAsyncRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.pauseSessionAsyncWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>释放 mcp session</p>
     * 
     * @param request ReleaseMcpSessionRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return ReleaseMcpSessionResponse
     */
    public ReleaseMcpSessionResponse releaseMcpSessionWithOptions(ReleaseMcpSessionRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "ReleaseMcpSession"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new ReleaseMcpSessionResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>释放 mcp session</p>
     * 
     * @param request ReleaseMcpSessionRequest
     * @return ReleaseMcpSessionResponse
     */
    public ReleaseMcpSessionResponse releaseMcpSession(ReleaseMcpSessionRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.releaseMcpSessionWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>异步休眠中恢复</p>
     * 
     * @param request ResumeSessionAsyncRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return ResumeSessionAsyncResponse
     */
    public ResumeSessionAsyncResponse resumeSessionAsyncWithOptions(ResumeSessionAsyncRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "ResumeSessionAsync"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new ResumeSessionAsyncResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>异步休眠中恢复</p>
     * 
     * @param request ResumeSessionAsyncRequest
     * @return ResumeSessionAsyncResponse
     */
    public ResumeSessionAsyncResponse resumeSessionAsync(ResumeSessionAsyncRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.resumeSessionAsyncWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>设置标签</p>
     * 
     * @param request SetLabelRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return SetLabelResponse
     */
    public SetLabelResponse setLabelWithOptions(SetLabelRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            body.put("Authorization", request.authorization);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.labels)) {
            body.put("Labels", request.labels);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "SetLabel"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new SetLabelResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>设置标签</p>
     * 
     * @param request SetLabelRequest
     * @return SetLabelResponse
     */
    public SetLabelResponse setLabel(SetLabelRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.setLabelWithOptions(request, runtime);
    }

    /**
     * <b>summary</b> : 
     * <p>同步上下文</p>
     * 
     * @param request SyncContextRequest
     * @param runtime runtime options for this request RuntimeOptions
     * @return SyncContextResponse
     */
    public SyncContextResponse syncContextWithOptions(SyncContextRequest request, com.aliyun.teautil.models.RuntimeOptions runtime) throws Exception {
        com.aliyun.teautil.Common.validateModel(request);
        java.util.Map<String, Object> query = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.authorization)) {
            query.put("Authorization", request.authorization);
        }

        java.util.Map<String, Object> body = new java.util.HashMap<>();
        if (!com.aliyun.teautil.Common.isUnset(request.contextId)) {
            body.put("ContextId", request.contextId);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.mode)) {
            body.put("Mode", request.mode);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.path)) {
            body.put("Path", request.path);
        }

        if (!com.aliyun.teautil.Common.isUnset(request.sessionId)) {
            body.put("SessionId", request.sessionId);
        }

        com.aliyun.teaopenapi.models.OpenApiRequest req = com.aliyun.teaopenapi.models.OpenApiRequest.build(TeaConverter.buildMap(
            new TeaPair("query", com.aliyun.openapiutil.Client.query(query)),
            new TeaPair("body", com.aliyun.openapiutil.Client.parseToMap(body))
        ));
        com.aliyun.teaopenapi.models.Params params = com.aliyun.teaopenapi.models.Params.build(TeaConverter.buildMap(
            new TeaPair("action", "SyncContext"),
            new TeaPair("version", "2025-05-06"),
            new TeaPair("protocol", "HTTPS"),
            new TeaPair("pathname", "/"),
            new TeaPair("method", "POST"),
            new TeaPair("authType", "Anonymous"),
            new TeaPair("style", "RPC"),
            new TeaPair("reqBodyType", "formData"),
            new TeaPair("bodyType", "json")
        ));
        return TeaModel.toModel(this.doRPCRequest(params.action, params.version, params.protocol, params.method, params.authType, params.bodyType, req, runtime), new SyncContextResponse());
    }

    /**
     * <b>summary</b> : 
     * <p>同步上下文</p>
     * 
     * @param request SyncContextRequest
     * @return SyncContextResponse
     */
    public SyncContextResponse syncContext(SyncContextRequest request) throws Exception {
        com.aliyun.teautil.models.RuntimeOptions runtime = new com.aliyun.teautil.models.RuntimeOptions();
        return this.syncContextWithOptions(request, runtime);
    }
}
