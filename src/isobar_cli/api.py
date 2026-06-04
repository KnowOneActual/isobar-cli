import json
import time
from enum import Enum
from pathlib import Path
from typing import Optional

import requests
from timezonefinder import TimezoneFinder

from .config import get_aqi_url, get_geocoding_url, get_weather_url
from .logic import format_time
from .models import ForecastDay, HourlyForecast, UnitSystem, WeatherData, WeatherUnits

CACHE_DIR = Path.home() / ".cache" / "isobar"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class WeatherAPIError(Exception):
    """Raised when the weather or geocoding API request fails."""
    pass



class GeocodingClient:
    @classmethod
    def get_base_url(cls) -> str:
        """Get geocoding API URL from configuration."""
        return get_geocoding_url()

    @classmethod
    def search(cls, city: str, count: int = 1) -> list[dict]:
        try:
            response = requests.get(
                f"{cls.get_base_url()}?name={city}&count={count}&format=json",
                timeout=10,
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"Geocoding error for '{city}': {e}") from e
        except Exception as e:
            raise WeatherAPIError(f"Unexpected geocoding error for '{city}': {e}") from e


class WeatherClient:
    @classmethod
    def get_base_url(cls) -> str:
        """Get weather API URL from configuration."""
        return get_weather_url()

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

        response = requests.get(self.get_base_url(), params=params, timeout=15)
        response.raise_for_status()
        return response.json()


class AirQualityClient:
    @classmethod
    def get_base_url(cls) -> str:
        """Get air quality API URL from configuration."""
        return get_aqi_url()

    @classmethod
    def get_aqi(cls, lat: float, lon: float) -> Optional[int]:
        try:
            response = requests.get(
                f"{cls.get_base_url()}?latitude={lat}&longitude={lon}&current=us_aqi",
                timeout=10,
            )
            response.raise_for_status()
            return response.json().get("current", {}).get("us_aqi")
        except requests.exceptions.RequestException as e:
            # Log error for debugging but don't crash
            import sys

            print(f"AQI error for ({lat},{lon}): {e}", file=sys.stderr)
            return None
        except Exception as e:
            # Catch-all for unexpected errors
            import sys

            print(f"Unexpected AQI error for ({lat},{lon}): {e}", file=sys.stderr)
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
    try:
        results = GeocodingClient.search(city, count=5)
    except WeatherAPIError:
        return []
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
        raise WeatherAPIError(f"Error fetching weather: {e}") from e

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
        sunrise=format_time(daily["sunrise"][0], timezone),
        sunset=format_time(daily["sunset"][0], timezone),
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
