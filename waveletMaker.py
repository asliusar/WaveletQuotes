from wavelets import WaveletAnalysis
import numpy as np
import os
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
    stockFile =[]
    try:
        print('Currently Pulling',stock)
        urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range='+wrange+'/csv'
        print('URL', urlToVisit)
        try:
            sourceCode = urllib.request.urlopen(urlToVisit).read().decode()
            splitSource = sourceCode.split('\n')
            for eachLine in splitSource:
                splitLine = eachLine.split(',')
                if len(splitLine)==6:
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
        x = hurst(x)
        folder_name = stock + '_' + wrange
        plot_name = common_folder + folder_name + '/'+input_plot_name+'.png'
        if not os.path.exists(common_folder + folder_name):
            os.makedirs(common_folder + folder_name)
        showPlot(date,x,plot_name)
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
    except Exception as e:
        print('mainLoop', str(e))


def calculateWavelet(stock, wrange, wavelet_name,moving_avg_width):
    # try:
        date, closep, highp, lowp, openp, volume = prepareData(stock, wrange)
        x = closep
        for i in range(moving_avg_width-1,len(x)):
            for j in range(i-moving_avg_width+1, i):
                x[i] += x[j]
            x[i] /= moving_avg_width

        time_scale = int(wrange[:-1])
        folder_name = stock + '_' + wrange

        plot_name = common_folder + folder_name + '/'+input_plot_name+'.png'

        wavelet = next((x for x in all_wavelets if x.__name__ == wavelet_name), None)


        if not os.path.exists(common_folder + folder_name):
            os.makedirs(common_folder + folder_name)
        showPlot(date,x,plot_name)
        wa = WaveletAnalysis(data=x, wavelet=wavelet())
        # wavelet power spectrum
        power = wa.wavelet_power
        # scales
        scales = wa.scales
        showResult(date, scales, power, math.ceil(time_scale/4.), '', common_folder + folder_name + '/' + wavelet.__name__ + '.png')
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
    #fig.show()
    #fig.waitforbuttonpress()

def showPlot(date, data, file_name):
    plt.plot(date, data)
    plt.savefig(file_name)

def hurst(ts):
    # Create the range of lag values
    hurst_ts = []
    for tail in (1,len(ts)):

        lags = range(1, min(100,len(ts)/2))
        # Calculate the array of the variances of the lagged differences
        cur_ts = ts[tail:]
        tau = [sqrt(std(subtract(cur_ts[lag:], cur_ts[:-lag]))) for lag in lags]

        # Use a linear fit to estimate the Hurst Exponent
        poly = polyfit(log(lags), log(tau), 1)

        # Return the Hurst exponent from the polyfit output
        hurst_ts.append(poly[0]*2.0)
    return hurst_ts
#mainLoop('usdeur=x', '20y')