from __future__ import annotations
import json
from typing import Any, Dict, List
from mhlib.mathf import Mathf
from mhlib import env

class Set:
    @classmethod
    def path(cls):
        return  env.SET_PATH

    @classmethod
    def read(cls) -> Dict[str, Dict[str, str]]:
        ret_dict : Dict[str, Dict[str, str]] = {}

        with open(cls.path(), encoding='utf8') as f:
            jsons = f.read()
            json_dicts : Dict[str, Dict[str, Dict[str, str]]] = json.loads(jsons)

        for k, v in json_dicts['property'].items():
            if v['tag'] != 'none':
                ret_dict[k] = v
                
        return ret_dict

    @classmethod
    def read_normal_property(cls) -> Dict[str, Dict[str, str]]:
        with open(cls.path(), encoding='utf-8') as f:
            jsons = f.read()
            json_dicts = json.loads(jsons)

        return json_dicts['normal_property']

    @classmethod
    def read_name_convert_dict(cls) -> Dict[str, str]:
        with open(cls.path(), encoding='utf-8') as f:
            return json.loads(f.read())['name_convert_dict']