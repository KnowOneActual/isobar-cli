import time

from rich.columns import Columns
from rich.console import Console
from rich.table import Table

from .logic import (
    WMO_CODES,
    get_aqi_label,
    get_feels_like_label,
    get_precip_headline,
    get_temp_color,
)
from .models import WeatherData

console = Console()


def get_weather_icon(code: int) -> tuple[str, str]:
    """Return (emoji, description) for a WMO weather code."""
    return WMO_CODES.get(code, ("🌡️", "Unknown"))


def build_weather_table(weather: WeatherData) -> Table:
    """Constructs the current conditions weather table."""
    icon, desc = get_weather_icon(weather.weather_code)
    temp_color = get_temp_color(weather.temp, weather.units.temp)
    feels_color = get_temp_color(weather.feels_like, weather.units.temp)
    feels_label = get_feels_like_label(
        weather.temp, weather.feels_like, weather.units.temp
    )

    table = Table(
        title=f"\n[bold white]{weather.city} Weather[/bold white]",
        show_header=False,
        box=None,
        padding=(0, 1),
    )
    table.add_column("Icon", justify="center")
    table.add_column("Label", justify="left")
    table.add_column("Value", justify="right")

    table.add_row(icon, "Conditions:", f"[bold]{desc}[/bold]")
    table.add_row(
        "🌡️",
        "Temperature:",
        f"[{temp_color}]{weather.temp}{weather.units.temp}[/{temp_color}]",
    )
    table.add_row(
        "🤔",
        feels_label,
        f"[{feels_color}]{weather.feels_like}{weather.units.temp}[/{feels_color}]",
    )
    table.add_row("💨", "Wind Speed:", f"{weather.wind_speed} {weather.units.wind}")
    table.add_row("💧", "Humidity:", f"{weather.humidity}%")

    if weather.aqi is not None:
        label, color = get_aqi_label(weather.aqi)
        table.add_row(
            "😷", "Air Quality:", f"[{color}]{weather.aqi} ({label})[/{color}]"
        )

    headline = get_precip_headline(
        weather.precip_prob, weather.rainfall, weather.snowfall, weather.units.precip
    )
    precip_val = f"{weather.precip_prob}% (6h)"
    if headline:
        precip_val += f" | [dim italic yellow]{headline}[/dim italic yellow]"
    table.add_row("☔", "Precip Chance:", precip_val)

    if weather.rainfall > 0.01:
        table.add_row(
            "🌧️", "Rain Expected:", f"~{weather.rainfall:.2f}{weather.units.precip}"
        )
    if weather.snowfall > 0.01:
        table.add_row(
            "❄️", "Snow Expected:", f"~{weather.snowfall:.2f}{weather.units.precip}"
        )

    table.add_row("🌅", "Sunrise:", f"[yellow]{weather.sunrise}[/yellow]")
    table.add_row("🌇", "Sunset:", f"[orange1]{weather.sunset}[/orange1]")

    return table


def display_weather(weather: WeatherData):
    """Renders the current conditions weather card for a single city."""
    if not weather:
        console.print("[bold red]No weather data available.[/bold red]")
        return

    if weather.last_updated:
        minutes_ago = int((time.time() - weather.last_updated) / 60)
        if minutes_ago > 0:
            console.print(f"[dim]Updated {minutes_ago} min ago[/dim]")

    console.print(build_weather_table(weather))
    print()


def display_multi_weather(weather_list: list[WeatherData]):
    """Renders multiple weather cards side-by-side using Columns."""
    tables = [build_weather_table(w) for w in weather_list if w]
    if not tables:
        console.print("[bold red]No weather data available.[/bold red]")
        return

    # Show cache info if any city was cached
    times = [w.last_updated for w in weather_list if w and w.last_updated]
    if times:
        minutes_ago = int((time.time() - (sum(times) / len(times))) / 60)
        if minutes_ago > 0:
            console.print(f"[dim]Cached data ~{minutes_ago} min ago[/dim]")

    console.print(Columns(tables, equal=True, expand=False))
    print()


def display_forecast(weather: WeatherData):
    """Renders a 7-day forecast table below the current conditions card."""
    if not weather.forecast:
        console.print("[yellow]No forecast data available.[/yellow]")
        return

    table = Table(
        title=f"[bold white]7-Day Forecast — {weather.city}[/bold white]",
        show_header=True,
        header_style="bold dim",
        box=None,
        padding=(0, 2),
    )
    table.add_column("Day", justify="left", min_width=10)
    table.add_column("", justify="center")
    table.add_column("Conditions", justify="left", min_width=18)
    table.add_column("High", justify="right")
    table.add_column("Low", justify="right")
    table.add_column("Rain%", justify="right")

    for i, day in enumerate(weather.forecast):
        day_label = "Today" if i == 0 else day.dt.strftime("%a %b %-d")
        icon, desc = get_weather_icon(day.weather_code)

        high_color = get_temp_color(day.high, weather.units.temp)
        low_color = get_temp_color(day.low, weather.units.temp)
        rain_color = (
            "cyan"
            if day.precip_prob >= 60
            else "yellow"
            if day.precip_prob >= 30
            else "dim"
        )

        table.add_row(
            f"[bold]{day_label}[/bold]" if i == 0 else day_label,
            icon,
            desc,
            f"[{high_color}]{day.high}{weather.units.temp}[/{high_color}]",
            f"[{low_color}]{day.low}{weather.units.temp}[/{low_color}]",
            f"[{rain_color}]{day.precip_prob}%[/{rain_color}]",
        )

    console.print(table)
    print()


def display_hourly(weather: WeatherData):
    """Renders a compact hourly forecast table for the next 12-24 hours."""
    if not weather.hourly:
        console.print("[yellow]No hourly data available.[/yellow]")
        return

    table = Table(
        title=f"[bold white]Hourly Forecast — {weather.city}[/bold white]",
        show_header=True,
        header_style="bold dim",
        box=None,
        padding=(0, 2),
    )
    table.add_column("Time", justify="left")
    table.add_column("", justify="center")
    table.add_column("Temp", justify="right")
    table.add_column("Rain%", justify="right")
    table.add_column("Conditions", justify="left")

    for hour in weather.hourly[:12]:
        time_label = hour.dt.strftime("%-I %p")
        icon, desc = get_weather_icon(hour.weather_code)
        temp_color = get_temp_color(hour.temp, weather.units.temp)
        rain_color = (
            "cyan"
            if hour.precip_prob >= 60
            else "yellow"
            if hour.precip_prob >= 30
            else "dim"
        )

        table.add_row(
            time_label,
            icon,
            f"[{temp_color}]{hour.temp}{weather.units.temp}[/{temp_color}]",
            f"[{rain_color}]{hour.precip_prob}%[/{rain_color}]",
            f"[dim]{desc}[/dim]",
        )

    console.print(table)
    print()
