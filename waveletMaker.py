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
from numpy.random import randn

common_folder = 'static/results/'
input_plot_name = 'input_plot'
hurst_plot_name = 'hurst_plot'
lyapunov_plot_name = 'lyapunov_plot'


def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)

    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)

    return bytesconverter


def loadStock(stock, wrange):
    '''
        Use this to dynamically pull a stock:
    '''
    stockFile = []
    try:
        print('Currently Pulling', stock)
        urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=' + wrange + '/csv'
        print('URL', urlToVisit)
        try:
            sourceCode = urllib.request.urlopen(urlToVisit).read().decode()
            splitSource = sourceCode.split('\n')
            for eachLine in splitSource:
                splitLine = eachLine.split(',')
                if len(splitLine) == 6:
                    if 'values' not in eachLine:
                        stockFile.append(eachLine)
        except Exception as e:
            print(str(e), 'failed to organize pulled data.')
    except Exception as e:
        print(str(e), 'failed to pull pricing data')
    return stockFile


def mainLoop(stock, wrange):
    try:
        date, closep, highp, lowp, openp, volume = prepareData(stock, wrange)
        x = closep
        folder_name = stock + '_' + wrange
        plot_name = common_folder + folder_name + '/' + input_plot_name + '.png'
        hurst_name = common_folder + folder_name + '/' + hurst_plot_name + '.png'
        lyapunov_name = common_folder + folder_name + '/' + lyapunov_plot_name + '.png'
        if not os.path.exists(common_folder + folder_name):
            os.makedirs(common_folder + folder_name)
        print("Main thread test")
        showPlot(date, x, plot_name)
        hurst_res = hurst(x)
        # lyapunov_res = lyapunov(x)
        # print("Hurst size/input size: ", len(hurst_res), len(date[-len(hurst_res):]))
        showPlot(date[-len(hurst_res):], hurst_res, hurst_name)
        print("lyapunov")
        showPlot(date, lyapunov(x), lyapunov_name)
        for wavelet in all_wavelets:
            wa = WaveletAnalysis(data=x, wavelet=wavelet())
            # wavelet power spectrum
            power = wa.wavelet_power
            # scales
            scales = wa.scales
            # associated time vector
            # t = wa.time
            # reconstruction of the original data
            # rx = wa.reconstruction()
            showResult(date, scales, power, 5, '', common_folder + folder_name + '/' + wavelet.__name__ + '.png')
        for wavelet in all_wavelets:
            wa = WaveletAnalysis(data=hurst_res, wavelet=wavelet())
            # wavelet power spectrum
            power = wa.wavelet_power
            # scales
            scales = wa.scales
            # associated time vector
            # t = wa.time
            # reconstruction of the original data
            # rx = wa.reconstruction()
            showResult(date[-len(hurst_res):], scales, power, 5, '',
                       common_folder + folder_name + '/' + wavelet.__name__ + '_hurst.png')
    except Exception as e:
        import traceback
        traceback.print_exc()


def calculateWavelet(stock, wrange, wavelet_name, moving_avg_width):
    # try:
    date, closep, highp, lowp, openp, volume = prepareData(stock, wrange)
    x = closep
    for i in range(moving_avg_width - 1, len(x)):
        for j in range(i - moving_avg_width + 1, i):
            x[i] += x[j]
        x[i] /= moving_avg_width

    time_scale = int(wrange[:-1])
    folder_name = stock + '_' + wrange

    plot_name = common_folder + folder_name + '/' + input_plot_name + '.png'
    hurst_name = common_folder + folder_name + '/' + hurst_plot_name + '.png'
    lyapunov_name = common_folder + folder_name + '/' + lyapunov_plot_name + '.png'
    wavelet = next((x for x in all_wavelets if x.__name__ == wavelet_name), None)

    if not os.path.exists(common_folder + folder_name):
        os.makedirs(common_folder + folder_name)
    showPlot(date, x, plot_name)
    showPlot(date, hurst(x), hurst_name)
    print("lyapunov")
    showPlot(date, lyapunov(x), lyapunov_name)
    wa = WaveletAnalysis(data=x, wavelet=wavelet())
    # wavelet power spectrum
    power = wa.wavelet_power
    # scales
    scales = wa.scales
    showResult(date, scales, power, math.ceil(time_scale / 4.), '',
               common_folder + folder_name + '/' + wavelet.__name__ + '.png')
    # except Exception as e:
    #     print('mainLoop', str(e))


def prepareData(stock, wrange):
    stockFile = loadStock(stock, wrange)
    try:
        date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile, delimiter=',', unpack=True)
        date = [datetime.strptime(str(x), '%Y%m%d.0') for x in date]
        return [date, closep, highp, lowp, openp, volume]
    except Exception as e:
        print('prepareData', str(e))


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


def showPlot(date, data, file_name):
    fig, ax = plt.subplots()
    ax.plot(date, data)
    fig.savefig(file_name)
    plt.close(fig)


def hurst(ts):
    # Create the range of lag values
    window_len = 30
    hurst_ts = np.zeros((0,), dtype=np.int)
    for tail in range(window_len, len(ts)):
        lags = range(1, window_len//2)
        # print(lags)
        # Calculate the array of the variances of the lagged differences
        cur_ts = ts[max(1,tail-window_len):tail]
        # cur_ts = ts[:tail]
        tau = [sqrt(std(subtract(cur_ts[lag:], cur_ts[:-lag]))) for lag in lags]

        # print("Time series slice len: ",len(cur_ts),len(tau),lags)
        # Use a linear fit to estimate the Hurst Exponent
        poly = polyfit(log(lags), log(tau), 1)

        # Return the Hurst exponent from the polyfit output
        # print(poly[0]*2.0)
        hurst_ts = np.append(hurst_ts, poly[0] * 2.0)
    return hurst_ts


def lyapunov(series):
    from math import log

    def d(series, i, j):
        return abs(series[i] - series[j])

    N = len(series)
    eps = 10
    dlist = [[] for _ in range(N)]
    resultlist = []
    for i in range(N):
        ilist = []
        for j in range(i + 1, N):
            # jlist = []
            if d(series, i, j) < eps:
                for k in range(min(N - i, N - j)):
                    delta = d(series, i + k, j + k)
                    # print(delta)
                    if delta > 0:
                        dlist[k].append(log(delta))
                        # jlist.append(delta)
        #     if len(jlist):
        #         ilist.append(sum(jlist) / len(jlist))
        # if len(ilist):
        #     resultlist.append(sum(ilist) / len(ilist))
        # else:
        #     resultlist.append(0)
        # print("result")
    # return (resultlist)
    # print(len(dlist))
    return([sum(dl) / len(dl) if len(dl) else 0 for dl in dlist])
    # for i in range(len(dlist)):
    #     if len(dlist[i]):
    #         print >> f, i, sum(dlist[i]) / len(dlist[i])


mainLoop('usdeur=x', '20y')
