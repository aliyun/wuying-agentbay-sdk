// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iPauseSessionAsyncResponse interface {
	dara.Model
	String() string
	GoString() string
	SetHeaders(v map[string]*string) *PauseSessionAsyncResponse
	GetHeaders() map[string]*string
	SetStatusCode(v int32) *PauseSessionAsyncResponse
	GetStatusCode() *int32
	SetBody(v *PauseSessionAsyncResponseBody) *PauseSessionAsyncResponse
	GetBody() *PauseSessionAsyncResponseBody
}

type PauseSessionAsyncResponse struct {
	Headers    map[string]*string             `json:"headers,omitempty" xml:"headers,omitempty"`
	StatusCode *int32                         `json:"statusCode,omitempty" xml:"statusCode,omitempty"`
	Body       *PauseSessionAsyncResponseBody `json:"body,omitempty" xml:"body,omitempty"`
}

func (s PauseSessionAsyncResponse) String() string {
	return dara.Prettify(s)
}

func (s PauseSessionAsyncResponse) GoString() string {
	return s.String()
}

func (s *PauseSessionAsyncResponse) GetHeaders() map[string]*string {
	return s.Headers
}

func (s *PauseSessionAsyncResponse) GetStatusCode() *int32 {
	return s.StatusCode
}

func (s *PauseSessionAsyncResponse) GetBody() *PauseSessionAsyncResponseBody {
	return s.Body
}

func (s *PauseSessionAsyncResponse) SetHeaders(v map[string]*string) *PauseSessionAsyncResponse {
	s.Headers = v
	return s
}

func (s *PauseSessionAsyncResponse) SetStatusCode(v int32) *PauseSessionAsyncResponse {
	s.StatusCode = &v
	return s
}

func (s *PauseSessionAsyncResponse) SetBody(v *PauseSessionAsyncResponseBody) *PauseSessionAsyncResponse {
	s.Body = v
	return s
}

func (s *PauseSessionAsyncResponse) Validate() error {
	if s.Body != nil {
		if err := s.Body.Validate(); err != nil {
			return err
		}
	}
	return nil
}