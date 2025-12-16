// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iDeleteSessionAsyncResponseBody interface {
	dara.Model
	String() string
	GoString() string
	SetCode(v string) *DeleteSessionAsyncResponseBody
	GetCode() *string
	SetHttpStatusCode(v int32) *DeleteSessionAsyncResponseBody
	GetHttpStatusCode() *int32
	SetMessage(v string) *DeleteSessionAsyncResponseBody
	GetMessage() *string
	SetRequestId(v string) *DeleteSessionAsyncResponseBody
	GetRequestId() *string
	SetSuccess(v bool) *DeleteSessionAsyncResponseBody
	GetSuccess() *bool
}

type DeleteSessionAsyncResponseBody struct {
	Code           *string `json:"Code,omitempty" xml:"Code,omitempty"`
	HttpStatusCode *int32  `json:"HttpStatusCode,omitempty" xml:"HttpStatusCode,omitempty"`
	Message        *string `json:"Message,omitempty" xml:"Message,omitempty"`
	RequestId      *string `json:"RequestId,omitempty" xml:"RequestId,omitempty"`
	Success        *bool   `json:"Success,omitempty" xml:"Success,omitempty"`
}

func (s DeleteSessionAsyncResponseBody) String() string {
	return dara.Prettify(s)
}

func (s DeleteSessionAsyncResponseBody) GoString() string {
	return s.String()
}

func (s *DeleteSessionAsyncResponseBody) GetCode() *string {
	return s.Code
}

func (s *DeleteSessionAsyncResponseBody) GetHttpStatusCode() *int32 {
	return s.HttpStatusCode
}

func (s *DeleteSessionAsyncResponseBody) GetMessage() *string {
	return s.Message
}

func (s *DeleteSessionAsyncResponseBody) GetRequestId() *string {
	return s.RequestId
}

func (s *DeleteSessionAsyncResponseBody) GetSuccess() *bool {
	return s.Success
}

func (s *DeleteSessionAsyncResponseBody) SetCode(v string) *DeleteSessionAsyncResponseBody {
	s.Code = &v
	return s
}

func (s *DeleteSessionAsyncResponseBody) SetHttpStatusCode(v int32) *DeleteSessionAsyncResponseBody {
	s.HttpStatusCode = &v
	return s
}

func (s *DeleteSessionAsyncResponseBody) SetMessage(v string) *DeleteSessionAsyncResponseBody {
	s.Message = &v
	return s
}

func (s *DeleteSessionAsyncResponseBody) SetRequestId(v string) *DeleteSessionAsyncResponseBody {
	s.RequestId = &v
	return s
}

func (s *DeleteSessionAsyncResponseBody) SetSuccess(v bool) *DeleteSessionAsyncResponseBody {
	s.Success = &v
	return s
}

func (s *DeleteSessionAsyncResponseBody) Validate() error {
	return dara.Validate(s)
}
