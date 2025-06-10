# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel


class ListSessionResponseBodyData(DaraModel):
    def __init__(
        self,
        session_id: str = None,
    ):
        self.session_id = session_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.session_id is not None:
            result["SessionId"] = self.session_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get("SessionId") is not None:
            self.session_id = m.get("SessionId")

        return self
