import csv
import constants
from weather_model import WeatherData, WeatherSummary
from datetime import datetime


class CSVExporter:
    def __init__(self, file_name: str, weather_data: list, summary: WeatherSummary):
        self.file_name = file_name
        self.weather_data = weather_data
        self.summary = summary

    @property
    def generate_file_name(self):
        timestamp = datetime.now().strftime("%m%d-%H%M%S")
        return f"{self.file_name}-{timestamp}.csv"

    @staticmethod
    def generate_row(model: WeatherData):
        return [
            model.city,
            model.dt.strftime("%Y-%m-%d %H:%M"),
            model.main.temp,
            model.main.humidity,
            model.wind.speed,
            model.weather[0].main,
        ]

    def write_file(self):
        filename = self.generate_file_name
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(constants.DEFAULT_CSV_HEADERS)
            for weather_data in self.weather_data:
                for forecast in weather_data:
                    row = self.generate_row(forecast)
                    writer.writerow(row)
            writer.writerow(self.summary)
