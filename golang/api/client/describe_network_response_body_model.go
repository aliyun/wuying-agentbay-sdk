// This file is auto-generated, don't edit it. Thanks.
package client

import (
	"github.com/alibabacloud-go/tea/dara"
)

type DescribeNetworkResponseBodyData struct {
	Online *bool `json:"Online,omitempty" xml:"Online,omitempty"`
}

func (s DescribeNetworkResponseBodyData) String() string {
	return dara.Prettify(s)
}

func (s DescribeNetworkResponseBodyData) GoString() string {
	return s.String()
}

func (s *DescribeNetworkResponseBodyData) SetOnline(v bool) *DescribeNetworkResponseBodyData {
	s.Online = &v
	return s
}

type DescribeNetworkResponseBody struct {
	Code      *string                          `json:"Code,omitempty" xml:"Code,omitempty"`
	Data      *DescribeNetworkResponseBodyData `json:"Data,omitempty" xml:"Data,omitempty"`
	Message   *string                          `json:"Message,omitempty" xml:"Message,omitempty"`
	RequestId *string                          `json:"RequestId,omitempty" xml:"RequestId,omitempty"`
	Success   *bool                            `json:"Success,omitempty" xml:"Success,omitempty"`
}

func (s DescribeNetworkResponseBody) String() string {
	return dara.Prettify(s)
}

func (s DescribeNetworkResponseBody) GoString() string {
	return s.String()
}

func (s *DescribeNetworkResponseBody) SetCode(v string) *DescribeNetworkResponseBody {
	s.Code = &v
	return s
}

func (s *DescribeNetworkResponseBody) SetData(v *DescribeNetworkResponseBodyData) *DescribeNetworkResponseBody {
	s.Data = v
	return s
}

func (s *DescribeNetworkResponseBody) SetMessage(v string) *DescribeNetworkResponseBody {
	s.Message = &v
	return s
}

func (s *DescribeNetworkResponseBody) SetRequestId(v string) *DescribeNetworkResponseBody {
	s.RequestId = &v
	return s
}

func (s *DescribeNetworkResponseBody) SetSuccess(v bool) *DescribeNetworkResponseBody {
	s.Success = &v
	return s
}
