import requests
import json
import time
from pathlib import Path
from typing import Dict, Any

CACHE_DIR = Path.home() / ".cache" / "isobar"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_weather_data(city: str) -> dict:
    """
    Converts the city name to coordinates, then fetches the weather with precip forecast.
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

        # Updated URL: adds hourly precip prob + snow, 2-day forecast
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,apparent_temperature,wind_speed_10m,relative_humidity_2m,precipitation&hourly=precipitation_probability,snowfall&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&forecast_days=2"
        
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        api_data = weather_response.json()
        current = api_data["current"]
        hourly = api_data["hourly"]
        
        # Next 6 hours precip probability (average)
        next_6h_probs = hourly["precipitation_probability"][:6]
        avg_precip_prob = sum(next_6h_probs) / len(next_6h_probs) if next_6h_probs else 0
        
        # Next 6 hours snowfall (total cm)
        next_6h_snow = sum(hourly["snowfall"][:6])
        
        result = {
            "city": clean_city_name,
            "temp": current["temperature_2m"],
            "feels_like": current["apparent_temperature"],
            "wind_speed": current["wind_speed_10m"],
            "humidity": current["relative_humidity_2m"],
            "precipitation": current["precipitation"],
            "precip_prob": round(avg_precip_prob),  # % chance next 6h
            "snowfall_cm": next_6h_snow  # Total snow cm next 6h
        }
        
        # Cache successful result
        result_with_ts = result.copy()
        result_with_ts["timestamp"] = time.time()
        cache_file.write_text(json.dumps(result_with_ts))
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return {}
