from datetime import datetime

from core.parts.preprocessing.preprocessing import prepareData
from core.parts.processing.indexes import hurst


def analyse(currency, startDate, endDate, frequency):
    timeSeries = prepareData(currency, frequency, startDate, endDate)
    hurstIndex = hurst(timeSeries)
    # waveletIndex = calculateWaveletIndex()


analyse('eurusd=x', "TIME_SERIES_DAILY", datetime(2006, 8, 2), datetime(2007, 8, 2))