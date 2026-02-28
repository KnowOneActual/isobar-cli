import json
import time

import pytest
from typer.testing import CliRunner

from isobar_cli import api, ui
from isobar_cli.api import (
    format_time,
    get_cached_cities,
    get_city_suggestions,
    get_weather_data,
)
from isobar_cli.main import app

runner = CliRunner()

@pytest.fixture
def mock_cache_dir(tmp_path, monkeypatch):
    """Ensure tests always use a clean, temporary cache directory."""
    monkeypatch.setattr(api, "CACHE_DIR", tmp_path)
    return tmp_path

# --- API Tests ---

def test_get_cached_cities_not_exists(monkeypatch, tmp_path):
    non_existent = tmp_path / "does_not_exist"
    monkeypatch.setattr(api, "CACHE_DIR", non_existent)
    assert get_cached_cities() == []

def test_format_time_edge_cases():
    assert format_time("") == "--"
    assert format_time(None) == "--"
    assert format_time("invalid-date") == "--"
    # 12 AM case
    assert format_time("2026-02-28T00:00:00Z") == "12:00 AM"
    # 12 PM case
    assert format_time("2026-02-28T12:00:00Z") == "12:00 PM"
    # PM case
    assert format_time("2026-02-28T13:00:00Z") == "1:00 PM"
    # AM case
    assert format_time("2026-02-28T08:00:00Z") == "8:00 AM"

def test_get_city_suggestions_no_results(requests_mock):
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=EmptyCity&count=5&format=json",
        json={"some_other_key": []}
    )
    assert get_city_suggestions("EmptyCity") == []

def test_get_city_suggestions_exception(requests_mock):
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=ErrorCity&count=5&format=json",
        exc=Exception("Connection error")
    )
    assert get_city_suggestions("ErrorCity") == []

def test_get_weather_data_cache_hit(mock_cache_dir, requests_mock):
    city = "CacheCity"
    cache_file = mock_cache_dir / "cachecity_imperial.json"
    cache_data = {
        "city": "CacheCity, TestState",
        "temp": 50,
        "timestamp": time.time() - 100 # 100 seconds ago
    }
    cache_file.write_text(json.dumps(cache_data))

    result = get_weather_data(city)
    assert result["city"] == "CacheCity, TestState"
    assert "last_updated" in result

def test_get_weather_data_cache_invalid_json(mock_cache_dir, requests_mock):
    # This should trigger the API call since cache is invalid
    city = "InvalidCache"
    cache_file = mock_cache_dir / "invalidcache_imperial.json"
    cache_file.write_text("not json")

    # Mock Geocoding API to return {} so we can see it proceeded
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=InvalidCache&count=1&format=json",
        json={}
    )
    result = get_weather_data(city)
    assert result == {}

def test_get_weather_data_aqi_error(requests_mock):
    # Mock Geocoding API
    geo_data = {"results": [{"name": "AQIFail", "latitude": 0, "longitude": 0}]}
    requests_mock.get("https://geocoding-api.open-meteo.com/v1/search?name=AQIFail&count=1&format=json", json=geo_data)

    # Mock Weather API
    weather_data = {
        "current": {"time": "2026-02-26T06:00", "temperature_2m": 37, "apparent_temperature": 30, "wind_speed_10m": 4, "relative_humidity_2m": 50, "precipitation": 0, "weather_code": 0},
        "daily": {"time": ["2026-02-26"], "sunrise": ["2026-02-26T06:00"], "sunset": ["2026-02-26T18:00"], "temperature_2m_max": [40], "temperature_2m_min": [30], "weather_code": [0], "precipitation_probability_max": [0]},
        "hourly": {"time": ["2026-02-26T06:00"], "temperature_2m": [37], "weather_code": [0], "precipitation_probability": [0], "rain": [0], "snowfall": [0]}
    }
    requests_mock.get("https://api.open-meteo.com/v1/forecast", json=weather_data)

    # Mock AQI API to fail - explicitly raise Exception to hit 'except Exception: pass'
    requests_mock.get("https://air-quality-api.open-meteo.com/v1/air-quality", exc=Exception("AQI Failed"))

    result = get_weather_data("AQIFail")
    assert result["aqi"] is None

def test_get_weather_data_hourly_index_error(requests_mock):
    # Mock Geocoding API
    geo_data = {"results": [{"name": "IndexError", "latitude": 0, "longitude": 0}]}
    requests_mock.get("https://geocoding-api.open-meteo.com/v1/search?name=IndexError&count=1&format=json", json=geo_data)

    # Mock Weather API where current time is NOT in hourly time list
    weather_data = {
        "current": {"time": "2026-02-26T06:00", "temperature_2m": 37, "apparent_temperature": 30, "wind_speed_10m": 4, "relative_humidity_2m": 50, "precipitation": 0, "weather_code": 0},
        "daily": {"time": ["2026-02-26"], "sunrise": ["2026-02-26T06:00"], "sunset": ["2026-02-26T18:00"], "temperature_2m_max": [40], "temperature_2m_min": [30], "weather_code": [0], "precipitation_probability_max": [0]},
        "hourly": {"time": ["2026-02-26T07:00"], "temperature_2m": [37], "weather_code": [0], "precipitation_probability": [0], "rain": [0], "snowfall": [0]}
    }
    requests_mock.get("https://api.open-meteo.com/v1/forecast", json=weather_data)
    requests_mock.get("https://air-quality-api.open-meteo.com/v1/air-quality", json={})

    result = get_weather_data("IndexError")
    assert len(result["hourly"]) == 1 # Should fallback to index 0

