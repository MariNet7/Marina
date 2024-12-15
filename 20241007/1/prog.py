def minus(chi, chichi):
    return tuple(i for i in chi if i not in chichi)

def Pareto(*nabor):
    nabdel = ()
    for para in nabor:
        for par in nabor:
            if ((para[0] <= par[0]) and (para[1] <= par[1]) and ((para[0] < par[0]) or (para[1] < par[1]))):
                nabdel += (para, )
                break
    return minus(nabor, nabdel)

print(Pareto(*eval(input())))