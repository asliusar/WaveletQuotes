from flask import Flask
from flask import render_template
import json
import numpy as np
import os
from flask import request
from waveletMaker import mainLoop,common_folder,calculateWavelet
from wavelets.wavelets import __all__
from os import listdir
from os.path import isfile, join
app = Flask(__name__)

@app.route('/')
def hello_page(name = None):
    wavelet_list_retrieved = ["All"] + __all__
    print(os.path.dirname(os.path.realpath(__file__)))
    print(wavelet_list_retrieved)
    return render_template('plot_page.html', name=name, wavelet_list=wavelet_list_retrieved)


@app.route('/wavelets', methods=['POST'])
def show_wavelets():
    print(request.form)
    wavelet_name = request.form["wavelet_name"]
    stock = request.form["ticker"] + "=x"
    wrange = request.form["period"]

    folder_name = stock + '_' + wrange
    wavelet_image_name = []
    print("1 - " + wavelet_name)
    if wavelet_name != 'All':
        print("1 - " + wavelet_name)
        calculateWavelet(stock, wrange, wavelet_name)
        wavelet_image_name.append(common_folder + folder_name + '/' + wavelet_name + '.png')
    else :
        mainLoop(stock, wrange)
        for name in __all__:
            wavelet_image_name.append(common_folder + folder_name + '/' + name + '.png')

    wavelet_list_retrieved = ["All"] + __all__
    print(wavelet_image_name)
    return render_template('plot_page.html', wavelet_list=wavelet_list_retrieved, wavelet_image_names=wavelet_image_name)

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