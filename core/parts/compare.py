from core.parts.indexes import *


def compare_hurst_macd():
    date, x = hist_data.get_historical_quotes(start_date=datetime.datetime(2003, 9, 2),
                                                  end_date=datetime.datetime(2004, 6, 2))

    # hx = exp_moving_average(x, 5)
    htx = hurst(x)

    # mx = exp_moving_average(x, 5)
    mtx = macd(x, 12, 26)
    print(type(x))
    print(type(htx))
    print(type(mtx))
    ax = list()

    ax += list(np.array(x))
    ax += list(np.array(htx))
    ax += list(np.array(mtx))
    # print(htx)
    showPlotCompare(ax, date, 'compare.jpg')

compare_hurst_macd()
