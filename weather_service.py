import argparse
import constants
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

    data = WeatherService(args.cities.split(",")).generate_bulk_forecast()
    CSVExporter(args.file, data).write_file()
