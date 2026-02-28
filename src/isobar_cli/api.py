import json
import time
from datetime import datetime
from pathlib import Path

import requests
from timezonefinder import TimezoneFinder

CACHE_DIR = Path.home() / ".cache" / "isobar"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def format_time(iso_string: str) -> str:
    """Convert ISO 8601 datetime to 12-hour format (e.g., '6:42 AM')."""
    if not iso_string:
        return "--"
    try:
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        hour = dt.hour
        minute = dt.minute
        if hour == 0:
            hour_12 = 12
            period = "AM"
        elif hour < 12:
            hour_12 = hour
            period = "AM"
        elif hour == 12:
            hour_12 = 12
            period = "PM"
        else:
            hour_12 = hour - 12
            period = "PM"
        return f"{hour_12}:{minute:02d} {period}"
    except (ValueError, AttributeError):
        return "--"


def get_city_suggestions(city: str) -> list[str]:
    """
    Fetches a list of likely city name matches for a given input string.
    Useful for 'Did you mean?' suggestions.
    """
    url = (
        f"https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count=5&format=json"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "results" not in data:
            return []

        suggestions = []
        for loc in data["results"]:
            region = loc.get("admin1", loc.get("country", ""))
            name = f"{loc['name']}, {region}".strip(", ")
            if name not in suggestions:
                suggestions.append(name)
        return suggestions
    except Exception:
        return []


def get_weather_data(city: str, metric: bool = False) -> dict:
    """
    Converts the city name to coordinates, then fetches the weather with precip
    forecast including rain, snow, sunrise/sunset, WMO weather code, and
    a 7-day daily forecast.
    Timezone is resolved dynamically from lat/lon using timezonefinder.
    """
    unit_suffix = "_metric" if metric else "_imperial"
    cache_file = CACHE_DIR / f"{city.lower().replace(' ', '_')}{unit_suffix}.json"

    # Check cache first
    if cache_file.exists():
        try:
            cache_data = json.loads(cache_file.read_text())
            timestamp = cache_data.get("timestamp", 0)
            if time.time() - timestamp < 900:  # 15 minutes
                # Return data with cache metadata
                cache_data["last_updated"] = timestamp
                return cache_data
        except (json.JSONDecodeError, KeyError, ValueError):
            pass  # Cache invalid, proceed to API

    geo_url = (
        f"https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count=1&format=json"
    )

    try:
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if "results" not in geo_data:
            return {}

        location = geo_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        region = location.get("admin1", location.get("country", ""))
        clean_city_name = f"{location['name']}, {region}".strip(", ")

        # Resolve timezone dynamically from coordinates
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lat=lat, lng=lon) or "UTC"

        # Build weather URL — 7-day daily forecast + current conditions
        temp_unit = "celsius" if metric else "fahrenheit"
        wind_unit = "kmh" if metric else "mph"
        precip_unit = "mm" if metric else "inch"

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"current=temperature_2m,apparent_temperature,wind_speed_10m,"
            f"relative_humidity_2m,precipitation,weather_code&"
            f"daily=sunrise,sunset,temperature_2m_max,temperature_2m_min,"
            f"weather_code,precipitation_probability_max&"
            f"hourly=precipitation_probability,rain,snowfall,temperature_2m,weather_code&"
            f"temperature_unit={temp_unit}&"
            f"wind_speed_unit={wind_unit}&precipitation_unit={precip_unit}&"
            f"timezone={timezone}&forecast_days=7"
        )

        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        api_data = weather_response.json()

        # Build Air Quality URL (separate API)
        aqi_url = (
            f"https://air-quality-api.open-meteo.com/v1/air-quality?"
            f"latitude={lat}&longitude={lon}&current=us_aqi"
        )
        aqi_value = None
        try:
            aqi_response = requests.get(aqi_url)
            aqi_response.raise_for_status()
            aqi_data = aqi_response.json()
            aqi_value = aqi_data.get("current", {}).get("us_aqi")
        except Exception:
            pass  # AQI is non-essential, don't fail if API is down

        current = api_data["current"]
        hourly = api_data["hourly"]
        daily = api_data["daily"]

        # Find the starting index in hourly data that matches current time (rounded down)
        current_time_iso = current["time"]
        try:
            start_idx = hourly["time"].index(current_time_iso)
        except ValueError:
            start_idx = 0

        # Build 24h hourly forecast (from current hour onwards)
        hourly_forecast = []
        for i in range(start_idx, min(start_idx + 24, len(hourly["time"]))):
            hourly_forecast.append(
                {
                    "time": hourly["time"][i],
                    "temp": hourly["temperature_2m"][i],
                    "weather_code": hourly["weather_code"][i],
                    "precip_prob": hourly["precipitation_probability"][i],
                }
            )

        # Next 6 hours precip probability (average)
        next_6h_probs = hourly["precipitation_probability"][start_idx : start_idx + 6]
        avg_precip_prob = (
            sum(next_6h_probs) / len(next_6h_probs) if next_6h_probs else 0
        )

        # Next 6 hours rainfall/snowfall (total inches)
        next_6h_rain = sum(hourly["rain"][start_idx : start_idx + 6])
        next_6h_snow = sum(hourly["snowfall"][start_idx : start_idx + 6])

        # Build 7-day forecast list (index 0 = today)
        num_days = len(daily["time"])
        forecast = []
        for i in range(num_days):
            forecast.append(
                {
                    "date": daily["time"][i],  # YYYY-MM-DD
                    "high": daily["temperature_2m_max"][i],
                    "low": daily["temperature_2m_min"][i],
                    "weather_code": daily["weather_code"][i],
                    "precip_prob": daily["precipitation_probability_max"][i] or 0,
                }
            )

        current_time = time.time()
        result = {
            "city": clean_city_name,
            "temp": current["temperature_2m"],
            "feels_like": current["apparent_temperature"],
            "wind_speed": current["wind_speed_10m"],
            "humidity": current["relative_humidity_2m"],
            "precipitation": current["precipitation"],
            "weather_code": current.get("weather_code", 0),
            "precip_prob": round(avg_precip_prob),  # % chance next 6h
            "rainfall": next_6h_rain,  # Total rain next 6h
            "snowfall": next_6h_snow,  # Total snow next 6h
            "sunrise": format_time(daily["sunrise"][0]),
            "sunset": format_time(daily["sunset"][0]),
            "forecast": forecast,  # List of 7 daily dicts
            "hourly": hourly_forecast,  # Next 24 hours
            "aqi": aqi_value,
            "last_updated": current_time,
            "units": {
                "temp": "°C" if metric else "°F",
                "wind": "km/h" if metric else "mph",
                "precip": "mm" if metric else "in",
            },
        }

        # Cache successful result
        result_with_ts = result.copy()
        result_with_ts["timestamp"] = current_time
        cache_file.write_text(json.dumps(result_with_ts))

        return result

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return {}
