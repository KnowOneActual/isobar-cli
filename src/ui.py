from rich.console import Console
from rich.table import Table
import json
import time
from pathlib import Path

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
    precip = weather_data.get("precipitation", "0.0")

    temp_color = get_temp_color(temp)
    feels_color = get_temp_color(feels_like)

    # Cache timestamp (only if cached)
    cache_timestamp = None
    if city != "Unknown Location":
        cache_file = CACHE_DIR / f"{city.split(',')[0].strip().lower().replace(' ',             '_')}.json"

        if cache_file.exists():
            try:
                cache_data = json.loads(cache_file.read_text())
                if "timestamp" in cache_data and time.time() - cache_data["timestamp"] < 900:
                    minutes_ago = int((time.time() - cache_data["timestamp"]) / 60)
                    console.print(f"[dim]Updated {minutes_ago} min ago[/dim]")
            except:
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
    table.add_row("🌧️", "Precipitation:", f"{precip} in")

    console.print(table)
    print() # Adds a blank line at the end for clean spacing
