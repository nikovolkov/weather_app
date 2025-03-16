import pytest
from src import constants
from freezegun import freeze_time
from src.exporter import CSVExporter
from unittest.mock import mock_open, patch


@pytest.fixture
def mock_constants():
    """Mocking DEFAULT_CSV_HEADERS."""
    with patch(
        "constants.DEFAULT_CSV_HEADERS",
        ["City", "Date", "Temperature", "Humidity", "Wind", "Description"],
    ):
        yield


@freeze_time("2024-03-16 14:30:00")
def test_generate_file_name():
    exporter = CSVExporter("test_file")
    assert exporter.generate_file_name == "test_file-0316-143000.csv"


@patch("builtins.open", new_callable=mock_open)
@patch("csv.writer")
@freeze_time("2025-03-16 15:00:00")
def test_export_weather_data(mock_csv_writer, mock_open_file, mock_constants):
    """Test if CSVExporter writes the weather data correctly."""

    weather_data = [
        ["London", "2025-03-16 15:00", "8.94", "51", "4.79", "Clouds"],
        ["Moscow", "2025-03-16 15:00", "1", "24", "2.58", "Clear"],
    ]
    exporter = CSVExporter("weather_test")

    exporter.export("w", weather_data)
    expected_filename = "weather_test-0316-150000.csv"

    # Ensure open was called with the expected filename and write mode
    mock_open_file.assert_called_once_with(expected_filename, "w", newline="")

    # Check if csv.writer was called correctly
    mock_csv_writer_instance = mock_csv_writer.return_value
    mock_csv_writer_instance.writerow.assert_called_once_with(
        ["City", "Date", "Temperature", "Humidity", "Wind", "Description"]
    )
    mock_csv_writer_instance.writerows.assert_called_once_with(weather_data)
