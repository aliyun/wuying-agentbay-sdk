// This file is auto-generated, don't edit it. Thanks.
package client

import (
	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	openapiutil "github.com/alibabacloud-go/darabonba-openapi/v2/utils"
	"github.com/alibabacloud-go/tea/dara"
)

type Client struct {
	openapi.Client
	DisableSDKError *bool
}

func NewClient(config *openapiutil.Config) (*Client, error) {
	client := new(Client)
	err := client.Init(config)
	return client, err
}

func (client *Client) Init(config *openapiutil.Config) (_err error) {
	_err = client.Client.Init(config)
	if _err != nil {
		return _err
	}
	client.SignatureAlgorithm = dara.String("v2")
	client.EndpointRule = dara.String("")
	_err = client.CheckConfig(config)
	if _err != nil {
		return _err
	}
	client.Endpoint, _err = client.GetEndpoint(dara.String("wuyingai"), client.RegionId, client.EndpointRule, client.Network, client.Suffix, client.EndpointMap, client.Endpoint)
	if _err != nil {
		return _err
	}

	return nil
}

func (client *Client) GetEndpoint(productId *string, regionId *string, endpointRule *string, network *string, suffix *string, endpointMap map[string]*string, endpoint *string) (_result *string, _err error) {
	if !dara.IsNil(endpoint) {
		_result = endpoint
		return _result, _err
	}

	if !dara.IsNil(endpointMap) && !dara.IsNil(endpointMap[dara.StringValue(regionId)]) {
		_result = endpointMap[dara.StringValue(regionId)]
		return _result, _err
	}

	_body, _err := openapiutil.GetEndpointRules(productId, regionId, endpointRule, network, suffix)
	if _err != nil {
		return _result, _err
	}
	_result = _body
	return _result, _err
}

// Summary:
//
// 调用mcp工具
//
// @param request - CallMcpToolRequest
//
// @param runtime - runtime options for this request RuntimeOptions
//
// @return CallMcpToolResponse
func (client *Client) CallMcpToolWithOptions(request *CallMcpToolRequest, runtime *dara.RuntimeOptions) (_result *CallMcpToolResponse, _err error) {
	_err = request.Validate()
	if _err != nil {
		return _result, _err
	}
	body := map[string]interface{}{}
	if !dara.IsNil(request.Args) {
		body["Args"] = request.Args
	}

	if !dara.IsNil(request.Authorization) {
		body["Authorization"] = request.Authorization
	}

	if !dara.IsNil(request.ExternalUserId) {
		body["ExternalUserId"] = request.ExternalUserId
	}

	if !dara.IsNil(request.ImageId) {
		body["ImageId"] = request.ImageId
	}

	if !dara.IsNil(request.Name) {
		body["Name"] = request.Name
	}

	if !dara.IsNil(request.Server) {
		body["Server"] = request.Server
	}

	if !dara.IsNil(request.SessionId) {
		body["SessionId"] = request.SessionId
	}

	if !dara.IsNil(request.Tool) {
		body["Tool"] = request.Tool
	}

	req := &openapiutil.OpenApiRequest{
		Body: openapiutil.ParseToMap(body),
	}
	params := &openapiutil.Params{
		Action:      dara.String("CallMcpTool"),
		Version:     dara.String("2025-05-06"),
		Protocol:    dara.String("HTTPS"),
		Pathname:    dara.String("/"),
		Method:      dara.String("POST"),
		AuthType:    dara.String("Anonymous"),
		Style:       dara.String("RPC"),
		ReqBodyType: dara.String("formData"),
		BodyType:    dara.String("json"),
	}
	_result = &CallMcpToolResponse{}
	_body, _err := client.CallApi(params, req, runtime)
	if _err != nil {
		return _result, _err
	}
	_err = dara.Convert(_body, &_result)
	return _result, _err
}

// Summary:
//
// 调用mcp工具
//
// @param request - CallMcpToolRequest
//
// @return CallMcpToolResponse
func (client *Client) CallMcpTool(request *CallMcpToolRequest) (_result *CallMcpToolResponse, _err error) {
	runtime := &dara.RuntimeOptions{}
	_result = &CallMcpToolResponse{}
	_body, _err := client.CallMcpToolWithOptions(request, runtime)
	if _err != nil {
		return _result, _err
	}
	_result = _body
	return _result, _err
}

