import json
import time
import pytest
from typer.testing import CliRunner
from isobar_cli import api, ui
from isobar_cli.api import (
    get_cached_cities,
    get_city_suggestions,
    get_weather_data,
)
from isobar_cli.logic import format_time
from isobar_cli.main import app
from isobar_cli.models import WeatherData, WeatherUnits, ForecastDay, HourlyForecast

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
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    cache_data = {
        "city": "CacheCity, TestState",
        "temp": 50.0,
        "feels_like": 45.0,
        "wind_speed": 10.0,
        "humidity": 50,
        "precipitation": 0.0,
        "weather_code": 0,
        "precip_prob": 0,
        "rainfall": 0.0,
        "snowfall": 0.0,
        "sunrise": "6:00 AM",
        "sunset": "6:00 PM",
        "forecast": [],
        "hourly": [],
        "units": units.__dict__,
        "aqi": 10,
        "last_updated": time.time(),
        "timestamp": time.time() - 100
    }
    cache_file.write_text(json.dumps(cache_data))

    result = get_weather_data(city)
    assert result.city == "CacheCity, TestState"
    assert result.last_updated > 0

def test_get_weather_data_cache_invalid_json(mock_cache_dir, requests_mock):
    city = "InvalidCache"
    cache_file = mock_cache_dir / "invalidcache_imperial.json"
    cache_file.write_text("not json")
    requests_mock.get("https://geocoding-api.open-meteo.com/v1/search?name=InvalidCache&count=1&format=json", json={})
    result = get_weather_data(city)
    assert result is None

def test_get_weather_data_aqi_error(requests_mock):
    geo_data = {"results": [{"name": "AQIFail", "latitude": 0, "longitude": 0, "admin1": "Illinois"}]}
    requests_mock.get("https://geocoding-api.open-meteo.com/v1/search?name=AQIFail&count=1&format=json", json=geo_data)
    weather_data = {
        "current": {"time": "2026-02-26T06:00", "temperature_2m": 37, "apparent_temperature": 30, "wind_speed_10m": 4, "relative_humidity_2m": 50, "precipitation": 0, "weather_code": 0},
        "daily": {"time": ["2026-02-26"], "sunrise": ["2026-02-26T06:00"], "sunset": ["2026-02-26T18:00"], "temperature_2m_max": [40], "temperature_2m_min": [30], "weather_code": [0], "precipitation_probability_max": [0]},
        "hourly": {"time": ["2026-02-26T06:00"], "temperature_2m": [37], "weather_code": [0], "precipitation_probability": [0], "rain": [0], "snowfall": [0]}
    }
    requests_mock.get("https://api.open-meteo.com/v1/forecast", json=weather_data)
    requests_mock.get("https://air-quality-api.open-meteo.com/v1/air-quality", exc=Exception("AQI Failed"))
    result = get_weather_data("AQIFail")
    assert result.aqi is None

def test_get_weather_data_hourly_index_error(requests_mock):
    geo_data = {"results": [{"name": "IndexError", "latitude": 0, "longitude": 0, "admin1": "State"}]}
    requests_mock.get("https://geocoding-api.open-meteo.com/v1/search?name=IndexError&count=1&format=json", json=geo_data)
    weather_data = {
        "current": {"time": "2026-02-26T06:00", "temperature_2m": 37, "apparent_temperature": 30, "wind_speed_10m": 4, "relative_humidity_2m": 50, "precipitation": 0, "weather_code": 0},
        "daily": {"time": ["2026-02-26"], "sunrise": ["2026-02-26T06:00"], "sunset": ["2026-02-26T18:00"], "temperature_2m_max": [40], "temperature_2m_min": [30], "weather_code": [0], "precipitation_probability_max": [0]},
        "hourly": {"time": ["2026-02-26T07:00"], "temperature_2m": [37], "weather_code": [0], "precipitation_probability": [0], "rain": [0], "snowfall": [0]}
    }
    requests_mock.get("https://api.open-meteo.com/v1/forecast", json=weather_data)
    requests_mock.get("https://air-quality-api.open-meteo.com/v1/air-quality", json={})
    result = get_weather_data("IndexError")
    assert len(result.hourly) == 1

