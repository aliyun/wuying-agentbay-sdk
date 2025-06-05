// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iApplyMqttTokenRequest interface {
	dara.Model
	String() string
	GoString() string
	SetDesktopId(v string) *ApplyMqttTokenRequest
	GetDesktopId() *string
	SetSessionToken(v string) *ApplyMqttTokenRequest
	GetSessionToken() *string
}

type ApplyMqttTokenRequest struct {
	DesktopId    *string `json:"DesktopId,omitempty" xml:"DesktopId,omitempty"`
	SessionToken *string `json:"SessionToken,omitempty" xml:"SessionToken,omitempty"`
}

func (s ApplyMqttTokenRequest) String() string {
	return dara.Prettify(s)
}

func (s ApplyMqttTokenRequest) GoString() string {
	return s.String()
}

func (s *ApplyMqttTokenRequest) GetDesktopId() *string {
	return s.DesktopId
}

func (s *ApplyMqttTokenRequest) GetSessionToken() *string {
	return s.SessionToken
}

func (s *ApplyMqttTokenRequest) SetDesktopId(v string) *ApplyMqttTokenRequest {
	s.DesktopId = &v
	return s
}

func (s *ApplyMqttTokenRequest) SetSessionToken(v string) *ApplyMqttTokenRequest {
	s.SessionToken = &v
	return s
}

func (s *ApplyMqttTokenRequest) Validate() error {
	return dara.Validate(s)
}