// Summary:
//
// 创建 mcp session
//
// @param request - CreateMcpSessionRequest
//
// @param runtime - runtime options for this request RuntimeOptions
//
// @return CreateMcpSessionResponse
func (client *Client) CreateMcpSessionWithOptions(request *CreateMcpSessionRequest, runtime *dara.RuntimeOptions) (_result *CreateMcpSessionResponse, _err error) {
	_err = request.Validate()
	if _err != nil {
		return _result, _err
	}
	body := map[string]interface{}{}
	if !dara.IsNil(request.Authorization) {
		body["Authorization"] = request.Authorization
	}

	if !dara.IsNil(request.ContextId) {
		body["ContextId"] = request.ContextId
	}

	if !dara.IsNil(request.ExternalUserId) {
		body["ExternalUserId"] = request.ExternalUserId
	}

	if !dara.IsNil(request.ImageId) {
		body["ImageId"] = request.ImageId
	}

	if !dara.IsNil(request.Labels) {
		body["Labels"] = request.Labels
	}

	if !dara.IsNil(request.SessionId) {
		body["SessionId"] = request.SessionId
	}

	req := &openapiutil.OpenApiRequest{
		Body: openapiutil.ParseToMap(body),
	}
	params := &openapiutil.Params{
		Action:      dara.String("CreateMcpSession"),
		Version:     dara.String("2025-05-06"),
		Protocol:    dara.String("HTTPS"),
		Pathname:    dara.String("/"),
		Method:      dara.String("POST"),
		AuthType:    dara.String("Anonymous"),
		Style:       dara.String("RPC"),
		ReqBodyType: dara.String("formData"),
		BodyType:    dara.String("json"),
	}
	_result = &CreateMcpSessionResponse{}
	_body, _err := client.CallApi(params, req, runtime)
	if _err != nil {
		return _result, _err
	}
	_err = dara.Convert(_body, &_result)
	return _result, _err
}

// Summary:
//
// 创建 mcp session
//
// @param request - CreateMcpSessionRequest
//
// @return CreateMcpSessionResponse
func (client *Client) CreateMcpSession(request *CreateMcpSessionRequest) (_result *CreateMcpSessionResponse, _err error) {
	runtime := &dara.RuntimeOptions{}
	_result = &CreateMcpSessionResponse{}
	_body, _err := client.CreateMcpSessionWithOptions(request, runtime)
	if _err != nil {
		return _result, _err
	}
	_result = _body
	return _result, _err
}

// Summary:
//
// 删除持久化上下文
//
// @param request - DeleteContextRequest
//
// @param runtime - runtime options for this request RuntimeOptions
//
// @return DeleteContextResponse
func (client *Client) DeleteContextWithOptions(request *DeleteContextRequest, runtime *dara.RuntimeOptions) (_result *DeleteContextResponse, _err error) {
	_err = request.Validate()
	if _err != nil {
		return _result, _err
	}
	body := map[string]interface{}{}
	if !dara.IsNil(request.Authorization) {
		body["Authorization"] = request.Authorization
	}

	if !dara.IsNil(request.Id) {
		body["Id"] = request.Id
	}

	req := &openapiutil.OpenApiRequest{
		Body: openapiutil.ParseToMap(body),
	}
	params := &openapiutil.Params{
		Action:      dara.String("DeleteContext"),
		Version:     dara.String("2025-05-06"),
		Protocol:    dara.String("HTTPS"),
		Pathname:    dara.String("/"),
		Method:      dara.String("POST"),
		AuthType:    dara.String("Anonymous"),
		Style:       dara.String("RPC"),
		ReqBodyType: dara.String("formData"),
		BodyType:    dara.String("json"),
	}
	_result = &DeleteContextResponse{}
	_body, _err := client.CallApi(params, req, runtime)
	if _err != nil {
		return _result, _err
	}
	_err = dara.Convert(_body, &_result)
	return _result, _err
}

// Summary:
//
// 删除持久化上下文
//
// @param request - DeleteContextRequest
//
// @return DeleteContextResponse
func (client *Client) DeleteContext(request *DeleteContextRequest) (_result *DeleteContextResponse, _err error) {
	runtime := &dara.RuntimeOptions{}
	_result = &DeleteContextResponse{}
	_body, _err := client.DeleteContextWithOptions(request, runtime)
	if _err != nil {
		return _result, _err
	}
	_result = _body
	return _result, _err
}

