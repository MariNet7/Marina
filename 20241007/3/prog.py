def Calc(s, t, u):
    def ff(vblr):
        form = f"def func(x): return {vblr}"
        exec(form, globals())
        return func
    x_func = ff(s)
    y_func = ff(t)

    def calc(z):
        local_vars = {'x': z}
        x = x_func(z)
        y = y_func(z)

        local_vars['y'] = y
        return eval(u, {}, local_vars)

    return calc

s, t, u = input().split(", ")
result = Calc(s, t, u)
z = eval(input())
print(result(z))