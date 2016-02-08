from flask import Flask
from flask import render_template
import json
from flask import request
from wavelets.wavelets import __all__
app = Flask(__name__)

@app.route('/')
def hello_page(name = None):
    return render_template('plot_page.html', name=name)


@app.route('/wavelets', methods=['POST'])
def show_wavelets():
    response = json.dumps(__all__)
    print(response)
    return response

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