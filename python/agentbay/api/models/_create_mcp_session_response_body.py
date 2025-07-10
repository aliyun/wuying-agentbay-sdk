# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations
from darabonba.model import DaraModel 
from agentbay.api import models as main_models 


class CreateMcpSessionResponseBody(DaraModel):
    def __init__(
        self,
        code: str = None,
        data: main_models.CreateMcpSessionResponseBodyData = None,
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
            temp_model = main_models.CreateMcpSessionResponseBodyData()
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

class CreateMcpSessionResponseBodyData(DaraModel):
    def __init__(
        self,
        app_instance_id: str = None,
        err_msg: str = None,
        resource_id: str = None,
        resource_url: str = None,
        session_id: str = None,
        success: bool = None,
    ):
        self.app_instance_id = app_instance_id
        self.err_msg = err_msg
        self.resource_id = resource_id
        self.resource_url = resource_url
        self.session_id = session_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.app_instance_id is not None:
            result['AppInstanceId'] = self.app_instance_id

        if self.err_msg is not None:
            result['ErrMsg'] = self.err_msg

        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id

        if self.resource_url is not None:
            result['ResourceUrl'] = self.resource_url

        if self.session_id is not None:
            result['SessionId'] = self.session_id

        if self.success is not None:
            result['Success'] = self.success

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AppInstanceId') is not None:
            self.app_instance_id = m.get('AppInstanceId')

        if m.get('ErrMsg') is not None:
            self.err_msg = m.get('ErrMsg')

        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')

        if m.get('ResourceUrl') is not None:
            self.resource_url = m.get('ResourceUrl')

        if m.get('SessionId') is not None:
            self.session_id = m.get('SessionId')

        if m.get('Success') is not None:
            self.success = m.get('Success')

        return self

