import json
from datetime import datetime

from flask import Flask, jsonify
from flask import render_template
from flask import request
from flask_cors import CORS, cross_origin

from core.parts.analysis.analyser import analyse
from core.parts.preprocessing.csv_retriever import get_historical_quotes
from core.parts.processing.elliot import elliot_waves
from core.parts.processing.wavelet import calculate_cwt
from core.parts.wavelets.wavelets import __all__
from server_side.utils import format_date, DateTimeEncoder
from wavelet_research.waveletMaker import *

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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


# @app.route('/analyser')
# def analyser_page(name=None):
#     wavelet_list_retrieved = ["All"] + __all__
#     return render_template('plot_page.html', name=name, wavelet_list=wavelet_list_retrieved)


@app.route('/elliott')
def elliot_page(name=None):
    return render_template('elliot.html',
                           elliot_list=[Image(name, common_folder + elliot_folder_name + name + '.jpg') for name in
                                        elliot_waves])


@app.route('/wavelets', methods=['POST'])
def show_wavelets():
    # print(request.form)
    wavelet_name = request.form["wavelet_name"]
    stock = request.form["ticker"] + "=x"
    wrange = request.form["period"]  #
    moving_avg_width = request.form["ma_param"]
    moving_avg_width = int(moving_avg_width)
    folder_name = stock + '_' + wrange
    wavelet_image_name = []

    print("1 - " + wavelet_name)
    # date, x, _, _, _, _ = prepareData(stock, wrange)
    # 2003 9 2 - 2004 6 2

    date, x = get_historical_quotes(start_date=datetime(1999, 2, 2),
                                    end_date=datetime(2003, 2, 2))
    for i in range(moving_avg_width - 1, len(x)):
        for j in range(i - moving_avg_width + 1, i):
            x[i] += x[j]
        x[i] /= moving_avg_width

    plot_name = common_folder + folder_name + '/' + input_plot_name + '.png'
    wavelet_image_name.append(Image('input_plot', plot_name))
    showPlot(date, x, plot_name)

    macd_plot = common_folder + folder_name + '/' + macd_name + '.png'
    ma1 = 10
    ma2 = 50
    wavelet_image_name.append(Image('macd_plot: %d-%d' % (ma1, ma2), macd_plot))
    calculateMACD(date, x, ma1, ma2, macd_plot)

    if wavelet_name != 'All':
        print("1 - " + wavelet_name)
        folder_name = stock + '_' + wrange
        time_scale = int(wrange[:-1])
        calculate_cwt(math.ceil(time_scale / 4.), date, x, folder_name, wavelet_name)
        wavelet_image_name.append(
            Image(wavelet_name, common_folder + folder_name + '/' + wavelet_name + '.png'))
    else:
        mainLoop(stock, wrange, date, x)
        for name in __all__:
            wavelet_image_name.append(Image(name, common_folder + folder_name + '/' + name + '.png'))

    print(123321)
    # hurst_plot = common_folder + folder_name + '/' + hurst_plot_name + '.png'
    # wavelet_image_name.append(Image('hurst_plot', hurst_plot))
    # calculateHurst(date, x, hurst_plot)

    # lyapunov_plot = common_folder + folder_name + '/' + lyapunov_plot_name + '.png'
    # wavelet_image_name.append(Image('lyapunov_plot', lyapunov_plot))
    # calculateLyapunov(date, x, lyapunov_plot)


    wavelet_list_retrieved = ["All"] + __all__
    return render_template('plot_page.html', wavelet_list=wavelet_list_retrieved,
                           wavelet_image_names=wavelet_image_name)


@app.route('/sendRequest', methods=['POST'])
def requestResponse():
    print(request.form)
    response = json.dumps(request.form)
    print(response)
    return response


@app.route('/analyse', methods=['POST'])
@cross_origin()
def analysis():
    parsed_json = json.loads(request.data.decode("utf-8"))

    startDate = format_date(parsed_json["startDate"])
    endDate = format_date(parsed_json["endDate"])

    result = analyse(parsed_json["currency"], parsed_json["frequency"], startDate, endDate)

    return jsonify(json.dumps(result, cls=DateTimeEncoder))


if __name__ == '__main__':
    app.run(debug=True)
