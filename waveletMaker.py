from wavelets import WaveletAnalysis
import numpy as np
import os
import wavelets
from wavelets.wavelets import all_wavelets

from core.tools import *
from core.parts.preprocessing import *
from core.parts.wavelet import *
from core.parts.indexes import *


def mainLoop(stock, wrange):
    try:
        import matplotlib
        date, closep, highp, lowp, openp, volume = prepareData(stock, wrange)
        x = closep
        # print(len(x))
        from scipy import signal
        # print(x-signal.detrend(x))
        # x = signal.detrend(x)
        degree = 10
        x = detrend(x,degree)
        mcd = macd(x,10,20)
        # x = macd(x)
        showPlot(date, mcd, macd_name)
        # print(x)
        folder_name = stock + '_' + wrange
        plot_name = common_folder + folder_name + '/' + input_plot_name + '.png'
        hurst_name = common_folder + folder_name + '/' + hurst_plot_name + '.png'
        lyapunov_name = common_folder + folder_name + '/' + lyapunov_plot_name + '.png'
        if not os.path.exists(common_folder + folder_name):
            os.makedirs(common_folder + folder_name)
        print("Main thread test")
        showPlot(date, x, plot_name)
        hurst_res = hurst(x)
        # lyapunov_res = lyapunov(x)
        # print("Hurst size/input size: ", len(hurst_res), len(date[-len(hurst_res):]))
        showPlot(date[-len(hurst_res):], hurst_res, hurst_name)
        # print("lyapunov")
        showPlot(date, lyapunov(x), lyapunov_name)
        for wavelet in all_wavelets:
            wa = WaveletAnalysis(data=x, wavelet=wavelet())
            # wavelet power spectrum
            power = wa.wavelet_power
            # scales
            scales = wa.scales
            # associated time vector
            # t = wa.time
            # reconstruction of the original data
            # rx = wa.reconstruction()
            showResult(date, scales, power, 5, '', common_folder + folder_name + '/' + wavelet.__name__ + '.png')
        for wavelet in all_wavelets:
            wa = WaveletAnalysis(data=hurst_res, wavelet=wavelet())
            # wavelet power spectrum
            power = wa.wavelet_power
            # scales
            scales = wa.scales
            # associated time vector
            # t = wa.time
            # reconstruction of the original data
            # rx = wa.reconstruction()
            showResult(date[-len(hurst_res):], scales, power, 5, '',
                       common_folder + folder_name + '/' + wavelet.__name__ + '_hurst.png')
    except Exception as e:
        import traceback
        traceback.print_exc()




# mainLoop('usdeur=x', '3m')
# loadCsv('static/data/GDP.csv')