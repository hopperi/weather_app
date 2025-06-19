from geocode.geocode import get_coords
from weather.weather_api import get_weather
from utils.time_utils import get_local_time

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
    except Exception as e:
        print("Произошла ошибка:", e)

if __name__ == "__main__":
    main()
