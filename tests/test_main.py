import pytest
from typer.testing import CliRunner

from isobar_cli.main import app
from isobar_cli.models import HourlyForecast, WeatherData, WeatherUnits

runner = CliRunner()


def test_main_help():
    result = runner.invoke(
        app, ["main", "--help"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"}
    )
    assert result.exit_code == 0
    assert "Get the weather and what it FEELS LIKE" in result.output


def test_main_metric_flag_exists():
    result = runner.invoke(
        app, ["main", "--help"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"}
    )
    assert "--metric" in result.output
    assert "-m" in result.output


@pytest.fixture
def mock_api(monkeypatch):
    from isobar_cli import main

    def mock_get_weather_data(city, metric=False):
        if city == "Unknown":
            return None

        units = WeatherUnits(
            temp="°C" if metric else "°F",
            wind="km/h" if metric else "mph",
            precip="mm" if metric else "in",
        )

        return WeatherData(
            city=f"{city}, TestState",
            temp=20.0,
            feels_like=18.0,
            wind_speed=5.0,
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
        )

    def mock_get_city_suggestions(city):
        if city == "Unknown":
            return ["Suggested City?", "Another City"]
        return []

    monkeypatch.setattr("isobar_cli.main.get_weather_data", mock_get_weather_data)
    monkeypatch.setattr(
        "isobar_cli.main.get_city_suggestions", mock_get_city_suggestions
    )


def test_main_with_city(mock_api):
    result = runner.invoke(
        app, ["main", "Chicago"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"}
    )
    assert result.exit_code == 0


def test_main_with_metric(mock_api):
    result = runner.invoke(
        app,
        ["main", "Chicago", "--metric"],
        color=False,
        env={"TERM": "dumb", "NO_COLOR": "1"},
    )
    assert result.exit_code == 0


def test_main_with_hourly(mock_api):
    result = runner.invoke(
        app,
        ["main", "Chicago", "--hourly"],
        color=False,
        env={"TERM": "dumb", "NO_COLOR": "1"},
    )
    assert result.exit_code == 0


def test_main_multiple_cities(mock_api):
    result = runner.invoke(
        app,
        ["main", "Chicago", "London"],
        color=False,
        env={"TERM": "dumb", "NO_COLOR": "1"},
    )
    assert result.exit_code == 0


def test_main_not_found_with_suggestions(mock_api):
    result = runner.invoke(
        app, ["main", "Unknown"], color=False, env={"TERM": "dumb", "NO_COLOR": "1"}
    )
    assert result.exit_code == 1
    assert "'Unknown' not found" in result.output
    assert "Did you mean: Suggested City?" in result.output
