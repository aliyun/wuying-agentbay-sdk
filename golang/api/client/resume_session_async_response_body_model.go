// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iResumeSessionAsyncResponseBody interface {
	dara.Model
	String() string
	GoString() string
	SetCode(v string) *ResumeSessionAsyncResponseBody
	GetCode() *string
	SetHttpStatusCode(v int32) *ResumeSessionAsyncResponseBody
	GetHttpStatusCode() *int32
	SetMessage(v string) *ResumeSessionAsyncResponseBody
	GetMessage() *string
	SetRequestId(v string) *ResumeSessionAsyncResponseBody
	GetRequestId() *string
	SetSuccess(v bool) *ResumeSessionAsyncResponseBody
	GetSuccess() *bool
}

type ResumeSessionAsyncResponseBody struct {
	Code           *string `json:"Code,omitempty" xml:"Code,omitempty"`
	HttpStatusCode *int32  `json:"HttpStatusCode,omitempty" xml:"HttpStatusCode,omitempty"`
	Message        *string `json:"Message,omitempty" xml:"Message,omitempty"`
	RequestId      *string `json:"RequestId,omitempty" xml:"RequestId,omitempty"`
	Success        *bool   `json:"Success,omitempty" xml:"Success,omitempty"`
}

func (s ResumeSessionAsyncResponseBody) String() string {
	return dara.Prettify(s)
}

func (s ResumeSessionAsyncResponseBody) GoString() string {
	return s.String()
}

func (s *ResumeSessionAsyncResponseBody) GetCode() *string {
	return s.Code
}

func (s *ResumeSessionAsyncResponseBody) GetHttpStatusCode() *int32 {
	return s.HttpStatusCode
}

func (s *ResumeSessionAsyncResponseBody) GetMessage() *string {
	return s.Message
}

func (s *ResumeSessionAsyncResponseBody) GetRequestId() *string {
	return s.RequestId
}

func (s *ResumeSessionAsyncResponseBody) GetSuccess() *bool {
	return s.Success
}

func (s *ResumeSessionAsyncResponseBody) SetCode(v string) *ResumeSessionAsyncResponseBody {
	s.Code = &v
	return s
}

func (s *ResumeSessionAsyncResponseBody) SetHttpStatusCode(v int32) *ResumeSessionAsyncResponseBody {
	s.HttpStatusCode = &v
	return s
}

func (s *ResumeSessionAsyncResponseBody) SetMessage(v string) *ResumeSessionAsyncResponseBody {
	s.Message = &v
	return s
}

func (s *ResumeSessionAsyncResponseBody) SetRequestId(v string) *ResumeSessionAsyncResponseBody {
	s.RequestId = &v
	return s
}

func (s *ResumeSessionAsyncResponseBody) SetSuccess(v bool) *ResumeSessionAsyncResponseBody {
	s.Success = &v
	return s
}

func (s *ResumeSessionAsyncResponseBody) Validate() error {
	return dara.Validate(s)
}