import json
from datetime import datetime

from core.parts.preprocessing.preprocessing import prepareData
from core.parts.processing.indexes import hurst
from server_side.utils import DateTimeEncoder


def analyse(currency, frequency, startDate, endDate):
    timeSeries = prepareData(currency, frequency, startDate, endDate)
    hurstIndex = hurst(timeSeries[1])  # hurst index of close
    # waveletIndex = calculateWaveletIndex()

    result = {"timeSeries": timeSeries, "hurstIndex": [timeSeries[0], hurstIndex.tolist()]}

    return result


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


res = analyse('eurusd=x', "TIME_SERIES_DAILY", datetime(2006, 8, 2), datetime(2007, 8, 2))
print(json.dumps(res, cls=DateTimeEncoder))
