def f(x, y=1, z=3):
    return [x, y, z]
f(1)
f(1, z=3)
f(z=3, y=2, x=1)

def Adder(x):
    def add_x(val):
        return val+x
    return add_x

add2 = Adder(2)
print add2(2) # 4
