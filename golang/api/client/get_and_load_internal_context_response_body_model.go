// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iGetAndLoadInternalContextResponseBody interface {
	dara.Model
	String() string
	GoString() string
	SetCode(v string) *GetAndLoadInternalContextResponseBody
	GetCode() *string
	SetData(v []*GetAndLoadInternalContextResponseBodyData) *GetAndLoadInternalContextResponseBody
	GetData() []*GetAndLoadInternalContextResponseBodyData
	SetHttpStatusCode(v int32) *GetAndLoadInternalContextResponseBody
	GetHttpStatusCode() *int32
	SetMessage(v string) *GetAndLoadInternalContextResponseBody
	GetMessage() *string
	SetRequestId(v string) *GetAndLoadInternalContextResponseBody
	GetRequestId() *string
	SetSuccess(v bool) *GetAndLoadInternalContextResponseBody
	GetSuccess() *bool
}

type GetAndLoadInternalContextResponseBody struct {
	Code           *string                                      `json:"Code,omitempty" xml:"Code,omitempty"`
	Data           []*GetAndLoadInternalContextResponseBodyData `json:"Data,omitempty" xml:"Data,omitempty" type:"Repeated"`
	HttpStatusCode *int32                                       `json:"HttpStatusCode,omitempty" xml:"HttpStatusCode,omitempty"`
	Message        *string                                      `json:"Message,omitempty" xml:"Message,omitempty"`
	RequestId      *string                                      `json:"RequestId,omitempty" xml:"RequestId,omitempty"`
	Success        *bool                                        `json:"Success,omitempty" xml:"Success,omitempty"`
}

func (s GetAndLoadInternalContextResponseBody) String() string {
	return dara.Prettify(s)
}

func (s GetAndLoadInternalContextResponseBody) GoString() string {
	return s.String()
}

func (s *GetAndLoadInternalContextResponseBody) GetCode() *string {
	return s.Code
}

func (s *GetAndLoadInternalContextResponseBody) GetData() []*GetAndLoadInternalContextResponseBodyData {
	return s.Data
}

func (s *GetAndLoadInternalContextResponseBody) GetHttpStatusCode() *int32 {
	return s.HttpStatusCode
}

func (s *GetAndLoadInternalContextResponseBody) GetMessage() *string {
	return s.Message
}

func (s *GetAndLoadInternalContextResponseBody) GetRequestId() *string {
	return s.RequestId
}

func (s *GetAndLoadInternalContextResponseBody) GetSuccess() *bool {
	return s.Success
}

func (s *GetAndLoadInternalContextResponseBody) SetCode(v string) *GetAndLoadInternalContextResponseBody {
	s.Code = &v
	return s
}

func (s *GetAndLoadInternalContextResponseBody) SetData(v []*GetAndLoadInternalContextResponseBodyData) *GetAndLoadInternalContextResponseBody {
	s.Data = v
	return s
}

func (s *GetAndLoadInternalContextResponseBody) SetHttpStatusCode(v int32) *GetAndLoadInternalContextResponseBody {
	s.HttpStatusCode = &v
	return s
}

func (s *GetAndLoadInternalContextResponseBody) SetMessage(v string) *GetAndLoadInternalContextResponseBody {
	s.Message = &v
	return s
}

func (s *GetAndLoadInternalContextResponseBody) SetRequestId(v string) *GetAndLoadInternalContextResponseBody {
	s.RequestId = &v
	return s
}

func (s *GetAndLoadInternalContextResponseBody) SetSuccess(v bool) *GetAndLoadInternalContextResponseBody {
	s.Success = &v
	return s
}

func (s *GetAndLoadInternalContextResponseBody) Validate() error {
	if s.Data != nil {
		for _, item := range s.Data {
			if item != nil {
				if err := item.Validate(); err != nil {
					return err
				}
			}
		}
	}
	return nil
}

type GetAndLoadInternalContextResponseBodyData struct {
	ContextId   *string `json:"ContextId,omitempty" xml:"ContextId,omitempty"`
	ContextPath *string `json:"ContextPath,omitempty" xml:"ContextPath,omitempty"`
	ContextType *string `json:"ContextType,omitempty" xml:"ContextType,omitempty"`
}

func (s GetAndLoadInternalContextResponseBodyData) String() string {
	return dara.Prettify(s)
}

func (s GetAndLoadInternalContextResponseBodyData) GoString() string {
	return s.String()
}

func (s *GetAndLoadInternalContextResponseBodyData) GetContextId() *string {
	return s.ContextId
}

func (s *GetAndLoadInternalContextResponseBodyData) GetContextPath() *string {
	return s.ContextPath
}

func (s *GetAndLoadInternalContextResponseBodyData) GetContextType() *string {
	return s.ContextType
}

func (s *GetAndLoadInternalContextResponseBodyData) SetContextId(v string) *GetAndLoadInternalContextResponseBodyData {
	s.ContextId = &v
	return s
}

func (s *GetAndLoadInternalContextResponseBodyData) SetContextPath(v string) *GetAndLoadInternalContextResponseBodyData {
	s.ContextPath = &v
	return s
}

func (s *GetAndLoadInternalContextResponseBodyData) SetContextType(v string) *GetAndLoadInternalContextResponseBodyData {
	s.ContextType = &v
	return s
}

func (s *GetAndLoadInternalContextResponseBodyData) Validate() error {
	return dara.Validate(s)
}
