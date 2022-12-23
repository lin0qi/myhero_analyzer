from __future__ import annotations
from typing import Any, Dict, List, Mapping, Tuple
from django.http.request import HttpRequest
from more_attr.other_attr import CmpAttr
from mhlib.attr import Attrs, Attr
from mhlib.func import Func
from mhlib.mathf import Mathf
from mhlib.cacul_master import CaculMaster

class MhResp:
    def __init__(self, request : HttpRequest, *args, **kwargs):
        self.cm         :   CaculMaster         = CaculMaster()
        self.cookie_dict:   Dict[str, str]      = {}
        self.cookie_time:   int                 = 60 * 60 * 12
        self.render_map :   Mapping[str, Any]  = {}

        self.init(request)

        if 'request' in kwargs.keys():
            self.init(kwargs['request'])

    def __getitem__(self, key : str) -> Attr:
        return self.cm[key]
    
    def __setitem__(self, key : str, value : Attr) -> None:
        self.cm[key] = value

    def items(self):
        return self.cm.items()

    def keys(self):
        return self.cm.keys()

    def init_cm(self, request : HttpRequest):
        post_form = request.POST['post_form']
        if post_form == 'none':
            for name in self.keys(): 
                self[name].set_val(request.POST[name])
        elif post_form == 'analyzer':
            for name in self.keys():
                self[name].set_val(request.POST[name])
                self[name].set_delta(request.POST[name + '_delta'])
        elif post_form == 'comparer':
            for name in self.keys():
                self[name].set_val(request.COOKIES[name])

    def set_cookie(self, request : HttpRequest):
        post_form = request.POST['post_form']
        if post_form == 'none':
            pass
        if post_form == 'analyzer':
            for k, v in self.items():
                self.cookie_dict[k] = v.value
        elif post_form == 'comparer':
            for k, v in self.items():
                self.cookie_dict[k] = v.value
    def set_render_map(self, request : HttpRequest):
        post_form = request.POST['post_form']
        if post_form == 'none':
            self.render_map = {
                'p_dict' : self.cm.property,
            }
        elif post_form == 'analyzer':
            self.render_map = {
                'p_dict'    : self.cm.property,
                'apf_dec'   : self.cm.apf_dec,
                'apf_exp'   : self.cm.apf_exp,
                'equal_dict': self.cm.equal_atk_pwr,
                'cur_page'  : 'analyzer'
            }
        elif post_form == 'comparer':
            dict_l, dict_r = {}, {}
            for k in request.POST.keys():
                if k[-2:] == '_l':
                    key_t = k[:-2]
                    dict_l[key_t] = CmpAttr(
                        cn_name=self.cm.property.name_convert_dict[key_t],
                        value=self.cm.property[key_t].value,
                        delta_value=request.POST[k])
                elif k[-2:] == '_r':
                    key_t = k[:-2]
                    dict_r[k[:-2]] = CmpAttr(
                        cn_name=self.cm.property.name_convert_dict[key_t],
                        value=self.cm.property[key_t].value,
                        delta_value=request.POST[k])
            l_apf, r_apf = self.cm.cmp_l_r(dict_l, dict_r)
            self.render_map = {
                'p_dict'        : self.cm.property,
                'apf_dec'       : self.cm.apf_dec,
                'apf_exp'       : self.cm.apf_exp,
                'equal_dict'    : self.cm.equal_atk_pwr,
                'cur_page'      : 'comparer',
                'cmp_apf_left'  : l_apf,
                'cmp_apf_right' : r_apf,
                'l_less_than_r' : l_apf < r_apf,
                'cmp_dict_l'    : dict_l,
                'cmp_dict_r'    : dict_r
            }

                
            

    def init(self, request : HttpRequest):
        if request.method == 'POST':
            self.init_cm(request)
            self.set_cookie(request)
            self.cm.base_cacul()
            self.set_render_map(request)
