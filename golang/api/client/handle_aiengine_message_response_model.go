// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iHandleAIEngineMessageResponse interface {
	dara.Model
	String() string
	GoString() string
	SetHeaders(v map[string]*string) *HandleAIEngineMessageResponse
	GetHeaders() map[string]*string
	SetStatusCode(v int32) *HandleAIEngineMessageResponse
	GetStatusCode() *int32
	SetBody(v *HandleAIEngineMessageResponseBody) *HandleAIEngineMessageResponse
	GetBody() *HandleAIEngineMessageResponseBody
}

type HandleAIEngineMessageResponse struct {
	Headers    map[string]*string                 `json:"headers,omitempty" xml:"headers,omitempty"`
	StatusCode *int32                             `json:"statusCode,omitempty" xml:"statusCode,omitempty"`
	Body       *HandleAIEngineMessageResponseBody `json:"body,omitempty" xml:"body,omitempty"`
}

func (s HandleAIEngineMessageResponse) String() string {
	return dara.Prettify(s)
}

func (s HandleAIEngineMessageResponse) GoString() string {
	return s.String()
}

func (s *HandleAIEngineMessageResponse) GetHeaders() map[string]*string {
	return s.Headers
}

func (s *HandleAIEngineMessageResponse) GetStatusCode() *int32 {
	return s.StatusCode
}

func (s *HandleAIEngineMessageResponse) GetBody() *HandleAIEngineMessageResponseBody {
	return s.Body
}

func (s *HandleAIEngineMessageResponse) SetHeaders(v map[string]*string) *HandleAIEngineMessageResponse {
	s.Headers = v
	return s
}

func (s *HandleAIEngineMessageResponse) SetStatusCode(v int32) *HandleAIEngineMessageResponse {
	s.StatusCode = &v
	return s
}

func (s *HandleAIEngineMessageResponse) SetBody(v *HandleAIEngineMessageResponseBody) *HandleAIEngineMessageResponse {
	s.Body = v
	return s
}

func (s *HandleAIEngineMessageResponse) Validate() error {
	return dara.Validate(s)
}
