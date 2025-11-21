// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iPauseSessionAsyncResponseBody interface {
	dara.Model
	String() string
	GoString() string
	SetCode(v string) *PauseSessionAsyncResponseBody
	GetCode() *string
	SetHttpStatusCode(v int32) *PauseSessionAsyncResponseBody
	GetHttpStatusCode() *int32
	SetMessage(v string) *PauseSessionAsyncResponseBody
	GetMessage() *string
	SetRequestId(v string) *PauseSessionAsyncResponseBody
	GetRequestId() *string
	SetSuccess(v bool) *PauseSessionAsyncResponseBody
	GetSuccess() *bool
}

type PauseSessionAsyncResponseBody struct {
	Code           *string `json:"Code,omitempty" xml:"Code,omitempty"`
	HttpStatusCode *int32  `json:"HttpStatusCode,omitempty" xml:"HttpStatusCode,omitempty"`
	Message        *string `json:"Message,omitempty" xml:"Message,omitempty"`
	RequestId      *string `json:"RequestId,omitempty" xml:"RequestId,omitempty"`
	Success        *bool   `json:"Success,omitempty" xml:"Success,omitempty"`
}

func (s PauseSessionAsyncResponseBody) String() string {
	return dara.Prettify(s)
}

func (s PauseSessionAsyncResponseBody) GoString() string {
	return s.String()
}

func (s *PauseSessionAsyncResponseBody) GetCode() *string {
	return s.Code
}

func (s *PauseSessionAsyncResponseBody) GetHttpStatusCode() *int32 {
	return s.HttpStatusCode
}

func (s *PauseSessionAsyncResponseBody) GetMessage() *string {
	return s.Message
}

func (s *PauseSessionAsyncResponseBody) GetRequestId() *string {
	return s.RequestId
}

func (s *PauseSessionAsyncResponseBody) GetSuccess() *bool {
	return s.Success
}

func (s *PauseSessionAsyncResponseBody) SetCode(v string) *PauseSessionAsyncResponseBody {
	s.Code = &v
	return s
}

func (s *PauseSessionAsyncResponseBody) SetHttpStatusCode(v int32) *PauseSessionAsyncResponseBody {
	s.HttpStatusCode = &v
	return s
}

func (s *PauseSessionAsyncResponseBody) SetMessage(v string) *PauseSessionAsyncResponseBody {
	s.Message = &v
	return s
}

func (s *PauseSessionAsyncResponseBody) SetRequestId(v string) *PauseSessionAsyncResponseBody {
	s.RequestId = &v
	return s
}

func (s *PauseSessionAsyncResponseBody) SetSuccess(v bool) *PauseSessionAsyncResponseBody {
	s.Success = &v
	return s
}

func (s *PauseSessionAsyncResponseBody) Validate() error {
	return dara.Validate(s)
}