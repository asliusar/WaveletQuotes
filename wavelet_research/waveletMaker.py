import math
import os

from core.parts.processing.indexes import *
from core.parts.wavelets.transform import WaveletAnalysis
from core.parts.wavelets.wavelets import all_wavelets

common_folder = 'static/results/'
input_plot_name = 'input_plot'
hurst_plot_name = 'hurst_plot'
lyapunov_plot_name = 'lyapunov_plot'
macd_name = 'macd_plot'


#
def mainLoop(stock, wrange, date, x):
    try:
        import matplotlib
        from scipy import signal

        mcd = macd(x, 10, 20)
        showPlot(date, mcd, macd_name)
        folder_name = stock + '_' + wrange
        if not os.path.exists(common_folder + folder_name):
            os.makedirs(common_folder + folder_name)
        hurst_res = hurst(x)

        for wavelet in all_wavelets:
            wa = WaveletAnalysis(data=x, wavelet=wavelet())
            power = wa.wavelet_power
            scales = wa.scales
            time_scale = int(wrange[:-1])
            showResult(date, scales, power, math.ceil(time_scale / 4.), '',
                       common_folder + folder_name + '/' + wavelet.__name__ + '.png')
        for wavelet in all_wavelets:
            wa = WaveletAnalysis(data=hurst_res, wavelet=wavelet())
            power = wa.wavelet_power
            scales = wa.scales

            showResult(date[-len(hurst_res):], scales, power, 5, '',
                       common_folder + folder_name + '/' + wavelet.__name__ + '_hurst.png')
    except Exception as e:
        import traceback
        traceback.print_exc()


def displayResults