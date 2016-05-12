import copy
from core.tools import *
import core.parts.csv_retriever as hist_data
import core.parts.elliot as elliot

import numpy as np
from numpy import log, polyfit, sqrt, std, subtract
import pywt
import datetime
from scipy.signal import blackman


def hurst(ts):
    # Create the range of lag values
    window_len = 30
    hurst_ts = np.zeros((0,), dtype=np.int)
    for tail in range(window_len, len(ts)):
        lags = range(1, window_len // 2)
        # print(lags)
        # Calculate the array of the variances of the lagged differences
        cur_ts = ts[max(1, tail - window_len):tail]
        # cur_ts = ts[:tail]
        tau = [sqrt(std(subtract(cur_ts[lag:], cur_ts[:-lag]))) for lag in lags]

        # print("Time series slice len: ",len(cur_ts),len(tau),lags)
        # Use a linear fit to estimate the Hurst Exponent
        poly = polyfit(log(lags), log(tau), 1)

        # Return the Hurst exponent from the polyfit output
        # print(poly[0]*2.0)
        hurst_ts = np.append(hurst_ts, poly[0] * 2.0)
    return hurst_ts


def calculateHurst(date, x, folder_name):
    hurst_res = hurst(x)
    showPlot(date[-len(hurst_res):], hurst_res, folder_name)


def lyapunov(series):
    from math import log

    def d(series, i, j):
        return abs(series[i] - series[j])

    N = len(series)
    eps = 10
    dlist = [[] for _ in range(N)]
    resultlist = []
    for i in range(N):
        ilist = []
        for j in range(i + 1, N):
            # jlist = []
            if d(series, i, j) < eps:
                for k in range(min(N - i, N - j)):
                    delta = d(series, i + k, j + k)
                    # print(delta)
                    if delta > 0:
                        dlist[k].append(log(delta))
                        # jlist.append(delta)
                        #     if len(jlist):
                        #         ilist.append(sum(jlist) / len(jlist))
                        # if len(ilist):
                        #     resultlist.append(sum(ilist) / len(ilist))
                        # else:
                        #     resultlist.append(0)
                        # print("result")
    # return (resultlist)
    # print(len(dlist))
    return ([sum(dl) / len(dl) if len(dl) else 0 for dl in dlist])
    # for i in range(len(dlist)):
    #     if len(dlist[i]):
    #         print >> f, i, sum(dlist[i]) / len(dlist[i])


def calculateLyapunov(date, x, folder_name):
    showPlot(date, lyapunov(x), folder_name)


# simple moving average: ts - time series vector, moving_average_width - width
def moving_average(ts, moving_average_width):
    for i in range(moving_average_width - 1, len(ts)):
        for j in range(i - moving_average_width + 1, i):
            ts[i] += ts[j]
        ts[i] /= moving_average_width
    return ts


# exponential moving average: ts - time series vector, moving_average_width - width
def exp_moving_average(ts, moving_average_width):
    if len(ts) < 2 * moving_average_width:
        raise ValueError("data is too short")
    c = 2.0 / (moving_average_width + 1)
    ts_ans = copy.deepcopy(ts)
    for i in range(1, len(ts)):
        # print(ts[0], ts_ans[0])
        ts_ans[i] = c * ts[i] + (1 - c) * ts_ans[i - 1]
    return ts_ans


# Moving Average Convergence Divergence - MACD: ts - time series vector, width1 - short EMA, width2 - long EMA
# default values are recommended for day-charts
def macd(ts, width1=12, width2=26):
    ts_ema_short = copy.deepcopy(exp_moving_average(ts, width1))

    ts_ema_long = copy.deepcopy(exp_moving_average(ts, width2))

    macd_ans = ts_ema_short - ts_ema_long
    return macd_ans


def calculateMACD(date, x, width1, width2, folder_name):
    print(folder_name)
    showPlot(date, macd(x, width1=width1, width2=width2), folder_name)


def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100. / (1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]  # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi


def movingaverage(values, window):
    weigths = np.repeat(1.0, window) / window
    smas = np.convolve(values, weigths, 'valid')
    return smas  # as a numpy array


def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def get_wavelet(x, wavelet_name='db1'):
    w = pywt.Wavelet(wavelet_name)
    scale = 3
    cA, cD = pywt.dwt(x, wavelet=w, mode='per')
    result = np.array([cA[0]])
    for i in range(1, len(cA)):
        temp = np.linspace(cA[i - 1], cA[i], scale)
        result = np.append(result, temp[1:])
        # result = result + temp[1:]
    if len(x) != len(result):
        result = np.append(result, [0])
    return result


def macd_research():
    # date, x, _, _, _, _ = prepareData('eurusd=x', '20y')
    # date, x = hist_data.get_historical_gdp()
    # print(date)
    # date, x = hist_data.get_historical_quotes(start_date=datetime.datetime(2003, 9, 2), end_date=datetime.datetime(2004, 6, 2))
    date, x = elliot.generate_elliot_waves_wrapper(50)
    print("11111111")
    print(type(date))
    # date = np.array(date, dtype=datetime.datetime)
    # print(x)
    # date, x = hist_data.get_historical_quotes()
    # print(hist_data.get_historical_gdp())
    # x = [1,4, 0, 3, -1, 0, -5, -2, 4, 5]
    # x = np.random.rand(277)
    # print(date)
    x = exp_moving_average(x, 5)
    tx = macd(x, 12, 26)
    ax = list()
    at = list()
    splt_x, splt_date = split_timeline(tx, date)
    ax += list(splt_x)
    at += list(splt_date)
    wx = list()
    wt = list()
    wt += list(splt_date)

    wavelet_sum = []
    for t in splt_x:
        temp = get_wavelet(t, 'haar')
        wavelet_sum.append(temp)
    wx += list(wavelet_sum)

    fx = list()
    ft = list()
    ft += list(splt_date)

    fft_sum = []
    for t in splt_x:
        temp = np.fft.fft(t)
        fft_sum.append(temp)
    fx += list(fft_sum)
    showPlot(date, x, 'perfect_w_x.png')
    # macd
    print('macd')
    shopPlotMixSeparate(ax, at, 'perfect_w_macd.png')
    # wavelet
    print('wt')
    shopPlotMixSeparate(wx, wt, 'perfect_w_wt.png')

    print('fft')
    shopPlotMixSeparate(fx, ft, 'perfect_w_fft.png')


def hurst_research():
    date, x = hist_data.get_historical_quotes(start_date=datetime.datetime(2003, 9, 2),
                                              end_date=datetime.datetime(2004, 6, 2))

    x = exp_moving_average(x, 5)
    tx = hurst(x)
    ax = list()
    at = list()

    splt_x, splt_date = split_timeline(tx, date, division_line=0.5)

    ax += list(splt_x)
    at += list(splt_date)

    wx = list()
    wt = list()
    wt += list(splt_date)

    wavelet_sum = []
    for t in splt_x:
        temp = get_wavelet(t, 'dmey')
        wavelet_sum.append(temp)
    wx += list(wavelet_sum)

    fx = list()
    ft = list()
    ft += list(splt_date)

    fft_sum = []
    for t in splt_x:
        temp = np.fft.fft(t)
        fft_sum.append(temp)
    fx += list(fft_sum)

    showPlot(date, x, 'w_x.png')

    # macd
    print('hurst', at)
    shopPlotMixSeparate(ax, at, 'w_hurst.png')

    # wavelet
    print('wt')
    shopPlotMixSeparate(wx, wt, 'w_hurst_wt.png')

    print('fft')
    shopPlotMixSeparate(fx, ft, 'w_hurst_fft.png')


hurst_research()
# macd_research()
