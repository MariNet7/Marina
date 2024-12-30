import math

def Calc():
    fun = {}
    strr = 0

    while True:
        vvod = input().strip()
        strr += 1

        if vvod.startswith(':'):
            v = vvod[1:].split(' ')
            f = v[0]
            xy = v[1:-1]
            vblr = v[-1]

            fun[f] = (xy, vblr)

        elif vvod.startswith('quit'):
            vblvod = vvod.split(' ', 1)[1].strip('"')
            print(vblvod.format(len(fun) + 1, strr))
            break

        else:
            v = vvod.split(' ')
            f = v[0]
            args = v[1:]

            if f in fun:
                p, vblr = fun[f]

                string = {p[i]: eval(args[i]) for i in range(len(p))} if len(p) > 1 else {p[0]: eval(args[0])}

                string.update(math.__dict__)

                try:
                    print(eval(vblr, {}, string))
                except:
                    raise Exception

Calc()
