// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iGetAndLoadInternalContextRequest interface {
	dara.Model
	String() string
	GoString() string
	SetAuthorization(v string) *GetAndLoadInternalContextRequest
	GetAuthorization() *string
	SetContextTypes(v []*string) *GetAndLoadInternalContextRequest
	GetContextTypes() []*string
	SetSessionId(v string) *GetAndLoadInternalContextRequest
	GetSessionId() *string
}

type GetAndLoadInternalContextRequest struct {
	Authorization *string   `json:"Authorization,omitempty" xml:"Authorization,omitempty"`
	ContextTypes  []*string `json:"ContextTypes,omitempty" xml:"ContextTypes,omitempty" type:"Repeated"`
	SessionId     *string   `json:"SessionId,omitempty" xml:"SessionId,omitempty"`
}

func (s GetAndLoadInternalContextRequest) String() string {
	return dara.Prettify(s)
}

func (s GetAndLoadInternalContextRequest) GoString() string {
	return s.String()
}

func (s *GetAndLoadInternalContextRequest) GetAuthorization() *string {
	return s.Authorization
}

func (s *GetAndLoadInternalContextRequest) GetContextTypes() []*string {
	return s.ContextTypes
}

func (s *GetAndLoadInternalContextRequest) GetSessionId() *string {
	return s.SessionId
}

func (s *GetAndLoadInternalContextRequest) SetAuthorization(v string) *GetAndLoadInternalContextRequest {
	s.Authorization = &v
	return s
}

func (s *GetAndLoadInternalContextRequest) SetContextTypes(v []*string) *GetAndLoadInternalContextRequest {
	s.ContextTypes = v
	return s
}

func (s *GetAndLoadInternalContextRequest) SetSessionId(v string) *GetAndLoadInternalContextRequest {
	s.SessionId = &v
	return s
}

func (s *GetAndLoadInternalContextRequest) Validate() error {
	return dara.Validate(s)
}
