from sklearn import metrics
import seaborn
from matplotlib import pyplot as plt
import numpy as np
import pywt

y = [1, 2, 3, 4]
x = np.arange(1, 5, 1)
cA, cD = pywt.dwt(y, 'db1')

plt.plot(x, y, 'red')
plt.plot(cA, 'green')
plt.show()