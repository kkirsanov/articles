from math import sin, cos
from time import time
import psyco
a,b,c,d = 1,2,3,4

def F(x):  
    return x*a/b+3-4/5*6-sin(c+d*2)/5*6+cos(x*x)

def Calc():
    t0 = time()
    for x in xrange(1, 100000):
        F(x);F(x);F(x);F(x);F(x)
    print time() - t0

Calc() # 1.07147097588
psyco.full()
Calc() # 0.17466211319