from core.parts.indexes import *

def macd_research():
    # date, x, _, _, _, _ = prepareData('eurusd=x', '20y')
    # date, x = hist_data.get_historical_gdp()
    # print(date)
    # date, x = hist_data.get_historical_quotes(start_date=datetime.datetime(1993, 9, 2), end_date=datetime.datetime(2014, 6, 2))
    date, x = hist_data.get_historical_quotes(start_date=datetime.datetime(2011, 9, 2), end_date=datetime.datetime(2012, 6, 2))
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
    showPlot(date, x, prefix+'_w_x.png')
    # macd
    print('macd')
    showPlotMixSeparate(ax, at, prefix+'_w_macd.png')
    # wavelet
    print('wt')
    showPlotMixSeparate(wx, wt, prefix+'_w_wt.png')

    print('fft')
    showPlotMixSeparate(fx, ft, prefix+'perfect_w_fft.png')


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


# hurst_research()
macd_research()