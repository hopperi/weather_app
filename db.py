import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

conn = None

def connect_db():
    global conn
    try:
        if DB_PASSWORD:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
        else:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                host=DB_HOST,
                port=DB_PORT
            )
        print("Подключение к базе данных установлено")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")

def create_table():
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    id SERIAL PRIMARY KEY,
                    city VARCHAR(100),
                    temperature NUMERIC(5,2),
                    humidity INTEGER,
                    weather_description VARCHAR(255),
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("Таблица weather_data создана или уже существует.")
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")

def insert_weather_data(city, temperature, humidity, weather_description):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO weather_data (city, temperature, humidity, weather_description)
                VALUES (%s, %s, %s, %s);
            """, (city, temperature, humidity, weather_description))
            conn.commit()
            print("Данные о погоде успешно добавлены.")
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")

def fetch_weather_data():
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM weather_data;")
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        print(f"Ошибка при извлечении данных: {e}")
        return []

def delete_weather_data_by_id(record_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM weather_data WHERE id = %s;", (record_id,))
            conn.commit()
            print(f"Запись с ID {record_id} удалена.")
    except Exception as e:
        print(f"Ошибка при удалении записи: {e}")

def close_connection():
    global conn
    if conn:
        conn.close()
        print("Соединение с базой данных закрыто.")
