import argparse
import constants
import statistics
from weather_model import WeatherSummary
from weather_repository import WeatherRepository
from concurrent.futures import ThreadPoolExecutor
from exporter import CSVExporter


class WeatherService:
    def __init__(self, cities: list):
        self.cities = cities

    def generate_bulk_forecast(self) -> list:
        weather_repo = WeatherRepository()
        with ThreadPoolExecutor() as executor:
            return list(executor.map(weather_repo.generate_forecast, self.cities))

    @staticmethod
    def generate_summary(weather_repo: list):
        temperatures = []
        humidities = []
        winds = []

        for weather_data in weather_repo:
            for forecast in weather_data:
                temperatures.append(forecast.main.temp)
                humidities.append(forecast.main.humidity)
                winds.append(forecast.wind.speed)

        summary = WeatherSummary(
            min_temperature=min(temperatures),
            max_temperature=max(temperatures),
            avg_temperature=statistics.mean(temperatures),
            min_humidity=min(humidities),
            max_humidity=max(humidities),
            avg_humidity=statistics.mean(humidities),
            min_wind=min(winds),
            max_wind=max(winds),
            avg_wind=statistics.mean(winds),
        )
        return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="pass the list of cities to get forecast"
    )
    parser.add_argument(
        "-c",
        "--cities",
        type=str,
        default=constants.DEFAULT_CITIES,
        help="enter cities list with comma delimeter",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="weekly_forecast",
        help="name of the output file",
    )
    parser.add_argument(
        "-b",
        "--bucket",
        type=str,
        default=None,
        help="to upload file specify name of the bucket",
    )
    args = parser.parse_args()

    weather_data = WeatherService(args.cities.split(",")).generate_bulk_forecast()
    summary = WeatherService.generate_summary(weather_data)
    CSVExporter(args.file, weather_data, summary).write_file()
