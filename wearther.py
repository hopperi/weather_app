import requests
import json
import datetime
#парсер lon^ lat
def get_coords(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
 
    headers = {
        "User-Agent": "MyApp/1.0 (email@example.com)"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if data:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return float(lat), float(lon)
    else:
        return None

lat, lon = get_coords(str(input("Введите город: ")))
print(f"Широта: {lat}, Долгота: {lon}")

#api погоды

url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={"478d25bd40ad35d4f445ced1bcc024d8"}"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    timezone_offset = data["timezone"]
    utc_now = datetime.datetime.now(datetime.UTC)
    tz = datetime.timezone(datetime.timedelta(seconds=timezone_offset))
    local_time = utc_now.replace(tzinfo=datetime.timezone.utc).astimezone(tz)
    celsius = data["main"]["temp"] - 273.15
    info = {
        "Город": data["name"],
        "Время": local_time.strftime('%H:%M:%S %Y-%m-%d'),
        "Температура": round(celsius, 2),
        "Код состояния": data["cod"]
    }
    print(info)
except requests.RequestException as e:
    print("Ошибка при запросе:", e)
except (KeyError, IndexError) as e:
    print("Ошибка обработки данных:", e)