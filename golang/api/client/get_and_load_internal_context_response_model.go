// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iGetAndLoadInternalContextResponse interface {
	dara.Model
	String() string
	GoString() string
	SetHeaders(v map[string]*string) *GetAndLoadInternalContextResponse
	GetHeaders() map[string]*string
	SetStatusCode(v int32) *GetAndLoadInternalContextResponse
	GetStatusCode() *int32
	SetBody(v *GetAndLoadInternalContextResponseBody) *GetAndLoadInternalContextResponse
	GetBody() *GetAndLoadInternalContextResponseBody
}

type GetAndLoadInternalContextResponse struct {
	Headers    map[string]*string                     `json:"headers,omitempty" xml:"headers,omitempty"`
	StatusCode *int32                                 `json:"statusCode,omitempty" xml:"statusCode,omitempty"`
	Body       *GetAndLoadInternalContextResponseBody `json:"body,omitempty" xml:"body,omitempty"`
}

func (s GetAndLoadInternalContextResponse) String() string {
	return dara.Prettify(s)
}

func (s GetAndLoadInternalContextResponse) GoString() string {
	return s.String()
}

func (s *GetAndLoadInternalContextResponse) GetHeaders() map[string]*string {
	return s.Headers
}

func (s *GetAndLoadInternalContextResponse) GetStatusCode() *int32 {
	return s.StatusCode
}

func (s *GetAndLoadInternalContextResponse) GetBody() *GetAndLoadInternalContextResponseBody {
	return s.Body
}

func (s *GetAndLoadInternalContextResponse) SetHeaders(v map[string]*string) *GetAndLoadInternalContextResponse {
	s.Headers = v
	return s
}

func (s *GetAndLoadInternalContextResponse) SetStatusCode(v int32) *GetAndLoadInternalContextResponse {
	s.StatusCode = &v
	return s
}

func (s *GetAndLoadInternalContextResponse) SetBody(v *GetAndLoadInternalContextResponseBody) *GetAndLoadInternalContextResponse {
	s.Body = v
	return s
}

func (s *GetAndLoadInternalContextResponse) Validate() error {
	if s.Body != nil {
		if err := s.Body.Validate(); err != nil {
			return err
		}
	}
	return nil
}
