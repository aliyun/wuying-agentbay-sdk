# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

from agentbay.api import models as main_models


class GetMcpResourceResponseBodyData(DaraModel):
    def __init__(
        self,
        desktop_info: main_models.GetMcpResourceResponseBodyDataDesktopInfo = None,
        resource_url: str = None,
        session_id: str = None,
    ):
        self.desktop_info = desktop_info
        self.resource_url = resource_url
        self.session_id = session_id

    def validate(self):
        if self.desktop_info:
            self.desktop_info.validate()

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.desktop_info is not None:
            result["DesktopInfo"] = self.desktop_info.to_map()

        if self.resource_url is not None:
            result["ResourceUrl"] = self.resource_url

        if self.session_id is not None:
            result["SessionId"] = self.session_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get("DesktopInfo") is not None:
            temp_model = main_models.GetMcpResourceResponseBodyDataDesktopInfo()
            self.desktop_info = temp_model.from_map(m.get("DesktopInfo"))

        if m.get("ResourceUrl") is not None:
            self.resource_url = m.get("ResourceUrl")

        if m.get("SessionId") is not None:
            self.session_id = m.get("SessionId")

        return self
