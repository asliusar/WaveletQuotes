import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

import numpy as np


def loadStock(stock, wrange, type='TIME_SERIES_DAILY'):
    '''
        Use this to dynamically pull a stock:
    '''
    stockFile = []
    try:
        print('Currently Pulling', stock)
        urlToVisit = 'https://www.alphavantage.co/query?function=' + type + '&' \
                     + 'symbol=' + stock + '&' \
                     + 'outputsize=full' + '&' \
                     + 'apikey=EAMPC2LUJ6VV0KEN' + '&' \
                     + 'datatype=csv'
        print('URL', urlToVisit)
        try:
            sourceCode = urllib.request.urlopen(urlToVisit).read().decode()
            splitSource = sourceCode.split('\n')

            # remove header
            del splitSource[0]
            del splitSource[-1]

            for eachLine in splitSource:
                splitLine = eachLine.split(',')
                if len(splitLine) == 6:
                    if float(splitLine[1]) != 0:
                        stockFile.append(eachLine)
        except Exception as e:
            print(str(e), 'failed to organize pulled data.')
    except Exception as e:
        print(str(e), 'failed to pull pricing data')
    return stockFile


def prepareData(stock, wrange):
    stockFile = loadStock(stock, wrange)
    try:
        types = {
            'names': ('timestamp', 'open', 'high', 'low', 'close', 'volume'),
            'formats': ('S10', 'f', 'f', 'f', 'f', 'i')
        }
        timestamp, open, high, low, close, volume = \
            np.loadtxt(stockFile, delimiter=',', unpack=True, dtype=types)
        timestamp = [datetime.strptime(str(x.decode('ascii')), '%Y-%m-%d') for x in timestamp]
        return [timestamp, close, high, low, open, volume]
    except Exception as e:
        print('prepareData', str(e))


def loadCsv(csvAddress):
    import pandas as pd
    df = pd.read_csv(csvAddress, error_bad_lines=False)

    print(df)
