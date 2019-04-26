import scipy.weave as wave
from time import time
data = 1
code = "return_val = data+1;"
result = wave.inline(code, ['data'], compiler='gcc')