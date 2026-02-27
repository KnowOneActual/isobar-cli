import json
import pytest
import requests_mock
from isobar_cli.api import get_weather_data

def test_get_weather_data_success(requests_mock):
    # Mock Geocoding API
    geo_data = {
        "results": [
            {
                "name": "Chicago",
                "latitude": 41.85,
                "longitude": -87.65,
                "admin1": "Illinois",
                "country": "United States"
            }
        ]
    }
    requests_mock.get("https://geocoding-api.open-meteo.com/v1/search?name=Chicago&count=1&format=json", json=geo_data)

    # Mock Weather API
    weather_data = {
        "current": {
            "temperature_2m": 37.1,
            "apparent_temperature": 30.4,
            "wind_speed_10m": 4.3,
            "relative_humidity_2m": 58,
            "precipitation": 0,
            "weather_code": 0
        },
        "daily": {
            "time": ["2026-02-26"],
            "sunrise": ["2026-02-26T06:29"],
            "sunset": ["2026-02-26T17:37"],
            "temperature_2m_max": [41.7],
            "temperature_2m_min": [23.9],
            "weather_code": [0],
            "precipitation_probability_max": [1]
        },
        "hourly": {
            "precipitation_probability": [0, 0, 0, 0, 0, 0],
            "rain": [0, 0, 0, 0, 0, 0],
            "snowfall": [0, 0, 0, 0, 0, 0]
        }
    }
    # Using real_http=True for local files (like timezonefinder) if needed, 
    # but here we just mock the URL with params
    requests_mock.get("https://api.open-meteo.com/v1/forecast", json=weather_data)

    result = get_weather_data("Chicago")
    
    assert result["city"] == "Chicago, Illinois"
    assert result["temp"] == 37.1
    assert result["sunrise"] == "6:29 AM"
    assert result["sunset"] == "5:37 PM"

def test_get_weather_data_not_found(requests_mock):
    requests_mock.get("https://geocoding-api.open-meteo.com/v1/search?name=NonExistentCity&count=1&format=json", json={})
    
    result = get_weather_data("NonExistentCity")
    assert result == {}
