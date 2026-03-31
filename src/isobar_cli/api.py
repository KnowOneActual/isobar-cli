import json
import time
from enum import Enum
from pathlib import Path
from typing import Optional

import requests
from timezonefinder import TimezoneFinder

from .logic import format_time
from .models import ForecastDay, HourlyForecast, UnitSystem, WeatherData, WeatherUnits

CACHE_DIR = Path.home() / ".cache" / "isobar"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class GeocodingClient:
    BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

    @classmethod
    def search(cls, city: str, count: int = 1) -> list[dict]:
        try:
            response = requests.get(
                f"{cls.BASE_URL}?name={city}&count={count}&format=json"
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except Exception:
            return []


class WeatherClient:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, lat: float, lon: float, timezone: str, metric: bool = False):
        self.lat = lat
        self.lon = lon
        self.timezone = timezone
        self.system = UnitSystem.METRIC if metric else UnitSystem.IMPERIAL
        self.units = WeatherUnits.from_system(self.system)

    def fetch(self) -> dict:
        temp_unit = "celsius" if self.system == UnitSystem.METRIC else "fahrenheit"
        wind_unit = "kmh" if self.system == UnitSystem.METRIC else "mph"
        precip_unit = "mm" if self.system == UnitSystem.METRIC else "inch"

        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "current": "temperature_2m,apparent_temperature,wind_speed_10m,"
            "relative_humidity_2m,precipitation,weather_code,wind_gusts_10m,uv_index",
            "daily": "sunrise,sunset,temperature_2m_max,temperature_2m_min,"
            "weather_code,precipitation_probability_max,uv_index_max",
            "hourly": "precipitation_probability,rain,snowfall,temperature_2m,weather_code",
            "temperature_unit": temp_unit,
            "wind_speed_unit": wind_unit,
            "precipitation_unit": precip_unit,
            "timezone": self.timezone,
            "forecast_days": 7,
        }

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()


class AirQualityClient:
    BASE_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

    @classmethod
    def get_aqi(cls, lat: float, lon: float) -> Optional[int]:
        try:
            response = requests.get(
                f"{cls.BASE_URL}?latitude={lat}&longitude={lon}&current=us_aqi"
            )
            response.raise_for_status()
            return response.json().get("current", {}).get("us_aqi")
        except Exception:
            return None


def get_cached_cities() -> list[str]:
    """Returns a list of unique city names from the local cache history."""
    if not CACHE_DIR.exists():
        return []

    cities = set()
    for f in CACHE_DIR.glob("*.json"):
        name = f.stem
        for suffix in ["_metric", "_imperial"]:
            if name.endswith(suffix):
                name = name[: -len(suffix)]
        cities.add(name.replace("_", " ").title())
    return sorted(cities)


def get_city_suggestions(city: str) -> list[str]:
    """Fetches a list of likely city name matches for a given input string."""
    results = GeocodingClient.search(city, count=5)
    suggestions = []
    for loc in results:
        region = loc.get("admin1", loc.get("country", ""))
        name = f"{loc['name']}, {region}".strip(", ")
        if name not in suggestions:
            suggestions.append(name)
    return suggestions


def get_weather_data(city: str, metric: bool = False) -> Optional[WeatherData]:
    """Coordinates-based weather fetcher with caching and unit awareness."""
    unit_suffix = "_metric" if metric else "_imperial"
    cache_file = CACHE_DIR / f"{city.lower().replace(' ', '_')}{unit_suffix}.json"

    # Cache Check
    if cache_file.exists():
        try:
            data = json.loads(cache_file.read_text())
            if time.time() - data.get("timestamp", 0) < 900:
                # Reconstruct WeatherData from cache
                data["units"] = WeatherUnits(**data["units"])
                data["forecast"] = [ForecastDay(**d) for d in data["forecast"]]
                data["hourly"] = [HourlyForecast(**h) for h in data["hourly"]]
                return WeatherData(**data)
        except (json.JSONDecodeError, TypeError, KeyError):
            pass

    # Geocoding
    results = GeocodingClient.search(city)
    if not results:
        return None

    location = results[0]
    lat, lon = location["latitude"], location["longitude"]
    region = location.get("admin1", location.get("country", ""))
    clean_city_name = f"{location['name']}, {region}".strip(", ")

    # Timezone & Weather
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lat=lat, lng=lon) or "UTC"

    try:
        weather_client = WeatherClient(lat, lon, timezone, metric)
        api_data = weather_client.fetch()
        aqi_value = AirQualityClient.get_aqi(lat, lon)
    except requests.RequestException as e:
        print(f"Error fetching weather: {e}")
        return None

    current = api_data["current"]
    hourly = api_data["hourly"]
    daily = api_data["daily"]

    # Hourly processing
    # Open-Meteo current time might include minutes (e.g. T12:32)
    # while hourly times are typically T12:00.
    target_hour = (
        current["time"][:13] + ":00" if len(current["time"]) >= 13 else current["time"]
    )
    try:
        start_idx = hourly["time"].index(target_hour)
    except ValueError:
        # Fallback: find first hourly slot that is NOT before current hour
        start_idx = 0
        for i, t in enumerate(hourly["time"]):
            if t >= target_hour:
                start_idx = i
                break

    hourly_forecast = [
        HourlyForecast(
            time=hourly["time"][i],
            temp=hourly["temperature_2m"][i],
            weather_code=hourly["weather_code"][i],
            precip_prob=hourly["precipitation_probability"][i],
        )
        for i in range(start_idx, min(start_idx + 24, len(hourly["time"])))
    ]

    # Derived metrics
    next_6h = slice(start_idx, start_idx + 6)
    avg_precip_prob = sum(hourly["precipitation_probability"][next_6h]) / 6
    next_6h_rain = sum(hourly["rain"][next_6h])
    next_6h_snow = sum(hourly["snowfall"][next_6h])

    # Daily forecast
    forecast = [
        ForecastDay(
            date=daily["time"][i],
            high=daily["temperature_2m_max"][i],
            low=daily["temperature_2m_min"][i],
            weather_code=daily["weather_code"][i],
            precip_prob=daily["precipitation_probability_max"][i] or 0,
            uv_index_max=daily.get("uv_index_max", [None] * len(daily["time"]))[i],
        )
        for i in range(len(daily["time"]))
    ]

    now = time.time()
    weather_data = WeatherData(
        city=clean_city_name,
        temp=current["temperature_2m"],
        feels_like=current["apparent_temperature"],
        wind_speed=current["wind_speed_10m"],
        humidity=current["relative_humidity_2m"],
        precipitation=current["precipitation"],
        weather_code=current.get("weather_code", 0),
        precip_prob=round(avg_precip_prob),
        rainfall=next_6h_rain,
        snowfall=next_6h_snow,
        sunrise=format_time(daily["sunrise"][0]),
        sunset=format_time(daily["sunset"][0]),
        forecast=forecast,
        hourly=hourly_forecast,
        units=weather_client.units,
        aqi=aqi_value,
        wind_gust=current.get("wind_gusts_10m"),
        uv_index=current.get("uv_index"),
        last_updated=now,
        timestamp=now,
    )

    # Caching (serialize to dict)
    cache_data = json.loads(
        json.dumps(
            weather_data,
            default=lambda o: o.__dict__ if not isinstance(o, Enum) else o.value,
        )
    )
    cache_file.write_text(json.dumps(cache_data))

    return weather_data
