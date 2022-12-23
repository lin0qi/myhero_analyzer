from __future__ import annotations
from typing import Any, Dict, List, Tuple
from mhlib.mathf import Mathf
from mhlib.attr import Attr

class AttrMain:
    def __init__(self, *args, **kwargs):
        self.cn_name    :   str     = ''
        self.value      :   float   = 0.

        if 'Attr' in kwargs.keys():
            a : Attr = kwargs['Attr']
            self.cn_name = a.cn_name
            self.value = a.value
        if 'cn_name' in kwargs.keys():
            self.cn_name = kwargs['cn_name']
        if 'value' in kwargs.keys():
            self.set_val(kwargs['value'])

    def set_val(self, val : Any):
        self.value = Mathf.to_float(val)

    def copy(self) -> AttrMain:
        return AttrMain(
            cn_name=self.cn_name,
            value=self.value
        )