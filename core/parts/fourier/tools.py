import numpy as np
import scipy


def compute_fft(x):
    # print('compute_fft')
    return np.fft.fft(x)


def compute_split_fft(arr_x, arr_t):
    # print('compute_split_fft')
    fx = list()
    ft = list()
    ft += list(arr_t)

    fft_sum = []
    for t in arr_x:
        temp = compute_fft(t)
        fft_sum.append(temp)
    fx += list(fft_sum)
    return fx, ft


def compute_cepstrum(x):
    # print('compute_cepstrum')
    return np.fft.ifft(np.log(np.abs(np.fft.fft(x))))


def compute_split_cepstrum(arr_x, arr_t):
    # print('compute_split_cepstrum')
    fx = list()
    ft = list()
    ft += list(arr_t)

    fft_sum = []
    for t in arr_x:
        temp = compute_cepstrum(t)
        fft_sum.append(temp)
    fx += list(fft_sum)
    return fx, ft