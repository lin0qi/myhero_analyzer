import json
from django.test import TestCase
from mhlib.attr import Attr, Attrs
from mhlib.coder import CodeLine, CodeBlock
from mhlib.func import Func
from mhlib.cacul_master import CaculMaster
from mhlib.mathf import Mathf
from mhlib.set import Set
from mhlib import env
from mhlib.data import Data
from mhlib.more_attr.other_attr import CmpAttr
from mhlib.more_attr.attr_main import AttrMain
import copy

cm = CaculMaster()
fs = Func()
# print(fs.func_str_dict['f_crit'])


# with open(Set.path(), encoding='utf8') as f:
#     jsons = f.read()
#     json_dicts = json.loads(jsons)

# for k, v in json_dicts['property'].items():
#     print('"{}": "{}",'.format(k, v['cn_name']))
Data.ip_filter()