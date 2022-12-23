from typing import Any, Dict, Tuple
class Mathf:
    '''
    with many math function
    '''
    @classmethod
    def decimal_part(cls, num : float) -> float :
        '''
        @brief  :   get num's decimal part
        @para   :
            num     :   num to get
        @ret    :   num's decimal part
        '''
        return num - int(num)



    @classmethod
    def float_10x_to_int(cls, num, accuracy : float) -> Tuple[int, int]:
        '''
        @brief  :   10x num untill num cast to integer with error less than accurcy
        @para   :
            num     :   num to cast
            accuracy:   accuracy
        @ret    :   10x-ed num and 10x-ed time
        '''
        _10xtime : int = 0
        while (cls.decimal_part(num) / num) > accuracy :
            _10xtime += 1
            num *= 10
        return int(num), _10xtime

    @classmethod
    def to_float(cls, s : str) -> float:
        ret = 0.
        try :
            ret = float(s)
        except:
            pass
        return ret

    @classmethod
    def to_int(cls, s : str) -> int:
        ret : int = 0
        try :
            ret = int(s)
        except:
            pass
        return ret

    @classmethod
    def key_of_value(cls, value : Any, dict : Dict[Any, Any]) -> Any:
        for k, v in dict.items():
            if v == value:
                return k

    @classmethod
    def large_num_split(cls, large_num : float) -> Tuple[float, int]:
        num_str = '{:e}'.format(large_num)
        dec, exp = '', ''
        flag = False
        for i in range(len(num_str)):
            if num_str[i] == 'e':
                flag = True
                continue
            if not flag:
                dec += num_str[i]
            else :
                exp += num_str[i]
        return cls.to_float(dec), cls.to_int(exp)

    @classmethod
    def clamp(cls, num : Any, min : float, max : float):
        if num < min :
            num = min
        elif num > max:
            num = max
        return num