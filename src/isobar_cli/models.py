from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class UnitSystem(Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"


@dataclass(frozen=True)
class WeatherUnits:
    temp: str  # °C or °F
    wind: str  # km/h or mph
    precip: str  # mm or in

    @classmethod
    def from_system(cls, system: UnitSystem) -> "WeatherUnits":
        if system == UnitSystem.METRIC:
            return cls(temp="°C", wind="km/h", precip="mm")
        return cls(temp="°F", wind="mph", precip="in")


@dataclass(frozen=True)
class ForecastDay:
    date: str  # YYYY-MM-DD
    high: float
    low: float
    weather_code: int
    precip_prob: int
    uv_index_max: Optional[float] = None

    @property
    def dt(self) -> datetime:
        return datetime.strptime(self.date, "%Y-%m-%d")


@dataclass(frozen=True)
class HourlyForecast:
    time: str  # ISO 8601
    temp: float
    weather_code: int
    precip_prob: int

    @property
    def dt(self) -> datetime:
        return datetime.fromisoformat(self.time.replace("Z", "+00:00"))


@dataclass(frozen=True)
class WeatherData:
    city: str
    temp: float
    feels_like: float
    wind_speed: float
    humidity: int
    precipitation: float
    weather_code: int
    precip_prob: int  # % chance next 6h
    rainfall: float  # Total rain next 6h
    snowfall: float  # Total snow next 6h
    sunrise: str  # Formatted time
    sunset: str  # Formatted time
    forecast: list[ForecastDay]
    hourly: list[HourlyForecast]
    units: WeatherUnits
    aqi: Optional[int] = None
    wind_gust: Optional[float] = None
    uv_index: Optional[float] = None
    previous_day_temp: Optional[float] = None
    last_updated: float = field(default_factory=lambda: 0.0)
    timestamp: float = field(default_factory=lambda: 0.0)
