import time
from datetime import datetime

from rich.console import Console
from rich.table import Table

console = Console()


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


def get_weather_icon(code: int) -> tuple[str, str]:
    """Return (emoji, description) for a WMO weather code."""
    return WMO_CODES.get(code, ("🌡️", "Unknown"))


def get_temp_color(temp_val, unit="°F") -> str:
    """Returns a Rich color tag based on the temperature and unit."""
    try:
        t = float(temp_val)
        if unit == "°C":
            # Celsius thresholds (approximate F to C conversion)
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
            # Fahrenheit thresholds
            if t < 32:
                return "bold cyan"
            if t < 60:
                return "bold blue"
            if t < 80:
                return "bold green"
            if t < 95:
                return "bold yellow"
            return "bold red"
    except (ValueError, TypeError):
        return "white"


def get_precip_headline(weather_data: dict) -> str:
    """Generate a single-line comfort summary for precip decisions."""
    precip_prob = weather_data.get("precip_prob", 0)
    rainfall = weather_data.get("rainfall", 0)
    snowfall = weather_data.get("snowfall", 0)
    units = weather_data.get("units", {})
    unit_precip = units.get("precip", "in")
    total_precip = rainfall + snowfall

    # Use metric thresholds if unit is 'mm'
    if unit_precip == "mm":
        low_precip_limit = 2.5
        med_precip_limit = 6.0
        high_precip_limit = 19.0
        snow_precip_limit = 6.0
    else:
        low_precip_limit = 0.1
        med_precip_limit = 0.25
        high_precip_limit = 0.75
        snow_precip_limit = 0.25

    if precip_prob < 30:
        return "Dry conditions expected"
    elif precip_prob < 60:
        if total_precip < low_precip_limit:
            return "Very low precip risk"
        return "Possible light precip"
    else:
        if snowfall > rainfall and snowfall > snow_precip_limit:
            return "Snowy conditions likely"
        elif rainfall > high_precip_limit:
            return "Heavy rain likely"
        elif rainfall > med_precip_limit:
            return "Moderate rain likely"
        else:
            return "Light rain likely"

    return ""


def display_weather(weather_data: dict):
    """
    Renders the current conditions weather card.
    """
    if not weather_data:
        console.print("[bold red]No weather data available.[/bold red]")
        return

    city = weather_data.get("city", "Unknown Location")
    temp = weather_data.get("temp", "--")
    feels_like = weather_data.get("feels_like", "--")
    wind_speed = weather_data.get("wind_speed", "--")
    humidity = weather_data.get("humidity", "--")
    precip_prob = weather_data.get("precip_prob", 0)
    rainfall = weather_data.get("rainfall", 0)
    snowfall = weather_data.get("snowfall", 0)
    sunrise = weather_data.get("sunrise", "--")
    sunset = weather_data.get("sunset", "--")
    weather_code = weather_data.get("weather_code", 0)
    units = weather_data.get("units", {"temp": "°F", "wind": "mph", "precip": "in"})

    temp_color = get_temp_color(temp, units["temp"])
    feels_color = get_temp_color(feels_like, units["temp"])
    condition_icon, condition_desc = get_weather_icon(weather_code)

    # Show "Updated X min ago" if data is from cache
    last_updated = weather_data.get("last_updated")
    if last_updated:
        minutes_ago = int((time.time() - last_updated) / 60)
        if minutes_ago > 0:
            console.print(f"[dim]Updated {minutes_ago} min ago[/dim]")

    table = Table(
        title=f"\n[bold white]{city} Weather[/bold white]",
        show_header=False,
        box=None,
        padding=(0, 1),
    )
    table.add_column("Icon", justify="center")
    table.add_column("Label", justify="left")
    table.add_column("Value", justify="right")

    table.add_row(condition_icon, "Conditions:", f"[bold]{condition_desc}[/bold]")
    table.add_row(
        "🌡️", "Temperature:", f"[{temp_color}]{temp}{units['temp']}[/{temp_color}]"
    )
    table.add_row(
        "🤔", "Real Feel:", f"[{feels_color}]{feels_like}{units['temp']}[/{feels_color}]"
    )
    table.add_row("💨", "Wind Speed:", f"{wind_speed} {units['wind']}")
    table.add_row("💧", "Humidity:", f"{humidity}%")

    headline = get_precip_headline(weather_data)
    precip_value = f"{precip_prob}% (6h)"
    if headline:
        precip_value += f" | [dim italic yellow]{headline}[/dim italic yellow]"
    table.add_row("☔", "Precip Chance:", precip_value)

    if rainfall > 0.01:
        table.add_row("🌧️", "Rain Expected:", f"~{rainfall:.2f}{units['precip']}")
    if snowfall > 0.01:
        table.add_row("❄️", "Snow Expected:", f"~{snowfall:.2f}{units['precip']}")

    table.add_row("🌅", "Sunrise:", f"[yellow]{sunrise}[/yellow]")
    table.add_row("🌇", "Sunset:", f"[orange1]{sunset}[/orange1]")

    console.print(table)
    print()


