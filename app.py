import logging
import os
import redis
import json
from flask import Flask, redirect, url_for
from db import connect_db, create_table ,fetch_weather_data, insert_weather_data, delete_weather_data_by_id, close_connection
from geocode.geocode import get_coords
from weather.weather_api import get_weather
from utils.time_utils import get_local_time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Инициализация Redis
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0
)

app = Flask(__name__)
connect_db()
create_table()
logging.info("Database connected and table ensured.")

@app.route('/')
def index():
    data = fetch_weather_data()
    logging.info(f"Fetched {len(data)} records from database.")
    result = ""
    for row in data:
        result += f"ID: {row[0]}, Город: {row[1]}, Температура: {row[2]}, Влажность: {row[3]}, Описание: {row[4]}, Время: {row[5]}\n"
    return "<pre>" + result + "</pre>"

# /add/<city>
@app.route('/add/<city>')
def add_city(city):
    logging.info(f"Add city request received: {city}")
    lat, lon = get_coords(city)
    if lat is None or lon is None:
        logging.warning(f"City '{city}' not found.")
        return f"Город '{city}' не найден"

    try:
        # Попытка получить данные из Redis
        cached_data = redis_client.get(city.lower())
        if cached_data:
            data = json.loads(cached_data)
            logging.info(f"Weather data for city '{city}' loaded from Redis cache.")
        else:
            data = get_weather(lat, lon)
            redis_client.setex(city.lower(), 600, json.dumps(data))  # кэш на 10 минут
            logging.info(f"Weather data for city '{city}' fetched from API and cached in Redis.")

        local_time = get_local_time(data["timezone"])
        celsius = round(data["main"]["temp"] - 273.15, 2)

        insert_weather_data(
            city=data["name"],
            temperature=celsius,
            humidity=data["main"]["humidity"],
            weather_description=data["weather"][0]["description"]
        )
        logging.info(f"Weather data for city '{data['name']}' inserted into database.")
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Error adding city '{city}': {e}")
        return f"Ошибка: {e}"

# Удаление по ID через путь: /delete/<id>
@app.route('/delete/<int:record_id>')
def delete_record(record_id):
    logging.info(f"Delete request for record ID: {record_id}")
    delete_weather_data_by_id(record_id)
    logging.info(f"Record ID {record_id} deleted.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    close_connection()
