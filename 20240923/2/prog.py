sum = 0
while True:
    chi = int(input())
    if chi <= 0:
        print(chi)
        break
    else:
        sum += chi
        if sum > 21:
            print(sum)
            break