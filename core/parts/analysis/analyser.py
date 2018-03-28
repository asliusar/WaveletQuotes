def analyse(currency, startDate, endDate, frequency):
    timeSeries = loadTimeSeries()
    hurstIndex = calculateHurstIndex(timeSeries)
    # waveletIndex = calculateWaveletIndex()