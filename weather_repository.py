import os
import constants
from dotenv import load_dotenv
from requests_sync import RequestsSync
from weather_model import WeatherData, CityCoords


class WeatherRepository:
    load_dotenv(override=True)
    api_key = os.getenv("WEATHER_API_KEY")
    request = RequestsSync(constants.WEATHER_API_URL)

    def get_city_coords(self, city: str) -> object:
        query = {"appid": type(self).api_key, "q": city}
        response = self.request.send_request(
            endpoint=constants.GEO_API_PATH, params=query
        )
        return CityCoords(**response[0])

    def get_city_weather_data(self, city: str) -> list:
        coords = self.get_city_coords(city)
        query = {
            "appid": type(self).api_key,
            "lat": format(coords.lat, ".2f"),
            "lon": format(coords.lon, ".2f"),
            "units": "metric",
        }
        response = self.request.send_request(
            endpoint=constants.FORECAST_API_PATH, params=query
        )
        return response["list"]

    def generate_forecast(self, city: str) -> list:
        return [
            WeatherData(**item, city=city) for item in self.get_city_weather_data(city)
        ]
