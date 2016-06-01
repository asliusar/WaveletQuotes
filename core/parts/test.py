from pylab import *
import pywt
from core.tools import prepareData
import scipy.io.wavfile as wavfile


# x = [3, 7, 1, 1, -2, 5, 4,1,1,1,1,1]
date, x, _, _, _, _ = prepareData('eurusd=x', '20y')
# Discrete Wavelet Transform
# cA, cD = pywt.dwt(x, 'db2')
# x2 = pywt.idwt(cA, cD, 'db2')
# print(len(cA), len(cD))

def get_wavelet(x, wavelet_name='db1'):
    w = pywt.Wavelet(wavelet_name)
    scale = 3
    cA, cD = pywt.dwt(x, wavelet=w, mode='per')
    result = np.array([cA[0]])
    for i in range(1, len(cA)):
        temp = np.linspace(cA[i-1], cA[i], scale)
        result = np.append(result, temp[1:])
        # result = result + temp[1:]
    if len(x) != len(result):
        result = np.append(result, [0])
    return result

import matplotlib.pyplot as plt
import numpy as np

# fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex=True)
# ax1.plot(np.arange(len(x)), x)
# ax2.plot(np.arange(len(cA)), cA)
# ax3.plot(np.arange(len(cD)), cD)
# ax4.plot(np.arange(len(x)), np.append(cA,cD))
# # fig.plot([1, 2, 3], [1, 1, 1])
# fig.savefig('test.png')
# plt.close(fig)

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True)
ax1.plot(np.arange(len(x)), x)
ax3.plot(np.arange(len(x)), np.abs(np.fft.fft(np.abs(np.fft.fft(x)))))
fig.savefig('test2.png')
# ax2.plot(np.arange(len(x)), get_wavelet(x, 'coif4'))
# ax3.plot(np.arange(len(x)), get_wavelet(get_wavelet(x), 'coif4'))
# fig.savefig('test3.png')
plt.close(fig)
