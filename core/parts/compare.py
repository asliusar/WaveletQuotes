from core.parts.indexes import *


def compare_hurst_macd():
    date, x = hist_data.get_historical_quotes(start_date=datetime.datetime(2003, 9, 2),
                                                  end_date=datetime.datetime(2004, 6, 2))

    # hx = exp_moving_average(x, 5)
    htx = hurst(x)

    # mx = exp_moving_average(x, 5)
    mtx = macd(x, 12, 26)
    ax = []
    ax.append(np.array(x[30:]))
    ax.append(np.array(htx))
    ax.append(np.array(mtx[30:]))
    # print(htx)
    showPlotCompare(ax, date[30:], 'compare.jpg')

def compare_wavelets():
    date, x = hist_data.get_historical_quotes(start_date=datetime.datetime(2003, 9, 2),
                                                  end_date=datetime.datetime(2004, 6, 2))

    ax = []
    l = len(x)
    ax.append(x[:l-10])
    ax.append(get_wavelet(x, 'db1')[:l-10])
    ax.append(get_wavelet(x, 'haar')[:l-10])
    ax.append(get_wavelet(x, 'coif1')[:l-10])
    showPlotCompare(ax, date[:l-10], 'comparewt.jpg')


def compare_fft():
    date, x = hist_data.get_historical_quotes(start_date=datetime.datetime(2003, 9, 2),
                                                  end_date=datetime.datetime(2004, 6, 2))

    ax = []
    l = len(x)
    t = 10
    ax.append(x[t:l-t])
    ax.append(np.fft.fft(x)[t:l-t])
    print(l, len(np.fft.fft(np.fft.fft(x)[5:l-5])[5:l-5]))
    ax.append(np.fft.fft(np.fft.fft(x)[5:l-5])[5:l-5])
    showPlotCompare(ax, date[t:l-t], 'comparefft.jpg')

compare_fft()
# compare_wavelets()
