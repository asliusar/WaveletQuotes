from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_page(name = None):
    return render_template('landing.html', name=name)
if __name__ == '__main__':
    app.run(debug=True)