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
    import matplotlib.ticker as mticker
    import matplotlib.dates as mdates
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(YearLocator(time_scale))
    # ax.set_yticks(y_ticks)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    ax.contourf(date, scales, power, 100)
    # ax.set_yscale('log')
    print("Wavelet saved to", file_name)
    fig.savefig(file_name)
    # fig.show()
    # fig.waitforbuttonpress()


def split_timeline(line, date, division_line=0):
    result = []
    result_date = []
    print('split_timeline')
    last_index = 0
    for i in range(last_index, len(line)):
        line[i] -= division_line
    while line[last_index] == 0:
        last_index += 1
    t = -np.sign(line[last_index])
    for i in range(last_index, len(line)):
        # print(line[i])
        if line[i] * t >= 0:
            result.append(line[last_index:i + 1])
            result_date.append(date[last_index:i + 1])
            last_index = i
        if line[i] * t > 0:
            t = -t
    result.append(line[last_index:len(line)])
    result_date.append(date[last_index:len(line)])
    for i in range(last_index, len(result)):
        result[i] += division_line
    return result, result_date


def showPlot(date, data, file_name):
    import matplotlib.ticker as mticker
    import matplotlib.dates as mdates
    import datetime
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(mticker.MaxNLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    print(date)
    # print(data)
    # date = [datetime.datetime(1, 1, 1, 0, 0), datetime.datetime(1, 1, 2, 0, 0), datetime.datetime(1, 1, 3, 0, 0), datetime.datetime(1, 1, 4, 0, 0)]
    # data = [1, 2, 3, 4]
    ax.plot(date, data)
    # fig.plot([1, 2, 3], [1, 1, 1])
    fig.savefig(file_name)
    plt.close(fig)


def showPlotMix(data, file_name='test.png'):
    fig, arr = plt.subplots(nrows=len(data), sharex=True)
    print('showPlotMix')
    for i, d in enumerate(data):
        # print(len(d[0]))
        for j, td in enumerate(d[0]):
            # print(len(td))
            print(len(d[1][j]))
            arr[i].plot(d[1][j], td)
    fig.savefig(file_name)
    plt.close(fig)


def showPlotMixSeparate(data, date, file_name='test.png'):
    print('shopPlotMixSeparate')
    import matplotlib.ticker as mticker
    import matplotlib.dates as mdates

    fig, arr = plt.subplots()
    ax1 = arr
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    for j, td in enumerate(date):
        arr.plot(td, data[j])

    fig.savefig(file_name)
    plt.close(fig)


def showPlotCompare(data, date, file_name):
    print("showPlotCompare")
    print(len(date))
    import matplotlib.ticker as mticker
    import matplotlib.dates as mdates

    fig, arr = plt.subplots(nrows=len(data), sharex=True)
    for i, d in enumerate(data):
        arr[i].xaxis.set_major_locator(mticker.MaxNLocator(7))
        arr[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        # fig.suptitle('test title', fontsize=20)
        # arr[i].set_title('ax1 title')
        arr[i].plot(date, d)
    fig.savefig(file_name)
    plt.close(fig)

def showPlotLabelsCompare(data, date, labels, file_name):
    print("showPlotCompare")
    print(len(date))
    import matplotlib.ticker as mticker
    import matplotlib.dates as mdates

    fig, arr = plt.subplots(nrows=len(data), sharex=True)
    for i, d in enumerate(data):
        arr[i].xaxis.set_major_locator(mticker.MaxNLocator(7))
        arr[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        # fig.suptitle('test title', fontsize=20)
        arr[i].set_title(labels[i])
        arr[i].plot(date, d)
    fig.savefig(file_name)
    plt.close(fig)


def showPlotMixSeparateCompare(data, date, labels, file_name='test.png'):
    print('shopPlotMixSeparate')
    import matplotlib.ticker as mticker
    import matplotlib.dates as mdates

    fig, arr = plt.subplots(nrows=len(data), sharex=True)
    for i, d in enumerate(data):
        arr[i].xaxis.set_major_locator(mticker.MaxNLocator(7))
        arr[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        # fig.suptitle('test title', fontsize=20)
        arr[i].set_title(labels[i])

        for j, td in enumerate(date[i]):
            arr[i].plot(td, d[j])

    fig.savefig(file_name)
    plt.close(fig)


def showPlotCompareSeparate(data, date, file_name):
    print("showPlotCompare")
    print(len(date))
    import matplotlib.ticker as mticker
    import matplotlib.dates as mdates

    fig, arr = plt.subplots(nrows=len(data), sharex=True)
    for i, d in enumerate(data):
        arr[i].xaxis.set_major_locator(mticker.MaxNLocator(7))
        arr[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        arr[i].plot(date[i], d)
    fig.savefig(file_name)
    plt.close(fig)