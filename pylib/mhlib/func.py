from __future__ import annotations
import json
from typing import List, Dict, Any
from mhlib.coder import CodeLine, CodeBlock
from mhlib import env

class Func:
    def __init__(self):
        self.func_str_dict  :   Dict[str, str]      = {}
        self.func_dict      :   Dict[str, function] = {}

        self.read_set()
        self.set_dict()

    def __getitem__(self, k : str) -> function:
        return self.func_dict[k]

    @classmethod
    def path(cls):
        return env.FUNC_PATH

    @classmethod
    def read_func_from_kv(cls, k : str, v : Any) -> CodeBlock:
        func = CodeBlock()
        #function head
        func += CodeLine('def {}(*args):'.format(k), ex_retract=1)

        #define para
        for i in range(int(v['para']['num'])):
            para_name = v['para']['para{}'.format(i + 1)] #v['para']['parai']
            func += '{}=args[{}]'.format(para_name, i)

        #define variable
        for i in range(int(v['var']['num'])):
            var_name = v['var']['var{}'.format(i + 1)] #v['var']['vari']
            func += '{}=0'.format(var_name)
        
        #if info
        for i in range(int(v['if_info']['num'])):
            statement = v['if_info']['{}'.format(i + 1)]
            func += CodeLine('if {}:'.format(statement['if']), ex_retract=1)
            func += CodeLine(statement['then'], ex_retract=-1)

        #return
        func += 'return {}'.format(v['ret'])
        return func

    @classmethod
    def read_func_from_dict(cls, func_dict : Dict[str, Any]) -> CodeBlock:
        for k, v in func_dict.items():
            return cls.read_func_from_kv(k, v)

    @classmethod
    def read_func_from_json(cls, path : str) -> CodeBlock:
        with open(path, encoding='utf8') as f:
            jsons = f.read()
            func_dicts = json.loads(jsons)
        
        return cls.read_func_from_dict(func_dicts)

    def read_set(self):
        with open(self.path()) as f:
            jsons = f.read()
            func_dicts = json.loads(jsons)


        for k, v in func_dicts['functions'].items():
            func = Func.read_func_from_kv(k, v)
            self.func_str_dict[k] = func.__str__()
    
    def set_dict(self):
        for k, v in self.func_str_dict.items():
            exec(v)
            exec('self.func_dict["{}"]={}'.format(k, k))