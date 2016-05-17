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

    from scipy.fftpack import fft, ifft
    ax = []
    at = []
    l = len(x)
    t = 10
    x = exp_moving_average(x, 5)
    ax.append(x[t:])
    at.append(date[t:])

    # print(l, len(np.fft.ifft(np.fft.fft(x)[5:l-5])[5:l-5]))
    print(len(x))
    print(len(ifft(np.log(np.abs(fft(x)[5:l-5])))[5:l-5]))
    ax.append(ifft(np.log(np.abs(fft(x)[:l/2][5:])))[t/2:])
    at.append(date[::2][5:])


    ax.append(fft(x)[:l/2][5:])
    at.append(date[::2][5:])

    showPlotCompareSeparate(ax, at, 'comparefft.jpg')

compare_fft()
# compare_wavelets()
