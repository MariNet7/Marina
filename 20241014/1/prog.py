from fractions import Fraction

data = input().split(", ")
s = Fraction(data[0])
w = Fraction(data[1])
stepena = int(data[2])
cofa = [Fraction(c) for c in data[3:4 + stepena]]
stepenb = int(data[4 + stepena])
codb = [Fraction(c) for c in data[5 + stepena: 6 + stepena + stepenb]]

ax = sum(coeff * (s ** exp) for exp, coeff in enumerate(cofa))
bx = sum(coeff * (s ** exp) for exp, coeff in enumerate(codb))

print(bx != 0 and ax / bx == w)
