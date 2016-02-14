from flask import Flask
from flask import render_template
import json
import numpy as np
import os
from flask import request
from waveletMaker import mainLoop,common_folder,calculateWavelet
from wavelets.wavelets import __all__
app = Flask(__name__)

@app.route('/')
def hello_page(name = None):
    wavelet_list_retrieved = __all__
    print(os.path.dirname(os.path.realpath(__file__)))
    print(wavelet_list_retrieved)
    return render_template('plot_page.html', name=name,wavelet_list=wavelet_list_retrieved)


@app.route('/wavelets', methods=['POST'])
def show_wavelets():
    print(request.form)
    wavelet_name = request.form["wavelet_name"]
    stock = request.form["ticker"] + "=x"
    wrange = request.form["period"]
    calculateWavelet(stock, wrange,wavelet_name)

    folder_name = stock + '_' + wrange
    wavelet_image_name = common_folder + folder_name + '/' + wavelet_name + '.png'
    wavelet_list_retrieved = __all__
    print(wavelet_image_name)
    return render_template('plot_page.html',wavelet_list=wavelet_list_retrieved, wavelet_image_name=wavelet_image_name)

@app.route('/sendRequest', methods=['POST'])
def requestResponse():
    print(request.form)
    response = json.dumps(request.form)
    print(response)
    return response

@app.route('/getpersonbyid', methods = ['POST'])
def getPersonById():
    personId = int(request.form['personId'])
    return str(personId)

if __name__ == '__main__':
    app.run(debug=True)