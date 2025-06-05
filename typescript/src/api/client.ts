// This file is auto-generated, don't edit it
import * as $dara from '@darabonba/typescript';
import OpenApi from '@alicloud/openapi-core';
import { OpenApiUtil, $OpenApiUtil }from '@alicloud/openapi-core';


import * as $_model from './models/model';
export * from './models/model';

export default class Client extends OpenApi {

  constructor(config: $OpenApiUtil.Config) {
    super(config);
    this._signatureAlgorithm = "v2";
    this._endpointRule = "";
    this.checkConfig(config);
    this._endpoint = this.getEndpoint("wuyingai", this._regionId, this._endpointRule, this._network, this._suffix, this._endpointMap, this._endpoint);
  }


  getEndpoint(productId: string, regionId: string, endpointRule: string, network: string, suffix: string, endpointMap: {[key: string ]: string}, endpoint: string): string {
    if (!$dara.isNull(endpoint)) {
      return endpoint;
    }

    if (!$dara.isNull(endpointMap) && !$dara.isNull(endpointMap[regionId])) {
      return endpointMap[regionId];
    }

    return OpenApiUtil.getEndpointRules(productId, regionId, endpointRule, network, suffix);
  }

  /**
   * 获取STS Token
   * 
   * @param request - ApplyMqttTokenRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns ApplyMqttTokenResponse
   */
  async applyMqttTokenWithOptions(request: $_model.ApplyMqttTokenRequest, runtime: $dara.RuntimeOptions): Promise<$_model.ApplyMqttTokenResponse> {
    request.validate();
    let query = { };
    if (!$dara.isNull(request.desktopId)) {
      query["DesktopId"] = request.desktopId;
    }

    if (!$dara.isNull(request.sessionToken)) {
      query["SessionToken"] = request.sessionToken;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      query: OpenApiUtil.query(query),
    });
    let params = new $OpenApiUtil.Params({
      action: "ApplyMqttToken",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.ApplyMqttTokenResponse>(await this.callApi(params, req, runtime), new $_model.ApplyMqttTokenResponse({}));
  }

  /**
   * 获取STS Token
   * 
   * @param request - ApplyMqttTokenRequest
   * @returns ApplyMqttTokenResponse
   */
  async applyMqttToken(request: $_model.ApplyMqttTokenRequest): Promise<$_model.ApplyMqttTokenResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.applyMqttTokenWithOptions(request, runtime);
  }

  /**
   * 调用mcp工具
   * 
   * @param request - CallMcpToolRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns CallMcpToolResponse
   */
  async callMcpToolWithOptions(request: $_model.CallMcpToolRequest, runtime: $dara.RuntimeOptions): Promise<$_model.CallMcpToolResponse> {
    request.validate();
    let body : {[key: string ]: any} = { };
    if (!$dara.isNull(request.args)) {
      body["Args"] = request.args;
    }

    if (!$dara.isNull(request.authorization)) {
      body["Authorization"] = request.authorization;
    }

    if (!$dara.isNull(request.externalUserId)) {
      body["ExternalUserId"] = request.externalUserId;
    }

    if (!$dara.isNull(request.name)) {
      body["Name"] = request.name;
    }

    if (!$dara.isNull(request.server)) {
      body["Server"] = request.server;
    }

    if (!$dara.isNull(request.sessionId)) {
      body["SessionId"] = request.sessionId;
    }

    if (!$dara.isNull(request.tool)) {
      body["Tool"] = request.tool;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      body: OpenApiUtil.parseToMap(body),
    });
    let params = new $OpenApiUtil.Params({
      action: "CallMcpTool",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.CallMcpToolResponse>(await this.callApi(params, req, runtime), new $_model.CallMcpToolResponse({}));
  }

  /**
   * 调用mcp工具
   * 
   * @param request - CallMcpToolRequest
   * @returns CallMcpToolResponse
   */
  async callMcpTool(request: $_model.CallMcpToolRequest): Promise<$_model.CallMcpToolResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.callMcpToolWithOptions(request, runtime);
  }

  /**
   * 创建 mcp session
   * 
   * @param request - CreateMcpSessionRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns CreateMcpSessionResponse
   */
  async createMcpSessionWithOptions(request: $_model.CreateMcpSessionRequest, runtime: $dara.RuntimeOptions): Promise<$_model.CreateMcpSessionResponse> {
    request.validate();
    let body : {[key: string ]: any} = { };
    if (!$dara.isNull(request.authorization)) {
      body["Authorization"] = request.authorization;
    }

    if (!$dara.isNull(request.contextId)) {
      body["ContextId"] = request.contextId;
    }

    if (!$dara.isNull(request.externalUserId)) {
      body["ExternalUserId"] = request.externalUserId;
    }

    if (!$dara.isNull(request.labels)) {
      body["Labels"] = request.labels;
    }

    if (!$dara.isNull(request.sessionId)) {
      body["SessionId"] = request.sessionId;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      body: OpenApiUtil.parseToMap(body),
    });
    let params = new $OpenApiUtil.Params({
      action: "CreateMcpSession",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.CreateMcpSessionResponse>(await this.callApi(params, req, runtime), new $_model.CreateMcpSessionResponse({}));
  }

  /**
   * 创建 mcp session
   * 
   * @param request - CreateMcpSessionRequest
   * @returns CreateMcpSessionResponse
   */
  async createMcpSession(request: $_model.CreateMcpSessionRequest): Promise<$_model.CreateMcpSessionResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.createMcpSessionWithOptions(request, runtime);
  }

