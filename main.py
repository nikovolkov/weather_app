import argparse
import boto3
import csv
import os
import more_itertools
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("WEATHER_API_KEY")
default_cities = "London,Moscow,Paris,New-York,Berlin,Batumi,\
    Sochi,Rome,Helsinki,Saint-Petersburg"

parser = argparse.ArgumentParser(description="pass the list of cities to get forecast")
parser.add_argument(
    "-c",
    "--cities",
    type=str,
    default=default_cities,
    help="enter cities list with comma delimeter",
)
parser.add_argument(
    "-f",
    "--file",
    type=str,
    default="weekly_forecast.csv",
    help="name of the output file",
)
parser.add_argument(
    "-b", "--bucket", type=str, default=None, help="to upload file specify name of the bucket"
)
args = parser.parse_args()
city_list = args.cities.split(",")


class Forecast:
    def __init__(self, city, date, temp, humidity, wind, description):
        self.date = date
        self.city = city
        self.temp = temp
        self.humidity = humidity
        self.wind = wind
        self.description = description

    def __str__(self):
        return f"{self.date},{self.city},{self.temp},{self.humidity},{self.wind},{self.description}"


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

    def get_weather_info(self) -> list:
        coords = self.get_coords()
        query = f"lat={coords['lat']}&lon={coords['lon']}&units=metric&&appid={api_key}"
        response = requests.get(f"{type(self).endpoint}/data/2.5/forecast?{query}")
        return response.json()["list"]

    def get_forecast(self) -> list:
        forecast = []
        for item in self.get_weather_info():
            timestamp = item["dt"]
            date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
            temp = item["main"]["temp"]
            humidity = item["main"]["humidity"]
            wind = item["wind"]["speed"]
            description = item["weather"][0]["description"]
            forecast.append(
                Forecast(self.city_name, date, temp, humidity, wind, description)
            )
        return forecast


class WeeklyForecast:
    def __init__(self, city_list):
        self.city_list = city_list

    def generate_forecast(self):
        weekly_forecast = []
        for city in self.city_list:
            forecast = CityWeather(city).get_forecast()
            weekly_forecast.append(forecast)
        return weekly_forecast

    def generate_csv(self):
        lines = list(more_itertools.flatten(self.generate_forecast()))
        with open(args.file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Date", "City", "Temperature", "Humidity", "Wind", "Description"]
            )
            for line in lines:
                writer.writerow([str(line)])
    @staticmethod
    def s3_upload():
        s3 = boto3.resource("s3").Bucket(args.bucket)
        s3.upload_file(args.file, f"forecasts/{args.file}")


if __name__ == "__main__":
    WeeklyForecast(city_list).generate_csv()

if args.bucket is not None:
    WeeklyForecast.s3_upload()
