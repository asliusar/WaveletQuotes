from core.parts.preprocessing.preprocessing import prepareData
from core.parts.processing.indexes import prepareHurstIndex
from core.tools import collectPlots
from wavelet_research.waveletMaker import countWaveletTransform


def analyse(currency, frequency, startDate, endDate):
    data = prepareData(currency, frequency, startDate, endDate)
    hurstIndex = prepareHurstIndex(data["timestamp"], data["open"])  # hurst index of close

    transforms = countWaveletTransform(data["date"], data["open"])
    waveletDetails = collectPlots(transforms)

    result = {"timeSeries": data, "hurstIndex": hurstIndex, "waveletDetails": waveletDetails}

    return result
