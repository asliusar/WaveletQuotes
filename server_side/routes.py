import json

from flask import Flask
from flask import render_template
from flask import request

from core.parts import elliot
from waveletMaker import mainLoop, common_folder, calculateWavelet, input_plot_name, hurst_plot_name
from wavelets.wavelets import __all__

app = Flask(__name__)
elliot_folder_name = 'elliot/'


class Image:
    def __init__(self, name, img):
        self.name = name
        self.img = img


@app.route('/')
def hello_page(name=None):
    wavelet_list_retrieved = ["All"] + __all__
    # print(os.path.dirname(os.path.realpath(__file__)))
    # print(wavelet_list_retrieved)
    return render_template('index.html')
    # return render_template('plot_page.html', name=name, wavelet_list=wavelet_list_retrieved)


@app.route('/analyser')
def analyser_page(name=None):
    wavelet_list_retrieved = ["All"] + __all__
    return render_template('plot_page.html', name=name, wavelet_list=wavelet_list_retrieved)


@app.route('/elliot')
def elliot_page(name=None):
    return render_template('elliot.html',
                           elliot_list=[Image(name, common_folder + elliot_folder_name + name + '.jpg') for name in
                                        elliot.elliot_waves])


@app.route('/wavelets', methods=['POST'])
def show_wavelets():
    # print(request.form)
    wavelet_name = request.form["wavelet_name"]
    stock = request.form["ticker"] + "=x"
    wrange = request.form["period"]
    moving_avg_width = request.form["ma_param"]
    moving_avg_width = int(moving_avg_width)
    folder_name = stock + '_' + wrange
    wavelet_image_name = []
    wavelet_image_name.append(Image('input_plot', common_folder + folder_name + '/' + input_plot_name + '.png'))
    wavelet_image_name.append(Image('hurst_plot', common_folder + folder_name + '/' + hurst_plot_name + '.png'))
    print("1 - " + wavelet_name)
    if wavelet_name != 'All':
        print("1 - " + wavelet_name)
        calculateWavelet(stock, wrange, None, None, wavelet_name, moving_avg_width)
        wavelet_image_name.append(
                Image(wavelet_name, common_folder + folder_name + '/' + wavelet_name + '.png'))
    else:
        mainLoop(stock, wrange)
        for name in __all__:
            wavelet_image_name.append(Image(name, common_folder + folder_name + '/' + name + '.png'))

    wavelet_list_retrieved = ["All"] + __all__
    return render_template('plot_page.html', wavelet_list=wavelet_list_retrieved,
                           wavelet_image_names=wavelet_image_name)


@app.route('/sendRequest', methods=['POST'])
def requestResponse():
    print(request.form)
    response = json.dumps(request.form)
    print(response)
    return response


@app.route('/getpersonbyid', methods=['POST'])
def getPersonById():
    personId = int(request.form['personId'])
    return str(personId)


if __name__ == '__main__':
    app.run(debug=True)
