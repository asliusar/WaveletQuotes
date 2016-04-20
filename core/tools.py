import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import YearLocator, DateFormatter
from core.parts.preprocessing import *

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
    print('split_timeline')
    last_index = 0
    while line[last_index] == 0:
        last_index += 1
    t = -np.sign(line[last_index])
    for i in range(last_index, len(line)):
        print(line[i])
        if line[i]*t >= 0:
            result.append(line[last_index:i+1])
            result_date.append(date[last_index:i+1])
            last_index = i
        if line[i]*t > 0:
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

def showPlotMix(date, data, file_name='test.png'):
    fig, (ax1, ax2) = plt.subplots(nrows = 2, sharex = True)
    print('showPlotMix')
    print(len(data))
    print(len(date))
    ax1.plot(date[0], data[0])
    for i, tx in enumerate(data[1:]):
        ax2.plot(date[i+1], tx)
    fig.savefig(file_name)
    plt.close(fig)




