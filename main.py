import psycopg2
from geocode.geocode import get_coords
from weather.weather_api import get_weather
from utils.time_utils import get_local_time
from db import connect_db, create_table, insert_weather_data, fetch_weather_data, close_connection


connect_db()

def main():
    city = input("Введите город: ")
    lat, lon = get_coords(city)
    if lat is None or lon is None:
        print("Город не найден")
        return

    try:
        data = get_weather(lat, lon)
        local_time = get_local_time(data["timezone"])
        celsius = data["main"]["temp"] - 273.15

        info = {
            "Город": data["name"],
            "Время": local_time,
            "Температура": round(celsius, 2),
            "Код состояния": data["cod"]
        }
        print(info)
        insert_weather_data(
    city=data["name"],
    temperature=round(celsius, 2),
    humidity=data["main"]["humidity"],
    weather_description=data["weather"][0]["description"]
)

    except Exception as e:
        print("Произошла ошибка:", e)

data = fetch_weather_data()
for row in data:
    print(row)
# close_connection()
if __name__ == "__main__":
    main()
close_connection()