from datetime import datetime

# WMO Weather interpretation codes -> (emoji, description)
# https://open-meteo.com/en/docs
WMO_CODES: dict[int, tuple[str, str]] = {
    0: ("☀️", "Clear sky"),
    1: ("🌤️", "Mainly clear"),
    2: ("⛅", "Partly cloudy"),
    3: ("☁️", "Overcast"),
    45: ("🌫️", "Foggy"),
    48: ("🌫️", "Rime fog"),
    51: ("🌦️", "Light drizzle"),
    53: ("🌦️", "Moderate drizzle"),
    55: ("🌧️", "Dense drizzle"),
    61: ("🌧️", "Slight rain"),
    63: ("🌧️", "Moderate rain"),
    65: ("🌧️", "Heavy rain"),
    71: ("🌨️", "Slight snow"),
    73: ("🌨️", "Moderate snow"),
    75: ("❄️", "Heavy snow"),
    77: ("🌨️", "Snow grains"),
    80: ("🌦️", "Slight showers"),
    81: ("🌧️", "Moderate showers"),
    82: ("🌧️", "Violent showers"),
    85: ("🌨️", "Slight snow showers"),
    86: ("❄️", "Heavy snow showers"),
    95: ("⛈️", "Thunderstorm"),
    96: ("⛈️", "Thunderstorm w/ hail"),
    99: ("⛈️", "Thunderstorm w/ heavy hail"),
}


def format_time(iso_string: str) -> str:
    """Convert ISO 8601 datetime to 12-hour format (e.g., '6:42 AM')."""
    if not iso_string:
        return "--"
    try:
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        return dt.strftime("%-I:%M %p")
    except (ValueError, AttributeError):
        return "--"


def get_temp_color(temp_val: float, unit="°F") -> str:
    """Returns a Rich color tag based on the temperature and unit."""
    t = float(temp_val)
    if unit == "°C":
        if t < 0:
            return "bold cyan"
        if t < 15:
            return "bold blue"
        if t < 26:
            return "bold green"
        if t < 35:
            return "bold yellow"
        return "bold red"
    else:
        if t < 32:
            return "bold cyan"
        if t < 60:
            return "bold blue"
        if t < 80:
            return "bold green"
        if t < 95:
            return "bold yellow"
        return "bold red"


def get_precip_headline(
    precip_prob: int, rainfall: float, snowfall: float, unit_precip: str
) -> str:
    """Generate a single-line comfort summary for precip decisions."""
    total_precip = rainfall + snowfall

    # Thresholds
    if unit_precip == "mm":
        low_limit, med_limit, high_limit, snow_limit = 2.5, 6.0, 19.0, 6.0
    else:
        low_limit, med_limit, high_limit, snow_limit = 0.1, 0.25, 0.75, 0.25

    if precip_prob < 30:
        return "Dry conditions expected"
    if precip_prob < 60:
        return (
            "Very low precip risk"
            if total_precip < low_limit
            else "Possible light precip"
        )

    if snowfall > rainfall and snowfall > snow_limit:
        return "Snowy conditions likely"
    if rainfall > high_limit:
        return "Heavy rain likely"
    if rainfall > med_limit:
        return "Moderate rain likely"
    return "Light rain likely"


def get_aqi_label(aqi_val: int) -> tuple[str, str]:
    """Returns (label, color) for a US AQI value."""
    thresholds = [
        (50, "Good", "bold green"),
        (100, "Moderate", "bold yellow"),
        (150, "Unhealthy (Sensitive)", "bold orange1"),
        (200, "Unhealthy", "bold red"),
        (300, "Very Unhealthy", "bold purple"),
    ]
    for limit, label, color in thresholds:
        if aqi_val <= limit:
            return label, color
    return "Hazardous", "bold dark_red"


def get_feels_like_label(temp: float, feels_like: float, unit: str) -> str:
    """Determine descriptive label for 'Feels Like' temperature."""
    is_metric = unit == "°C"
    if is_metric:
        if temp <= 10 and feels_like < temp:
            return "Wind Chill:"
        if temp >= 27 and feels_like > temp:
            return "Heat Index:"
    else:
        if temp <= 50 and feels_like < temp:
            return "Wind Chill:"
        if temp >= 80 and feels_like > temp:
            return "Heat Index:"
    return "Real Feel:"
