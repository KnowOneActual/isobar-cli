from isobar_cli.ui import (
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
    assert get_temp_color("invalid") == "white"

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
    from isobar_cli.ui import build_weather_table

    # Standard
    data = {
        "city": "Test",
        "temp": 70,
        "feels_like": 70,
        "units": {"temp": "°F", "wind": "mph", "precip": "in"},
    }
    table = build_weather_table(data)
    # Check if "Real Feel" is in the table (as a column/row value)
    assert any("Real Feel" in str(row) for row in table.columns[1]._cells)

    # Wind Chill
    data_cold = {
        "city": "Cold",
        "temp": 20,
        "feels_like": 10,
        "units": {"temp": "°F", "wind": "mph", "precip": "in"},
    }
    table_cold = build_weather_table(data_cold)
    assert any("Wind Chill" in str(row) for row in table_cold.columns[1]._cells)

    # Heat Index
    data_hot = {
        "city": "Hot",
        "temp": 95,
        "feels_like": 105,
        "units": {"temp": "°F", "wind": "mph", "precip": "in"},
    }
    table_hot = build_weather_table(data_hot)
    assert any("Heat Index" in str(row) for row in table_hot.columns[1]._cells)
    # Dry
    assert get_precip_headline({"precip_prob": 10}) == "Dry conditions expected"

    # Low risk (Imperial)
    assert (
        get_precip_headline({"precip_prob": 40, "rainfall": 0.05, "snowfall": 0})
        == "Very low precip risk"
    )

    # Possible light (Imperial)
    assert (
        get_precip_headline({"precip_prob": 40, "rainfall": 0.2, "snowfall": 0})
        == "Possible light precip"
    )

    # Snowy likely (Imperial)
    assert (
        get_precip_headline({"precip_prob": 80, "rainfall": 0.1, "snowfall": 0.5})
        == "Snowy conditions likely"
    )

    # Metric tests
    metric_units = {"units": {"precip": "mm"}}
    # Dry (Metric)
    assert (
        get_precip_headline({"precip_prob": 10, **metric_units})
        == "Dry conditions expected"
    )

    # Low risk (Metric - 1mm is < 2.5mm limit)
    assert (
        get_precip_headline({"precip_prob": 40, "rainfall": 1.0, "snowfall": 0, **metric_units})
        == "Very low precip risk"
    )

    # Heavy rain (Metric - 20mm is > 19mm limit)
    assert (
        get_precip_headline({"precip_prob": 80, "rainfall": 20.0, "snowfall": 0, **metric_units})
        == "Heavy rain likely"
    )
