import pytest

from isobar_cli.models import WeatherData, WeatherUnits
from isobar_cli.ui import (
    build_weather_table,
    get_aqi_label,
    get_precip_headline,
    get_temp_color,
    get_weather_icon,
)


def test_get_weather_icon():
    assert get_weather_icon(0) == ("☀️", "Clear sky")
    assert get_weather_icon(95) == ("⛈️", "Thunderstorm")
    assert get_weather_icon(999) == ("🌡️", "Unknown")


def test_get_temp_color():
    # Imperial (default)
    assert get_temp_color(20) == "bold cyan"
    assert get_temp_color(40) == "bold blue"
    assert get_temp_color(70) == "bold green"
    assert get_temp_color(90) == "bold yellow"
    assert get_temp_color(100) == "bold red"

    with pytest.raises(ValueError):
        get_temp_color("invalid")

    # Metric
    assert get_temp_color(-5, unit="°C") == "bold cyan"
    assert get_temp_color(10, unit="°C") == "bold blue"
    assert get_temp_color(20, unit="°C") == "bold green"
    assert get_temp_color(30, unit="°C") == "bold yellow"
    assert get_temp_color(40, unit="°C") == "bold red"


def test_get_aqi_label():
    assert get_aqi_label(20) == ("Good", "bold green")
    assert get_aqi_label(75) == ("Moderate", "bold yellow")
    assert get_aqi_label(125) == ("Unhealthy (Sensitive)", "bold orange1")
    assert get_aqi_label(175) == ("Unhealthy", "bold red")
    assert get_aqi_label(250) == ("Very Unhealthy", "bold purple")
    assert get_aqi_label(400) == ("Hazardous", "bold dark_red")


def test_build_weather_table_labels():
    # Standard
    units_f = WeatherUnits(temp="°F", wind="mph", precip="in")
    data = WeatherData(
        city="Test",
        temp=70,
        feels_like=70,
        wind_speed=10,
        humidity=50,
        precipitation=0,
        weather_code=0,
        precip_prob=10,
        rainfall=0,
        snowfall=0,
        sunrise="6:00 AM",
        sunset="6:00 PM",
        forecast=[],
        hourly=[],
        units=units_f,
    )
    table = build_weather_table(data)
    assert any("Real Feel" in str(row) for row in table.columns[1]._cells)

    # Wind Chill
    data_cold = WeatherData(
        city="Cold",
        temp=20,
        feels_like=10,
        wind_speed=10,
        humidity=50,
        precipitation=0,
        weather_code=0,
        precip_prob=10,
        rainfall=0,
        snowfall=0,
        sunrise="6:00 AM",
        sunset="6:00 PM",
        forecast=[],
        hourly=[],
        units=units_f,
    )
    table_cold = build_weather_table(data_cold)
    assert any("Wind Chill" in str(row) for row in table_cold.columns[1]._cells)

    # Heat Index
    data_hot = WeatherData(
        city="Hot",
        temp=95,
        feels_like=105,
        wind_speed=10,
        humidity=50,
        precipitation=0,
        weather_code=0,
        precip_prob=10,
        rainfall=0,
        snowfall=0,
        sunrise="6:00 AM",
        sunset="6:00 PM",
        forecast=[],
        hourly=[],
        units=units_f,
    )
    table_hot = build_weather_table(data_hot)
    assert any("Heat Index" in str(row) for row in table_hot.columns[1]._cells)


def test_get_precip_headline_logic():
    # Dry
    assert get_precip_headline(10, 0, 0, "in") == "Dry conditions expected"

    # Low risk (Imperial)
    assert get_precip_headline(40, 0.05, 0, "in") == "Very low precip risk"

    # Possible light (Imperial)
    assert get_precip_headline(40, 0.2, 0, "in") == "Possible light precip"

    # Snowy likely (Imperial)
    assert get_precip_headline(80, 0.1, 0.5, "in") == "Snowy conditions likely"

    # Dry (Metric)
    assert get_precip_headline(10, 0, 0, "mm") == "Dry conditions expected"

    # Low risk (Metric - 1mm is < 2.5mm limit)
    assert get_precip_headline(40, 1.0, 0, "mm") == "Very low precip risk"

    # Heavy rain (Metric - 20mm is > 19mm limit)
    assert get_precip_headline(80, 20.0, 0, "mm") == "Heavy rain likely"
