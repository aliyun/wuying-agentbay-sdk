# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations
from typing import Optional
from darabonba.model import DaraModel


class CreateNetworkResponseBodyData:
    def __init__(
        self,
        network_id: Optional[str] = None,
        network_token: Optional[str] = None,
    ):
        self.network_id = network_id
        self.network_token = network_token

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        if self.network_id is not None:
            result['NetworkId'] = self.network_id
        if self.network_token is not None:
            result['NetworkToken'] = self.network_token
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NetworkId') is not None:
            self.network_id = m.get('NetworkId')
        if m.get('NetworkToken') is not None:
            self.network_token = m.get('NetworkToken')
        return self


class CreateNetworkResponseBody(DaraModel):
    def __init__(
        self,
        request_id: Optional[str] = None,
        success: Optional[bool] = None,
        data: Optional[CreateNetworkResponseBodyData] = None,
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
            temp_model = CreateNetworkResponseBodyData()
            self.data = temp_model.from_map(m.get('Data'))
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Message') is not None:
            self.message = m.get('Message')
        return self
