import numpy as np
import matplotlib.pyplot as plt
import os

elliot_waves = []

def showPlot(date, data, file_name):
    fig, ax = plt.subplots()
    ax.plot(date, data)
    fig.savefig(file_name)
    plt.close(fig)

# def generate_elliot_waves(folder):

common_folder = 'static/results/'
folder_name = 'elliot/'

def trend(data):
    return 1 / 3 * np.arange(len(data))

def print_wave(data, trend, file_name):
    date = np.arange(len(data))
    if trend:
        template = data + trend(data)
        showPlot(date, template, file_name)

def build_elliot_waves(path):
    x = [1, 3, 2, 4]
    z = [1, 3, 2, 4, 3, 5]

    if not os.path.exists(path):
        os.makedirs(path)
    minus_x = np.subtract(np.max(x), x)
    minus_z = np.subtract(np.max(z), z)

    print_wave(x, trend, path + 'x.jpg')
    elliot_waves.append('x')
    print_wave(z, trend, path + 'z.jpg')
    elliot_waves.append('z')
    print_wave(minus_x, trend, path + 'minus_x.jpg')
    elliot_waves.append('minus_x')
    print_wave(minus_z, trend, path + 'minus_z.jpg')
    elliot_waves.append('minus_z')


build_elliot_waves('/home/joby/PycharmProjects/Wavelets/server_side/static/results/elliot/')