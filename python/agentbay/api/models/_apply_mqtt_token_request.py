# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations
from darabonba.model import DaraModel


class ApplyMqttTokenRequest(DaraModel):
    def __init__(
        self,
        desktop_id: str = None,
        session_token: str = None,
    ):
        self.desktop_id = desktop_id
        self.session_token = session_token

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.desktop_id is not None:
            result["DesktopId"] = self.desktop_id

        if self.session_token is not None:
            result["SessionToken"] = self.session_token

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get("DesktopId") is not None:
            self.desktop_id = m.get("DesktopId")

        if m.get("SessionToken") is not None:
            self.session_token = m.get("SessionToken")

        return self
