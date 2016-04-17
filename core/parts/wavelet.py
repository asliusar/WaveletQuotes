from wavelets import WaveletAnalysis
import os
from wavelets.wavelets import all_wavelets
import math
from core.parts.preprocessing import *
from core.tools import *

common_folder = 'static/results/'
input_plot_name = 'input_plot'
hurst_plot_name = 'hurst_plot'
lyapunov_plot_name = 'lyapunov_plot'
macd_name = 'macd_plot'

def calculateWavelet(stock, wrange, date, x, wavelet_name, moving_avg_width):
    # try:
    for i in range(moving_avg_width - 1, len(x)):
        for j in range(i - moving_avg_width + 1, i):
            x[i] += x[j]
        x[i] /= moving_avg_width

    time_scale = int(wrange[:-1])
    folder_name = stock + '_' + wrange

    plot_name = common_folder + folder_name + '/' + input_plot_name + '.png'
    hurst_name = common_folder + folder_name + '/' + hurst_plot_name + '.png'
    lyapunov_name = common_folder + folder_name + '/' + lyapunov_plot_name + '.png'
    wavelet = next((x for x in all_wavelets if x.__name__ == wavelet_name), None)

    if not os.path.exists(common_folder + folder_name):
        os.makedirs(common_folder + folder_name)
    showPlot(date, x, plot_name)
    print("lyapunov")
    wa = WaveletAnalysis(data=x, wavelet=wavelet())
    # wavelet power spectrum
    power = wa.wavelet_power
    # scales
    scales = wa.scales
    showResult(date, scales, power, math.ceil(time_scale / 4.), '',
               common_folder + folder_name + '/' + wavelet.__name__ + '.png')
    # except Exception as e:
    #     print('mainLoop', str(e))
