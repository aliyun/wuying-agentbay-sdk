# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations
from typing import Optional
from darabonba.model import DaraModel


class DescribeNetworkResponseBodyData:
    def __init__(
        self,
        online: Optional[bool] = None,
    ):
        self.online = online

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.online is not None:
            result['Online'] = self.online
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Online') is not None:
            self.online = m.get('Online')
        return self


class DescribeNetworkResponseBody(DaraModel):
    def __init__(
        self,
        request_id: Optional[str] = None,
        success: Optional[bool] = None,
        data: Optional[DescribeNetworkResponseBodyData] = None,
        code: Optional[str] = None,
        message: Optional[str] = None,
    ):
        self.request_id = request_id
        self.success = success
        self.data = data
        self.code = code
        self.message = message

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.code is not None:
            result['Code'] = self.code
        if self.message is not None:
            result['Message'] = self.message
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Data') is not None:
            temp_model = DescribeNetworkResponseBodyData()
            self.data = temp_model.from_map(m.get('Data'))
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        return self
