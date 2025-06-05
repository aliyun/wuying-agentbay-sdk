// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iCreateMcpSessionRequest interface {
	dara.Model
	String() string
	GoString() string
	SetAuthorization(v string) *CreateMcpSessionRequest
	GetAuthorization() *string
	SetContextId(v string) *CreateMcpSessionRequest
	GetContextId() *string
	SetExternalUserId(v string) *CreateMcpSessionRequest
	GetExternalUserId() *string
	SetLabels(v string) *CreateMcpSessionRequest
	GetLabels() *string
	SetSessionId(v string) *CreateMcpSessionRequest
	GetSessionId() *string
}

type CreateMcpSessionRequest struct {
	Authorization  *string `json:"Authorization,omitempty" xml:"Authorization,omitempty"`
	ContextId      *string `json:"ContextId,omitempty" xml:"ContextId,omitempty"`
	ExternalUserId *string `json:"ExternalUserId,omitempty" xml:"ExternalUserId,omitempty"`
	Labels         *string `json:"Labels,omitempty" xml:"Labels,omitempty"`
	SessionId      *string `json:"SessionId,omitempty" xml:"SessionId,omitempty"`
}

func (s CreateMcpSessionRequest) String() string {
	return dara.Prettify(s)
}

func (s CreateMcpSessionRequest) GoString() string {
	return s.String()
}

func (s *CreateMcpSessionRequest) GetAuthorization() *string {
	return s.Authorization
}

func (s *CreateMcpSessionRequest) GetContextId() *string {
	return s.ContextId
}

func (s *CreateMcpSessionRequest) GetExternalUserId() *string {
	return s.ExternalUserId
}

func (s *CreateMcpSessionRequest) GetLabels() *string {
	return s.Labels
}

func (s *CreateMcpSessionRequest) GetSessionId() *string {
	return s.SessionId
}

func (s *CreateMcpSessionRequest) SetAuthorization(v string) *CreateMcpSessionRequest {
	s.Authorization = &v
	return s
}

func (s *CreateMcpSessionRequest) SetContextId(v string) *CreateMcpSessionRequest {
	s.ContextId = &v
	return s
}

func (s *CreateMcpSessionRequest) SetExternalUserId(v string) *CreateMcpSessionRequest {
	s.ExternalUserId = &v
	return s
}

func (s *CreateMcpSessionRequest) SetLabels(v string) *CreateMcpSessionRequest {
	s.Labels = &v
	return s
}

func (s *CreateMcpSessionRequest) SetSessionId(v string) *CreateMcpSessionRequest {
	s.SessionId = &v
	return s
}

func (s *CreateMcpSessionRequest) Validate() error {
	return dara.Validate(s)
}
