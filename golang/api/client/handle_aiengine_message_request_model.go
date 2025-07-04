// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iHandleAIEngineMessageRequest interface {
	dara.Model
	String() string
	GoString() string
	SetData(v string) *HandleAIEngineMessageRequest
	GetData() *string
	SetMsgType(v string) *HandleAIEngineMessageRequest
	GetMsgType() *string
	SetSessionToken(v string) *HandleAIEngineMessageRequest
	GetSessionToken() *string
}

type HandleAIEngineMessageRequest struct {
	Data         *string `json:"Data,omitempty" xml:"Data,omitempty"`
	MsgType      *string `json:"MsgType,omitempty" xml:"MsgType,omitempty"`
	SessionToken *string `json:"SessionToken,omitempty" xml:"SessionToken,omitempty"`
}

func (s HandleAIEngineMessageRequest) String() string {
	return dara.Prettify(s)
}

func (s HandleAIEngineMessageRequest) GoString() string {
	return s.String()
}

func (s *HandleAIEngineMessageRequest) GetData() *string {
	return s.Data
}

func (s *HandleAIEngineMessageRequest) GetMsgType() *string {
	return s.MsgType
}

func (s *HandleAIEngineMessageRequest) GetSessionToken() *string {
	return s.SessionToken
}

func (s *HandleAIEngineMessageRequest) SetData(v string) *HandleAIEngineMessageRequest {
	s.Data = &v
	return s
}

func (s *HandleAIEngineMessageRequest) SetMsgType(v string) *HandleAIEngineMessageRequest {
	s.MsgType = &v
	return s
}

func (s *HandleAIEngineMessageRequest) SetSessionToken(v string) *HandleAIEngineMessageRequest {
	s.SessionToken = &v
	return s
}

func (s *HandleAIEngineMessageRequest) Validate() error {
	return dara.Validate(s)
}
