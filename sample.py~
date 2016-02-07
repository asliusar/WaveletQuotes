from wavelets import WaveletAnalysis
import numpy as np
from wavelets import *
import urllib.request, urllib.error, urllib.parse
import matplotlib.dates as mdates
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, drange
from datetime import datetime
from numpy import arange

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

def graphData(stock, wrange):
    stockFile = loadStock(stock, wrange)

    try:
        date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',', unpack=True)
        date = [datetime.strptime(str(x), '%Y%m%d.0') for x in date]
        print((date))
           # # given a signal x(t)
        x = closep
        # and a sample spacing
        dt = 0.1

        wa = WaveletAnalysis(data=x, wavelet=DOG(), dt=dt)

        # wavelet power spectrum
        power = wa.wavelet_power

        # scales
        scales = wa.scales
        # associated time vector
        t = wa.time
        print(len(t))
        # reconstruction of the original data
        rx = wa.reconstruction()


        import matplotlib.pyplot as plt
        y_ticks = np.arange(0, 15, 2)
        fig, ax = plt.subplots()
        ax.xaxis.set_major_locator(YearLocator(5))
        # ax.set_yticks(y_ticks)
        ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')

        ax.contourf(date, scales, power, 100)
        # ax.set_yscale('log')
        fig.savefig('test_wavelet_power_spectrum.png')
        fig.show()
        fig.waitforbuttonpress()
    except Exception as e:
        print('main loop', str(e))




graphData('usdeur=x', '20y')