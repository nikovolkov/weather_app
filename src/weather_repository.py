import os
import constants
import logging
from dotenv import load_dotenv
from requests_sync import RequestsSync
from weather_model import WeatherData, CityCoords


class WeatherRepository:
    load_dotenv(override=True)
    api_key = os.getenv("WEATHER_API_KEY")
    request = RequestsSync(constants.WEATHER_API_URL)

    def get_city_coords(self, city: str) -> object:
        logging.info(f"Fetching coordinates for city: {city}")
        query = {"appid": type(self).api_key, "q": city}
        response = self.request.send_request(
            endpoint=constants.GEO_API_PATH, params=query
        )
        coords = CityCoords(**response[0])
        logging.info(f"Coordinates for {city}: lat={coords.lat}, lon={coords.lon}")
        return coords

    def get_city_weather_data(self, city: str) -> list:
        logging.info(f"Fetching weather data for city: {city}")
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
        logging.info(f"Generating forecast for city: {city}")
        try:
            forecast = [
                WeatherData(**item, city=city)
                for item in self.get_city_weather_data(city)
            ]
            logging.info(f"Successfully generated forecast for {city}")
            return forecast
        except Exception as e:
            logging.error(f"Error generating forecast for {city}: {e}")
            raise
