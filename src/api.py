import requests

def get_weather_data(city: str) -> dict:
    """
    Converts the city name to coordinates, then fetches the weather.
    """
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

        # Added humidity and precipitation to the API request
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,apparent_temperature,wind_speed_10m,relative_humidity_2m,precipitation&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
        
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()["current"]
        
        return {
            "city": clean_city_name,
            "temp": weather_data["temperature_2m"],
            "feels_like": weather_data["apparent_temperature"],
            "wind_speed": weather_data["wind_speed_10m"],
            "humidity": weather_data["relative_humidity_2m"],
            "precipitation": weather_data["precipitation"]
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return {}