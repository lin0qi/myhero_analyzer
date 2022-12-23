from __future__ import annotations
from typing import Any, Dict, List, Tuple
from mhlib.set import Set
from mhlib.mathf import Mathf

class Attr :
    def __init__(self, attr : Dict[str, str]):
        self.value              : float             = Mathf.to_float(attr['value'])
        self.tag                : str               = attr['tag']
        self.family             : str               = attr['family']
        self.apf_func_name      : str               = attr['apf_func_name']
        self.func_pos           : str               = attr['func_pos']
        self.cn_name            : str               = attr['cn_name']

        self.delta              : float             = 1.
        self.apf_apf            : float             = 0.
        self.delta_pct_process1 : int               = 0
        self.delta_pct_process2 : int               = 0
        self.delta_pct_process3 : int               = 0
        self.delta_pct_process4 : int               = 0
        self.std_pct_process    : int               = 0


    def __str__(self) -> str:
        return 'attr:{}\n\t|value:{}, tag:{}, family:{}, apf_func_name:{}, func_pos:{}|'.format(
                self.cn_name,
                self.value, 
                self.tag, 
                self.family,
                self.apf_func_name, 
                self.func_pos)

    def __eq__(self, other: Attr) -> bool:
        return self.value == other.value and self.tag == other.tag

    def set_val(self, val : Any):
        self.value = Mathf.to_float(val)

    def set_delta(self, delta : Any):
        self.delta = Mathf.to_float(delta)

    def copy(self) -> Attr:
        return Attr(attr={
            'value' : self.value,
            'tag' : self.tag,
            'family' : self.family,
            'apf_func_name' : self.apf_func_name,
            'func_pos' : self.func_pos,
            'cn_name' : self.cn_name
            })


class Attrs :
    def __init__(self, *args, **kwargs) :
        self.ATTR               : Dict[str, Attr]               = {}
        self.normals_a          : Dict[str, Dict[str, str]]     = {}

        self.name_convert_dict  : Dict[str, str]                = Set.read_name_convert_dict()
        '''
        init should be like this
        d = {'a' : Attr(), 'b' : Attr()}
        attrs = Attrs(ATTR=d)
        '''
        if 'ATTR' in kwargs.keys() :
            attr_dict : Dict[str, Attr] = kwargs['ATTR']
            for k, v in attr_dict.items():
                self[k] = v.copy()

        if 'json' in kwargs.keys() :
            if kwargs['json'] == 'inner':
                self.init()

    def __len__(self):
        return len(self.ATTR)

    def __eq__(self, other : Attrs) -> bool:
        return self.ATTR == other.ATTR

    def __ne__(self, other : Attrs) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        ret = ''
        for k, v in self.ATTR.items():
            ret += '--k:{}\n``v:{}\n'.format(k, v.__str__())
        return ret

    def __add__(self, other : Attrs) -> Attrs:
        return Attrs(ATTR=Attrs.ATTR_add(self.ATTR, other.ATTR))

    def __getitem__(self, key : str) -> Attr:
        return self.ATTR[key]
    
    def __setitem__(self, key : str, value : Attr) -> None:
        self.ATTR[key] = value

    def copy(self) -> Attrs:
        return Attrs(ATTR=self.ATTR)

    @classmethod
    def ATTR_add(cls, obj1 : Dict[str, Attr], obj2 : Dict[str, Attr]) -> Dict[str, Attr]:
        return {**obj1, **obj2}

    def init(self):
        property_dict = Set.read()
        self.set_property(property_dict)
        self.normals_a = Set.read_normal_property()


    def items(self):
        return self.ATTR.items()

    def keys(self):
        return self.ATTR.keys()


    def set_property(self, property_dict : Dict[str, Dict[str, str]]) -> None:
        for k, v in property_dict.items():
            self.ATTR[k] = Attr(v)

    
    @classmethod
    def get_families(cls, attr_key : str, attr : Attr, all_attrs : Attrs) -> Tuple[List[Attr], Dict[str, Attr]] :
        families_ls : List[Attr] = []
        families_dict : Dict[str, Attr] = {}
        if attr.family != 'none':
            for k, v in all_attrs.items():
                if v.family == attr.family:
                    families_ls.append(v)
                    families_dict[k] = v
        else :
            families_ls.append(attr)
            families_dict[attr_key] = attr
        return sorted(families_ls, key=lambda x : Mathf.to_int(x.func_pos)), families_dict

    @classmethod
    def get_paras_from_families(cls, families : List[Attr]) -> Tuple[float]:
        para_ret = []
        for member in families:
            para_ret.append(member.value)
        return tuple(para_ret)

    @classmethod
    def get_paras_from_attr(cls, attr : Attr, all_attrs : Attrs) -> Tuple[float]:
        return cls.get_paras_from_families(cls.get_families('none', attr, all_attrs)[0])

    @classmethod
    def key_of_value(cls, value : Attr, dict : Dict[str, Attr]) -> str:
        for k, v in dict.items():
            if v.func_pos == value.func_pos:
                return k