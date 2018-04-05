import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

import numpy as np


def generatePath(stock, frequency):
    return os.path.dirname(os.path.abspath(__file__)) + "/cache/" + stock + frequency + ".csv"


def checkExistingCache(path):
    return os.path.exists(path)


def loadStock(stock, frequency, withCache=True):
    path = generatePath(stock, frequency)
    if checkExistingCache(path) and withCache:
        return loadFormCache(path)
    else:
        return fetchStockData(stock, frequency, withCache)


def saveStockDataCache(path, stockFile):
    file = open(path, "w")
    file.writelines(stockFile)
    file.close()


def fetchStockData(stock, frequency, withCache):
    stockFile = []
    try:
        print('Currently Pulling', stock)
        urlToVisit = 'https://www.alphavantage.co/query?function=' + frequency + '&' \
                     + 'symbol=' + stock + '&' \
                     + 'outputsize=full' + '&' \
                     + 'apikey=EAMPC2LUJ6VV0KEN' + '&' \
                     + 'datatype=csv'
        print('URL', urlToVisit)
        try:
            sourceCode = urllib.request.urlopen(urlToVisit).read().decode()
            splitSource = sourceCode.split('\n')

            # remove headerhttps://www.alphavantage.co/query?function=20y&symbol=eurusd=x&outputsize=full&apikey=EAMPC2LUJ6VV0KEN&datatype=csv
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

    if len(stock) > 0 and withCache:
        saveStockDataCache(generatePath(stock, type), stockFile)

    return stockFile


def loadFormCache(path):
    file = open(path, "r")
    lines = file.readlines()
    file.close()

    return lines


# start - direction = -1
# end   - direction = 1
def findValidDateIndex(startDate, dateRange, direction):
    result = -1
    while result < 0:
        try:
            result = dateRange.index(startDate)
        except ValueError:
            startDate = startDate.replace(day=(startDate.day + direction))
            result = -1

    return result


def trim(dates, prices, start_date, end_date):
    start_cut = findValidDateIndex(start_date, dates, 1)
    end_cut = findValidDateIndex(end_date, dates, -1)

    updated_values = []
    dates = dates[start_cut:end_cut]
    for value in prices:
        updated_values.append(value[start_cut:end_cut])

    return (dates, *updated_values)


def prepareData(stock, frequency, startDate, endDate):
    stockFile = loadStock(stock, frequency)
    stockFile.reverse()  # depends on API
    types = {
        'names': ('timestamp', 'open', 'high', 'low', 'close', 'volume'),
        'formats': ('S10', 'f', 'f', 'f', 'f', 'i')
    }
    timestamp, open, high, low, close, volume = \
        np.loadtxt(stockFile, delimiter=',', unpack=True, dtype=types)
    timestamp = [datetime.strptime(str(x.decode('ascii')), '%Y-%m-%d') for x in timestamp]

    trimmedData = trim(timestamp, [close, high, low, open, volume], startDate, endDate)

    columns = ['date', 'open', 'high', 'low', 'close', 'volume']

    return dict(zip(columns, trimmedData))
