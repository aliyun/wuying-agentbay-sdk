// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iHandleAIEngineMessageResponseBody interface {
	dara.Model
	String() string
	GoString() string
	SetCode(v string) *HandleAIEngineMessageResponseBody
	GetCode() *string
	SetHttpStatusCode(v int32) *HandleAIEngineMessageResponseBody
	GetHttpStatusCode() *int32
	SetMessage(v string) *HandleAIEngineMessageResponseBody
	GetMessage() *string
	SetRequestId(v string) *HandleAIEngineMessageResponseBody
	GetRequestId() *string
	SetSuccess(v bool) *HandleAIEngineMessageResponseBody
	GetSuccess() *bool
}

type HandleAIEngineMessageResponseBody struct {
	Code           *string `json:"Code,omitempty" xml:"Code,omitempty"`
	HttpStatusCode *int32  `json:"HttpStatusCode,omitempty" xml:"HttpStatusCode,omitempty"`
	Message        *string `json:"Message,omitempty" xml:"Message,omitempty"`
	RequestId      *string `json:"RequestId,omitempty" xml:"RequestId,omitempty"`
	Success        *bool   `json:"Success,omitempty" xml:"Success,omitempty"`
}

func (s HandleAIEngineMessageResponseBody) String() string {
	return dara.Prettify(s)
}

func (s HandleAIEngineMessageResponseBody) GoString() string {
	return s.String()
}

func (s *HandleAIEngineMessageResponseBody) GetCode() *string {
	return s.Code
}

func (s *HandleAIEngineMessageResponseBody) GetHttpStatusCode() *int32 {
	return s.HttpStatusCode
}

func (s *HandleAIEngineMessageResponseBody) GetMessage() *string {
	return s.Message
}

func (s *HandleAIEngineMessageResponseBody) GetRequestId() *string {
	return s.RequestId
}

func (s *HandleAIEngineMessageResponseBody) GetSuccess() *bool {
	return s.Success
}

func (s *HandleAIEngineMessageResponseBody) SetCode(v string) *HandleAIEngineMessageResponseBody {
	s.Code = &v
	return s
}

func (s *HandleAIEngineMessageResponseBody) SetHttpStatusCode(v int32) *HandleAIEngineMessageResponseBody {
	s.HttpStatusCode = &v
	return s
}

func (s *HandleAIEngineMessageResponseBody) SetMessage(v string) *HandleAIEngineMessageResponseBody {
	s.Message = &v
	return s
}

func (s *HandleAIEngineMessageResponseBody) SetRequestId(v string) *HandleAIEngineMessageResponseBody {
	s.RequestId = &v
	return s
}

func (s *HandleAIEngineMessageResponseBody) SetSuccess(v bool) *HandleAIEngineMessageResponseBody {
	s.Success = &v
	return s
}

func (s *HandleAIEngineMessageResponseBody) Validate() error {
	return dara.Validate(s)
}
