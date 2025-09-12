// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type CreateNetworkResponseBodyData struct {
	NetworkId    *string `json:"NetworkId,omitempty" xml:"NetworkId,omitempty"`
	NetworkToken *string `json:"NetworkToken,omitempty" xml:"NetworkToken,omitempty"`
}

func (s CreateNetworkResponseBodyData) String() string {
	return dara.Prettify(s)
}

func (s CreateNetworkResponseBodyData) GoString() string {
	return s.String()
}

func (s *CreateNetworkResponseBodyData) SetNetworkId(v string) *CreateNetworkResponseBodyData {
	s.NetworkId = &v
	return s
}

func (s *CreateNetworkResponseBodyData) SetNetworkToken(v string) *CreateNetworkResponseBodyData {
	s.NetworkToken = &v
	return s
}

type CreateNetworkResponseBody struct {
	Code      *string                        `json:"Code,omitempty" xml:"Code,omitempty"`
	Data      *CreateNetworkResponseBodyData `json:"Data,omitempty" xml:"Data,omitempty"`
	Message   *string                        `json:"Message,omitempty" xml:"Message,omitempty"`
	RequestId *string                        `json:"RequestId,omitempty" xml:"RequestId,omitempty"`
	Success   *bool                          `json:"Success,omitempty" xml:"Success,omitempty"`
}

func (s CreateNetworkResponseBody) String() string {
	return dara.Prettify(s)
}

func (s CreateNetworkResponseBody) GoString() string {
	return s.String()
}

func (s *CreateNetworkResponseBody) SetCode(v string) *CreateNetworkResponseBody {
	s.Code = &v
	return s
}

func (s *CreateNetworkResponseBody) SetData(v *CreateNetworkResponseBodyData) *CreateNetworkResponseBody {
	s.Data = v
	return s
}

func (s *CreateNetworkResponseBody) SetMessage(v string) *CreateNetworkResponseBody {
	s.Message = &v
	return s
}

func (s *CreateNetworkResponseBody) SetRequestId(v string) *CreateNetworkResponseBody {
	s.RequestId = &v
	return s
}

func (s *CreateNetworkResponseBody) SetSuccess(v bool) *CreateNetworkResponseBody {
	s.Success = &v
	return s
}