// Summary:
//
// 获取上下文
//
// @param request - GetContextRequest
//
// @param runtime - runtime options for this request RuntimeOptions
//
// @return GetContextResponse
func (client *Client) GetContextWithOptions(request *GetContextRequest, runtime *dara.RuntimeOptions) (_result *GetContextResponse, _err error) {
	_err = request.Validate()
	if _err != nil {
		return _result, _err
	}
	body := map[string]interface{}{}
	if !dara.IsNil(request.AllowCreate) {
		body["AllowCreate"] = request.AllowCreate
	}

	if !dara.IsNil(request.Authorization) {
		body["Authorization"] = request.Authorization
	}

	if !dara.IsNil(request.Name) {
		body["Name"] = request.Name
	}

	req := &openapiutil.OpenApiRequest{
		Body: openapiutil.ParseToMap(body),
	}
	params := &openapiutil.Params{
		Action:      dara.String("GetContext"),
		Version:     dara.String("2025-05-06"),
		Protocol:    dara.String("HTTPS"),
		Pathname:    dara.String("/"),
		Method:      dara.String("POST"),
		AuthType:    dara.String("Anonymous"),
		Style:       dara.String("RPC"),
		ReqBodyType: dara.String("formData"),
		BodyType:    dara.String("json"),
	}
	_result = &GetContextResponse{}
	_body, _err := client.CallApi(params, req, runtime)
	if _err != nil {
		return _result, _err
	}
	_err = dara.Convert(_body, &_result)
	return _result, _err
}

// Summary:
//
// 获取上下文
//
// @param request - GetContextRequest
//
// @return GetContextResponse
func (client *Client) GetContext(request *GetContextRequest) (_result *GetContextResponse, _err error) {
	runtime := &dara.RuntimeOptions{}
	_result = &GetContextResponse{}
	_body, _err := client.GetContextWithOptions(request, runtime)
	if _err != nil {
		return _result, _err
	}
	_result = _body
	return _result, _err
}

// Summary:
//
// 获取标签
//
// @param request - GetLabelRequest
//
// @param runtime - runtime options for this request RuntimeOptions
//
// @return GetLabelResponse
func (client *Client) GetLabelWithOptions(request *GetLabelRequest, runtime *dara.RuntimeOptions) (_result *GetLabelResponse, _err error) {
	_err = request.Validate()
	if _err != nil {
		return _result, _err
	}
	body := map[string]interface{}{}
	if !dara.IsNil(request.Authorization) {
		body["Authorization"] = request.Authorization
	}

	if !dara.IsNil(request.MaxResults) {
		body["MaxResults"] = request.MaxResults
	}

	if !dara.IsNil(request.NextToken) {
		body["NextToken"] = request.NextToken
	}

	if !dara.IsNil(request.SessionId) {
		body["SessionId"] = request.SessionId
	}

	req := &openapiutil.OpenApiRequest{
		Body: openapiutil.ParseToMap(body),
	}
	params := &openapiutil.Params{
		Action:      dara.String("GetLabel"),
		Version:     dara.String("2025-05-06"),
		Protocol:    dara.String("HTTPS"),
		Pathname:    dara.String("/"),
		Method:      dara.String("POST"),
		AuthType:    dara.String("Anonymous"),
		Style:       dara.String("RPC"),
		ReqBodyType: dara.String("formData"),
		BodyType:    dara.String("json"),
	}
	_result = &GetLabelResponse{}
	_body, _err := client.CallApi(params, req, runtime)
	if _err != nil {
		return _result, _err
	}
	_err = dara.Convert(_body, &_result)
	return _result, _err
}

// Summary:
//
// 获取标签
//
// @param request - GetLabelRequest
//
// @return GetLabelResponse
func (client *Client) GetLabel(request *GetLabelRequest) (_result *GetLabelResponse, _err error) {
	runtime := &dara.RuntimeOptions{}
	_result = &GetLabelResponse{}
	_body, _err := client.GetLabelWithOptions(request, runtime)
	if _err != nil {
		return _result, _err
	}
	_result = _body
	return _result, _err
}

