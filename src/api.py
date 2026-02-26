import json
import time
from datetime import datetime
from pathlib import Path

import requests

CACHE_DIR = Path.home() / ".cache" / "isobar"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_weather_data(city: str) -> dict:
    """
    Converts the city name to coordinates, then fetches the weather with precip
    forecast including rain, snow, sunrise/sunset.
    """
    cache_file = CACHE_DIR / f"{city.lower().replace(' ', '_')}.json"

    # Check cache first
    if cache_file.exists():
        try:
            cache_data = json.loads(cache_file.read_text())
            if time.time() - cache_data["timestamp"] < 900:  # 15 minutes
                del cache_data["timestamp"]  # Clean up before return
                return cache_data
        except (json.JSONDecodeError, KeyError, ValueError):
            pass  # Cache invalid, proceed to API

    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&format=json"

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

        # Updated URL with sunrise/sunset
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"current=temperature_2m,apparent_temperature,wind_speed_10m,"
            f"relative_humidity_2m,precipitation&"
            f"daily=sunrise,sunset&"
            f"hourly=precipitation_probability,rain,snowfall&"
            f"temperature_unit=fahrenheit&"
            f"wind_speed_unit=mph&precipitation_unit=inch&"
            f"timezone=America/Chicago&forecast_days=2"
        )

        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        api_data = weather_response.json()
        current = api_data["current"]
        hourly = api_data["hourly"]
        daily = api_data["daily"]

        # Sunrise/Sunset (today's local time)
        sunrise = daily["sunrise"][0].split("T")[1][:5]  # HH:MM
        sunset = daily["sunset"][0].split("T")[1][:5]    # HH:MM

        # Next 6 hours precip probability (average)
        next_6h_probs = hourly["precipitation_probability"][:6]
        avg_precip_prob = (
            sum(next_6h_probs) / len(next_6h_probs) if next_6h_probs else 0
        )

        # Next 6 hours rainfall/snowfall (total inches)
        next_6h_rain = sum(hourly["rain"][:6])
        next_6h_snow = sum(hourly["snowfall"][:6])

        # Parse sunrise/sunset times (today's data is first in array)
        sunrise_iso = daily["sunrise"][0]
        sunset_iso = daily["sunset"][0]
        
        # Format times (API returns ISO 8601 format in local timezone)
        def format_time(iso_string: str) -> str:
            """Convert ISO 8601 datetime to 12-hour format (e.g., '6:42 AM')."""
            if not iso_string:
                return "--"
            try:
                dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
                hour = dt.hour
                minute = dt.minute
                
                # Convert to 12-hour format
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

        result = {
            "city": clean_city_name,
            "temp": current["temperature_2m"],
            "feels_like": current["apparent_temperature"],
            "wind_speed": current["wind_speed_10m"],
            "humidity": current["relative_humidity_2m"],
            "precipitation": current["precipitation"],
            "precip_prob": round(avg_precip_prob),  # % chance next 6h
            "rainfall_inch": next_6h_rain,  # Total rain inches next 6h
            "snowfall_inch": next_6h_snow,  # Total snow inches next 6h
            "sunrise": sunrise,
            "sunset": sunset,
        }

        # Cache successful result
        result_with_ts = result.copy()
        result_with_ts["timestamp"] = time.time()
        cache_file.write_text(json.dumps(result_with_ts))

        return result

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return {}
