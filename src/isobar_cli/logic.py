from datetime import datetime
from typing import Optional

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


def format_time(iso_string: str, timezone: str = "UTC") -> str:
    """Convert ISO 8601 datetime to 12-hour format in specified timezone.

    Args:
        iso_string: ISO 8601 datetime string
        timezone: Timezone name (e.g., 'America/New_York'), defaults to UTC

    Returns:
        Formatted time string (e.g., '6:42 AM') or '--' on error
    """
    if not iso_string:
        return "--"

    try:
        # Parse the datetime
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))

        # Convert to local timezone if not UTC
        if timezone != "UTC":
            try:
                import pytz

                utc_dt = dt.replace(tzinfo=pytz.UTC)
                local_tz = pytz.timezone(timezone)
                local_dt = utc_dt.astimezone(local_tz)
                return local_dt.strftime("%-I:%M %p")
            except ImportError:
                # pytz not installed, fall back to UTC
                pass

        return dt.strftime("%-I:%M %p")
    except (ValueError, AttributeError):
        return "--"

    # Try to import pytz for timezone conversion
    pytz_available = False
    if timezone != "UTC":
        try:
            import pytz

            pytz_available = True
        except ImportError:
            pytz_available = False

    try:
        # Parse the datetime
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))

        # Convert to local timezone if not UTC and pytz is available
        if timezone != "UTC" and pytz_available:
            utc_dt = dt.replace(tzinfo=pytz.UTC)
            local_tz = pytz.timezone(timezone)
            local_dt = utc_dt.astimezone(local_tz)
            return local_dt.strftime("%-I:%M %p")

        return dt.strftime("%-I:%M %p")
    except (ValueError, AttributeError):
        return "--"
    try:
        # Parse the datetime
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))

        # Convert to local timezone if not UTC
        if timezone != "UTC":
            import pytz

            utc_dt = dt.replace(tzinfo=pytz.UTC)
            local_tz = pytz.timezone(timezone)
            local_dt = utc_dt.astimezone(local_tz)
            return local_dt.strftime("%-I:%M %p")

        return dt.strftime("%-I:%M %p")
    except (ValueError, AttributeError, ImportError):
        # Fallback to UTC if pytz not available or other error
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


def get_uv_guidance(uv_index: float) -> tuple[str, str]:
    """Returns (label, color) based on UV intensity.

    UV Index Scale:
    0-2: Low
    3-5: Moderate
    6-7: High
    8-10: Very High
    11+: Extreme
    """
    if uv_index <= 2:
        return "Low", "bold green"
    elif uv_index <= 5:
        return "Moderate", "bold yellow"
    elif uv_index <= 7:
        return "High", "bold orange1"
    elif uv_index <= 10:
        return "Very High", "bold red"
    else:
        return "Extreme", "bold dark_red"


def get_wind_gust_alert(wind_speed: float, wind_gust: Optional[float]) -> Optional[str]:
    """Returns alert if gusts are significantly higher than sustained wind.

    Alerts when gusts are > 1.5x sustained wind speed and > 20 mph (or 32 km/h).
    """
    if wind_gust is None:
        return None

    # Check if gusts are significantly higher than sustained wind
    if wind_gust > wind_speed * 1.5:
        # Check if gusts are strong enough to warrant alert
        if wind_gust > 20:  # mph threshold
            return f"⚠️ Gusts up to {wind_gust:.0f} mph"
    return None


def get_preparation_guidance(
    temp: float,
    feels_like: float,
    precip_prob: int,
    weather_code: int,
    uv_index: Optional[float],
    unit: str,
) -> list[str]:
    """Returns clothing/gear suggestions based on weather conditions."""
    suggestions = []

    # Temperature-based clothing
    is_metric = unit == "°C"
    if is_metric:
        if temp < 0:
            suggestions.append("🧥 Heavy winter coat")
            suggestions.append("🧤 Gloves and hat")
        elif temp < 10:
            suggestions.append("🧥 Warm jacket")
        elif temp < 20:
            suggestions.append("🧥 Light jacket")
        elif temp > 30:
            suggestions.append("👕 Light, breathable clothing")
    else:
        if temp < 32:
            suggestions.append("🧥 Heavy winter coat")
            suggestions.append("🧤 Gloves and hat")
        elif temp < 50:
            suggestions.append("🧥 Warm jacket")
        elif temp < 68:
            suggestions.append("🧥 Light jacket")
        elif temp > 86:
            suggestions.append("👕 Light, breathable clothing")

    # Precipitation gear
    if precip_prob > 50:
        if weather_code in [71, 73, 75, 77, 85, 86]:  # Snow codes
            suggestions.append("❄️ Waterproof boots")
        else:
            suggestions.append("☂️ Umbrella or raincoat")

    # UV protection
    if uv_index and uv_index >= 3:
        suggestions.append("🧴 Sunscreen recommended")
    if uv_index and uv_index >= 6:
        suggestions.append("🕶️ Sunglasses recommended")

    # Wind protection
    if feels_like < temp - 5:  # Significant wind chill
        suggestions.append("🧣 Scarf for wind protection")

    return suggestions


def get_temporal_context(
    current_temp: float, previous_temp: Optional[float], unit: str
) -> Optional[str]:
    """Returns context comparing current temperature to previous day."""
    if previous_temp is None:
        return None

    diff = current_temp - previous_temp
    if abs(diff) < 0.5:  # Less than 0.5 degree difference
        return None

    direction = "↑" if diff > 0 else "↓"
    abs_diff = abs(diff)

    if unit == "°C":
        return f"{direction} {abs_diff:.1f}°C {'warmer' if diff > 0 else 'cooler'} than yesterday"
    else:
        return f"{direction} {abs_diff:.1f}°F {'warmer' if diff > 0 else 'cooler'} than yesterday"
