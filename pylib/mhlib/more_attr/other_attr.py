from __future__ import annotations
from typing import Any
from mhlib.mathf import Mathf
from mhlib.more_attr.attr_main import AttrMain

class CmpAttr(AttrMain):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delta_value : float    = 0.

        if 'delta_value' in kwargs.keys():
            self.set_delta(kwargs['delta_value'])

    def set_delta(self, delta : Any):
        self.delta_value = Mathf.to_float(delta)