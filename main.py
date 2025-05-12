from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/hotels_russia.json')
def serve_hotels():
    return send_from_directory('templates', 'hotels_russia.json')

@app.route('/logo.jpg')
def logo():
    return send_from_directory('templates', 'logo.jpg')

if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)