import argparse
import constants
import logging
import statistics
from datetime import datetime
from weather_model import WeatherSummary
from weather_repository import WeatherRepository
from concurrent.futures import ThreadPoolExecutor
from exporter import CSVExporter


class WeatherService:
    def __init__(self, cities: list):
        self.cities = cities
        logging.info(f"WeatherService initialized with cities: {cities}")

    def generate_bulk_forecast(self) -> list:
        weather_repo = WeatherRepository()
        logging.info("Starting bulk forecast generation")
        with ThreadPoolExecutor() as executor:
            bulk_forecast = list(
                executor.map(weather_repo.generate_forecast, self.cities)
            )
        logging.info("Bulk forecast generation complete")
        return bulk_forecast


class ReportConstructor:
    def __init__(self, raw_data: list):
        self.raw_data = raw_data

    def generate_data(self) -> list:
        logging.info("Generating structured weather data")
        data = []
        for weather_data in self.raw_data:
            for forecast in weather_data:
                model = [
                    forecast.city,
                    forecast.dt.strftime("%Y-%m-%d %H:%M"),
                    forecast.main.temp,
                    forecast.main.humidity,
                    forecast.wind.speed,
                    forecast.weather[0].main,
                ]
                data.append(model)
        logging.info("Structured weather data generation complete")
        return data

    def generate_summary(self) -> WeatherSummary:
        logging.info("Generating weather summary")
        temperatures = []
        humidities = []
        winds = []

        for weather_data in self.raw_data:
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
        logging.info("Weather summary generation complete")
        return summary

    def full_weather_report(self) -> list:
        logging.info("Generating full weather report")
        report = self.generate_data() + [self.generate_summary()]
        logging.info("Full weather report generated successfully")
        return report


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

    logging.basicConfig(
        level=logging.INFO,
        filename=f"weather_service-{datetime.now().strftime('%m%d-%H%M%S')}.log",
        filemode="w",
        format="%(asctime)s %(levelname)s %(message)s",
    )

    weather_raw_data = WeatherService(args.cities.split(",")).generate_bulk_forecast()
    weather_data = ReportConstructor(weather_raw_data).full_weather_report()
    export_file = CSVExporter(args.file)
    export_file.export("w", weather_data)
