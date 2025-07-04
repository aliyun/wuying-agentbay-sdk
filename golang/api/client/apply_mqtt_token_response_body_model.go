// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iApplyMqttTokenResponseBody interface {
	dara.Model
	String() string
	GoString() string
	SetCode(v string) *ApplyMqttTokenResponseBody
	GetCode() *string
	SetData(v *ApplyMqttTokenResponseBodyData) *ApplyMqttTokenResponseBody
	GetData() *ApplyMqttTokenResponseBodyData
	SetHttpStatusCode(v int32) *ApplyMqttTokenResponseBody
	GetHttpStatusCode() *int32
	SetMessage(v string) *ApplyMqttTokenResponseBody
	GetMessage() *string
	SetRequestId(v string) *ApplyMqttTokenResponseBody
	GetRequestId() *string
	SetSuccess(v bool) *ApplyMqttTokenResponseBody
	GetSuccess() *bool
}

type ApplyMqttTokenResponseBody struct {
	Code           *string                         `json:"Code,omitempty" xml:"Code,omitempty"`
	Data           *ApplyMqttTokenResponseBodyData `json:"Data,omitempty" xml:"Data,omitempty" type:"Struct"`
	HttpStatusCode *int32                          `json:"HttpStatusCode,omitempty" xml:"HttpStatusCode,omitempty"`
	Message        *string                         `json:"Message,omitempty" xml:"Message,omitempty"`
	RequestId      *string                         `json:"RequestId,omitempty" xml:"RequestId,omitempty"`
	Success        *bool                           `json:"Success,omitempty" xml:"Success,omitempty"`
}

func (s ApplyMqttTokenResponseBody) String() string {
	return dara.Prettify(s)
}

func (s ApplyMqttTokenResponseBody) GoString() string {
	return s.String()
}

func (s *ApplyMqttTokenResponseBody) GetCode() *string {
	return s.Code
}

func (s *ApplyMqttTokenResponseBody) GetData() *ApplyMqttTokenResponseBodyData {
	return s.Data
}

func (s *ApplyMqttTokenResponseBody) GetHttpStatusCode() *int32 {
	return s.HttpStatusCode
}

func (s *ApplyMqttTokenResponseBody) GetMessage() *string {
	return s.Message
}

func (s *ApplyMqttTokenResponseBody) GetRequestId() *string {
	return s.RequestId
}

func (s *ApplyMqttTokenResponseBody) GetSuccess() *bool {
	return s.Success
}

func (s *ApplyMqttTokenResponseBody) SetCode(v string) *ApplyMqttTokenResponseBody {
	s.Code = &v
	return s
}

func (s *ApplyMqttTokenResponseBody) SetData(v *ApplyMqttTokenResponseBodyData) *ApplyMqttTokenResponseBody {
	s.Data = v
	return s
}

func (s *ApplyMqttTokenResponseBody) SetHttpStatusCode(v int32) *ApplyMqttTokenResponseBody {
	s.HttpStatusCode = &v
	return s
}

func (s *ApplyMqttTokenResponseBody) SetMessage(v string) *ApplyMqttTokenResponseBody {
	s.Message = &v
	return s
}

func (s *ApplyMqttTokenResponseBody) SetRequestId(v string) *ApplyMqttTokenResponseBody {
	s.RequestId = &v
	return s
}

func (s *ApplyMqttTokenResponseBody) SetSuccess(v bool) *ApplyMqttTokenResponseBody {
	s.Success = &v
	return s
}

func (s *ApplyMqttTokenResponseBody) Validate() error {
	return dara.Validate(s)
}

type ApplyMqttTokenResponseBodyData struct {
	AccessKeyId   *string `json:"AccessKeyId,omitempty" xml:"AccessKeyId,omitempty"`
	ClientId      *string `json:"ClientId,omitempty" xml:"ClientId,omitempty"`
	Expiration    *string `json:"Expiration,omitempty" xml:"Expiration,omitempty"`
	InstanceId    *string `json:"InstanceId,omitempty" xml:"InstanceId,omitempty"`
	RegionId      *string `json:"RegionId,omitempty" xml:"RegionId,omitempty"`
	SecurityToken *string `json:"SecurityToken,omitempty" xml:"SecurityToken,omitempty"`
}

func (s ApplyMqttTokenResponseBodyData) String() string {
	return dara.Prettify(s)
}

func (s ApplyMqttTokenResponseBodyData) GoString() string {
	return s.String()
}

func (s *ApplyMqttTokenResponseBodyData) GetAccessKeyId() *string {
	return s.AccessKeyId
}

func (s *ApplyMqttTokenResponseBodyData) GetClientId() *string {
	return s.ClientId
}

func (s *ApplyMqttTokenResponseBodyData) GetExpiration() *string {
	return s.Expiration
}

func (s *ApplyMqttTokenResponseBodyData) GetInstanceId() *string {
	return s.InstanceId
}

func (s *ApplyMqttTokenResponseBodyData) GetRegionId() *string {
	return s.RegionId
}

func (s *ApplyMqttTokenResponseBodyData) GetSecurityToken() *string {
	return s.SecurityToken
}

func (s *ApplyMqttTokenResponseBodyData) SetAccessKeyId(v string) *ApplyMqttTokenResponseBodyData {
	s.AccessKeyId = &v
	return s
}

func (s *ApplyMqttTokenResponseBodyData) SetClientId(v string) *ApplyMqttTokenResponseBodyData {
	s.ClientId = &v
	return s
}

func (s *ApplyMqttTokenResponseBodyData) SetExpiration(v string) *ApplyMqttTokenResponseBodyData {
	s.Expiration = &v
	return s
}

func (s *ApplyMqttTokenResponseBodyData) SetInstanceId(v string) *ApplyMqttTokenResponseBodyData {
	s.InstanceId = &v
	return s
}

func (s *ApplyMqttTokenResponseBodyData) SetRegionId(v string) *ApplyMqttTokenResponseBodyData {
	s.RegionId = &v
	return s
}

func (s *ApplyMqttTokenResponseBodyData) SetSecurityToken(v string) *ApplyMqttTokenResponseBodyData {
	s.SecurityToken = &v
	return s
}

func (s *ApplyMqttTokenResponseBodyData) Validate() error {
	return dara.Validate(s)
}
