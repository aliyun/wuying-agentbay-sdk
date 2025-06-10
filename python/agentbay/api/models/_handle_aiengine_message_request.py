# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel


class HandleAIEngineMessageRequest(DaraModel):
    def __init__(
        self,
        data: str = None,
        msg_type: str = None,
        session_token: str = None,
    ):
        self.data = data
        self.msg_type = msg_type
        self.session_token = session_token

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.data is not None:
            result["Data"] = self.data

        if self.msg_type is not None:
            result["MsgType"] = self.msg_type

        if self.session_token is not None:
            result["SessionToken"] = self.session_token

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get("Data") is not None:
            self.data = m.get("Data")

        if m.get("MsgType") is not None:
            self.msg_type = m.get("MsgType")

        if m.get("SessionToken") is not None:
            self.session_token = m.get("SessionToken")

        return self
