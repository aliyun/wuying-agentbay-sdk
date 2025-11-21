// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iResumeSessionAsyncRequest interface {
	dara.Model
	String() string
	GoString() string
	SetAuthorization(v string) *ResumeSessionAsyncRequest
	GetAuthorization() *string
	SetSessionId(v string) *ResumeSessionAsyncRequest
	GetSessionId() *string
}

type ResumeSessionAsyncRequest struct {
	Authorization *string `json:"Authorization,omitempty" xml:"Authorization,omitempty"`
	SessionId     *string `json:"SessionId,omitempty" xml:"SessionId,omitempty"`
}

func (s ResumeSessionAsyncRequest) String() string {
	return dara.Prettify(s)
}

func (s ResumeSessionAsyncRequest) GoString() string {
	return s.String()
}

func (s *ResumeSessionAsyncRequest) GetAuthorization() *string {
	return s.Authorization
}

func (s *ResumeSessionAsyncRequest) GetSessionId() *string {
	return s.SessionId
}

func (s *ResumeSessionAsyncRequest) SetAuthorization(v string) *ResumeSessionAsyncRequest {
	s.Authorization = &v
	return s
}

func (s *ResumeSessionAsyncRequest) SetSessionId(v string) *ResumeSessionAsyncRequest {
	s.SessionId = &v
	return s
}

func (s *ResumeSessionAsyncRequest) Validate() error {
	return dara.Validate(s)
}