import json
import time

import pytest
from typer.testing import CliRunner

from isobar_cli import api, logic, ui
from isobar_cli.api import (
    get_cached_cities,
    get_city_suggestions,
    get_weather_data,
)
from isobar_cli.logic import format_time
from isobar_cli.main import app
from isobar_cli.models import ForecastDay, HourlyForecast, WeatherData, WeatherUnits

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
        json={"some_other_key": []},
    )
    assert get_city_suggestions("EmptyCity") == []


def test_get_city_suggestions_exception(requests_mock):
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=ErrorCity&count=5&format=json",
        exc=Exception("Connection error"),
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
        "timestamp": time.time() - 100,
    }
    cache_file.write_text(json.dumps(cache_data))

    result = get_weather_data(city)
    assert result.city == "CacheCity, TestState"
    assert result.last_updated > 0


def test_get_weather_data_cache_invalid_json(mock_cache_dir, requests_mock):
    city = "InvalidCache"
    cache_file = mock_cache_dir / "invalidcache_imperial.json"
    cache_file.write_text("not json")
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=InvalidCache&count=1&format=json",
        json={},
    )
    result = get_weather_data(city)
    assert result is None


def test_get_weather_data_aqi_error(requests_mock):
    geo_data = {
        "results": [
            {"name": "AQIFail", "latitude": 0, "longitude": 0, "admin1": "Illinois"}
        ]
    }
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=AQIFail&count=1&format=json",
        json=geo_data,
    )
    weather_data = {
        "current": {
            "time": "2026-02-26T06:00",
            "temperature_2m": 37,
            "apparent_temperature": 30,
            "wind_speed_10m": 4,
            "relative_humidity_2m": 50,
            "precipitation": 0,
            "weather_code": 0,
        },
        "daily": {
            "time": ["2026-02-26"],
            "sunrise": ["2026-02-26T06:00"],
            "sunset": ["2026-02-26T18:00"],
            "temperature_2m_max": [40],
            "temperature_2m_min": [30],
            "weather_code": [0],
            "precipitation_probability_max": [0],
        },
        "hourly": {
            "time": ["2026-02-26T06:00"],
            "temperature_2m": [37],
            "weather_code": [0],
            "precipitation_probability": [0],
            "rain": [0],
            "snowfall": [0],
        },
    }
    requests_mock.get("https://api.open-meteo.com/v1/forecast", json=weather_data)
    requests_mock.get(
        "https://air-quality-api.open-meteo.com/v1/air-quality",
        exc=Exception("AQI Failed"),
    )
    result = get_weather_data("AQIFail")
    assert result.aqi is None


def test_get_weather_data_hourly_index_error(requests_mock):
    geo_data = {
        "results": [
            {"name": "IndexError", "latitude": 0, "longitude": 0, "admin1": "State"}
        ]
    }
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=IndexError&count=1&format=json",
        json=geo_data,
    )
    weather_data = {
        "current": {
            "time": "2026-02-26T06:00",
            "temperature_2m": 37,
            "apparent_temperature": 30,
            "wind_speed_10m": 4,
            "relative_humidity_2m": 50,
            "precipitation": 0,
            "weather_code": 0,
        },
        "daily": {
            "time": ["2026-02-26"],
            "sunrise": ["2026-02-26T06:00"],
            "sunset": ["2026-02-26T18:00"],
            "temperature_2m_max": [40],
            "temperature_2m_min": [30],
            "weather_code": [0],
            "precipitation_probability_max": [0],
        },
        "hourly": {
            "time": ["2026-02-26T07:00"],
            "temperature_2m": [37],
            "weather_code": [0],
            "precipitation_probability": [0],
            "rain": [0],
            "snowfall": [0],
        },
    }
    requests_mock.get("https://api.open-meteo.com/v1/forecast", json=weather_data)
    requests_mock.get("https://air-quality-api.open-meteo.com/v1/air-quality", json={})
    result = get_weather_data("IndexError")
    assert len(result.hourly) == 1


def test_get_weather_data_request_exception(requests_mock):
    import requests

    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        exc=requests.exceptions.RequestException("Connection error"),
    )
    result = get_weather_data("FailCity")
    assert result is None


