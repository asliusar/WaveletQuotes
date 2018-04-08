from core.parts.preprocessing.preprocessing import prepareData
from core.parts.processing.indexes import prepareHurstIndex
from core.tools import collectPlots
from wavelet_research.waveletMaker import countWaveletTransform, flatWaveletTransform


def analyse(currency, frequency, startDate, endDate):
    data = prepareData(currency, frequency, startDate, endDate)
    hurstIndex = prepareHurstIndex(data["date"], data["open"])  # hurst index of close

    transforms = countWaveletTransform(data["date"], data["open"])
    flattenTransforms = flatWaveletTransform(transforms)
    waveletDetails = collectPlots(transforms)

    result = {"timeSeries": data,
              "hurstIndex": hurstIndex,
              "waveletDetails": waveletDetails,
              "flattenTransforms": flattenTransforms}

    return result
