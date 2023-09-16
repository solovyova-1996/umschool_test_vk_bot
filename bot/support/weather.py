import requests
from transliterate import translit

from config import weather_token
from datetime import datetime, timedelta

appid = weather_token


def get_id_city(city):
    city_update = f"{translit(city, language_code='ru', reversed=True)},RU"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': city_update, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        return data['list'][0]['id']
    except Exception:
        raise AttributeError


def get_weather(city):
    try:
        city_id = get_id_city(city)
    except AttributeError:
        return None

    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        return data
    except Exception:
        return None


def weather_tomorrow(city):
    try:
        city_id = get_id_city(city)
    except AttributeError:
        return None
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        result = []
        date_tomorrov = datetime.now().date() + timedelta(days=1)
        for date_day in data["list"]:
            date_day_in_date = datetime.strptime(date_day['dt_txt'], "%Y-%m-%d %H:%M:%S").date()
            if date_day_in_date == date_tomorrov:
                result.append(date_day)

        return result
    except Exception:
        return None


def parse_weather(lst_weather, city):
    result_string = f"Погода на завтра ({city})\n"
    for item in lst_weather:
        result_string += f"{list(item['dt_txt'].split())[-1]}: {item['weather'][0]['description']} - температура {item['main']['temp']} °C; ощущается {item['main']['feels_like']} °C\n"
    return result_string
