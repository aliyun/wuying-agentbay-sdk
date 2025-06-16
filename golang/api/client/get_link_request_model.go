// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iGetLinkRequest interface {
	dara.Model
	String() string
	GoString() string
	SetAuthorization(v string) *GetLinkRequest
	GetAuthorization() *string
	SetSessionId(v string) *GetLinkRequest
	GetSessionId() *string
}

type GetLinkRequest struct {
	Authorization *string `json:"Authorization,omitempty" xml:"Authorization,omitempty"`
	SessionId     *string `json:"SessionId,omitempty" xml:"SessionId,omitempty"`
}

func (s GetLinkRequest) String() string {
	return dara.Prettify(s)
}

func (s GetLinkRequest) GoString() string {
	return s.String()
}

func (s *GetLinkRequest) GetAuthorization() *string {
	return s.Authorization
}

func (s *GetLinkRequest) GetSessionId() *string {
	return s.SessionId
}

func (s *GetLinkRequest) SetAuthorization(v string) *GetLinkRequest {
	s.Authorization = &v
	return s
}

func (s *GetLinkRequest) SetSessionId(v string) *GetLinkRequest {
	s.SessionId = &v
	return s
}

func (s *GetLinkRequest) Validate() error {
	return dara.Validate(s)
}
