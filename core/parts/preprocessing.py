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



def prepareData(stock, wrange):
    stockFile = loadStock(stock, wrange)
    try:
        date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile, delimiter=',', unpack=True)
        date = [datetime.strptime(str(x), '%Y%m%d.0') for x in date]
        return [date, closep, highp, lowp, openp, volume]
    except Exception as e:
        print('prepareData', str(e))

def loadCsv(csvAddress):
    import pandas as pd
    df = pd.read_csv(csvAddress, error_bad_lines=False)

    print(df)