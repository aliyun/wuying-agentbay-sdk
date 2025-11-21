// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iPauseSessionAsyncRequest interface {
	dara.Model
	String() string
	GoString() string
	SetAuthorization(v string) *PauseSessionAsyncRequest
	GetAuthorization() *string
	SetSessionId(v string) *PauseSessionAsyncRequest
	GetSessionId() *string
}

type PauseSessionAsyncRequest struct {
	Authorization *string `json:"Authorization,omitempty" xml:"Authorization,omitempty"`
	SessionId     *string `json:"SessionId,omitempty" xml:"SessionId,omitempty"`
}

func (s PauseSessionAsyncRequest) String() string {
	return dara.Prettify(s)
}

func (s PauseSessionAsyncRequest) GoString() string {
	return s.String()
}

func (s *PauseSessionAsyncRequest) GetAuthorization() *string {
	return s.Authorization
}

func (s *PauseSessionAsyncRequest) GetSessionId() *string {
	return s.SessionId
}

func (s *PauseSessionAsyncRequest) SetAuthorization(v string) *PauseSessionAsyncRequest {
	s.Authorization = &v
	return s
}

func (s *PauseSessionAsyncRequest) SetSessionId(v string) *PauseSessionAsyncRequest {
	s.SessionId = &v
	return s
}

func (s *PauseSessionAsyncRequest) Validate() error {
	return dara.Validate(s)
}