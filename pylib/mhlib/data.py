import json
from typing import Dict
from mhlib import env
from mhlib.mathf import Mathf
import time

class Data:
    
    @classmethod
    def path(cls):
        return env.DATA_PATH
    
    @classmethod
    def get_data(cls) -> Dict[str, str]:
        with open(cls.path() + 'data.json', 'r', encoding='utf8') as f:
            jsons = f.read()
            json_dicts : Dict[str, str] = json.loads(jsons)

        f.close()

        return json_dicts

    @classmethod
    def set_data(cls, data_dicts : Dict[str, str]) :
        with open(cls.path() + 'data.json', 'w', encoding='utf8') as f:
            json.dump(data_dicts, f)

        f.close()

    @classmethod
    def page_view_add(cls):
        page_view = Mathf.to_int(cls.get_data()['page_view'])
        cls.set_data({'page_view' : str(page_view + 1)})

    @classmethod
    def store_ip(cls, ip : str):
        with open(cls.path() + 'ip_data.txt', 'a+', encoding='utf-8') as f:
            f.write(time.strftime('[%Y-%m-%d  %H:%M:%S] ', time.localtime()))
            f.write(ip)
            f.write('\n')

    @classmethod
    def ip_filter(cls, isprint : bool = True):
        with open(cls.path() + 'ip_data.txt', 'r', encoding='utf-8') as f:
            while(True):
                line = f.readline()
                if(len(line) <= 3):
                    break
            