// Summary:
//
// 获取特定端口的转发链接
//
// @param request - GetLinkRequest
//
// @param runtime - runtime options for this request RuntimeOptions
//
// @return GetLinkResponse
func (client *Client) GetLinkWithOptions(request *GetLinkRequest, runtime *dara.RuntimeOptions) (_result *GetLinkResponse, _err error) {
	_err = request.Validate()
	if _err != nil {
		return _result, _err
	}
	body := map[string]interface{}{}
	if !dara.IsNil(request.Authorization) {
		body["Authorization"] = request.Authorization
	}

	if !dara.IsNil(request.SessionId) {
		body["SessionId"] = request.SessionId
	}

	req := &openapiutil.OpenApiRequest{
		Body: openapiutil.ParseToMap(body),
	}
	params := &openapiutil.Params{
		Action:      dara.String("GetLink"),
		Version:     dara.String("2025-05-06"),
		Protocol:    dara.String("HTTPS"),
		Pathname:    dara.String("/"),
		Method:      dara.String("POST"),
		AuthType:    dara.String("Anonymous"),
		Style:       dara.String("RPC"),
		ReqBodyType: dara.String("formData"),
		BodyType:    dara.String("json"),
	}
	_result = &GetLinkResponse{}
	_body, _err := client.CallApi(params, req, runtime)
	if _err != nil {
		return _result, _err
	}
	_err = dara.Convert(_body, &_result)
	return _result, _err
}

// Summary:
//
// 获取特定端口的转发链接
//
// @param request - GetLinkRequest
//
// @return GetLinkResponse
func (client *Client) GetLink(request *GetLinkRequest) (_result *GetLinkResponse, _err error) {
	runtime := &dara.RuntimeOptions{}
	_result = &GetLinkResponse{}
	_body, _err := client.GetLinkWithOptions(request, runtime)
	if _err != nil {
		return _result, _err
	}
	_result = _body
	return _result, _err
}

// Summary:
//
// 获取mcp资源信息
//
// @param request - GetMcpResourceRequest
//
// @param runtime - runtime options for this request RuntimeOptions
//
// @return GetMcpResourceResponse
func (client *Client) GetMcpResourceWithOptions(request *GetMcpResourceRequest, runtime *dara.RuntimeOptions) (_result *GetMcpResourceResponse, _err error) {
	_err = request.Validate()
	if _err != nil {
		return _result, _err
	}
	body := map[string]interface{}{}
	if !dara.IsNil(request.Authorization) {
		body["Authorization"] = request.Authorization
	}

	if !dara.IsNil(request.SessionId) {
		body["SessionId"] = request.SessionId
	}

	req := &openapiutil.OpenApiRequest{
		Body: openapiutil.ParseToMap(body),
	}
	params := &openapiutil.Params{
		Action:      dara.String("GetMcpResource"),
		Version:     dara.String("2025-05-06"),
		Protocol:    dara.String("HTTPS"),
		Pathname:    dara.String("/"),
		Method:      dara.String("POST"),
		AuthType:    dara.String("Anonymous"),
		Style:       dara.String("RPC"),
		ReqBodyType: dara.String("formData"),
		BodyType:    dara.String("json"),
	}
	_result = &GetMcpResourceResponse{}
	_body, _err := client.CallApi(params, req, runtime)
	if _err != nil {
		return _result, _err
	}
	_err = dara.Convert(_body, &_result)
	return _result, _err
}

// Summary:
//
// 获取mcp资源信息
//
// @param request - GetMcpResourceRequest
//
// @return GetMcpResourceResponse
func (client *Client) GetMcpResource(request *GetMcpResourceRequest) (_result *GetMcpResourceResponse, _err error) {
	runtime := &dara.RuntimeOptions{}
	_result = &GetMcpResourceResponse{}
	_body, _err := client.GetMcpResourceWithOptions(request, runtime)
	if _err != nil {
		return _result, _err
	}
	_result = _body
	return _result, _err
}

// Summary:
//
// 获取上下文列表
//
// @param request - ListContextsRequest
//
// @param runtime - runtime options for this request RuntimeOptions
//
// @return ListContextsResponse
func (client *Client) ListContextsWithOptions(request *ListContextsRequest, runtime *dara.RuntimeOptions) (_result *ListContextsResponse, _err error) {
	_err = request.Validate()
	if _err != nil {
		return _result, _err
	}
	body := map[string]interface{}{}
	if !dara.IsNil(request.Authorization) {
		body["Authorization"] = request.Authorization
	}

	if !dara.IsNil(request.MaxResults) {
		body["MaxResults"] = request.MaxResults
	}

	if !dara.IsNil(request.NextToken) {
		body["NextToken"] = request.NextToken
	}

	req := &openapiutil.OpenApiRequest{
		Body: openapiutil.ParseToMap(body),
	}
	params := &openapiutil.Params{
		Action:      dara.String("ListContexts"),
		Version:     dara.String("2025-05-06"),
		Protocol:    dara.String("HTTPS"),
		Pathname:    dara.String("/"),
		Method:      dara.String("POST"),
		AuthType:    dara.String("Anonymous"),
		Style:       dara.String("RPC"),
		ReqBodyType: dara.String("formData"),
		BodyType:    dara.String("json"),
	}
	_result = &ListContextsResponse{}
	_body, _err := client.CallApi(params, req, runtime)
	if _err != nil {
		return _result, _err
	}
	_err = dara.Convert(_body, &_result)
	return _result, _err
}

