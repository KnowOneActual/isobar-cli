import requests
import json
import time
from pathlib import Path
from typing import Dict, Any

CACHE_DIR = Path.home() / ".cache" / "isobar"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_weather_data(city: str) -> dict:
    """
    Fetches weather data with 15-minute local caching.
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
    
    # API call (existing logic)
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
    
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,apparent_temperature,wind_speed_10m,relative_humidity_2m,precipitation&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
        
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()["current"]
        
        result = {
            "city": clean_city_name,
            "temp": weather_data["temperature_2m"],
            "feels_like": weather_data["apparent_temperature"],
            "wind_speed": weather_data["wind_speed_10m"],
            "humidity": weather_data["relative_humidity_2m"],
            "precipitation": weather_data["precipitation"]
        }
        
        # Cache successful result
        result_with_ts = result.copy()
        result_with_ts["timestamp"] = time.time()
        cache_file.write_text(json.dumps(result_with_ts))
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return {}
