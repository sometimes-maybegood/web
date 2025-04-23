from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import json

# Замените на свои ключи от Amadeus
AMADEUS_API_KEY = '5AgIk7C0UiPirlAIIXO1fVxSo66oU7nT'
AMADEUS_API_SECRET = 'Pv8dpLKsts9ZIjBx'


def get_amadeus_access_token():
    url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'client_credentials',
        'client_id': AMADEUS_API_KEY,
        'client_secret': AMADEUS_API_SECRET
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get('access_token')


def search_hotels(latitude, longitude):
    token = get_amadeus_access_token()
    if not token:
        return []

    url = (
        'https://test.api.amadeus.com/v1/shopping/hotel-offers'
        f'?latitude={latitude}&longitude={longitude}&radius=10&radiusUnit=KM'
    )

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    results = response.json().get('data', [])
    hotels = []

    for item in results:
        hotel = item.get('hotel', {})
        offers = item.get('offers', [])
        if hotel and offers:
            hotels.append({
                'name': hotel.get('name', 'Неизвестный отель'),
                'price': f"{offers[0]['price']['total']} {offers[0]['price']['currency']}",
                'booking_url': hotel.get('website', '#')  # Можно заменить ссылкой на Google Maps
            })

    return hotels

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на более надёжный ключ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

API_KEY = '8cbce1cd-3366-4f5f-b725-bbd916b1bcf0'  # Пример ключа

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hotels', methods=['POST'])
def hotels():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    latitude = request.form['latitude']
    longitude = request.form['longitude']
    hotels_data = search_hotels(latitude, longitude)
    return render_template('hotels.html', hotels=hotels_data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)
        user = User(username=username, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно. Войдите.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash('Неверные данные')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из аккаунта.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)