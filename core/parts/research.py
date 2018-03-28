from core.parts.test import get_wavelet
from wavelet_research.waveletMaker import *
from core.parts.wavelet import compute_dwt

class Image:
    def __init__(self, name, img):
        self.name = name
        self.img = img


def macd_research():
    date, x, _, _, _, _ = prepareData('eurusd=x', '20y')
    # date, x = hist_data.get_historical_gdp()
    # print(date)
  # date, x = hist_data.get_historical_quotes(start_date=datetime.datetime(2001, 8, 2), end_date=datetime.datetime(2002, 5, 2))
    # date, x = elliot.generate_elliot_waves_wrapper(50)
    prefix = "no_elliott"
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
    showPlot(date, x, prefix + '_w_x.png')
    # macd
    print('macd')
    showPlotMixSeparate(ax, at, prefix + '_w_macd.png')
    # wavelet
    print('wt')
    showPlotMixSeparate(wx, wt, prefix + '_w_wt.png')

    print('fft')
    showPlotMixSeparate(fx, ft, prefix + 'perfect_w_fft.png')

    mainLoop("x", "2y", date, x)


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
    showPlotMixSeparate(ax, at, 'w_hurst.png')

    # wavelet
    print('wt')
    showPlotMixSeparate(wx, wt, 'w_hurst_wt.png')

    print('fft')
    showPlotMixSeparate(fx, ft, 'w_hurst_fft.png')


def wavelet_reserch(date, x, type='macd', wavelet='db1'):
    tx = []
    x = exp_moving_average(x, 5)

    if type == 'hurst':
        tx = hurst(x)
    elif type == 'macd':
        tx = macd(x, 12, 26)

    ax = list()
    at = list()

    if type == 'hurst':
        division_line = 0
    else:
        division_line = .5
    splt_x, splt_date = split_timeline(tx, date, division_line=division_line)

    ax += list(splt_x)
    at += list(splt_date)

    wx = list()
    wt = list()
    wt += list(splt_date)

    wavelet_sum = []
    for t in splt_x:
        temp = compute_dwt(t, wavelet)
        wavelet_sum.append(temp)
    wx += list(wavelet_sum)

    # fx = list()
    # ft = list()
    # ft += list(splt_date)
    #
    # fft_sum = []
    # for t in splt_x:
    #     temp = np.fft.fft(t)
    #     fft_sum.append(temp)
    # fx += list(fft_sum)

    showPlot(date, x, 'w_x.png')

    # showPlotMixSeparate(ax, at, 'w_hurst.png')
    # showPlotMixSeparate(wx, wt, 'w_hurst_wt.png')
    # showPlotMixSeparate(fx, ft, 'w_hurst_fft.png')
    return ax, at, wx, wt


# hurst_research()
macd_research()
