import pytest

from isobar_cli import api
from isobar_cli.api import get_city_suggestions, get_weather_data


@pytest.fixture(autouse=True)
def mock_cache_dir(tmp_path, monkeypatch):
    """Ensure tests always use a clean, temporary cache directory."""
    monkeypatch.setattr(api, "CACHE_DIR", tmp_path)


def test_get_weather_data_success(requests_mock):
    # Mock Geocoding API
    geo_data = {
        "results": [
            {
                "name": "Chicago",
                "latitude": 41.85,
                "longitude": -87.65,
                "admin1": "Illinois",
                "country": "United States",
            }
        ]
    }
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=Chicago&count=1&format=json",
        json=geo_data,
    )

    # Mock Air Quality API
    aqi_data = {"current": {"us_aqi": 42}}
    requests_mock.get(
        "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=41.85&longitude=-87.65&current=us_aqi",
        json=aqi_data,
    )

    # Mock Weather API
    weather_data = {
        "current": {
            "time": "2026-02-26T06:00",
            "temperature_2m": 37.1,
            "apparent_temperature": 30.4,
            "wind_speed_10m": 4.3,
            "relative_humidity_2m": 58,
            "precipitation": 0,
            "weather_code": 0,
        },
        "daily": {
            "time": ["2026-02-26"],
            "sunrise": ["2026-02-26T06:29"],
            "sunset": ["2026-02-26T17:37"],
            "temperature_2m_max": [41.7],
            "temperature_2m_min": [23.9],
            "weather_code": [0],
            "precipitation_probability_max": [1],
        },
        "hourly": {
            "time": ["2026-02-26T06:00", "2026-02-26T07:00"],
            "temperature_2m": [37.1, 38.2],
            "weather_code": [0, 1],
            "precipitation_probability": [0, 5],
            "rain": [0, 0],
            "snowfall": [0, 0],
        },
    }
    requests_mock.get("https://api.open-meteo.com/v1/forecast", json=weather_data)

    result = get_weather_data("Chicago")

    assert result["city"] == "Chicago, Illinois"
    assert result["temp"] == 37.1
    assert result["sunrise"] == "6:29 AM"
    assert result["sunset"] == "5:37 PM"
    assert result["units"]["temp"] == "°F"
    assert len(result["hourly"]) > 0
    assert result["hourly"][0]["temp"] == 37.1


def test_get_weather_data_metric(requests_mock):
    # Mock Geocoding API
    geo_data = {
        "results": [
            {
                "name": "London",
                "latitude": 51.5,
                "longitude": -0.12,
                "admin1": "England",
                "country": "United Kingdom",
            }
        ]
    }
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=London&count=1&format=json",
        json=geo_data,
    )

    # Mock Air Quality API
    requests_mock.get(
        "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=51.5&longitude=-0.12&current=us_aqi",
        json={"current": {"us_aqi": 10}},
    )

    # Mock Weather API (Metric)
    weather_data = {
        "current": {
            "time": "2026-02-26T06:00",
            "temperature_2m": 12.5,
            "apparent_temperature": 10.2,
            "wind_speed_10m": 15.0,
            "relative_humidity_2m": 80,
            "precipitation": 0,
            "weather_code": 3,
        },
        "daily": {
            "time": ["2026-02-26"],
            "sunrise": ["2026-02-26T06:45"],
            "sunset": ["2026-02-26T17:35"],
            "temperature_2m_max": [14.0],
            "temperature_2m_min": [8.0],
            "weather_code": [3],
            "precipitation_probability_max": [10],
        },
        "hourly": {
            "time": ["2026-02-26T06:00"],
            "temperature_2m": [12.5],
            "weather_code": [3],
            "precipitation_probability": [0],
            "rain": [0],
            "snowfall": [0],
        },
    }
    requests_mock.get("https://api.open-meteo.com/v1/forecast", json=weather_data)

    result = get_weather_data("London", metric=True)

    assert result["city"] == "London, England"
    assert result["temp"] == 12.5
    assert result["units"]["temp"] == "°C"
    assert result["units"]["wind"] == "km/h"
    assert result["units"]["precip"] == "mm"


def test_get_weather_data_not_found(requests_mock):
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=NonExistentCity&count=1&format=json",
        json={},
    )

    result = get_weather_data("NonExistentCity")
    assert result == {}


def test_get_city_suggestions(requests_mock):
    geo_data = {
        "results": [
            {"name": "Paris", "admin1": "Ile-de-France"},
            {"name": "Paris", "admin1": "Texas"},
        ]
    }
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=Paris&count=5&format=json",
        json=geo_data,
    )

    suggestions = get_city_suggestions("Paris")
    assert "Paris, Ile-de-France" in suggestions
    assert "Paris, Texas" in suggestions
    assert len(suggestions) == 2
