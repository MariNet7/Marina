def bykva(stroka):
    stroka = stroka.lower()
    par = set()

    for i in stroka:
        c = 0
        if i.isalpha() and stroka[c + 1].isalpha():
            par.add(i + stroka[c + 1])
        c += 1
    return len(par)

print(bykva(input()))