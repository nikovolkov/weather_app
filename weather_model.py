from pydantic import BaseModel
from typing import List
from datetime import datetime
from typing import Optional


class CityCoords(BaseModel):
    lat: float
    lon: float


class Main(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    sea_level: int
    grnd_level: int
    humidity: int
    temp_kf: float


class Weather(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class Clouds(BaseModel):
    all: int


class Wind(BaseModel):
    speed: float
    deg: int
    gust: float


class Sys(BaseModel):
    pod: str


class WeatherData(BaseModel):
    dt: datetime
    city: str
    main: Main
    weather: List[Weather]
    clouds: Clouds
    wind: Wind
    visibility: Optional[int] = None
    pop: float
    sys: Sys
    dt_txt: str


class WeatherSummary(BaseModel):
    min_temperature: float
    max_temperature: float
    avg_temperature: float
    min_humidity: int
    max_humidity: int
    avg_humidity: float
    min_wind: float
    max_wind: float
    avg_wind: float
