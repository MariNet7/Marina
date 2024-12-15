from collections import Counter
W = int(input())
text = []
while strok := input():
    text.append(strok)
text = " ".join(text)

for s in ("-,.?!:';1234567890&()/*+" + '"'):
    text = text.replace(s, ' ')

sch = Counter([slovo for slovo in text.split() if len(slovo) == W])
kolvo = max(sch.values())
slova = [slovo for slovo, kolv in sch.items() if kolv == kolvo]
slova.sort()
print(" ".join(slova))
