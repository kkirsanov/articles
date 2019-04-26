data = range(100)
def CalcPow2(a):
    for x in a:
        yield x*x

for x in CalcPow2(data):
    print x
    
d = (x*x for x in data)