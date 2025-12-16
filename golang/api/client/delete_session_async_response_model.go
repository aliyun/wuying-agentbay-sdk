// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iDeleteSessionAsyncResponse interface {
	dara.Model
	String() string
	GoString() string
	SetHeaders(v map[string]*string) *DeleteSessionAsyncResponse
	GetHeaders() map[string]*string
	SetStatusCode(v int32) *DeleteSessionAsyncResponse
	GetStatusCode() *int32
	SetBody(v *DeleteSessionAsyncResponseBody) *DeleteSessionAsyncResponse
	GetBody() *DeleteSessionAsyncResponseBody
}

type DeleteSessionAsyncResponse struct {
	Headers    map[string]*string              `json:"headers,omitempty" xml:"headers,omitempty"`
	StatusCode *int32                          `json:"statusCode,omitempty" xml:"statusCode,omitempty"`
	Body       *DeleteSessionAsyncResponseBody `json:"body,omitempty" xml:"body,omitempty"`
}

func (s DeleteSessionAsyncResponse) String() string {
	return dara.Prettify(s)
}

func (s DeleteSessionAsyncResponse) GoString() string {
	return s.String()
}

func (s *DeleteSessionAsyncResponse) GetHeaders() map[string]*string {
	return s.Headers
}

func (s *DeleteSessionAsyncResponse) GetStatusCode() *int32 {
	return s.StatusCode
}

func (s *DeleteSessionAsyncResponse) GetBody() *DeleteSessionAsyncResponseBody {
	return s.Body
}

func (s *DeleteSessionAsyncResponse) SetHeaders(v map[string]*string) *DeleteSessionAsyncResponse {
	s.Headers = v
	return s
}

func (s *DeleteSessionAsyncResponse) SetStatusCode(v int32) *DeleteSessionAsyncResponse {
	s.StatusCode = &v
	return s
}

func (s *DeleteSessionAsyncResponse) SetBody(v *DeleteSessionAsyncResponseBody) *DeleteSessionAsyncResponse {
	s.Body = v
	return s
}

func (s *DeleteSessionAsyncResponse) Validate() error {
	if s.Body != nil {
		if err := s.Body.Validate(); err != nil {
			return err
		}
	}
	return nil
}
