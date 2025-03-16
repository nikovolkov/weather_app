import pytest
import os
import src.constants
from unittest.mock import MagicMock
from src.weather_repository import WeatherRepository


@pytest.fixture
def mock_environment():
    os.environ["WEATHER_API_KEY"] = "test-api-key"
    yield
    del os.environ["WEATHER_API_KEY"]


@pytest.fixture
def mock_requests_sync(mocker):
    mock_request_instance = MagicMock()
    mocker.patch("weather_repository.RequestsSync", return_value=mock_request_instance)
    return mock_request_instance


@pytest.fixture
def mock_city_coords(mocker):
    return mocker.patch("weather_model.CityCoords")


@pytest.fixture
def mock_weather_data(mocker):
    return mocker.patch("weather_model.WeatherData")


def test_get_city_coords(mock_environment, mock_requests_sync, mock_city_coords):
    mock_repo = WeatherRepository()
    mock_response = [
        {
            "name": "New York County",
            "local_names": {"en": "New York"},
            "lat": 40.7127281,
            "lon": -74.0060152,
            "country": "US",
            "state": "New York",
        }
    ]
    mock_requests_sync.send_request.return_value = mock_response

    mock_coords = MagicMock()
    mock_coords.lat = 40.7127281
    mock_coords.lon = -74.0060152
    mock_city_coords.return_value = mock_coords

    city = "New York"
    coords = mock_repo.get_city_coords(city)

    mock_requests_sync.return_value.send_request.assert_called_once_with(
        endpoint=src.constants.GEO_API_PATH, params={"appid": "test-api-key", "q": city}
    )

    mock_city_coords.assert_called_once_with(**mock_response[0])

    assert coords.lat == 40.7127281
    assert coords.lon == -74.0060152


def test_get_city_weather_data(mock_environment, mock_requests_sync):
    # Setup mock response
    mock_repo = WeatherRepository()
    mock_coords = MagicMock()
    mock_coords.lat = 40.7128
    mock_coords.lon = -74.0060
    mock_repo.get_city_coords = MagicMock(return_value=mock_coords)
    mock_response = {
        "list": [
            {
                "dt": 1618317040,
                "main": {"temp": 285.13},
                "weather": [{"description": "clear sky"}],
            }
        ]
    }
    mock_requests_sync.return_value.send_request.return_value = mock_response

    city = "New York"
    weather_data = mock_repo.get_city_weather_data(city)

    mock_requests_sync.return_value.send_request.assert_called_once()
    assert len(weather_data) == 1
    assert weather_data[0]["weather"][0]["description"] == "clear sky"


def test_generate_forecast(mock_environment, mock_requests_sync, mock_weather_data):
    mock_repo = WeatherRepository()
    mock_coords = MagicMock()
    mock_coords.lat = 40.7128
    mock_coords.lon = -74.0060
    mock_repo.get_city_coords = MagicMock(return_value=mock_coords)
    mock_response = {
        "list": [
            {
                "dt": 1618317040,
                "main": {"temp": 285.13},
                "weather": [{"description": "clear sky"}],
            }
        ]
    }
    mock_requests_sync.return_value.send_request.return_value = mock_response

    mock_weather = MagicMock()
    mock_weather_data.return_value = mock_weather

    city = "New York"
    forecast = mock_repo.generate_forecast(city)

    mock_weather_data.assert_called_once_with(**mock_response["list"][0], city=city)
    assert len(forecast) == 1
    assert forecast[0] == mock_weather


def test_generate_forecast_error(mock_environment, mock_requests_sync):
    mock_repo = WeatherRepository()
    mock_coords = MagicMock()
    mock_coords.lat = 40.7128
    mock_coords.lon = None
    mock_repo.get_city_coords = MagicMock(return_value=mock_coords)
    mock_response = {"list": []}
    mock_requests_sync.return_value.send_request.return_value = mock_response

    with pytest.raises(Exception):
        mock_repo.generate_forecast("New York")
