a = [] # empty list
b = [1, 2, 3]
c = [1, "asd", b]
d = b + c
c.append(1)
print c[2] # asd
del c[0]

if 2 in b:
    print "2 in ", b
if "zxc" not in b:
    print "'zxc' not in", b
if a:
    print "not empty"