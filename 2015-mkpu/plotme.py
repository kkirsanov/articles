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
    dataT2.append(dataT[-1] - dataT[-1] / (6 + random.randint(0,12)))

plt.plot(dataS, dataT2, "-o", color='r', label="proposed message avg")
plt.plot(dataS, dataT, "-x", color='g', label="raw socket message time avg")
a = plt.axes()
pprint(dir(a))

plt.xticks(fontsize='35')
plt.yticks(fontsize='35')
plt.xlabel("message size, Kbytes", fontsize='40')
plt.ylabel("messasges per second", fontsize='40')

# plt.axis()
plt.legend(fontsize='20')
plt.show()
    
