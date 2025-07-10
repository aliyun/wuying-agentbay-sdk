# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations
from darabonba.model import DaraModel 
from agentbay.api import models as main_models 


class ApplyMqttTokenResponseBody(DaraModel):
    def __init__(
        self,
        code: str = None,
        data: main_models.ApplyMqttTokenResponseBodyData = None,
        http_status_code: int = None,
        message: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.data = data
        self.http_status_code = http_status_code
        self.message = message
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.code is not None:
            result['Code'] = self.code

        if self.data is not None:
            result['Data'] = self.data.to_map()

        if self.http_status_code is not None:
            result['HttpStatusCode'] = self.http_status_code

        if self.message is not None:
            result['Message'] = self.message

        if self.request_id is not None:
            result['RequestId'] = self.request_id

        if self.success is not None:
            result['Success'] = self.success

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')

        if m.get('Data') is not None:
            temp_model = main_models.ApplyMqttTokenResponseBodyData()
            self.data = temp_model.from_map(m.get('Data'))

        if m.get('HttpStatusCode') is not None:
            self.http_status_code = m.get('HttpStatusCode')

        if m.get('Message') is not None:
            self.message = m.get('Message')

        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')

        if m.get('Success') is not None:
            self.success = m.get('Success')

        return self



class ApplyMqttTokenResponseBodyData(DaraModel):
    def __init__(
        self,
        access_key_id: str = None,
        client_id: str = None,
        expiration: str = None,
        instance_id: str = None,
        region_id: str = None,
        security_token: str = None,
    ):
        self.access_key_id = access_key_id
        self.client_id = client_id
        self.expiration = expiration
        self.instance_id = instance_id
        self.region_id = region_id
        self.security_token = security_token

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.access_key_id is not None:
            result['AccessKeyId'] = self.access_key_id

        if self.client_id is not None:
            result['ClientId'] = self.client_id

        if self.expiration is not None:
            result['Expiration'] = self.expiration

        if self.instance_id is not None:
            result['InstanceId'] = self.instance_id

        if self.region_id is not None:
            result['RegionId'] = self.region_id

        if self.security_token is not None:
            result['SecurityToken'] = self.security_token

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccessKeyId') is not None:
            self.access_key_id = m.get('AccessKeyId')

        if m.get('ClientId') is not None:
            self.client_id = m.get('ClientId')

        if m.get('Expiration') is not None:
            self.expiration = m.get('Expiration')

        if m.get('InstanceId') is not None:
            self.instance_id = m.get('InstanceId')

        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')

        if m.get('SecurityToken') is not None:
            self.security_token = m.get('SecurityToken')

        return self

