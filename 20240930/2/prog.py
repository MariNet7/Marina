s = input()
spisok = []
for i in eval(s):
    spisok.append(i)
n = len(spisok)

for i in range(n):
    for j in range(0, n-i-1):
        ky = spisok[j] ** 2 % 100
        kyy = spisok[j+1] ** 2 % 100
        if ky > kyy:
            spisok[j], spisok[j+1] = spisok[j+1], spisok[j]
print(spisok)
