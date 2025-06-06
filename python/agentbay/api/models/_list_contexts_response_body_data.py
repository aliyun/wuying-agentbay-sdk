# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel


class ListContextsResponseBodyData(DaraModel):
    def __init__(
        self,
        create_time: str = None,
        id: str = None,
        last_used_time: str = None,
        name: str = None,
        os_type: str = None,
        state: str = None,
    ):
        self.create_time = create_time
        self.id = id
        self.last_used_time = last_used_time
        self.name = name
        self.os_type = os_type
        self.state = state

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.create_time is not None:
            result["CreateTime"] = self.create_time

        if self.id is not None:
            result["Id"] = self.id

        if self.last_used_time is not None:
            result["LastUsedTime"] = self.last_used_time

        if self.name is not None:
            result["Name"] = self.name

        if self.os_type is not None:
            result["OsType"] = self.os_type

        if self.state is not None:
            result["State"] = self.state

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get("CreateTime") is not None:
            self.create_time = m.get("CreateTime")

        if m.get("Id") is not None:
            self.id = m.get("Id")

        if m.get("LastUsedTime") is not None:
            self.last_used_time = m.get("LastUsedTime")

        if m.get("Name") is not None:
            self.name = m.get("Name")

        if m.get("OsType") is not None:
            self.os_type = m.get("OsType")

        if m.get("State") is not None:
            self.state = m.get("State")

        return self
