from flask import jsonify

from core.parts.preprocessing.preprocessing import prepareData
from core.parts.processing.indexes import prepareHurstIndex, preparePrediction
from core.tools import collectPlots
from wavelet_research.waveletMaker import countWaveletTransform, flatWaveletTransform

import pandas as pd
import json


def analyse(currency, frequency, startDate, endDate):
    data = prepareData(currency, frequency, startDate, endDate)
    dataFrame = pd.DataFrame(data)

    hurstIndex = prepareHurstIndex(data["date"], data["open"])  # hurst index of close
    dataFrame["hurst"] = pd.Series(hurstIndex["value"], index=dataFrame.index)

    transforms = countWaveletTransform(data["date"], data["open"])
    flattenTransforms = flatWaveletTransform(transforms)

    tsDf = pd.concat([dataFrame, pd.DataFrame(flattenTransforms)], axis=1)

    recommendation = preparePrediction(flattenTransforms["Paul"])
    waveletDetails = collectPlots(transforms)

    result = {"timeSeries": json.loads(tsDf.to_json(orient="records", date_format="iso")),
              "waveletDetails": waveletDetails,
              "prediction": str(recommendation).lower()}

    return json.dumps(result)
