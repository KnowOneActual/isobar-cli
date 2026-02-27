from isobar_cli.ui import get_precip_headline, get_temp_color, get_weather_icon


def test_get_weather_icon():
    assert get_weather_icon(0) == ("☀️", "Clear sky")
    assert get_weather_icon(95) == ("⛈️", "Thunderstorm")
    assert get_weather_icon(999) == ("🌡️", "Unknown")


def test_get_temp_color():
    assert get_temp_color(20) == "bold cyan"
    assert get_temp_color(40) == "bold blue"
    assert get_temp_color(70) == "bold green"
    assert get_temp_color(90) == "bold yellow"
    assert get_temp_color(100) == "bold red"
    assert get_temp_color("invalid") == "white"


def test_get_precip_headline():
    # Dry
    assert get_precip_headline({"precip_prob": 10}) == "Dry conditions expected"

    # Low risk
    assert (
        get_precip_headline(
            {"precip_prob": 40, "rainfall_inch": 0.05, "snowfall_inch": 0}
        )
        == "Very low precip risk"
    )

    # Possible light
    assert (
        get_precip_headline(
            {"precip_prob": 40, "rainfall_inch": 0.2, "snowfall_inch": 0}
        )
        == "Possible light precip"
    )

    # Snowy likely
    assert (
        get_precip_headline(
            {"precip_prob": 80, "rainfall_inch": 0.1, "snowfall_inch": 0.5}
        )
        == "Snowy conditions likely"
    )

    # Heavy rain
    assert (
        get_precip_headline(
            {"precip_prob": 80, "rainfall_inch": 1.0, "snowfall_inch": 0}
        )
        == "Heavy rain likely"
    )

    # Moderate rain
    assert (
        get_precip_headline(
            {"precip_prob": 80, "rainfall_inch": 0.5, "snowfall_inch": 0}
        )
        == "Moderate rain likely"
    )

    # Light rain
    assert (
        get_precip_headline(
            {"precip_prob": 80, "rainfall_inch": 0.1, "snowfall_inch": 0}
        )
        == "Light rain likely"
    )