  /**
   * 删除持久化上下文
   * 
   * @param request - DeleteContextRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns DeleteContextResponse
   */
  async deleteContextWithOptions(request: $_model.DeleteContextRequest, runtime: $dara.RuntimeOptions): Promise<$_model.DeleteContextResponse> {
    request.validate();
    let body : {[key: string ]: any} = { };
    if (!$dara.isNull(request.authorization)) {
      body["Authorization"] = request.authorization;
    }

    if (!$dara.isNull(request.id)) {
      body["Id"] = request.id;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      body: OpenApiUtil.parseToMap(body),
    });
    let params = new $OpenApiUtil.Params({
      action: "DeleteContext",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.DeleteContextResponse>(await this.callApi(params, req, runtime), new $_model.DeleteContextResponse({}));
  }

  /**
   * 删除持久化上下文
   * 
   * @param request - DeleteContextRequest
   * @returns DeleteContextResponse
   */
  async deleteContext(request: $_model.DeleteContextRequest): Promise<$_model.DeleteContextResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.deleteContextWithOptions(request, runtime);
  }

  /**
   * 获取上下文
   * 
   * @param request - GetContextRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns GetContextResponse
   */
  async getContextWithOptions(request: $_model.GetContextRequest, runtime: $dara.RuntimeOptions): Promise<$_model.GetContextResponse> {
    request.validate();
    let body : {[key: string ]: any} = { };
    if (!$dara.isNull(request.allowCreate)) {
      body["AllowCreate"] = request.allowCreate;
    }

    if (!$dara.isNull(request.authorization)) {
      body["Authorization"] = request.authorization;
    }

    if (!$dara.isNull(request.name)) {
      body["Name"] = request.name;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      body: OpenApiUtil.parseToMap(body),
    });
    let params = new $OpenApiUtil.Params({
      action: "GetContext",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.GetContextResponse>(await this.callApi(params, req, runtime), new $_model.GetContextResponse({}));
  }

  /**
   * 获取上下文
   * 
   * @param request - GetContextRequest
   * @returns GetContextResponse
   */
  async getContext(request: $_model.GetContextRequest): Promise<$_model.GetContextResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.getContextWithOptions(request, runtime);
  }

  /**
   * 获取标签
   * 
   * @param request - GetLabelRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns GetLabelResponse
   */
  async getLabelWithOptions(request: $_model.GetLabelRequest, runtime: $dara.RuntimeOptions): Promise<$_model.GetLabelResponse> {
    request.validate();
    let body : {[key: string ]: any} = { };
    if (!$dara.isNull(request.authorization)) {
      body["Authorization"] = request.authorization;
    }

    if (!$dara.isNull(request.maxResults)) {
      body["MaxResults"] = request.maxResults;
    }

    if (!$dara.isNull(request.nextToken)) {
      body["NextToken"] = request.nextToken;
    }

    if (!$dara.isNull(request.sessionId)) {
      body["SessionId"] = request.sessionId;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      body: OpenApiUtil.parseToMap(body),
    });
    let params = new $OpenApiUtil.Params({
      action: "GetLabel",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.GetLabelResponse>(await this.callApi(params, req, runtime), new $_model.GetLabelResponse({}));
  }

  /**
   * 获取标签
   * 
   * @param request - GetLabelRequest
   * @returns GetLabelResponse
   */
  async getLabel(request: $_model.GetLabelRequest): Promise<$_model.GetLabelResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.getLabelWithOptions(request, runtime);
  }

  /**
   * 获取mcp资源信息
   * 
   * @param request - GetMcpResourceRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns GetMcpResourceResponse
   */
  async getMcpResourceWithOptions(request: $_model.GetMcpResourceRequest, runtime: $dara.RuntimeOptions): Promise<$_model.GetMcpResourceResponse> {
    request.validate();
    let body : {[key: string ]: any} = { };
    if (!$dara.isNull(request.authorization)) {
      body["Authorization"] = request.authorization;
    }

    if (!$dara.isNull(request.sessionId)) {
      body["SessionId"] = request.sessionId;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      body: OpenApiUtil.parseToMap(body),
    });
    let params = new $OpenApiUtil.Params({
      action: "GetMcpResource",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.GetMcpResourceResponse>(await this.callApi(params, req, runtime), new $_model.GetMcpResourceResponse({}));
  }

  /**
   * 获取mcp资源信息
   * 
   * @param request - GetMcpResourceRequest
   * @returns GetMcpResourceResponse
   */
  async getMcpResource(request: $_model.GetMcpResourceRequest): Promise<$_model.GetMcpResourceResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.getMcpResourceWithOptions(request, runtime);
  }

