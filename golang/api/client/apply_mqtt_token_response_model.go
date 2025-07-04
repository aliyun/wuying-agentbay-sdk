// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iApplyMqttTokenResponse interface {
	dara.Model
	String() string
	GoString() string
	SetHeaders(v map[string]*string) *ApplyMqttTokenResponse
	GetHeaders() map[string]*string
	SetStatusCode(v int32) *ApplyMqttTokenResponse
	GetStatusCode() *int32
	SetBody(v *ApplyMqttTokenResponseBody) *ApplyMqttTokenResponse
	GetBody() *ApplyMqttTokenResponseBody
}

type ApplyMqttTokenResponse struct {
	Headers    map[string]*string          `json:"headers,omitempty" xml:"headers,omitempty"`
	StatusCode *int32                      `json:"statusCode,omitempty" xml:"statusCode,omitempty"`
	Body       *ApplyMqttTokenResponseBody `json:"body,omitempty" xml:"body,omitempty"`
}

func (s ApplyMqttTokenResponse) String() string {
	return dara.Prettify(s)
}

func (s ApplyMqttTokenResponse) GoString() string {
	return s.String()
}

func (s *ApplyMqttTokenResponse) GetHeaders() map[string]*string {
	return s.Headers
}

func (s *ApplyMqttTokenResponse) GetStatusCode() *int32 {
	return s.StatusCode
}

func (s *ApplyMqttTokenResponse) GetBody() *ApplyMqttTokenResponseBody {
	return s.Body
}

func (s *ApplyMqttTokenResponse) SetHeaders(v map[string]*string) *ApplyMqttTokenResponse {
	s.Headers = v
	return s
}

func (s *ApplyMqttTokenResponse) SetStatusCode(v int32) *ApplyMqttTokenResponse {
	s.StatusCode = &v
	return s
}

func (s *ApplyMqttTokenResponse) SetBody(v *ApplyMqttTokenResponseBody) *ApplyMqttTokenResponse {
	s.Body = v
	return s
}

func (s *ApplyMqttTokenResponse) Validate() error {
	return dara.Validate(s)
}
