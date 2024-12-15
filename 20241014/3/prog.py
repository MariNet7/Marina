def povovrot(gas, gid, visota):
    stena = "#" * (visota + 2)
    print(stena)
    gass = gas // visota
    gidd = gid // visota
    for i in range(gass):
        print("#" + "." * visota + "#")
    for i in range(gidd):
        print("#" + "~" * visota + "#")
    print(stena)


def vvod():
    gas = 0
    gid = 1
    while True:
        if input()[1] != '.':
            break
        gas += 1
    while True:
        if input()[1] != '~':
            break
        gid += 1
    return gas, gid


def vivod(gas, gid):
    gass = round(20 * gas / max(gas, gid))
    gidd = round(20 * gid / max(gas, gid))
    dl = max(len(str(gas)), len(str(gid)))
    print('.' * gass + ' ' * (20 - gass) + ' ' * dl + f"{gas}/{gas + gid}")
    print('~' * gidd + ' ' * (20 - gidd) + ' ' * dl + f"{gid}/{gas + gid}")


shirina = len(input()) - 2
gasv, gidv = vvod()
visota = gasv + gidv
gasv = gasv * shirina
gidv = gidv * shirina
povovrot(gasv, gidv, visota)
vivod(gasv, gidv)
