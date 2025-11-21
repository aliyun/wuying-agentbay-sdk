// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iResumeSessionAsyncResponse interface {
	dara.Model
	String() string
	GoString() string
	SetHeaders(v map[string]*string) *ResumeSessionAsyncResponse
	GetHeaders() map[string]*string
	SetStatusCode(v int32) *ResumeSessionAsyncResponse
	GetStatusCode() *int32
	SetBody(v *ResumeSessionAsyncResponseBody) *ResumeSessionAsyncResponse
	GetBody() *ResumeSessionAsyncResponseBody
}

type ResumeSessionAsyncResponse struct {
	Headers    map[string]*string              `json:"headers,omitempty" xml:"headers,omitempty"`
	StatusCode *int32                          `json:"statusCode,omitempty" xml:"statusCode,omitempty"`
	Body       *ResumeSessionAsyncResponseBody `json:"body,omitempty" xml:"body,omitempty"`
}

func (s ResumeSessionAsyncResponse) String() string {
	return dara.Prettify(s)
}

func (s ResumeSessionAsyncResponse) GoString() string {
	return s.String()
}

func (s *ResumeSessionAsyncResponse) GetHeaders() map[string]*string {
	return s.Headers
}

func (s *ResumeSessionAsyncResponse) GetStatusCode() *int32 {
	return s.StatusCode
}

func (s *ResumeSessionAsyncResponse) GetBody() *ResumeSessionAsyncResponseBody {
	return s.Body
}

func (s *ResumeSessionAsyncResponse) SetHeaders(v map[string]*string) *ResumeSessionAsyncResponse {
	s.Headers = v
	return s
}

func (s *ResumeSessionAsyncResponse) SetStatusCode(v int32) *ResumeSessionAsyncResponse {
	s.StatusCode = &v
	return s
}

func (s *ResumeSessionAsyncResponse) SetBody(v *ResumeSessionAsyncResponseBody) *ResumeSessionAsyncResponse {
	s.Body = v
	return s
}

func (s *ResumeSessionAsyncResponse) Validate() error {
	if s.Body != nil {
		if err := s.Body.Validate(); err != nil {
			return err
		}
	}
	return nil
}