  /**
   * 处理来自AI Engine的消息
   * 
   * @param request - HandleAIEngineMessageRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns HandleAIEngineMessageResponse
   */
  async handleAIEngineMessageWithOptions(request: $_model.HandleAIEngineMessageRequest, runtime: $dara.RuntimeOptions): Promise<$_model.HandleAIEngineMessageResponse> {
    request.validate();
    let query = { };
    if (!$dara.isNull(request.sessionToken)) {
      query["SessionToken"] = request.sessionToken;
    }

    let body : {[key: string ]: any} = { };
    if (!$dara.isNull(request.data)) {
      body["Data"] = request.data;
    }

    if (!$dara.isNull(request.msgType)) {
      body["MsgType"] = request.msgType;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      query: OpenApiUtil.query(query),
      body: OpenApiUtil.parseToMap(body),
    });
    let params = new $OpenApiUtil.Params({
      action: "HandleAIEngineMessage",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.HandleAIEngineMessageResponse>(await this.callApi(params, req, runtime), new $_model.HandleAIEngineMessageResponse({}));
  }

  /**
   * 处理来自AI Engine的消息
   * 
   * @param request - HandleAIEngineMessageRequest
   * @returns HandleAIEngineMessageResponse
   */
  async handleAIEngineMessage(request: $_model.HandleAIEngineMessageRequest): Promise<$_model.HandleAIEngineMessageResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.handleAIEngineMessageWithOptions(request, runtime);
  }

  /**
   * 获取上下文列表
   * 
   * @param request - ListContextsRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns ListContextsResponse
   */
  async listContextsWithOptions(request: $_model.ListContextsRequest, runtime: $dara.RuntimeOptions): Promise<$_model.ListContextsResponse> {
    request.validate();
    let body : {[key: string ]: any} = { };
    if (!$dara.isNull(request.authorization)) {
      body["Authorization"] = request.authorization;
    }

    if (!$dara.isNull(request.maxResults)) {
      body["MaxResults"] = request.maxResults;
    }

    if (!$dara.isNull(request.nextToken)) {
      body["NextToken"] = request.nextToken;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      body: OpenApiUtil.parseToMap(body),
    });
    let params = new $OpenApiUtil.Params({
      action: "ListContexts",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.ListContextsResponse>(await this.callApi(params, req, runtime), new $_model.ListContextsResponse({}));
  }

  /**
   * 获取上下文列表
   * 
   * @param request - ListContextsRequest
   * @returns ListContextsResponse
   */
  async listContexts(request: $_model.ListContextsRequest): Promise<$_model.ListContextsResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.listContextsWithOptions(request, runtime);
  }

  /**
   * ListMcpTools
   * 
   * @param request - ListMcpToolsRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns ListMcpToolsResponse
   */
  async listMcpToolsWithOptions(request: $_model.ListMcpToolsRequest, runtime: $dara.RuntimeOptions): Promise<$_model.ListMcpToolsResponse> {
    request.validate();
    let body : {[key: string ]: any} = { };
    if (!$dara.isNull(request.authorization)) {
      body["Authorization"] = request.authorization;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      body: OpenApiUtil.parseToMap(body),
    });
    let params = new $OpenApiUtil.Params({
      action: "ListMcpTools",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.ListMcpToolsResponse>(await this.callApi(params, req, runtime), new $_model.ListMcpToolsResponse({}));
  }

  /**
   * ListMcpTools
   * 
   * @param request - ListMcpToolsRequest
   * @returns ListMcpToolsResponse
   */
  async listMcpTools(request: $_model.ListMcpToolsRequest): Promise<$_model.ListMcpToolsResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.listMcpToolsWithOptions(request, runtime);
  }

