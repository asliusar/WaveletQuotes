from wavelets import WaveletAnalysis
import numpy as np
import os
import wavelets
from wavelets.wavelets import all_wavelets
import urllib.request, urllib.error, urllib.parse
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, drange
from datetime import datetime
import math
from numpy import cumsum, log, polyfit, sqrt, std, subtract
import copy
from numpy.random import randn


def detrend(data, degree=10):
    detrended = data
    for i in range(1, len(data)):
        chunk = data[max(1, i - degree):min(i + degree, len(data))]
        chunk = sum(chunk) / len(chunk)
        detrended[i] = data[i] - chunk
    return detrended


def showResult(date, scales, power, time_scale, window, file_name):
    # y_ticks = np.arange(0, 15, 2)
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(YearLocator(time_scale))
    # ax.set_yticks(y_ticks)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')

    ax.contourf(date, scales, power, 100)
    # ax.set_yscale('log')
    fig.savefig(file_name)
    # fig.show()
    # fig.waitforbuttonpress()


def split_timeline(line, date):
    result = []
    result_date = []
    t = -np.sign(line[0])
    last_index = 0
    for i, x in enumerate(line):
        if x*t >= 0:
            result.append(line[last_index:i+1])
            result_date.append(date[last_index:i+1])
            last_index = i
        if x*t > 0:
            t = -t
    result.append(line[last_index:len(line)])
    result_date.append(date[last_index:len(line)])

    return result, result_date

def showPlot(date, data, file_name):
    fig, ax = plt.subplots()
    ax.plot(date, data)
    # fig.plot([1, 2, 3], [1, 1, 1])
    fig.savefig(file_name)
    plt.close(fig)
#
# x = [1,4, 0, 3, -1, 0, -5, -2, 4, 5]
# print(split_timeline(x, np.arange(len(x))))
# splt_x, splt_date = split_timeline(x, np.arange(len(x)))
# fig, ax = plt.subplots()
# ax.plot(np.arange(len(x)), x)
# for i, tx in enumerate(splt_x):
#     ax.plot(splt_date[i], tx)
# fig.savefig('test.png')
# plt.close(fig)
