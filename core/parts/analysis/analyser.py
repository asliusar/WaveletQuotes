import json
from datetime import datetime

from core.parts.preprocessing.preprocessing import prepareData
from core.parts.processing.indexes import hurst, prepareHurstIndex
from server_side.utils import DateTimeEncoder


def analyse(currency, frequency, startDate, endDate):
    data = prepareData(currency, frequency, startDate, endDate)
    hurstIndex = prepareHurstIndex(data["timestamp"], data["open"])  # hurst index of close
    # waveletIndex = prepareWaveletIndex()

    result = {"timeSeries": data, "hurstIndex": hurstIndex}

    return result

# res = analyse('eurusd=x', "TIME_SERIES_DAILY", datetime(2006, 8, 2), datetime(2007, 8, 2))
# print(json.dumps(res, cls=DateTimeEncoder))
