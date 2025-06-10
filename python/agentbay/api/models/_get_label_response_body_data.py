# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel


class GetLabelResponseBodyData(DaraModel):
    def __init__(
        self,
        labels: str = None,
    ):
        self.labels = labels

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.labels is not None:
            result["Labels"] = self.labels

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get("Labels") is not None:
            self.labels = m.get("Labels")

        return self