def display_forecast(weather_data: dict):
    """
    Renders a 7-day forecast table below the current conditions card.
    """
    forecast = weather_data.get("forecast", [])
    if not forecast:
        console.print("[yellow]No forecast data available.[/yellow]")
        return

    city = weather_data.get("city", "Unknown Location")
    units = weather_data.get("units", {"temp": "°F", "wind": "mph", "precip": "in"})

    table = Table(
        title=f"[bold white]7-Day Forecast — {city}[/bold white]",
        show_header=True,
        header_style="bold dim",
        box=None,
        padding=(0, 2),
    )
    table.add_column("Day", justify="left", min_width=10)
    table.add_column("", justify="center")  # emoji
    table.add_column("Conditions", justify="left", min_width=18)
    table.add_column("High", justify="right")
    table.add_column("Low", justify="right")
    table.add_column("Rain%", justify="right")

    for i, day in enumerate(forecast):
        # Parse date string to get weekday name
        try:
            dt = datetime.strptime(day["date"], "%Y-%m-%d")
            day_label = "Today" if i == 0 else dt.strftime("%a %b %-d")
        except ValueError:
            day_label = day["date"]

        icon, desc = get_weather_icon(int(day["weather_code"]))
        high = day["high"]
        low = day["low"]
        precip = int(day["precip_prob"])

        high_color = get_temp_color(high, units["temp"])
        low_color = get_temp_color(low, units["temp"])
        rain_color = "cyan" if precip >= 60 else "yellow" if precip >= 30 else "dim"

        table.add_row(
            f"[bold]{day_label}[/bold]" if i == 0 else day_label,
            icon,
            desc,
            f"[{high_color}]{high}{units['temp']}[/{high_color}]",
            f"[{low_color}]{low}{units['temp']}[/{low_color}]",
            f"[{rain_color}]{precip}%[/{rain_color}]",
        )

    console.print(table)
    print()


def display_hourly(weather_data: dict):
    """
    Renders a compact hourly forecast table for the next 12-24 hours.
    """
    hourly = weather_data.get("hourly", [])
    if not hourly:
        console.print("[yellow]No hourly data available.[/yellow]")
        return

    city = weather_data.get("city", "Unknown Location")
    units = weather_data.get("units", {"temp": "°F", "wind": "mph", "precip": "in"})

    table = Table(
        title=f"[bold white]Hourly Forecast — {city}[/bold white]",
        show_header=True,
        header_style="bold dim",
        box=None,
        padding=(0, 2),
    )
    table.add_column("Time", justify="left")
    table.add_column("", justify="center")  # emoji
    table.add_column("Temp", justify="right")
    table.add_column("Rain%", justify="right")
    table.add_column("Conditions", justify="left")

    # Show only next 12 hours for compactness
    for hour in hourly[:12]:
        try:
            dt = datetime.fromisoformat(hour["time"].replace("Z", "+00:00"))
            time_label = dt.strftime("%-I %p")
        except ValueError:
            time_label = hour["time"]

        icon, desc = get_weather_icon(int(hour["weather_code"]))
        temp = hour["temp"]
        precip = int(hour["precip_prob"])

        temp_color = get_temp_color(temp, units["temp"])
        rain_color = "cyan" if precip >= 60 else "yellow" if precip >= 30 else "dim"

        table.add_row(
            time_label,
            icon,
            f"[{temp_color}]{temp}{units['temp']}[/{temp_color}]",
            f"[{rain_color}]{precip}%[/{rain_color}]",
            f"[dim]{desc}[/dim]",
        )

    console.print(table)
    print()
