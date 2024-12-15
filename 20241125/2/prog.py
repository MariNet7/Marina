class Num:
    def set(self, obj, val):
        if type(val) == int or type(val) == float:
            obj.n = val
        elif hasattr(val, '__len__'):
            obj.n = len(val)
    __set__ = set

    def get(self, obj, cls):
        if hasattr(obj, 'n'):
            return obj.n
        else:
            return 0
    __get__ = get

import sys
exec(sys.stdin.read())