// Summary:
//
// 获取上下文列表
//
// @param request - ListContextsRequest
//
// @return ListContextsResponse
func (client *Client) ListContexts(request *ListContextsRequest) (_result *ListContextsResponse, _err error) {
	runtime := &dara.RuntimeOptions{}
	_result = &ListContextsResponse{}
	_body, _err := client.ListContextsWithOptions(request, runtime)
	if _err != nil {
		return _result, _err
	}
	_result = _body
	return _result, _err
}

// Summary:
//
// 根据Lable查询Session列表
//
// @param request - ListSessionRequest
//
// @param runtime - runtime options for this request RuntimeOptions
//
// @return ListSessionResponse
func (client *Client) ListSessionWithOptions(request *ListSessionRequest, runtime *dara.RuntimeOptions) (_result *ListSessionResponse, _err error) {
	_err = request.Validate()
	if _err != nil {
		return _result, _err
	}
	body := map[string]interface{}{}
	if !dara.IsNil(request.Authorization) {
		body["Authorization"] = request.Authorization
	}

	if !dara.IsNil(request.Labels) {
		body["Labels"] = request.Labels
	}

	if !dara.IsNil(request.MaxResults) {
		body["MaxResults"] = request.MaxResults
	}

	if !dara.IsNil(request.NextToken) {
		body["NextToken"] = request.NextToken
	}

	req := &openapiutil.OpenApiRequest{
		Body: openapiutil.ParseToMap(body),
	}
	params := &openapiutil.Params{
		Action:      dara.String("ListSession"),
		Version:     dara.String("2025-05-06"),
		Protocol:    dara.String("HTTPS"),
		Pathname:    dara.String("/"),
		Method:      dara.String("POST"),
		AuthType:    dara.String("Anonymous"),
		Style:       dara.String("RPC"),
		ReqBodyType: dara.String("formData"),
		BodyType:    dara.String("json"),
	}
	_result = &ListSessionResponse{}
	_body, _err := client.CallApi(params, req, runtime)
	if _err != nil {
		return _result, _err
	}
	_err = dara.Convert(_body, &_result)
	return _result, _err
}

// Summary:
//
// 根据Lable查询Session列表
//
// @param request - ListSessionRequest
//
// @return ListSessionResponse
func (client *Client) ListSession(request *ListSessionRequest) (_result *ListSessionResponse, _err error) {
	runtime := &dara.RuntimeOptions{}
	_result = &ListSessionResponse{}
	_body, _err := client.ListSessionWithOptions(request, runtime)
	if _err != nil {
		return _result, _err
	}
	_result = _body
	return _result, _err
}

// Summary:
//
// 修改上下文
//
// @param request - ModifyContextRequest
//
// @param runtime - runtime options for this request RuntimeOptions
//
// @return ModifyContextResponse
func (client *Client) ModifyContextWithOptions(request *ModifyContextRequest, runtime *dara.RuntimeOptions) (_result *ModifyContextResponse, _err error) {
	_err = request.Validate()
	if _err != nil {
		return _result, _err
	}
	body := map[string]interface{}{}
	if !dara.IsNil(request.Authorization) {
		body["Authorization"] = request.Authorization
	}

	if !dara.IsNil(request.Id) {
		body["Id"] = request.Id
	}

	if !dara.IsNil(request.Name) {
		body["Name"] = request.Name
	}

	req := &openapiutil.OpenApiRequest{
		Body: openapiutil.ParseToMap(body),
	}
	params := &openapiutil.Params{
		Action:      dara.String("ModifyContext"),
		Version:     dara.String("2025-05-06"),
		Protocol:    dara.String("HTTPS"),
		Pathname:    dara.String("/"),
		Method:      dara.String("POST"),
		AuthType:    dara.String("Anonymous"),
		Style:       dara.String("RPC"),
		ReqBodyType: dara.String("formData"),
		BodyType:    dara.String("json"),
	}
	_result = &ModifyContextResponse{}
	_body, _err := client.CallApi(params, req, runtime)
	if _err != nil {
		return _result, _err
	}
	_err = dara.Convert(_body, &_result)
	return _result, _err
}

