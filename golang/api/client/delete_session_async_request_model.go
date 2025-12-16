// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iDeleteSessionAsyncRequest interface {
	dara.Model
	String() string
	GoString() string
	SetAuthorization(v string) *DeleteSessionAsyncRequest
	GetAuthorization() *string
	SetSessionId(v string) *DeleteSessionAsyncRequest
	GetSessionId() *string
}

type DeleteSessionAsyncRequest struct {
	Authorization *string `json:"Authorization,omitempty" xml:"Authorization,omitempty"`
	SessionId     *string `json:"SessionId,omitempty" xml:"SessionId,omitempty"`
}

func (s DeleteSessionAsyncRequest) String() string {
	return dara.Prettify(s)
}

func (s DeleteSessionAsyncRequest) GoString() string {
	return s.String()
}

func (s *DeleteSessionAsyncRequest) GetAuthorization() *string {
	return s.Authorization
}

func (s *DeleteSessionAsyncRequest) GetSessionId() *string {
	return s.SessionId
}

func (s *DeleteSessionAsyncRequest) SetAuthorization(v string) *DeleteSessionAsyncRequest {
	s.Authorization = &v
	return s
}

func (s *DeleteSessionAsyncRequest) SetSessionId(v string) *DeleteSessionAsyncRequest {
	s.SessionId = &v
	return s
}

func (s *DeleteSessionAsyncRequest) Validate() error {
	return dara.Validate(s)
}