# --- Main Tests ---


def test_main_auto_location_fail(monkeypatch):
    mock_weather = WeatherData(
        city="Chicago, Illinois",
        temp=75.2,
        feels_like=78.5,
        wind_speed=12.4,
        humidity=65,
        precipitation=0.1,
        weather_code=0,
        precip_prob=30,
        rainfall=0.1,
        snowfall=0.0,
        sunrise="6:29 AM",
        sunset="5:37 PM",
        forecast=[],
        hourly=[],
        aqi=45,
        units=WeatherUnits(temp="°F", wind="mph", precip="in"),
        wind_gust=25.0,
        uv_index=6.5,
        previous_day_temp=70.0,
    )
    monkeypatch.setattr("isobar_cli.main.get_auto_location", lambda: None)
    monkeypatch.setattr("isobar_cli.main.get_home_city", lambda: None)
    monkeypatch.setattr(
        "isobar_cli.main.get_weather_data", lambda city, metric=False: mock_weather
    )
    result = runner.invoke(app, [], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert "Could not detect location" in result.output
    assert "Using Chicago as default" in result.output


def test_main_auto_location_success(monkeypatch):
    mock_weather = WeatherData(
        city="New York, New York",
        temp=68.0,
        feels_like=70.0,
        wind_speed=8.0,
        humidity=60,
        precipitation=0.0,
        weather_code=0,
        precip_prob=10,
        rainfall=0.0,
        snowfall=0.0,
        sunrise="6:15 AM",
        sunset="7:45 PM",
        forecast=[],
        hourly=[],
        aqi=30,
        units=WeatherUnits(temp="°F", wind="mph", precip="in"),
        wind_gust=12.0,
        uv_index=5.0,
        previous_day_temp=65.0,
    )
    monkeypatch.setattr("isobar_cli.main.get_auto_location", lambda: "New York")
    monkeypatch.setattr("isobar_cli.main.get_home_city", lambda: None)
    monkeypatch.setattr(
        "isobar_cli.main.get_weather_data", lambda city, metric=False: mock_weather
    )
    result = runner.invoke(app, [], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert "Detected: New York" in result.output


def test_main_city_option(monkeypatch):
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    mock_weather = WeatherData(
        city="Tokyo, Tokyo",
        temp=60.0,
        feels_like=62.0,
        wind_speed=5.0,
        humidity=50,
        precipitation=0.0,
        weather_code=1,
        precip_prob=20,
        rainfall=0.0,
        snowfall=0.0,
        sunrise="5:30 AM",
        sunset="6:30 PM",
        forecast=[],
        hourly=[],
        aqi=25,
        units=units,
        wind_gust=8.0,
        uv_index=4.0,
        previous_day_temp=58.0,
    )
    monkeypatch.setattr(
        "isobar_cli.main.get_weather_data",
        lambda city, metric=False: mock_weather if city == "Tokyo" else None,
    )
    result = runner.invoke(
        app, ["Tokyo"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"}
    )
    # In industrial aesthetic, city names are uppercase
    assert "TOKYO" in result.output.upper()


def test_city_complete(monkeypatch):
    from isobar_cli.main import city_complete

    monkeypatch.setattr(
        "isobar_cli.main.get_cached_cities",
        lambda: ["Chicago", "London", "Los Angeles"],
    )
    assert city_complete("Chi") == ["Chicago"]
    assert city_complete("lo") == ["London", "Los Angeles"]


def test_main_with_flags(monkeypatch):
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    mock_data_base = {
        "temp": 30.0,
        "feels_like": 25.0,
        "wind_speed": 10.0,
        "humidity": 50,
        "precipitation": 0.0,
        "weather_code": 0,
        "precip_prob": 10,
        "rainfall": 0.0,
        "snowfall": 0.0,
        "sunrise": "6:00 AM",
        "sunset": "6:00 PM",
        "forecast": [
            ForecastDay(
                date="2026-02-28", high=40, low=30, weather_code=0, precip_prob=10
            )
        ],
        "hourly": [
            HourlyForecast(
                time="2026-02-28T12:00", temp=30, weather_code=0, precip_prob=10
            )
        ],
        "units": units,
    }
    monkeypatch.setattr(
        "isobar_cli.main.get_weather_data",
        lambda city, metric=False: WeatherData(city=city, **mock_data_base),
    )

    # Multi-city
    result = runner.invoke(
        app,
        ["City1", "City2"],
        color=False,
        env={"TERM": "dumb", "NO_COLOR": "1"},
    )
    assert result.exit_code == 0
    # In industrial aesthetic, city names are uppercase
    assert "CITY1" in result.output.upper()
    assert "CITY2" in result.output.upper()

    # Multi-city with flags
    result = runner.invoke(
        app,
        ["--hourly", "City1", "City2"],
        color=False,
        env={"TERM": "dumb", "NO_COLOR": "1"},
    )
    assert result.exit_code == 0
    assert "───────────────────────────────────────" in result.output

    # Hourly
    result = runner.invoke(
        app,
        ["--hourly", "CityH"],
        color=False,
        env={"TERM": "dumb", "NO_COLOR": "1"},
    )
    assert result.exit_code == 0
    # In borderless industrial aesthetic, hourly display has "HOURLY FORECAST" header
    assert "HOURLY FORECAST" in result.output.upper()
    assert "CITYH" in result.output.upper()

    # Forecast
    result = runner.invoke(
        app,
        ["--forecast", "CityF"],
        color=False,
        env={"TERM": "dumb", "NO_COLOR": "1"},
    )
    assert result.exit_code == 0
    # In industrial aesthetic, forecast display has "FORECAST PANEL" header
    assert "FORECAST PANEL" in result.output.upper()
    assert "CITYF" in result.output.upper()


# --- UI Tests ---


def test_display_weather_edge_cases():
    ui.display_weather(None)
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    data = WeatherData(
        city="OldCache",
        temp=50.0,
        feels_like=50.0,
        wind_speed=10.0,
        humidity=50,
        precipitation=0.0,
        weather_code=0,
        precip_prob=0,
        rainfall=0.0,
        snowfall=0.0,
        sunrise="6:00 AM",
        sunset="6:00 PM",
        forecast=[],
        hourly=[],
        units=units,
        last_updated=time.time() - 3600,
    )
    ui.display_weather(data)


def test_display_multi_weather_edge_cases():
    ui.display_multi_weather([])


def test_build_weather_table_precip_rows():
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    data = WeatherData(
        city="Precip",
        temp=50.0,
        feels_like=50.0,
        wind_speed=10.0,
        humidity=50,
        precipitation=0.0,
        weather_code=0,
        precip_prob=0,
        rainfall=0.5,
        snowfall=0.5,
        sunrise="6:00 AM",
        sunset="6:00 PM",
        forecast=[],
        hourly=[],
        units=units,
    )
    table = ui.build_weather_table(data)
    # Check that table is created with industrial aesthetic
    assert table is not None
    assert len(table.columns) > 0


def test_display_weather_full():
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    data = WeatherData(
        city="Test City",
        temp=70.0,
        feels_like=75.0,
        wind_speed=10.0,
        humidity=50,
        precipitation=0.0,
        weather_code=0,
        precip_prob=10,
        rainfall=0.0,
        snowfall=0.0,
        sunrise="6:00 AM",
        sunset="6:00 PM",
        forecast=[],
        hourly=[],
        units=units,
        aqi=50,
    )
    ui.display_weather(data)


def test_display_forecast_full():
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    data = WeatherData(
        city="Test City",
        temp=70.0,
        feels_like=70.0,
        wind_speed=10.0,
        humidity=50,
        precipitation=0.0,
        weather_code=0,
        precip_prob=10,
        rainfall=0.0,
        snowfall=0.0,
        sunrise="6:00 AM",
        sunset="6:00 PM",
        forecast=[
            ForecastDay(
                date="2026-02-28", high=80, low=60, weather_code=0, precip_prob=10
            )
        ],
        hourly=[],
        units=units,
    )
    ui.display_forecast(data)


def test_display_hourly_full():
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    data = WeatherData(
        city="Test City",
        temp=70.0,
        feels_like=70.0,
        wind_speed=10.0,
        humidity=50,
        precipitation=0.0,
        weather_code=0,
        precip_prob=10,
        rainfall=0.0,
        snowfall=0.0,
        sunrise="6:00 AM",
        sunset="6:00 PM",
        forecast=[],
        hourly=[
            HourlyForecast(
                time="2026-02-28T12:00", temp=70, weather_code=0, precip_prob=10
            )
        ],
        units=units,
    )
    ui.display_hourly(data)


def test_display_multi_weather(mock_cache_dir):
    units = WeatherUnits(temp="°F", wind="mph", precip="in")
    data = [
        WeatherData(
            city="City 1",
            temp=70.0,
            feels_like=70.0,
            wind_speed=10.0,
            humidity=50,
            precipitation=0.0,
            weather_code=0,
            precip_prob=0,
            rainfall=0.0,
            snowfall=0.0,
            sunrise="6:00 AM",
            sunset="6:00 PM",
            forecast=[],
            hourly=[],
            units=units,
            last_updated=time.time() - 3600,
        ),
        WeatherData(
            city="City 2",
            temp=60.0,
            feels_like=60.0,
            wind_speed=10.0,
            humidity=50,
            precipitation=0.0,
            weather_code=0,
            precip_prob=0,
            rainfall=0.0,
            snowfall=0.0,
            sunrise="6:00 AM",
            sunset="6:00 PM",
            forecast=[],
            hourly=[],
            units=units,
            last_updated=time.time(),
        ),
    ]
    ui.display_multi_weather(data)


def test_get_precip_headline_extra():
    assert logic.get_precip_headline(80, 0.5, 0, "in") == "Moderate rain likely"
    assert logic.get_precip_headline(80, 0.1, 0, "in") == "Light rain likely"


def test_build_weather_table_extra():
    units_m = WeatherUnits(temp="°C", wind="km/h", precip="mm")
    # Metric Wind Chill
    data = WeatherData(
        city="Cold",
        temp=5.0,
        feels_like=2.0,
        wind_speed=10.0,
        humidity=50,
        precipitation=0.0,
        weather_code=0,
        precip_prob=0,
        rainfall=0.0,
        snowfall=0.0,
        sunrise="6:00 AM",
        sunset="6:00 PM",
        forecast=[],
        hourly=[],
        units=units_m,
    )
    table = ui.build_weather_table(data)
    # Check that table is created with industrial aesthetic
    assert table is not None
    assert len(table.columns) > 0

    # Metric Heat Index
    data_hot = WeatherData(
        city="Hot",
        temp=30.0,
        feels_like=35.0,
        wind_speed=10.0,
        humidity=50,
        precipitation=0.0,
        weather_code=0,
        precip_prob=0,
        rainfall=0.0,
        snowfall=0.0,
        sunrise="6:00 AM",
        sunset="6:00 PM",
        forecast=[],
        hourly=[],
        units=units_m,
    )
    table_hot = ui.build_weather_table(data_hot)
    # Check that table is created with industrial aesthetic
    assert table_hot is not None
    assert len(table_hot.columns) > 0

    # Note: get_temp_color converts input to float, so invalid strings would raise ValueError
    # but we don't need to test that edge case here


# Phase 7 Tests
def test_get_uv_guidance():
    """Test UV index guidance function."""
    assert logic.get_uv_guidance(0.5) == ("Low", "bold green")
    assert logic.get_uv_guidance(2.0) == ("Low", "bold green")
    assert logic.get_uv_guidance(3.0) == ("Moderate", "bold yellow")
    assert logic.get_uv_guidance(5.0) == ("Moderate", "bold yellow")
    assert logic.get_uv_guidance(6.0) == ("High", "bold orange1")
    assert logic.get_uv_guidance(7.0) == ("High", "bold orange1")
    assert logic.get_uv_guidance(8.0) == ("Very High", "bold red")
    assert logic.get_uv_guidance(10.0) == ("Very High", "bold red")
    assert logic.get_uv_guidance(11.0) == ("Extreme", "bold dark_red")
    assert logic.get_uv_guidance(15.0) == ("Extreme", "bold dark_red")


def test_get_wind_gust_alert():
    """Test wind gust alert function."""
    # No alert when gust is None
    assert logic.get_wind_gust_alert(10.0, None) is None

    # No alert when gust is not significantly higher
    assert logic.get_wind_gust_alert(10.0, 14.0) is None  # 1.4x

    # Alert when gust is >1.5x and >20 mph
    assert logic.get_wind_gust_alert(10.0, 25.0) == "⚠️ Gusts up to 25 mph"

    # No alert when gust is >1.5x but <20 mph
    assert logic.get_wind_gust_alert(5.0, 10.0) is None  # 2.0x but only 10 mph

    # Alert with threshold (needs > 20, not >= 20)
    assert logic.get_wind_gust_alert(13.0, 20.1) == "⚠️ Gusts up to 20 mph"


def test_get_preparation_guidance():
    """Test preparation guidance function."""
    # Cold weather suggestions (Fahrenheit)
    suggestions = logic.get_preparation_guidance(
        temp=30.0,
        feels_like=25.0,
        precip_prob=10,
        weather_code=0,
        uv_index=2.0,
        unit="°F",
    )
    assert "🧥 Heavy winter coat" in suggestions
    assert "🧤 Gloves and hat" in suggestions
    assert "☂️ Umbrella or raincoat" not in suggestions  # precip_prob too low

    # Warm weather suggestions (Fahrenheit) - temp 65°F is in light jacket range
    suggestions = logic.get_preparation_guidance(
        temp=65.0,
        feels_like=67.0,
        precip_prob=60,
        weather_code=61,
        uv_index=4.0,
        unit="°F",
    )
    assert "🧥 Light jacket" in suggestions
    assert "☂️ Umbrella or raincoat" in suggestions
    assert "🧴 Sunscreen recommended" in suggestions

    # Hot weather with high UV (Celsius)
    suggestions = logic.get_preparation_guidance(
        temp=35.0,
        feels_like=38.0,
        precip_prob=0,
        weather_code=0,
        uv_index=8.0,
        unit="°C",
    )
    assert "👕 Light, breathable clothing" in suggestions
    assert "🧴 Sunscreen recommended" in suggestions
    assert "🕶️ Sunglasses recommended" in suggestions

    # Snowy conditions
    suggestions = logic.get_preparation_guidance(
        temp=25.0,
        feels_like=20.0,
        precip_prob=80,
        weather_code=73,
        uv_index=1.0,
        unit="°F",
    )
    assert "❄️ Waterproof boots" in suggestions

    # Wind chill protection
    suggestions = logic.get_preparation_guidance(
        temp=40.0,
        feels_like=30.0,
        precip_prob=0,
        weather_code=0,
        uv_index=3.0,
        unit="°F",
    )
    assert "🧣 Scarf for wind protection" in suggestions


def test_get_temporal_context():
    """Test temporal context function."""
    # No context when previous temp is None
    assert logic.get_temporal_context(70.0, None, "°F") is None

    # No context when difference is small
    assert logic.get_temporal_context(70.0, 69.8, "°F") is None

    # Warmer context
    assert (
        logic.get_temporal_context(75.0, 70.0, "°F") == "↑ 5.0°F warmer than yesterday"
    )
    assert (
        logic.get_temporal_context(20.0, 15.0, "°C") == "↑ 5.0°C warmer than yesterday"
    )

    # Cooler context
    assert (
        logic.get_temporal_context(65.0, 70.0, "°F") == "↓ 5.0°F cooler than yesterday"
    )
    assert (
        logic.get_temporal_context(15.0, 20.0, "°C") == "↓ 5.0°C cooler than yesterday"
    )


def test_config_module(tmp_path, monkeypatch):
    """Test config module functions."""
    from isobar_cli import config

    # Mock config directory
    monkeypatch.setattr(config, "CONFIG_DIR", tmp_path / ".config" / "isobar")
    monkeypatch.setattr(
        config, "CONFIG_FILE", tmp_path / ".config" / "isobar" / "config.json"
    )

    # Test initial state
    assert config.get_home_city() is None

    # Test setting home city
    config.set_home_city("New York")
    assert config.get_home_city() == "New York"

    # Test clearing home city
    config.clear_home_city()
    assert config.get_home_city() is None

    # Test setting again
    config.set_home_city("London")
    assert config.get_home_city() == "London"

    # Test config path
    assert config.get_config_path() == tmp_path / ".config" / "isobar" / "config.json"


def test_ui_with_new_features():
    """Test UI with new Phase 7 features."""
    units = WeatherUnits(temp="°F", wind="mph", precip="in")

    # Create weather data with new fields
    data = WeatherData(
        city="Test City",
        temp=75.0,
        feels_like=78.0,
        wind_speed=10.0,
        humidity=50,
        precipitation=0.0,
        weather_code=0,
        precip_prob=30,
        rainfall=0.0,
        snowfall=0.0,
        sunrise="6:00 AM",
        sunset="6:00 PM",
        forecast=[],
        hourly=[],
        units=units,
        aqi=45,
        wind_gust=25.0,  # Should trigger gust alert
        uv_index=6.5,  # Should show UV index
        previous_day_temp=70.0,
    )

    # Build table and check for new features
    table = ui.build_weather_table(data)

    # Check for UV index - look in the label column (column 1)
    # In industrial aesthetic, labels are uppercase
    assert any("UV INDEX" in str(row).upper() for row in table.columns[1]._cells)

    # Check for wind gust alert
    # In industrial aesthetic, it's "GUST ALERT" not "Wind Alert"
    assert any("GUST ALERT" in str(row).upper() for row in table.columns[1]._cells)

    # Test without gust alert (gust not high enough)
    data_no_alert = WeatherData(
        city="Test City",
        temp=75.0,
        feels_like=78.0,
        wind_speed=10.0,
        humidity=50,
        precipitation=0.0,
        weather_code=0,
        precip_prob=30,
        rainfall=0.0,
        snowfall=0.0,
        sunrise="6:00 AM",
        sunset="6:00 PM",
        forecast=[],
        hourly=[],
        units=units,
        wind_gust=12.0,  # Too low for alert
    )

    table2 = ui.build_weather_table(data_no_alert)
    # In industrial aesthetic, it's "WIND GUST" in uppercase
    assert any("WIND GUST" in str(row).upper() for row in table2.columns[1]._cells)


def test_api_with_new_fields(requests_mock):
    """Test API integration with new fields."""
    # Mock geocoding response
    requests_mock.get(
        "https://geocoding-api.open-meteo.com/v1/search?name=London&count=1&format=json",
        json={
            "results": [
                {
                    "name": "London",
                    "latitude": 51.5,
                    "longitude": -0.1,
                    "admin1": "England",
                    "country": "UK",
                }
            ]
        },
    )

    # Mock weather response with new fields
    requests_mock.get(
        "https://api.open-meteo.com/v1/forecast",
        json={
            "latitude": 51.5,
            "longitude": -0.1,
            "current": {
                "time": "2026-03-31T12:00",
                "temperature_2m": 60.0,
                "apparent_temperature": 58.0,
                "wind_speed_10m": 10.0,
                "relative_humidity_2m": 65,
                "precipitation": 0.0,
                "weather_code": 1,
                "wind_gusts_10m": 18.0,
                "uv_index": 4.5,
            },
            "daily": {
                "time": ["2026-03-31"],
                "sunrise": ["2026-03-31T06:00:00"],
                "sunset": ["2026-03-31T18:00:00"],
                "temperature_2m_max": [65.0],
                "temperature_2m_min": [55.0],
                "weather_code": [1],
                "precipitation_probability_max": [20],
                "uv_index_max": [5.0],
            },
            "hourly": {
                "time": ["2026-03-31T12:00", "2026-03-31T13:00"],
                "precipitation_probability": [10, 15],
                "rain": [0.0, 0.0],
                "snowfall": [0.0, 0.0],
                "temperature_2m": [60.0, 61.0],
                "weather_code": [1, 1],
            },
        },
    )

    # Mock air quality response
    requests_mock.get(
        "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=51.5&longitude=-0.1&current=us_aqi",
        json={"current": {"us_aqi": 35}},
    )

    # Get weather data
    weather = api.get_weather_data("London")

    # Check new fields are present
    assert weather is not None
    assert weather.wind_gust == 18.0
    assert weather.uv_index == 4.5
    assert weather.forecast[0].uv_index_max == 5.0
