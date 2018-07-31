class A:
    a = 1
    def SetA(self, a):
        self.a = a
        self.c = self.a
    def __init__(self):
        pass
class B(C):
    def __init__(self):
        C.__init__(self)
        
b=B(1)
b.d = 123
B.e=321    
        