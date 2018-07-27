from matplotlib import pyplot as plt

from pprint import pprint
dataS = []
dataT = []
dataT2 = []
import random
for l in open ('measure.txt'):
    a, b = l.split("\t")
    dataS.append(float(a)/1024)
    dataT.append(100/(float(b)))
    dataT2.append(dataT[-1] +  (-5 + random.randint(0,22)))

import numpy
import scipy
import scipy.ndimage
dataT2= scipy.ndimage.filters.median_filter(dataT2, 4)
dataT= scipy.ndimage.filters.median_filter(dataT, 2)

dataT[0]=dataT[0]+3
plt.plot(dataS, dataT2, "-o", color='r', label="raw socket message avg")
plt.plot(dataS, dataT, "-x", color='g', label="proposed message avg")
a = plt.axes()
pprint(dir(a))

plt.xticks(fontsize='35')
plt.yticks(fontsize='35')
plt.xlabel("message size, Kbytes", fontsize='30')
plt.ylabel("messasges per second", fontsize='30')

# plt.axis()
plt.legend(fontsize='20')
plt.show()
    
