import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("WEATHER_API_KEY")
cities_list = [
    "London",
    "Moscow",
    "Paris",
    "New-York",
    "Berlin",
    "Batumi",
    "Sochi",
    "Rome",
    "Helsinki",
    "Saint-Petersburg",
]


class Forecast:
    def __init__(self, city, date, temp, humidity, wind, description):
        self.date = date
        self.city = city
        self.temp = temp
        self.humidity = humidity
        self.wind = wind
        self.description = description


class CityWeather:
    endpoint = "https://api.openweathermap.org"

    def __init__(
        self,
        city_name: str,
        state_code: str = None,
        country_code: str = None,
        limit: int = None,
    ):
        self.city_name = city_name
        self.state_code = state_code
        self.country_code = country_code
        self.limit = limit

    def generate_query(self):
        pass

    def get_coords(self) -> dict:
        geoapi_url = (
            f"{type(self).endpoint}/geo/1.0/direct?q={self.city_name},&appid={api_key}"
        )
        response = json.loads(requests.get(geoapi_url).text)[0]
        coords = {
            "lat": format(response["lat"], ".2f"),
            "lon": format(response["lon"], ".2f"),
        }
        return coords

    def get_weather_info(self):
        coords = self.get_coords()
        response = requests.get(
            f"{type(self).endpoint}/data/2.5/forecast?lat={coords['lat']}&lon={coords['lon']}&units=metric&appid={api_key}"
        )
        return response.json()["list"]

    def get_forecast(self):
        forecast = []
        for item in self.get_weather_info():
            timestamp = item["dt"]
            date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            temp = item["main"]["temp"]
            humidity = item["main"]["humidity"]
            wind = item["wind"]["speed"]
            description = item["weather"][0]["description"]
            forecast.append(Forecast(self.city_name, date, temp, humidity, wind, description))
        return forecast


london = CityWeather("London")

print(london.get_forecast())
