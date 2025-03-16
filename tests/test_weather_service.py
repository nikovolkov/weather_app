import pytest
import logging
import statistics
from datetime import datetime
from unittest.mock import MagicMock
from src.weather_service import ReportConstructor, WeatherService


@pytest.fixture
def sample_raw_data():
    mock_forecast = MagicMock()
    mock_forecast.city = "New York"
    mock_forecast.dt = datetime(2025, 3, 16, 12, 0)
    mock_forecast.main.temp = 22.5
    mock_forecast.main.humidity = 60
    mock_forecast.wind.speed = 5.2
    mock_forecast.weather = [MagicMock(main="Clear")]

    return [[mock_forecast]]


def test_generate_data(sample_raw_data):
    report_constructor = ReportConstructor(sample_raw_data)
    expected_data = [["New York", "2025-03-16 12:00", 22.5, 60, 5.2, "Clear"]]
    assert report_constructor.generate_data() == expected_data


def test_generate_data_empty():
    empty_constructor = ReportConstructor([])
    assert empty_constructor.generate_data() == []


def test_logging(sample_raw_data, caplog):
    report_constructor = ReportConstructor(sample_raw_data)
    with caplog.at_level(logging.INFO):
        report_constructor.generate_data()
    assert "Generating structured weather data" in caplog.text
    assert "Structured weather data generation complete" in caplog.text


@pytest.fixture
def sample_summary_data():
    mock_forecast1 = MagicMock()
    mock_forecast1.main.temp = 20.0
    mock_forecast1.main.humidity = 50
    mock_forecast1.wind.speed = 3.0

    mock_forecast2 = MagicMock()
    mock_forecast2.main.temp = 25.0
    mock_forecast2.main.humidity = 70
    mock_forecast2.wind.speed = 6.0

    return [[mock_forecast1, mock_forecast2]]


def test_generate_summary(sample_summary_data):
    report_constructor = ReportConstructor(sample_summary_data)
    summary = report_constructor.generate_summary()

    assert summary.min_temperature == 20.0
    assert summary.max_temperature == 25.0
    assert summary.avg_temperature == statistics.mean([20.0, 25.0])
    assert summary.min_humidity == 50
    assert summary.max_humidity == 70
    assert summary.avg_humidity == statistics.mean([50, 70])
    assert summary.min_wind == 3.0
    assert summary.max_wind == 6.0
    assert summary.avg_wind == statistics.mean([3.0, 6.0])


def test_generate_summary_empty():
    empty_constructor = ReportConstructor([])
    with pytest.raises(ValueError):
        empty_constructor.generate_summary()


def test_summary_logging(sample_summary_data, caplog):
    report_constructor = ReportConstructor(sample_summary_data)
    with caplog.at_level(logging.INFO):
        report_constructor.generate_summary()
    assert "Generating weather summary" in caplog.text
    assert "Weather summary generation complete" in caplog.text


@pytest.fixture
def sample_cities():
    return ["New York", "Los Angeles"]


def test_weather_service_logging(sample_cities, caplog):
    with caplog.at_level(logging.INFO):
        WeatherService(sample_cities)
    assert "WeatherService initialized with cities" in caplog.text
