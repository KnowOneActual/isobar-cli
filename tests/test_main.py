import pytest
from typer.testing import CliRunner

from isobar_cli.main import app

runner = CliRunner()

def test_main_help():
    result = runner.invoke(app, ["--help"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert result.exit_code == 0
    assert "Get the weather and what it FEELS LIKE" in result.output

def test_main_metric_flag_exists():
    result = runner.invoke(app, ["--help"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert "--metric" in result.output
    assert "-m" in result.output

@pytest.fixture
def mock_api(monkeypatch):
    from isobar_cli import main

    def mock_get_weather_data(city, metric=False):
        return {
            "city": f"{city}, TestState",
            "temp": 20,
            "feels_like": 18,
            "wind_speed": 5,
            "humidity": 50,
            "precipitation": 0,
            "weather_code": 0,
            "precip_prob": 0,
            "rainfall": 0,
            "snowfall": 0,
            "sunrise": "6:00 AM",
            "sunset": "6:00 PM",
            "forecast": [],
            "hourly": [
                {
                    "time": "2026-02-28T12:00",
                    "temp": 20,
                    "weather_code": 0,
                    "precip_prob": 0,
                }
            ],
            "units": {
                "temp": "°C" if metric else "°F",
                "wind": "km/h" if metric else "mph",
                "precip": "mm" if metric else "in"
            }
        }

    monkeypatch.setattr(main, "get_weather_data", mock_get_weather_data)

def test_main_with_city(mock_api):
    result = runner.invoke(app, ["Chicago"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert result.exit_code == 0
    assert "Chicago, TestState Weather" in result.output
    assert "20°F" in result.output


def test_main_with_metric(mock_api):
    result = runner.invoke(app, ["London", "--metric"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert result.exit_code == 0
    assert "London, TestState Weather" in result.output
    assert "20°C" in result.output


def test_main_with_hourly(mock_api):
    result = runner.invoke(app, ["Chicago", "--hourly"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"})
    assert result.exit_code == 0
    assert "Hourly Forecast — Chicago, TestState" in result.output
    assert "12 PM" in result.output