// Summary:
//
// 修改上下文
//
// @param request - ModifyContextRequest
//
// @return ModifyContextResponse
func (client *Client) ModifyContext(request *ModifyContextRequest) (_result *ModifyContextResponse, _err error) {
	runtime := &dara.RuntimeOptions{}
	_result = &ModifyContextResponse{}
	_body, _err := client.ModifyContextWithOptions(request, runtime)
	if _err != nil {
		return _result, _err
	}
	_result = _body
	return _result, _err
}

// Summary:
//
// 释放 mcp session
//
// @param request - ReleaseMcpSessionRequest
//
// @param runtime - runtime options for this request RuntimeOptions
//
// @return ReleaseMcpSessionResponse
func (client *Client) ReleaseMcpSessionWithOptions(request *ReleaseMcpSessionRequest, runtime *dara.RuntimeOptions) (_result *ReleaseMcpSessionResponse, _err error) {
	_err = request.Validate()
	if _err != nil {
		return _result, _err
	}
	body := map[string]interface{}{}
	if !dara.IsNil(request.Authorization) {
		body["Authorization"] = request.Authorization
	}

	if !dara.IsNil(request.SessionId) {
		body["SessionId"] = request.SessionId
	}

	req := &openapiutil.OpenApiRequest{
		Body: openapiutil.ParseToMap(body),
	}
	params := &openapiutil.Params{
		Action:      dara.String("ReleaseMcpSession"),
		Version:     dara.String("2025-05-06"),
		Protocol:    dara.String("HTTPS"),
		Pathname:    dara.String("/"),
		Method:      dara.String("POST"),
		AuthType:    dara.String("Anonymous"),
		Style:       dara.String("RPC"),
		ReqBodyType: dara.String("formData"),
		BodyType:    dara.String("json"),
	}
	_result = &ReleaseMcpSessionResponse{}
	_body, _err := client.CallApi(params, req, runtime)
	if _err != nil {
		return _result, _err
	}
	_err = dara.Convert(_body, &_result)
	return _result, _err
}

// Summary:
//
// 释放 mcp session
//
// @param request - ReleaseMcpSessionRequest
//
// @return ReleaseMcpSessionResponse
func (client *Client) ReleaseMcpSession(request *ReleaseMcpSessionRequest) (_result *ReleaseMcpSessionResponse, _err error) {
	runtime := &dara.RuntimeOptions{}
	_result = &ReleaseMcpSessionResponse{}
	_body, _err := client.ReleaseMcpSessionWithOptions(request, runtime)
	if _err != nil {
		return _result, _err
	}
	_result = _body
	return _result, _err
}

// Summary:
//
// 设置标签
//
// @param request - SetLabelRequest
//
// @param runtime - runtime options for this request RuntimeOptions
//
// @return SetLabelResponse
func (client *Client) SetLabelWithOptions(request *SetLabelRequest, runtime *dara.RuntimeOptions) (_result *SetLabelResponse, _err error) {
	_err = request.Validate()
	if _err != nil {
		return _result, _err
	}
	body := map[string]interface{}{}
	if !dara.IsNil(request.Authorization) {
		body["Authorization"] = request.Authorization
	}

	if !dara.IsNil(request.Labels) {
		body["Labels"] = request.Labels
	}

	if !dara.IsNil(request.SessionId) {
		body["SessionId"] = request.SessionId
	}

	req := &openapiutil.OpenApiRequest{
		Body: openapiutil.ParseToMap(body),
	}
	params := &openapiutil.Params{
		Action:      dara.String("SetLabel"),
		Version:     dara.String("2025-05-06"),
		Protocol:    dara.String("HTTPS"),
		Pathname:    dara.String("/"),
		Method:      dara.String("POST"),
		AuthType:    dara.String("Anonymous"),
		Style:       dara.String("RPC"),
		ReqBodyType: dara.String("formData"),
		BodyType:    dara.String("json"),
	}
	_result = &SetLabelResponse{}
	_body, _err := client.CallApi(params, req, runtime)
	if _err != nil {
		return _result, _err
	}
	_err = dara.Convert(_body, &_result)
	return _result, _err
}

// Summary:
//
// 设置标签
//
// @param request - SetLabelRequest
//
// @return SetLabelResponse
func (client *Client) SetLabel(request *SetLabelRequest) (_result *SetLabelResponse, _err error) {
	runtime := &dara.RuntimeOptions{}
	_result = &SetLabelResponse{}
	_body, _err := client.SetLabelWithOptions(request, runtime)
	if _err != nil {
		return _result, _err
	}
	_result = _body
	return _result, _err
}
