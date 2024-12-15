st = eval(input())
dl = len(st)
mat1 = []
mat2 = []
mat1.append(st)
for i in range(dl-1):
    st = eval(input())
    if len(st) == dl:
        mat1.append(st)
    else:
        raise Exception("несоответствие размеру матрицы")
for i in range(dl):
    st = eval(input())
    mat2.append(st)

multiResult = [[sum(a * b for a, b in zip(mat1row, mat2col)) for mat2col in zip(*mat2)] for mat1row in mat1]

for i in range(dl):
    print(*multiResult[i], sep=",")