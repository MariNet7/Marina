N = int(input())
i = N
while i <= N+2:
    print()
    t = N
    while t <= N+2:
        pr = i * t
        sum = 0
        p = pr
        while p != 0:
            sum += p % 10
            p = p // 10

        if sum == 6:
            print(i, " * ", t, " = :=)", end=" ")
        else:
            print(i, " * ", t, " = ", pr, end=" ")
        t += 1
    i += 1
