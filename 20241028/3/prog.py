from itertools import product


def schet(tor):
    return tor.count('TOR') == 2


def nadpiss(length):
    return (''.join(nadpis) for nadpis in product('TOR', repeat=length))


n = int(input())
nadpisi = filter(schet, nadpiss(n))
print(', '.join(sorted(nadpisi)))
