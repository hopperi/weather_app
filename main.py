from fastapi import FastAPI, HTTPException
from geocode.geocode import get_coords
from weather.weather_api import get_weather
from utils.time_utils import get_local_time
from db import connect_db, insert_weather_data, close_connection

app = FastAPI()

connect_db()

@app.get("/getWeather/{city}")
def api_get_weather(city: str):
    lat, lon = get_coords(city)
    if lat is None or lon is None:
        raise HTTPException(status_code=404, detail="Город не найден")

    try:
        data = get_weather(lat, lon)
        local_time = get_local_time(data["timezone"])
        celsius = round(data["main"]["temp"] - 273.15, 2)

        insert_weather_data(
            city=data["name"],
            temperature=celsius,
            humidity=data["main"]["humidity"],
            weather_description=data["weather"][0]["description"]
        )

        return {
            "city": data["name"],
            "time": local_time,
            "temperature_celsius": celsius,
            "description": data["weather"][0]["description"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
def shutdown():
    close_connection()
