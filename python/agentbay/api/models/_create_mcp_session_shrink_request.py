# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations
from darabonba.model import DaraModel 


class CreateMcpSessionShrinkRequest(DaraModel):
    def __init__(
        self,
        authorization: str = None,
        context_id: str = None,
        external_user_id: str = None,
        image_id: str = None,
        labels: str = None,
        persistence_data_list_shrink: str = None,
        session_id: str = None,
    ):
        self.authorization = authorization
        self.context_id = context_id
        self.external_user_id = external_user_id
        self.image_id = image_id
        self.labels = labels
        self.persistence_data_list_shrink = persistence_data_list_shrink
        self.session_id = session_id

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.authorization is not None:
            result['Authorization'] = self.authorization

        if self.context_id is not None:
            result['ContextId'] = self.context_id

        if self.external_user_id is not None:
            result['ExternalUserId'] = self.external_user_id

        if self.image_id is not None:
            result['ImageId'] = self.image_id

        if self.labels is not None:
            result['Labels'] = self.labels

        if self.persistence_data_list_shrink is not None:
            result['PersistenceDataList'] = self.persistence_data_list_shrink

        if self.session_id is not None:
            result['SessionId'] = self.session_id

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Authorization') is not None:
            self.authorization = m.get('Authorization')

        if m.get('ContextId') is not None:
            self.context_id = m.get('ContextId')

        if m.get('ExternalUserId') is not None:
            self.external_user_id = m.get('ExternalUserId')

        if m.get('ImageId') is not None:
            self.image_id = m.get('ImageId')

        if m.get('Labels') is not None:
            self.labels = m.get('Labels')

        if m.get('PersistenceDataList') is not None:
            self.persistence_data_list_shrink = m.get('PersistenceDataList')

        if m.get('SessionId') is not None:
            self.session_id = m.get('SessionId')

        return self

