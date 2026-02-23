import json
import time
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
CACHE_DIR = Path.home() / ".cache" / "isobar"

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
        # High chance (>60%)
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
    Renders the weather data in a visually pleasing terminal panel.
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

    temp_color = get_temp_color(temp)
    feels_color = get_temp_color(feels_like)

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
                pass  # Silently ignore cache issues

    table = Table(
        title=f"\n[bold white]{city} Weather[/bold white]",
        show_header=False,
        box=None,
        padding=(0, 1)
    )

    table.add_column("Icon", justify="center")
    table.add_column("Label", justify="left")
    table.add_column("Value", justify="right")

    table.add_row("🌡️", "Temperature:", f"[{temp_color}]{temp}°F[/{temp_color}]")
    table.add_row("🤔", "Real Feel:", f"[{feels_color}]{feels_like}°F[/{feels_color}]")
    table.add_row("💨", "Wind Speed:", f"{wind_speed} mph")
    table.add_row("💧", "Humidity:", f"{humidity}%")
    
    # Precip Chance + Headline (together!)
    headline = get_precip_headline(weather_data)
    precip_value = f"{precip_prob}% (6h)"
    if headline:
        precip_value += f" | [dim italic yellow]{headline}[/dim italic yellow]"
    
    table.add_row("☔", "Precip Chance:", precip_value)

    # Rain only if meaningful accumulation expected
    if rainfall_inch > 0.01:
        table.add_row("🌧️", "Rain Expected:", f"~{rainfall_inch:.2f}\"")
    
    # Snow only if meaningful accumulation expected
    if snowfall_inch > 0.01:
        table.add_row("❄️", "Snow Expected:", f"~{snowfall_inch:.2f}\"")

    console.print(table)
    print()  # Adds a blank line at the end for clean spacing
