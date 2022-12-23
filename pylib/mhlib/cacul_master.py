from __future__ import annotations
from typing import Any, Dict, List, Tuple

from more_attr.other_attr import CmpAttr
from mhlib.attr import Attrs, Attr
from mhlib.func import Func
from mhlib.mathf import Mathf

class CaculMaster:
    def __init__(self, *args, **kwargs) -> None:
        self.property       : Attrs                     = Attrs()
        self.fs             : Func                      = Func()
        self.is_print       : bool                      = False

        self.apf_result     : float                     = 1
        self.apf_dec        : float                     = 0
        self.apf_exp        : int                       = 0

        self.equal_atk_pwr  : Dict[str, Dict[str, Any]] = {}

        if 'property' in kwargs.keys():
            prpty : Attrs = kwargs['property']
            self.property = prpty.copy()
        else :
            self.property.init()

    def __getitem__(self, key : str) -> Attr:
        return self.property[key]
    
    def __setitem__(self, key : str, value : Attr) -> None:
        self.property[key] = value

    def copy(self) -> CaculMaster:
        return CaculMaster(property=self.property)

    def items(self):
        return self.property.items()

    def keys(self):
        return self.property.keys()

    def get_attr_func(self, attr : Attr):
        return self.fs[attr.apf_func_name]

    def get_apf(self) -> float:
        score = 1.
        family_black_list : List[str] = []
        families_ls : List[Attr] = []
        families_dict : Dict[str, Attr] = {}
        for k, v in self.property.items():
            family = v.family
            if family in family_black_list:
                continue
            elif family != 'none' :
                family_black_list.append(family)
            families_ls, families_dict = Attrs.get_families(k, v, self.property)
            paras_tp = Attrs.get_paras_from_families(families_ls)
            families_score = self.get_attr_func(v)(*paras_tp)
            
            if self.is_print:
                print('family name:{}'.format(families_ls[0].family))

                print('family member({}): '.format(len(families_ls)))
                for member in families_ls:
                    print('    key:{}, value:{}'.format(Attrs.key_of_value(member, families_dict), member))

                print('family score:{}'.format(families_score))

            score *= families_score

        return score
        
    def get_delta_apf(self, attr_name : str, delta_val : float = 1.) -> float:
        if(attr_name == 'damage_amplify'):
            return delta_val
        apf_old, apf_new = 0., 0.
        attr = self.property[attr_name]
        apf_func = self.get_attr_func(attr)
        apf_para = Attrs.get_paras_from_attr(attr, self.property)
        apf_old = apf_func(*apf_para)

        apf_para = list(apf_para)
        apf_para[Mathf.to_int(attr.func_pos) - 1] += Mathf.to_float(delta_val)
        apf_new = apf_func(*tuple(apf_para))

        apf_apf : float = round((apf_new / apf_old - 1) * 100., 3)

        if self.is_print:
            print('apf_old:{}, apf_new:{}'.format(apf_old, apf_new))
            print('apf_apf:{}'.format(apf_apf))
        
        return apf_apf

    def get_deltas_apf(self, deltas : Dict[str, float], equip=False):
        p_cpy = self.copy()
        apf_apf = 1.
        if not equip:
            for k, v in deltas.items():
                p_cpy.property[k].value += Mathf.to_float(v)
            apf_apf = p_cpy.get_apf() / self.get_apf()
        else :
            for k, v in deltas.items():
                p_cpy.property[k].value -= Mathf.to_float(v)
            apf_apf = self.get_apf() / p_cpy.get_apf()
        return apf_apf

    def cacul_all_delta_apf(self):
        for k, v in self.property.items():
            self.property[k].apf_apf =  self.get_delta_apf(k ,v.delta)

    def cacul_delta_pct(self):
        for k, v in self.property.items():
            self.property[k].delta_pct_process1 = Mathf.clamp((v.apf_apf - 0 ) * 10 * 0.4 , 0, 50)
            self.property[k].delta_pct_process2 = Mathf.clamp((v.apf_apf - 10) * 10 * 0.2 , 0, 25)
            self.property[k].delta_pct_process3 = Mathf.clamp((v.apf_apf - 20) * 10 * 0.15, 0, 15)
            self.property[k].delta_pct_process4 = Mathf.clamp((v.apf_apf - 40) * 10 * 0.05, 0, 10)

    def cacul_std_pct(self):
        pass

    def base_cacul(self):
        self.cacul_all_delta_apf()
        self.cacul_delta_pct()
        self.cacul_std_pct()

        self.apf_result = self.get_apf()
        self.apf_dec, self.apf_exp = Mathf.large_num_split(self.apf_result)

        for k, v in self.property.normals_a.items():
            self.equal_atk_pwr[v['cn_name']] = {}
            self.equal_atk_pwr[v['cn_name']] ['atk_pwr_value'] = self.cacul_equal_atk_pwr(k, Mathf.to_float(v['value']))
            self.equal_atk_pwr[v['cn_name']] ['self_value'] = Mathf.to_float(v['value'])

    def cacul_equal_atk_pwr(self, attr_name : str, delta_val : float):
        return self.get_delta_apf(attr_name, delta_val) * (700 + self.property['attack_power'].value) / 100.

    def cmp_l_r(self, left_dict : Dict[str, CmpAttr], right_dict : Dict[str, CmpAttr]):
        v_dict_l, v_dict_r = {}, {}
        for k, v in left_dict.items():
            v_dict_l[k] = v.delta_value
        for k, v in right_dict.items():
            v_dict_r[k] = v.delta_value
        return self.get_deltas_apf(v_dict_l), self.get_deltas_apf(v_dict_r)
