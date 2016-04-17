import numpy as np
import matplotlib.pyplot as plt
import os
import pywt

elliot_waves = []
wavelets = pywt.families()


def showPlot(date, data, file_name):
    fig, ax = plt.subplots()
    ax.plot(date, data)
    fig.savefig(file_name)
    plt.close(fig)


# def generate_elliot_waves(folder):

common_folder = 'static/results/'
folder_name = 'elliot/'


def trend(data):
    return 0 * np.arange(len(data))


def print_wave(data, file_name):
    date = np.arange(len(data))
    return showPlot(date, data, file_name)


def print_fft(data, file_name):
    A = np.fft.fft(data)
    frrAbs = np.abs(A)
    return print_wave(frrAbs, file_name)


def get_filter(arr):
    return list([x for x in arr])


def print_wavelet(data, wavelet_name, filter, file_name):
    result = pywt.dwt(data, wavelet_name)
    if filter == 'high':
        return print_wave(result[0], file_name)
    elif filter == 'low':
        return print_wave(result[1], file_name)


def build_elliot_waves(path):
    x = [1, 3, 2, 4]
    z = [1, 3, 2, 4, 3, 5]
    # print('lol1', os.path.abspath(path))
    if not os.path.exists(os.path.abspath(path)):
        os.makedirs(os.path.abspath(path))
    minus_x = np.subtract(np.max(x), x)
    minus_z = np.subtract(np.max(z), z)

    # print_wave(x, trend, path + 'x.png')
    elliot_waves.append('x')
    # print_wave(z, trend, path + 'z.png')
    elliot_waves.append('z')

    # print_wave(minus_x, trend, path + 'minus_x.png')
    elliot_waves.append('minus_x')
    # print_wave(minus_z, trend, path + 'minus_z.png')
    elliot_waves.append('minus_z')

    # print_fft(z, trend, 'fft.png')
    # print_wavelet(z, trend, 'coif1', 'high', 'db.png')


# build_elliot_waves('static/results/elliot/')

z = [0, 4, 2, 6, 4, 8]
mx = [6, 7, 5]
print_wave(z + mx, 'zx.png')

# def generate_elliot_wave