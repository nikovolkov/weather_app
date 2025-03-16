import csv
import constants
import logging
from datetime import datetime


class CSVExporter:
    def __init__(self, file_name: str):
        self.file_name = file_name

    @property
    def generate_file_name(self) -> str:
        timestamp = datetime.now().strftime("%m%d-%H%M%S")
        return f"{self.file_name}-{timestamp}.csv"

    def export(self, write_method, data) -> None:
        filename = self.generate_file_name
        with open(filename, write_method, newline="") as file:
            writer = csv.writer(file)
            writer.writerow(constants.DEFAULT_CSV_HEADERS)
            writer.writerows(data)
            logging.info(f"Data successfully exported to {filename}")
