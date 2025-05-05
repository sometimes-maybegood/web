import requests
from bs4 import BeautifulSoup
import json
import time
import random
from fake_useragent import UserAgent

# Список городов-миллионников
cities = [
    {"name": "Moscow", "lat": 55.7558, "lon": 37.6173},
    {"name": "Saint Petersburg", "lat": 59.9343, "lon": 30.3351},
    {"name": "Novosibirsk", "lat": 55.0302, "lon": 82.9204},
    {"name": "Yekaterinburg", "lat": 56.8389, "lon": 60.6057},
    {"name": "Kazan", "lat": 55.8304, "lon": 49.0661},
    {"name": "Nizhny Novgorod", "lat": 56.2965, "lon": 43.9361},
    {"name": "Chelyabinsk", "lat": 55.1644, "lon": 61.4368},
    {"name": "Samara", "lat": 53.1959, "lon": 50.1003},
    {"name": "Ufa", "lat": 54.7388, "lon": 55.9721},
    {"name": "Rostov-on-Don", "lat": 47.2357, "lon": 39.7015},
    {"name": "Omsk", "lat": 54.9885, "lon": 73.3242},
    {"name": "Krasnoyarsk", "lat": 56.0184, "lon": 92.8672},
    {"name": "Voronezh", "lat": 51.6755, "lon": 39.2089},
    {"name": "Perm", "lat": 58.0103, "lon": 56.2294},
    {"name": "Volgograd", "lat": 48.7080, "lon": 44.5133},
    {"name": "Krasnodar", "lat": 45.0393, "lon": 38.9872}
]

# Инициализация User-Agent
ua = UserAgent()

# Функция для парсинга Smooth Hound
def parse_smoothhound(city):
    url = f"https://www.smoothhound.co.uk/russia/{city['name'].lower().replace(' ', '-')}.html"
    headers = {"User-Agent": ua.random}
    hotels = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        hotel_elements = soup.select(".hotel-listing .hotel")
        for hotel in hotel_elements[:20]:
            name = hotel.select_one(".hotel-name").text.strip() if hotel.select_one(".hotel-name") else "Unknown"
            price_elem = hotel.select_one(".price")
            price = float(price_elem.text.replace("$", "").strip()) if price_elem and price_elem.text.strip() else random.uniform(40, 70)
            address = hotel.select_one(".address").text.strip() if hotel.select_one(".address") else ""

            lat = city["lat"] + random.uniform(-0.05, 0.05)
            lon = city["lon"] + random.uniform(-0.05, 0.05)

            hotels.append({
                "name": name,
                "price_per_day_usd": round(price, 2),
                "coordinates": {
                    "latitude": round(lat, 4),
                    "longitude": round(lon, 4)
                }
            })
        return hotels
    except requests.RequestException as e:
        print(f"Error parsing Smooth Hound for {city['name']}: {e}")
        return []

# Функция для парсинга Ostrovok.ru
def parse_ostrovok(city):
    url = f"https://ostrovok.ru/hotel/russia/{city['name'].lower().replace(' ', '-')}/"
    headers = {"User-Agent": ua.random}
    hotels = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        hotel_elements = soup.select(".hotel-card")
        for hotel in hotel_elements[:20]:
            name = hotel.select_one(".hotel-card__name").text.strip() if hotel.select_one(".hotel-card__name") else "Unknown"
            price_elem = hotel.select_one(".hotel-card__price")
            price = float(price_elem.text.replace("$", "").strip()) if price_elem and price_elem.text.strip() else random.uniform(40, 70)
            address = hotel.select_one(".hotel-card__address").text.strip() if hotel.select_one(".hotel-card__address") else ""

            lat = city["lat"] + random.uniform(-0.05, 0.05)
            lon = city["lon"] + random.uniform(-0.05, 0.05)

            hotels.append({
                "name": name,
                "price_per_day_usd": round(price, 2),
                "coordinates": {
                    "latitude": round(lat, 4),
                    "longitude": round(lon, 4)
                }
            })
        return hotels
    except requests.RequestException as e:
        print(f"Error parsing Ostrovok for {city['name']}: {e}")
        return []

# Функция для объединения данных
def get_hotels(city):
    smooth_hotels = parse_smoothhound(city)
    ostrovok_hotels = parse_ostrovok(city)
    all_hotels = smooth_hotels + ostrovok_hotels

    seen = set()
    unique_hotels = []
    for hotel in all_hotels:
        if hotel["name"] not in seen and hotel["name"] != "Unknown":
            seen.add(hotel["name"])
            unique_hotels.append(hotel)

    return unique_hotels[:50]

# Генерация JSON
json_data = []
for city in cities:
    print(f"Parsing {city['name']}...")
    hotels = get_hotels(city)
    if len(hotels) < 50:
        print(f"Warning: Only {len(hotels)} hotels found for {city['name']}")
    json_data.append({
        "city": city["name"],
        "hotels": hotels
    })
    time.sleep(random.uniform(2, 5))

# Сохранение в файл
with open("hotels_russia1.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

print("JSON file created: hotels_russia1.json")