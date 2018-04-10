from core.parts.preprocessing.preprocessing import prepareData
from core.parts.processing.indexes import prepareHurstIndex
from core.tools import collectPlots
from wavelet_research.waveletMaker import countWaveletTransform, flatWaveletTransform

import pandas as pd


def analyse(currency, frequency, startDate, endDate):
    data = prepareData(currency, frequency, startDate, endDate)
    dataFrame = pd.DataFrame(data)

    hurstIndex = prepareHurstIndex(data["date"], data["open"])  # hurst index of close
    dataFrame["hurst"] = pd.Series(hurstIndex["value"], index=dataFrame.index)

    transforms = countWaveletTransform(data["date"], data["open"])
    flattenTransforms = flatWaveletTransform(transforms)
    dataFrame.append(pd.DataFrame(flattenTransforms))

    waveletDetails = collectPlots(transforms)

    resData = dataFrame.to_dict()
    resData = dict(zip(resDat))

    result = {"timeSeries": {**dataFrame.to_dict(), **flattenTransforms},
              "waveletDetails": waveletDetails}

    return result
