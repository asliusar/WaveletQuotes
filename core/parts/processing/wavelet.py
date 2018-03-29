from core.parts.processing.indexes import *
from core.parts.wavelets.transform import WaveletAnalysis
from core.parts.wavelets.wavelets import all_wavelets
common_folder = 'static/results/'
input_plot_name = 'input_plot'
hurst_plot_name = 'hurst_plot'
lyapunov_plot_name = 'lyapunov_plot'
macd_name = 'macd_plot'


def calculate_cwt(time_scale, date, x, folder_name, wavelet_name):

    plot_name = common_folder + folder_name + '/' + input_plot_name + '.png'
    hurst_name = common_folder + folder_name + '/' + hurst_plot_name + '.png'
    lyapunov_name = common_folder + folder_name + '/' + lyapunov_plot_name + '.png'
    wavelet = next((x for x in all_wavelets if x.__name__ == wavelet_name), None)

    if not os.path.exists(common_folder + folder_name):
        os.makedirs(common_folder + folder_name)
    showPlot(date, x, plot_name)
    # showPlot(date, hurst(x), hurst_name)
    print("lyapunov")
    # showPlot(date, lyapunov(x), lyapunov_name)
    wa = WaveletAnalysis(data=x, wavelet=wavelet())
    # wavelet power spectrum
    power = wa.wavelet_power
    # scales
    scales = wa.scales
    showResult(date, scales, power, time_scale, '',
               common_folder + folder_name + '/' + wavelet.__name__ + '.png')
    # except Exception as e:
    #     print('mainLoop', str(e))


def compute_dwt(x, wavelet_name='db1'):
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