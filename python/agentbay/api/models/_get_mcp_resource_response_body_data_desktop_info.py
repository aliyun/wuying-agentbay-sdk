# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel


class GetMcpResourceResponseBodyDataDesktopInfo(DaraModel):
    def __init__(
        self,
        app_id: str = None,
        auth_code: str = None,
        connection_properties: str = None,
        resource_id: str = None,
        resource_type: str = None,
    ):
        self.app_id = app_id
        self.auth_code = auth_code
        self.connection_properties = connection_properties
        self.resource_id = resource_id
        self.resource_type = resource_type

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.app_id is not None:
            result["AppId"] = self.app_id

        if self.auth_code is not None:
            result["AuthCode"] = self.auth_code

        if self.connection_properties is not None:
            result["ConnectionProperties"] = self.connection_properties

        if self.resource_id is not None:
            result["ResourceId"] = self.resource_id

        if self.resource_type is not None:
            result["ResourceType"] = self.resource_type

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get("AppId") is not None:
            self.app_id = m.get("AppId")

        if m.get("AuthCode") is not None:
            self.auth_code = m.get("AuthCode")

        if m.get("ConnectionProperties") is not None:
            self.connection_properties = m.get("ConnectionProperties")

        if m.get("ResourceId") is not None:
            self.resource_id = m.get("ResourceId")

        if m.get("ResourceType") is not None:
            self.resource_type = m.get("ResourceType")

        return self
