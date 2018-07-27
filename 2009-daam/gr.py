import pylab

a = range(10)

def double(xs):
    for x in xs:
        yield x
        yield x
a = [x for x in double(a)]

pylab.plot(a)
pylab.show()