def test_get_weather_data_request_exception(requests_mock):
    import requests
    requests_mock.get("https://geocoding-api.open-meteo.com/v1/search", exc=requests.exceptions.RequestException("Connection error"))
    result = get_weather_data("FailCity")
    assert result is None

# --- Main Tests ---

def test_main_auto_location_fail(monkeypatch):
    monkeypatch.setattr("isobar_cli.main.get_auto_location", lambda: None)
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    mock_weather = WeatherData(
        city="Chicago", temp=30.0, feels_like=25.0, wind_speed=10.0, humidity=50,
        precipitation=0.0, weather_code=0, precip_prob=10, rainfall=0.0, snowfall=0.0,
        sunrise="6:00 AM", sunset="6:00 PM", forecast=[], hourly=[], units=units
    )
    monkeypatch.setattr("isobar_cli.main.get_weather_data", lambda city, metric=False: mock_weather)
    result = runner.invoke(app, [], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert "Could not detect location" in result.output
    assert "Using Chicago as default" in result.output

def test_main_auto_location_success(monkeypatch):
    monkeypatch.setattr("isobar_cli.main.get_auto_location", lambda: "New York")
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    mock_weather = WeatherData(
        city="New York", temp=30.0, feels_like=25.0, wind_speed=10.0, humidity=50,
        precipitation=0.0, weather_code=0, precip_prob=10, rainfall=0.0, snowfall=0.0,
        sunrise="6:00 AM", sunset="6:00 PM", forecast=[], hourly=[], units=units
    )
    monkeypatch.setattr("isobar_cli.main.get_weather_data", lambda city, metric=False: mock_weather)
    result = runner.invoke(app, [], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert "Detected: New York" in result.output

def test_main_city_option(monkeypatch):
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    monkeypatch.setattr("isobar_cli.main.get_weather_data", lambda city, metric=False: WeatherData(
        city=city, temp=30.0, feels_like=25.0, wind_speed=10.0, humidity=50,
        precipitation=0.0, weather_code=0, precip_prob=10, rainfall=0.0, snowfall=0.0,
        sunrise="6:00 AM", sunset="6:00 PM", forecast=[], hourly=[], units=units
    ))
    result = runner.invoke(app, ["Tokyo"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert "Tokyo" in result.output

def test_city_complete(monkeypatch):
    from isobar_cli.main import city_complete
    monkeypatch.setattr("isobar_cli.main.get_cached_cities", lambda: ["Chicago", "London", "Los Angeles"])
    assert city_complete("Chi") == ["Chicago"]
    assert city_complete("lo") == ["London", "Los Angeles"]

def test_main_with_flags(monkeypatch):
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    mock_data_base = dict(
        temp=30.0, feels_like=25.0, wind_speed=10.0, humidity=50,
        precipitation=0.0, weather_code=0, precip_prob=10, rainfall=0.0, snowfall=0.0,
        sunrise="6:00 AM", sunset="6:00 PM",
        forecast=[ForecastDay(date="2026-02-28", high=40, low=30, weather_code=0, precip_prob=10)],
        hourly=[HourlyForecast(time="2026-02-28T12:00", temp=30, weather_code=0, precip_prob=10)],
        units=units
    )
    monkeypatch.setattr("isobar_cli.main.get_weather_data", lambda city, metric=False: WeatherData(city=city, **mock_data_base))

    # Multi-city
    result = runner.invoke(app, ["City1", "City2"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert result.exit_code == 0
    assert "City1" in result.output
    assert "City2" in result.output

    # Multi-city with flags
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
    ui.display_weather(None)
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    data = WeatherData(
        city="OldCache", temp=50.0, feels_like=50.0, wind_speed=10.0, humidity=50,
        precipitation=0.0, weather_code=0, precip_prob=0, rainfall=0.0, snowfall=0.0,
        sunrise="6:00 AM", sunset="6:00 PM", forecast=[], hourly=[], units=units,
        last_updated=time.time() - 3600
    )
    ui.display_weather(data)

def test_display_multi_weather_edge_cases():
    ui.display_multi_weather([])

def test_build_weather_table_precip_rows():
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    data = WeatherData(
        city="Precip", temp=50.0, feels_like=50.0, wind_speed=10.0, humidity=50,
        precipitation=0.0, weather_code=0, precip_prob=0, rainfall=0.5, snowfall=0.5,
        sunrise="6:00 AM", sunset="6:00 PM", forecast=[], hourly=[], units=units
    )
    table = ui.build_weather_table(data)
    rows_str = "".join(str(row) for row in table.columns[1]._cells)
    assert "Rain Expected" in rows_str
    assert "Snow Expected" in rows_str

def test_display_weather_full():
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    data = WeatherData(
        city="Test City", temp=70.0, feels_like=75.0, wind_speed=10.0, humidity=50,
        precipitation=0.0, weather_code=0, precip_prob=10, rainfall=0.0, snowfall=0.0,
        sunrise="6:00 AM", sunset="6:00 PM", forecast=[], hourly=[], units=units,
        aqi=50
    )
    ui.display_weather(data)

def test_display_forecast_full():
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    data = WeatherData(
        city="Test City", temp=70.0, feels_like=70.0, wind_speed=10.0, humidity=50,
        precipitation=0.0, weather_code=0, precip_prob=10, rainfall=0.0, snowfall=0.0,
        sunrise="6:00 AM", sunset="6:00 PM", 
        forecast=[ForecastDay(date="2026-02-28", high=80, low=60, weather_code=0, precip_prob=10)], 
        hourly=[], units=units
    )
    ui.display_forecast(data)

def test_display_hourly_full():
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    data = WeatherData(
        city="Test City", temp=70.0, feels_like=70.0, wind_speed=10.0, humidity=50,
        precipitation=0.0, weather_code=0, precip_prob=10, rainfall=0.0, snowfall=0.0,
        sunrise="6:00 AM", sunset="6:00 PM", forecast=[],
        hourly=[HourlyForecast(time="2026-02-28T12:00", temp=70, weather_code=0, precip_prob=10)],
        units=units
    )
    ui.display_hourly(data)

def test_display_multi_weather(mock_cache_dir):
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    data = [
        WeatherData(
            city="City 1", temp=70.0, feels_like=70.0, wind_speed=10.0, humidity=50,
            precipitation=0.0, weather_code=0, precip_prob=0, rainfall=0.0, snowfall=0.0,
            sunrise="6:00 AM", sunset="6:00 PM", forecast=[], hourly=[], units=units,
            last_updated=time.time() - 3600
        ),
        WeatherData(
            city="City 2", temp=60.0, feels_like=60.0, wind_speed=10.0, humidity=50,
            precipitation=0.0, weather_code=0, precip_prob=0, rainfall=0.0, snowfall=0.0,
            sunrise="6:00 AM", sunset="6:00 PM", forecast=[], hourly=[], units=units,
            last_updated=time.time()
        )
    ]
    ui.display_multi_weather(data)

def test_get_precip_headline_extra():
    assert ui.get_precip_headline(80, 0.5, 0, "in") == "Moderate rain likely"
    assert ui.get_precip_headline(80, 0.1, 0, "in") == "Light rain likely"

def test_build_weather_table_extra():
    units_m = WeatherUnits(temp="°C", wind="km/h", precip="mm")
    # Metric Wind Chill
    data = WeatherData(
        city="Cold", temp=5.0, feels_like=2.0, wind_speed=10.0, humidity=50,
        precipitation=0.0, weather_code=0, precip_prob=0, rainfall=0.0, snowfall=0.0,
        sunrise="6:00 AM", sunset="6:00 PM", forecast=[], hourly=[], units=units_m
    )
    table = ui.build_weather_table(data)
    assert any("Wind Chill" in str(row) for row in table.columns[1]._cells)

    # Metric Heat Index
    data_hot = WeatherData(
        city="Hot", temp=30.0, feels_like=35.0, wind_speed=10.0, humidity=50,
        precipitation=0.0, weather_code=0, precip_prob=0, rainfall=0.0, snowfall=0.0,
        sunrise="6:00 AM", sunset="6:00 PM", forecast=[], hourly=[], units=units_m
    )
    table_hot = ui.build_weather_table(data_hot)
    assert any("Heat Index" in str(row) for row in table_hot.columns[1]._cells)

    # ValueError case
    with pytest.raises(ValueError):
        ui.get_temp_color("invalid")
