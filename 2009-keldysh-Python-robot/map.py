inc = lambda x:x+1
def inc(x): return x + 1

a = [1, 2, 3]

incs = map (inc, a)
incs = map (lambda x:x + 1, a)#2,3,4
f = filter (lambda x:x<2, a) #1

measureTimes = [1,2,3]
m = min(measureTimes)
measureTimes = map(lambda x:x-m, measureTimes)