def test_get_weather_data_request_exception(requests_mock):
    import requests
    requests_mock.get("https://geocoding-api.open-meteo.com/v1/search", exc=requests.exceptions.RequestException("Connection error"))
    result = get_weather_data("FailCity")
    assert result == {}

# --- Main Tests ---

def test_main_auto_location_fail(monkeypatch):
    monkeypatch.setattr("isobar_cli.main.get_auto_location", lambda: None)
    # Mock get_weather_data to avoid real API call
    monkeypatch.setattr("isobar_cli.main.get_weather_data", lambda city, metric=False: {
        "city": "Chicago",
        "temp": 30,
        "feels_like": 25,
        "wind_speed": 10,
        "humidity": 50,
        "precipitation": 0,
        "weather_code": 0,
        "precip_prob": 10,
        "rainfall": 0,
        "snowfall": 0,
        "sunrise": "6:00 AM",
        "sunset": "6:00 PM",
        "units": {"temp": "F", "wind": "mph", "precip": "in"}
    })

    result = runner.invoke(app, [], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert "Could not detect location" in result.output
    assert "Using Chicago as default" in result.output

def test_main_auto_location_success(monkeypatch):
    monkeypatch.setattr("isobar_cli.main.get_auto_location", lambda: "New York")
    monkeypatch.setattr("isobar_cli.main.get_weather_data", lambda city, metric=False: {
        "city": "New York",
        "temp": 30,
        "feels_like": 25,
        "wind_speed": 10,
        "humidity": 50,
        "precipitation": 0,
        "weather_code": 0,
        "precip_prob": 10,
        "rainfall": 0,
        "snowfall": 0,
        "sunrise": "6:00 AM",
        "sunset": "6:00 PM",
        "units": {"temp": "F", "wind": "mph", "precip": "in"}
    })

    result = runner.invoke(app, [], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert "Detected: New York" in result.output

def test_main_city_option(monkeypatch):
    monkeypatch.setattr("isobar_cli.main.get_weather_data", lambda city, metric=False: {
        "city": city,
        "temp": 30,
        "feels_like": 25,
        "wind_speed": 10,
        "humidity": 50,
        "precipitation": 0,
        "weather_code": 0,
        "precip_prob": 10,
        "rainfall": 0,
        "snowfall": 0,
        "sunrise": "6:00 AM",
        "sunset": "6:00 PM",
        "units": {"temp": "F", "wind": "mph", "precip": "in"}
    })
    result = runner.invoke(app, ["--city", "Tokyo"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert "Tokyo" in result.output

def test_city_complete(monkeypatch):
    from isobar_cli.main import city_complete
    monkeypatch.setattr("isobar_cli.main.get_cached_cities", lambda: ["Chicago", "London", "Los Angeles"])
    assert city_complete("Chi") == ["Chicago"]
    assert city_complete("lo") == ["London", "Los Angeles"]

def test_main_with_flags(monkeypatch):
    # Mock data with all necessary keys
    mock_data = {
        "city": "TestCity",
        "temp": 30,
        "feels_like": 25,
        "wind_speed": 10,
        "humidity": 50,
        "precipitation": 0,
        "weather_code": 0,
        "precip_prob": 10,
        "rainfall": 0,
        "snowfall": 0,
        "sunrise": "6:00 AM",
        "sunset": "6:00 PM",
        "forecast": [{"date": "2026-02-28", "high": 40, "low": 30, "weather_code": 0, "precip_prob": 10}],
        "hourly": [{"time": "2026-02-28T12:00", "temp": 30, "weather_code": 0, "precip_prob": 10}],
        "units": {"temp": "F", "wind": "mph", "precip": "in"}
    }
    monkeypatch.setattr("isobar_cli.main.get_weather_data", lambda city, metric=False: {**mock_data, "city": city})

    # Multi-city
    result = runner.invoke(app, ["City1", "City2"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert result.exit_code == 0
    assert "City1" in result.output
    assert "City2" in result.output

    # Multi-city with flags (covers line 130 in main.py)
    result = runner.invoke(app, ["City1", "City2", "--hourly"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert result.exit_code == 0
    assert "───────────────────────────────────────" in result.output

    # Hourly
    result = runner.invoke(app, ["CityH", "--hourly"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert result.exit_code == 0
    assert "Hourly Forecast — CityH" in result.output

    # Forecast
    result = runner.invoke(app, ["CityF", "--forecast"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert result.exit_code == 0
    assert "7-Day Forecast — CityF" in result.output

# --- UI Tests ---

def test_display_weather_edge_cases():
    # No data
    ui.display_weather({})

    # Old cache
    data = {
        "city": "OldCache",
        "temp": 50,
        "last_updated": time.time() - 3600,
        "units": {"temp": "F", "wind": "mph", "precip": "in"}
    }
    ui.display_weather(data)

def test_display_multi_weather_edge_cases():
    # No tables
    ui.display_multi_weather([{}, {}])

def test_build_weather_table_precip_rows():
    from isobar_cli.ui import build_weather_table
    data = {
        "city": "Precip", "temp": 50,
        "rainfall": 0.5, "snowfall": 0.5,
        "units": {"temp": "F", "wind": "mph", "precip": "in"}
    }
    table = build_weather_table(data)
    # Check if Rain Expected and Snow Expected are in the table
    rows_str = "".join(str(row) for row in table.columns[1]._cells)
    assert "Rain Expected" in rows_str
    assert "Snow Expected" in rows_str

def test_display_forecast_date_parse_error():
    data = {
        "city": "Test",
        "forecast": [{"date": "invalid", "weather_code": 0, "high": 50, "low": 40, "precip_prob": 0}],
        "units": {"temp": "F", "wind": "mph", "precip": "in"}
    }
    ui.display_forecast(data)

def test_display_hourly_time_parse_error():
    data = {
        "city": "Test",
        "hourly": [{"time": "invalid", "weather_code": 0, "temp": 50, "precip_prob": 0}],
        "units": {"temp": "F", "wind": "mph", "precip": "in"}
    }
    ui.display_hourly(data)

def test_display_weather_full(monkeypatch):
    # Just to execute the code paths
    data = {
        "city": "Test City",
        "temp": 70,
        "feels_like": 75,
        "wind_speed": 10,
        "humidity": 50,
        "precipitation": 0,
        "weather_code": 0,
        "precip_prob": 10,
        "rainfall": 0,
        "snowfall": 0,
        "sunrise": "6:00 AM",
        "sunset": "6:00 PM",
        "aqi": 50,
        "units": {"temp": "°F", "wind": "mph", "precip": "in"}
    }
    ui.display_weather(data)

def test_display_forecast_full():
    data = {
        "city": "Test City",
        "forecast": [
            {"date": "2026-02-28", "high": 80, "low": 60, "weather_code": 0, "precip_prob": 10},
            {"date": "invalid-date", "high": 80, "low": 60, "weather_code": 0, "precip_prob": 10}
        ],
        "units": {"temp": "°F", "wind": "mph", "precip": "in"}
    }
    ui.display_forecast(data)

def test_display_hourly_full():
    data = {
        "city": "Test City",
        "hourly": [
            {"time": "2026-02-28T12:00", "temp": 70, "weather_code": 0, "precip_prob": 10},
            {"time": "invalid-time", "temp": 70, "weather_code": 0, "precip_prob": 10}
        ],
        "units": {"temp": "°F", "wind": "mph", "precip": "in"}
    }
    ui.display_hourly(data)

def test_display_multi_weather(mock_cache_dir):
    data = [
        {
            "city": "City 1",
            "temp": 70,
            "feels_like": 70,
            "last_updated": time.time() - 3600, # 1 hour ago
            "units": {"temp": "°F", "wind": "mph", "precip": "in"}
        },
        {
            "city": "City 2",
            "temp": 60,
            "feels_like": 60,
            "last_updated": time.time(),
            "units": {"temp": "°F", "wind": "mph", "precip": "in"}
        }
    ]
    ui.display_multi_weather(data)

def test_get_precip_headline_extra():
    # Moderate rain
    assert ui.get_precip_headline({"precip_prob": 80, "rainfall": 0.5, "snowfall": 0, "units": {"precip": "in"}}) == "Moderate rain likely"
    # Light rain
    assert ui.get_precip_headline({"precip_prob": 80, "rainfall": 0.1, "snowfall": 0, "units": {"precip": "in"}}) == "Light rain likely"

def test_build_weather_table_extra():
    from isobar_cli.ui import build_weather_table
    # Metric Wind Chill
    data = {
        "city": "Cold", "temp": 5, "feels_like": 2,
        "units": {"temp": "°C", "wind": "km/h", "precip": "mm"}
    }
    table = build_weather_table(data)
    assert any("Wind Chill" in str(row) for row in table.columns[1]._cells)

    # Metric Heat Index
    data = {
        "city": "Hot", "temp": 30, "feels_like": 35,
        "units": {"temp": "°C", "wind": "km/h", "precip": "mm"}
    }
    table = build_weather_table(data)
    assert any("Heat Index" in str(row) for row in table.columns[1]._cells)

    # ValueError case
    data = {
        "city": "Error", "temp": "invalid", "feels_like": "invalid",
        "units": {"temp": "°C", "wind": "km/h", "precip": "mm"}
    }
    build_weather_table(data) # Should not raise exception
