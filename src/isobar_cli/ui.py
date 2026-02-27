import json
import time
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
CACHE_DIR = Path.home() / ".cache" / "isobar"


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


def get_temp_color(temp_val) -> str:
    """Returns a Rich color tag based on the temperature."""
    try:
        t = float(temp_val)
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
    rainfall = weather_data.get("rainfall_inch", 0)
    snowfall = weather_data.get("snowfall_inch", 0)
    total_precip = rainfall + snowfall

    if precip_prob < 30:
        return "Dry conditions expected"
    elif precip_prob < 60:
        if total_precip < 0.1:
            return "Very low precip risk"
        return "Possible light precip"
    else:
        if snowfall > rainfall and snowfall > 0.25:
            return "Snowy conditions likely"
        elif rainfall > 0.75:
            return "Heavy rain likely"
        elif rainfall > 0.25:
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
    rainfall_inch = weather_data.get("rainfall_inch", 0)
    snowfall_inch = weather_data.get("snowfall_inch", 0)
    sunrise = weather_data.get("sunrise", "--")
    sunset = weather_data.get("sunset", "--")
    weather_code = weather_data.get("weather_code", 0)

    temp_color = get_temp_color(temp)
    feels_color = get_temp_color(feels_like)
    condition_icon, condition_desc = get_weather_icon(weather_code)

    # Cache timestamp (only if cached)
    if city != "Unknown Location":
        input_city = city.split(",")[0].strip().lower().replace(" ", "_")
        cache_file = CACHE_DIR / f"{input_city}.json"
        if cache_file.exists():
            try:
                cache_data = json.loads(cache_file.read_text())
                timestamp = cache_data.get("timestamp")
                if timestamp and time.time() - timestamp < 900:
                    minutes_ago = int((time.time() - timestamp) / 60)
                    console.print(f"[dim]Updated {minutes_ago} min ago[/dim]")
            except Exception:
                pass

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
    table.add_row("🌡️", "Temperature:", f"[{temp_color}]{temp}°F[/{temp_color}]")
    table.add_row("🤔", "Real Feel:", f"[{feels_color}]{feels_like}°F[/{feels_color}]")
    table.add_row("💨", "Wind Speed:", f"{wind_speed} mph")
    table.add_row("💧", "Humidity:", f"{humidity}%")

    headline = get_precip_headline(weather_data)
    precip_value = f"{precip_prob}% (6h)"
    if headline:
        precip_value += f" | [dim italic yellow]{headline}[/dim italic yellow]"
    table.add_row("☔", "Precip Chance:", precip_value)

    if rainfall_inch > 0.01:
        table.add_row("🌧️", "Rain Expected:", f'~{rainfall_inch:.2f}"')
    if snowfall_inch > 0.01:
        table.add_row("❄️", "Snow Expected:", f'~{snowfall_inch:.2f}"')

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

        high_color = get_temp_color(high)
        low_color = get_temp_color(low)
        rain_color = "cyan" if precip >= 60 else "yellow" if precip >= 30 else "dim"

        table.add_row(
            f"[bold]{day_label}[/bold]" if i == 0 else day_label,
            icon,
            desc,
            f"[{high_color}]{high}°F[/{high_color}]",
            f"[{low_color}]{low}°F[/{low_color}]",
            f"[{rain_color}]{precip}%[/{rain_color}]",
        )

    console.print(table)
    print()