  /**
   * 根据Lable查询Session列表
   * 
   * @param request - ListSessionRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns ListSessionResponse
   */
  async listSessionWithOptions(request: $_model.ListSessionRequest, runtime: $dara.RuntimeOptions): Promise<$_model.ListSessionResponse> {
    request.validate();
    let body : {[key: string ]: any} = { };
    if (!$dara.isNull(request.authorization)) {
      body["Authorization"] = request.authorization;
    }

    if (!$dara.isNull(request.labels)) {
      body["Labels"] = request.labels;
    }

    if (!$dara.isNull(request.maxResults)) {
      body["MaxResults"] = request.maxResults;
    }

    if (!$dara.isNull(request.nextToken)) {
      body["NextToken"] = request.nextToken;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      body: OpenApiUtil.parseToMap(body),
    });
    let params = new $OpenApiUtil.Params({
      action: "ListSession",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.ListSessionResponse>(await this.callApi(params, req, runtime), new $_model.ListSessionResponse({}));
  }

  /**
   * 根据Lable查询Session列表
   * 
   * @param request - ListSessionRequest
   * @returns ListSessionResponse
   */
  async listSession(request: $_model.ListSessionRequest): Promise<$_model.ListSessionResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.listSessionWithOptions(request, runtime);
  }

  /**
   * 修改上下文
   * 
   * @param request - ModifyContextRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns ModifyContextResponse
   */
  async modifyContextWithOptions(request: $_model.ModifyContextRequest, runtime: $dara.RuntimeOptions): Promise<$_model.ModifyContextResponse> {
    request.validate();
    let body : {[key: string ]: any} = { };
    if (!$dara.isNull(request.authorization)) {
      body["Authorization"] = request.authorization;
    }

    if (!$dara.isNull(request.id)) {
      body["Id"] = request.id;
    }

    if (!$dara.isNull(request.name)) {
      body["Name"] = request.name;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      body: OpenApiUtil.parseToMap(body),
    });
    let params = new $OpenApiUtil.Params({
      action: "ModifyContext",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.ModifyContextResponse>(await this.callApi(params, req, runtime), new $_model.ModifyContextResponse({}));
  }

  /**
   * 修改上下文
   * 
   * @param request - ModifyContextRequest
   * @returns ModifyContextResponse
   */
  async modifyContext(request: $_model.ModifyContextRequest): Promise<$_model.ModifyContextResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.modifyContextWithOptions(request, runtime);
  }

  /**
   * 释放 mcp session
   * 
   * @param request - ReleaseMcpSessionRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns ReleaseMcpSessionResponse
   */
  async releaseMcpSessionWithOptions(request: $_model.ReleaseMcpSessionRequest, runtime: $dara.RuntimeOptions): Promise<$_model.ReleaseMcpSessionResponse> {
    request.validate();
    let body : {[key: string ]: any} = { };
    if (!$dara.isNull(request.authorization)) {
      body["Authorization"] = request.authorization;
    }

    if (!$dara.isNull(request.sessionId)) {
      body["SessionId"] = request.sessionId;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      body: OpenApiUtil.parseToMap(body),
    });
    let params = new $OpenApiUtil.Params({
      action: "ReleaseMcpSession",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.ReleaseMcpSessionResponse>(await this.callApi(params, req, runtime), new $_model.ReleaseMcpSessionResponse({}));
  }

  /**
   * 释放 mcp session
   * 
   * @param request - ReleaseMcpSessionRequest
   * @returns ReleaseMcpSessionResponse
   */
  async releaseMcpSession(request: $_model.ReleaseMcpSessionRequest): Promise<$_model.ReleaseMcpSessionResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.releaseMcpSessionWithOptions(request, runtime);
  }

  /**
   * 设置标签
   * 
   * @param request - SetLabelRequest
   * @param runtime - runtime options for this request RuntimeOptions
   * @returns SetLabelResponse
   */
  async setLabelWithOptions(request: $_model.SetLabelRequest, runtime: $dara.RuntimeOptions): Promise<$_model.SetLabelResponse> {
    request.validate();
    let body : {[key: string ]: any} = { };
    if (!$dara.isNull(request.authorization)) {
      body["Authorization"] = request.authorization;
    }

    if (!$dara.isNull(request.labels)) {
      body["Labels"] = request.labels;
    }

    if (!$dara.isNull(request.sessionId)) {
      body["SessionId"] = request.sessionId;
    }

    let req = new $OpenApiUtil.OpenApiRequest({
      body: OpenApiUtil.parseToMap(body),
    });
    let params = new $OpenApiUtil.Params({
      action: "SetLabel",
      version: "2025-05-06",
      protocol: "HTTPS",
      pathname: "/",
      method: "POST",
      authType: "Anonymous",
      style: "RPC",
      reqBodyType: "formData",
      bodyType: "json",
    });
    return $dara.cast<$_model.SetLabelResponse>(await this.callApi(params, req, runtime), new $_model.SetLabelResponse({}));
  }

  /**
   * 设置标签
   * 
   * @param request - SetLabelRequest
   * @returns SetLabelResponse
   */
  async setLabel(request: $_model.SetLabelRequest): Promise<$_model.SetLabelResponse> {
    let runtime = new $dara.RuntimeOptions({ });
    return await this.setLabelWithOptions(request, runtime);
  }

}
