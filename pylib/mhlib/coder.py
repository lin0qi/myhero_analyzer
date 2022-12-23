from __future__ import annotations
from typing import List
import re

class CodeLine:
    def __init__(self, 
        code        :   str     = '', 
        linenum     :   int     = -1, 
        ex_retract  :   int     = 0, 
        tabsize     :   int     = 4
        ):
        self.code           : str   = code
        self.linenum        : int   = linenum
        self.ex_retract     : int   = ex_retract
        self.tabsize        : int   = tabsize

        self.retract        : int   = 0

    def __str__(self):
        return '{}{}\n'.format(
            ' ' * self.tabsize * self.retract, 
            self.code)

    def __eq__(self, other : str):
        return other.lower() == '__codeline__' or other.lower() == '__cl__'

    def have_func(self):
        return re.search(r'[a-zA-Z_]+[\w]*\([\w]*\)', self.code) is not None

class CodeBlock:
    def __init__(self):
        self.codelines  : List[CodeLine] = []

    def __str__(self):
        ret = ''
        for codeline in self.codelines:
            ret += codeline.__str__()
        return ret

    def __iadd__(self, other) -> CodeBlock:
        if other == '__cl__':
            self.append(other=other)
        else :
            self.append(CodeLine(code=other))
        return self

    def have_func(self):
        if len(self.codelines) <= 1:
            return False
        for cl in self.codelines[1:]:
            if cl.have_func():
                return True
        return False

    def append(self, other : CodeLine) -> None:
        if len(self.codelines) == 0:  #the first line
            other.retract = 0
            other.linenum = 1
        else :                         #other line
            lastline = self.codelines[-1]
            other.retract = lastline.retract + lastline.ex_retract

        self.codelines.append(other)

    def set_ex_retract(self, ex_retract : int):
        self.codelines[-1].ex_retract = ex_retract