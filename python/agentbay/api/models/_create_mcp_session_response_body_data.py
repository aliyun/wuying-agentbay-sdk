# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel


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
            result["AppInstanceId"] = self.app_instance_id

        if self.err_msg is not None:
            result["ErrMsg"] = self.err_msg

        if self.resource_id is not None:
            result["ResourceId"] = self.resource_id

        if self.resource_url is not None:
            result["ResourceUrl"] = self.resource_url

        if self.session_id is not None:
            result["SessionId"] = self.session_id

        if self.success is not None:
            result["Success"] = self.success

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get("AppInstanceId") is not None:
            self.app_instance_id = m.get("AppInstanceId")

        if m.get("ErrMsg") is not None:
            self.err_msg = m.get("ErrMsg")

        if m.get("ResourceId") is not None:
            self.resource_id = m.get("ResourceId")

        if m.get("ResourceUrl") is not None:
            self.resource_url = m.get("ResourceUrl")

        if m.get("SessionId") is not None:
            self.session_id = m.get("SessionId")

        if m.get("Success") is not None:
            self.success = m.get("Success")

        return self
