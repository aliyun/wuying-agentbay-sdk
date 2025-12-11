// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type iListContextsRequest interface {
	dara.Model
	String() string
	GoString() string
	SetAuthorization(v string) *ListContextsRequest
	GetAuthorization() *string
	SetMaxResults(v int32) *ListContextsRequest
	GetMaxResults() *int32
	SetNextToken(v string) *ListContextsRequest
	GetNextToken() *string
}

type ListContextsRequest struct {
	Authorization *string `json:"Authorization,omitempty" xml:"Authorization,omitempty"`
	MaxResults    *int32  `json:"MaxResults,omitempty" xml:"MaxResults,omitempty"`
	NextToken     *string `json:"NextToken,omitempty" xml:"NextToken,omitempty"`
	SessionId     *string `json:"SessionId,omitempty" xml:"SessionId,omitempty"`
	Type          *string `json:"ContextType,omitempty" xml:"ContextType,omitempty"`
}

func (s ListContextsRequest) String() string {
	return dara.Prettify(s)
}

func (s ListContextsRequest) GoString() string {
	return s.String()
}

func (s *ListContextsRequest) GetAuthorization() *string {
	return s.Authorization
}

func (s *ListContextsRequest) GetMaxResults() *int32 {
	return s.MaxResults
}

func (s *ListContextsRequest) GetNextToken() *string {
	return s.NextToken
}

func (s *ListContextsRequest) GetSessionId() *string {
	return s.SessionId
}

func (s *ListContextsRequest) GetType() *string {
	return s.Type
}

func (s *ListContextsRequest) SetAuthorization(v string) *ListContextsRequest {
	s.Authorization = &v
	return s
}

func (s *ListContextsRequest) SetMaxResults(v int32) *ListContextsRequest {
	s.MaxResults = &v
	return s
}

func (s *ListContextsRequest) SetNextToken(v string) *ListContextsRequest {
	s.NextToken = &v
	return s
}

func (s *ListContextsRequest) SetSessionId(v string) *ListContextsRequest {
	s.SessionId = &v
	return s
}

func (s *ListContextsRequest) SetType(v string) *ListContextsRequest {
	s.Type = &v
	return s
}

func (s *ListContextsRequest) Validate() error {
	return dara.Validate(s)
}
