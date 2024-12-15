def objcount(clas):
    clas.counter = 0
    clas.__initt__ = clas.__init__
    def init(instance):
        clas.__initt__(instance)
        clas.counter += 1
    clas.__init__ = init

    if hasattr(clas, '__del__'):
        clas.__dell__ = clas.__del__
    else:
        clas.__dell__ = None

    def dell(instance):
        if clas.__dell__:
            clas.__dell__(instance)
        clas.counter -= 1
    clas.__del__ = dell

    return clas

import sys
exec(sys.stdin.read())