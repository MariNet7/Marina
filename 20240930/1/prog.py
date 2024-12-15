M, N = eval(input())
print([p for p in range(M, N) if all(p % i != 0 for i in range(2, int(p**0.5)+1)) and p > 1])
