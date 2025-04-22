from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Замените на ваш API ключ для получения отелей
API_KEY = '8cbce1cd-3366-4f5f-b725-bbd916b1bcf0'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hotels', methods=['POST'])
def hotels():
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    # Здесь вы можете использовать API для получения отелей
    # Пример запроса к API (замените на ваш API)
    response = requests.get(f'https://api.example.com/hotels?lat={latitude}&lon={longitude}&apikey={API_KEY}')
    hotels_data = response.json()  # Предполагается, что API возвращает JSON

    return render_template('hotels.html', hotels=hotels_data)


if __name__ == '__main__':
    app.run(debug=True)