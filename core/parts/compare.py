from core.parts.indexes import *
from core.parts.research import wavelet_reserch
from core.parts.fourier.tools import compute_cepstrum
from core.parts.wavelet import compute_dwt


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


def compare_dwt(date, x, file_name='comparewt.jpg'):

    ax = []
    labels = []
    l = len(x)
    ax.append(x[:l-10])
    labels.append("Часовий ряд")
    ax.append(compute_dwt(x, 'db2')[:l - 10])
    labels.append("Вейвлет Добеши")
    ax.append(compute_dwt(x, 'haar')[:l - 10])
    labels.append("Вейвлет Хаара")
    ax.append(compute_dwt(x, 'coif2')[:l - 10])
    labels.append("Вейвлет Койфлет")
    showPlotLabelsCompare(ax, date[:l-10], labels, file_name)


def compare_fft(date, x, file_name='comparefft.jpg'):

    from scipy.fftpack import fft, ifft
    ax = []
    l = len(x)
    t = 50
    x = exp_moving_average(x, 10)

    labels = []
    ax.append(x[t:l-t])
    labels.append("Часовий ряд")
    ax.append((fft(x)[t:l-t]))
    labels.append("Фур’є перетворення")

    # print(l, len(np.fft.ifft(np.fft.fft(x)[5:l-5])[5:l-5]))
    print(len(x))
    # print(len(ifft(np.log(np.abs(fft(x)[5:l-5])))[5:l-5]))
    # ax.append((ifft(np.log(np.abs(fft(x))))[t:l-t])[:l/2 - t])
    # at.append((date[t:l-t])[::2])
    print("---")
    showPlotLabelsCompare(ax, date[t:l-t], labels, file_name)


def compare_cepstrum(date, x, file_name='comparecep.jpg'):
    # date, x = hist_data.get_historical_quotes(start_date=datetime.datetime(2000, 2, 2),
    #                                               end_date=datetime.datetime(2001, 2, 2),
    #                                           csv_path='../../data/usdgbp1990.csv')

    from scipy.fftpack import fft, ifft
    ax = []
    at = []
    l = len(x)
    t = 50
    x = exp_moving_average(x, 10)
    ax.append(x[t:l-t])
    at.append(date[t:l-t])

    # print(l, len(np.fft.ifft(np.fft.fft(x)[5:l-5])[5:l-5]))
    print(len(x))
    # print(len(ifft(np.log(np.abs(fft(x)[5:l-5])))[5:l-5]))
    ax.append((ifft(np.log(np.abs(fft(x))))[t:l-t])[:l/2 - t])
    at.append((date[t:l-t])[::2])
    print("---")
    showPlotCompareSeparate(ax, at, file_name)


def compare_split_wavelets(date, x, split_method='hurst', file_name='compare_sep_wt.jpg'):
    sum_x = []
    sum_t = []
    labels = []
    ax, at, wx, wt = wavelet_reserch(date, x, split_method, 'db2')
    sum_x.append(ax)
    sum_t.append(at)
    labels.append("Часовий ряд")
    sum_x.append(wx)
    sum_t.append(wt)
    labels.append("Вейвлет Добеши")
    ax, at, wx, wt = wavelet_reserch(date, x, 'hurst', 'haar')
    sum_x.append(wx)
    sum_t.append(wt)
    labels.append("Вейвлет Хаара")
    ax, at, wx, wt = wavelet_reserch(date, x, 'hurst', 'coif2')
    sum_x.append(wx)
    sum_t.append(wt)
    labels.append("Вейвлет Койфлет")
    showPlotMixSeparateCompare(sum_x, sum_t, labels, file_name)

# date, x = hist_data.get_historical_quotes(start_date=datetime.datetime(2003, 9, 2),
#                                                   end_date=datetime.datetime(2004, 6, 2))
date, x = hist_data.get_historical_quotes(start_date=datetime.datetime(2000, 2, 2),
                                                  end_date=datetime.datetime(2001, 2, 2),
                                              csv_path='../../data/usdgbp1990.csv')

# compare_cepstrum()
compare_fft(date, x)
# compare_dwt()
# compare_split_wavelets()