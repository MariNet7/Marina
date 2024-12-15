def minus(chi, chichi):
    match chi:
        case _ if isinstance(chi, int) or isinstance(chi, float):
            return chi - chichi
        case _ if isinstance(chi, list):
            return [i for i in chi if i not in chichi]
        case _ if isinstance(chi, tuple):
            return tuple(i for i in chi if i not in chichi)
        case _ if isinstance(chi, str):
            return "".join([i for i in chi if i not in chichi])

print(minus(*eval(input())))
