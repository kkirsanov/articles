import time, random
def AddTime(fn, *args, **kwargs):
    #generates new new_fn every time
    def new_fn(*args, **kwargs):
        data = fn(*args, **kwargs)
        return (time.time(), data)
    return new_fn

@AddTime #decorator
def GetMeasure():
    return random.random()
print GetMeasure() # (1254785016.7783949, 0.46029099903771442)
