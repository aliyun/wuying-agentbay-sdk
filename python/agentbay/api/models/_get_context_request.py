# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations
from darabonba.model import DaraModel


class GetContextRequest(DaraModel):
    def __init__(
        self,
        allow_create: bool = None,
        authorization: str = None,
        context_id: str = None,
        name: str = None,
    ):
        self.allow_create = allow_create
        self.authorization = authorization
        self.context_id = context_id
        self.name = name

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.allow_create is not None:
            result['AllowCreate'] = self.allow_create

        if self.authorization is not None:
            result['Authorization'] = self.authorization

        if self.name is not None:
            result['Name'] = self.name

        if self.context_id is not None:
            result['ContextId'] = self.context_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AllowCreate') is not None:
            self.allow_create = m.get('AllowCreate')

        if m.get('Authorization') is not None:
            self.authorization = m.get('Authorization')

        if m.get('ContextId') is not None:
            self.context_id = m.get('ContextId')

        if m.get('Name') is not None:
            self.name = m.get('Name')

        return self

