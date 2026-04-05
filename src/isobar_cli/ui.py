import time

from rich.columns import Columns
from rich.console import Console
from rich.table import Table

from .logic import (
    WMO_CODES,
    get_aqi_label,
    get_feels_like_label,
    get_humidity_category,
    get_preparation_guidance,
    get_temp_color,
    get_temperature_comfort,
    get_temporal_context,
    get_uv_category,
    get_wind_category_label,
    get_wind_gust_alert,
)
from .models import WeatherData

console = Console()

# Industrial color palette
COLORS = {
    "primary": "bright_white",
    "secondary": "bright_black",
    "accent": "bright_cyan",
    "warning": "bright_yellow",
    "danger": "bright_red",
    "success": "bright_green",
    "muted": "grey50",
    "highlight": "bright_magenta",
    "steel": "bright_blue",
    "concrete": "white",
}


def get_weather_icon(code: int) -> tuple[str, str]:
    """Return (emoji, description) for a WMO weather code."""
    return WMO_CODES.get(code, ("🌡️", "Unknown"))


def build_weather_table(weather: WeatherData) -> Table:
    """Constructs the current conditions weather table with borderless industrial aesthetic."""
    icon, desc = get_weather_icon(weather.weather_code)
    temp_color = get_temp_color(weather.temp, weather.units.temp)
    feels_color = get_temp_color(weather.feels_like, weather.units.temp)
    feels_label = get_feels_like_label(
        weather.temp, weather.feels_like, weather.units.temp
    )

    # Get meaningful labels for weather data
    temp_comfort, temp_comfort_color = get_temperature_comfort(
        weather.temp, weather.units.temp
    )
    humidity_category, humidity_color = get_humidity_category(weather.humidity)
    wind_category, wind_color = get_wind_category_label(
        weather.wind_speed, weather.units.wind
    )

    # Create borderless industrial-style table
    table = Table(
        title=f"[{COLORS['primary']} bold]WEATHER OBSERVATORY · {weather.city.upper()}[/{COLORS['primary']} bold]",
        show_header=False,
        box=None,  # No borders
        padding=(0, 1),
        width=60,
        title_style=f"{COLORS['primary']} bold",
    )

    # Add columns: icon, metric, value, category
    table.add_column("", justify="center", width=3, style=COLORS["accent"])
    table.add_column(
        "METRIC", justify="left", width=18, style=f"{COLORS['muted']} bold"
    )
    table.add_column("VALUE", justify="right", width=12, style=COLORS["primary"])
    table.add_column("CATEGORY", justify="right", width=20, style=COLORS["secondary"])

    # Weather condition
    table.add_row(
        f"[{COLORS['accent']}]{icon}[/{COLORS['accent']}]",
        "CONDITIONS",
        f"[{COLORS['primary']}]{desc.upper()}[/{COLORS['primary']}]",
        "",
    )

    # Temperature with comfort category
    table.add_row(
        "🌡️",
        "TEMPERATURE",
        f"[{temp_color}]{weather.temp}{weather.units.temp}[/{temp_color}]",
        f"[{temp_comfort_color}]{temp_comfort}[/{temp_comfort_color}]",
    )

    # Feels like with difference
    temp_diff = weather.feels_like - weather.temp
    diff_symbol = "▲" if temp_diff > 0 else "▼" if temp_diff < 0 else "▬"
    diff_color = (
        COLORS["danger"]
        if temp_diff > 5
        else COLORS["success"]
        if temp_diff < -5
        else COLORS["muted"]
    )
    feels_comfort, feels_comfort_color = get_temperature_comfort(
        weather.feels_like, weather.units.temp
    )
    table.add_row(
        "🤔",
        f"{feels_label.upper()}",
        f"[{feels_color}]{weather.feels_like}{weather.units.temp}[/{feels_color}]",
        f"[{feels_comfort_color}]{feels_comfort} [{diff_color}]{diff_symbol}{abs(temp_diff):.1f}{weather.units.temp}[/{diff_color}][/{feels_comfort_color}]",
    )

    # Wind with category
    table.add_row(
        "💨",
        "WIND SPEED",
        f"{weather.wind_speed} {weather.units.wind}",
        f"[{wind_color}]{wind_category}[/{wind_color}]",
    )

    # Humidity with category
    table.add_row(
        "💧",
        "HUMIDITY",
        f"{weather.humidity}%",
        f"[{humidity_color}]{humidity_category}[/{humidity_color}]",
    )

    # Air Quality
    if weather.aqi is not None:
        label, color = get_aqi_label(weather.aqi)
        table.add_row(
            "😷",
            "AIR QUALITY",
            f"[{color}]{weather.aqi}[/{color}]",
            f"[{color}]{label.upper()}[/{color}]",
        )

    # Precipitation
    precip_category = (
        "DRY"
        if weather.precip_prob < 20
        else "LIGHT"
        if weather.precip_prob < 50
        else "MODERATE"
        if weather.precip_prob < 80
        else "HEAVY"
    )
    precip_color = (
        COLORS["success"]
        if weather.precip_prob < 20
        else COLORS["warning"]
        if weather.precip_prob < 50
        else COLORS["danger"]
    )
    table.add_row(
        "☔",
        "PRECIPITATION",
        f"{weather.precip_prob}% (6h)",
        f"[{precip_color}]{precip_category}[/{precip_color}]",
    )

    # Sunrise/Sunset
    table.add_row(
        "🌅",
        "SUNRISE",
        f"[{COLORS['warning']}]{weather.sunrise}[/{COLORS['warning']}]",
        "",
    )

    table.add_row(
        "🌇",
        "SUNSET",
        f"[{COLORS['danger']}]{weather.sunset}[/{COLORS['danger']}]",
        "",
    )

    # UV Index
    if weather.uv_index is not None:
        uv_category, uv_color = get_uv_category(weather.uv_index)
        table.add_row(
            "☀️",
            "UV INDEX",
            f"[{uv_color}]{weather.uv_index:.1f}[/{uv_color}]",
            f"[{uv_color}]{uv_category}[/{uv_color}]",
        )

    # Wind Gust
    if weather.wind_gust is not None:
        gust_alert = get_wind_gust_alert(weather.wind_speed, weather.wind_gust)
        gust_category, gust_color = get_wind_category_label(
            weather.wind_gust, weather.units.wind
        )
        if gust_alert:
            table.add_row(
                "⚡",
                "[bold yellow]GUST ALERT[/bold yellow]",
                f"[bold yellow]{weather.wind_gust} {weather.units.wind}[/bold yellow]",
                f"[bold yellow]{gust_category} ⚠️[/bold yellow]",
            )
        else:
            table.add_row(
                "💨",
                "WIND GUST",
                f"{weather.wind_gust} {weather.units.wind}",
                f"[{gust_color}]{gust_category}[/{gust_color}]",
            )

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

    # Show preparation guidance
    display_preparation_guidance(weather)

    print()


def display_preparation_guidance(weather: WeatherData):
    """Displays clothing and gear suggestions with industrial aesthetic."""
    suggestions = get_preparation_guidance(
        temp=weather.temp,
        feels_like=weather.feels_like,
        precip_prob=weather.precip_prob,
        weather_code=weather.weather_code,
        uv_index=weather.uv_index,
        unit=weather.units.temp,
    )

    if not suggestions:
        return

    # Temporal context with industrial styling
    temporal_context = get_temporal_context(
        current_temp=weather.temp,
        previous_temp=weather.previous_day_temp,
        unit=weather.units.temp,
    )

    if temporal_context:
        console.print(
            f"[{COLORS['muted']}]────────────────────────────────────────[/{COLORS['muted']}]"
        )
        console.print(
            f"[{COLORS['primary']} bold]TREND ANALYSIS[/{COLORS['primary']} bold]"
        )
        console.print(
            f"[{COLORS['muted']}]{temporal_context.upper()}[/{COLORS['muted']}]"
        )
        console.print(
            f"[{COLORS['muted']}]────────────────────────────────────────[/{COLORS['muted']}]"
        )
        print()

    # Create borderless guidance panel
    console.print(
        f"[{COLORS['muted']}]────────────────────────────────────────[/{COLORS['muted']}]"
    )
    console.print(
        f"[{COLORS['primary']} bold]PREPARATION PROTOCOL[/{COLORS['primary']} bold]"
    )
    console.print(
        f"[{COLORS['muted']}]────────────────────────────────────────[/{COLORS['muted']}]"
    )

    # Categorize suggestions by priority
    high_priority = []
    medium_priority = []
    low_priority = []

    for suggestion in suggestions:
        if any(
            keyword in suggestion.lower()
            for keyword in ["severe", "danger", "warning", "extreme", "emergency"]
        ):
            high_priority.append(suggestion)
        elif any(
            keyword in suggestion.lower()
            for keyword in ["recommended", "suggest", "consider", "advisable"]
        ):
            medium_priority.append(suggestion)
        else:
            low_priority.append(suggestion)

    # Display high priority items with danger styling
    if high_priority:
        console.print(
            f"[{COLORS['danger']} bold]⚠️  HIGH PRIORITY[/{COLORS['danger']} bold]"
        )
        for suggestion in high_priority:
            console.print(f"  [{COLORS['danger']}]▶[/{COLORS['danger']}] {suggestion}")
        print()

    # Display medium priority items with warning styling
    if medium_priority:
        console.print(
            f"[{COLORS['warning']} bold]▲  RECOMMENDED[/{COLORS['warning']} bold]"
        )
        for suggestion in medium_priority:
            console.print(
                f"  [{COLORS['warning']}]▶[/{COLORS['warning']}] {suggestion}"
            )
        print()

    # Display low priority items with muted styling
    if low_priority:
        console.print(f"[{COLORS['muted']} bold]○  ADVISORY[/{COLORS['muted']} bold]")
        for suggestion in low_priority:
            console.print(f"  [{COLORS['muted']}]▶[/{COLORS['muted']}] {suggestion}")

    console.print(
        f"[{COLORS['muted']}]────────────────────────────────────────[/{COLORS['muted']}]"
    )


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
    """Renders a 7-day forecast table with borderless industrial aesthetic."""
    if not weather.forecast:
        console.print(
            f"[{COLORS['warning']}]No forecast data available.[/{COLORS['warning']}]"
        )
        return

    # Create borderless forecast table
    table = Table(
        title=f"[{COLORS['primary']} bold]FORECAST PANEL · {weather.city.upper()}[/{COLORS['primary']} bold]",
        show_header=True,
        box=None,  # No borders
        header_style=f"{COLORS['muted']} bold",
        padding=(0, 1),
        width=70,
    )

    # Borderless column headers
    table.add_column("DAY", justify="left", width=10, style=f"{COLORS['accent']} bold")
    table.add_column("", justify="center", width=2, style=COLORS["accent"])
    table.add_column("CONDITIONS", justify="left", width=18, style=COLORS["muted"])
    table.add_column(
        "HIGH", justify="right", width=8, style=f"{COLORS['primary']} bold"
    )
    table.add_column("LOW", justify="right", width=8, style=f"{COLORS['primary']} bold")
    table.add_column(
        "RAIN%", justify="right", width=8, style=f"{COLORS['accent']} bold"
    )

    for i, day in enumerate(weather.forecast):
        day_label = "TODAY" if i == 0 else day.dt.strftime("%a").upper()
        icon, desc = get_weather_icon(day.weather_code)

        # Temperature colors
        high_color = get_temp_color(day.high, weather.units.temp)
        low_color = get_temp_color(day.low, weather.units.temp)

        # Precipitation color based on probability
        if day.precip_prob >= 70:
            rain_color = COLORS["danger"]
        elif day.precip_prob >= 40:
            rain_color = COLORS["warning"]
        elif day.precip_prob >= 20:
            rain_color = COLORS["accent"]
        else:
            rain_color = COLORS["muted"]

        table.add_row(
            f"[{COLORS['primary']} bold]{day_label}[/{COLORS['primary']} bold]"
            if i == 0
            else f"[{COLORS['muted']}]{day_label}[/{COLORS['muted']}]",
            f"[{COLORS['accent']}]{icon}[/{COLORS['accent']}]",
            f"[{COLORS['concrete']}]{desc.upper()}[/{COLORS['concrete']}]",
            f"[{high_color}]{day.high}{weather.units.temp}[/{high_color}]",
            f"[{low_color}]{day.low}{weather.units.temp}[/{low_color}]",
            f"[{rain_color}]{day.precip_prob}%[/{rain_color}]",
        )

    console.print(table)
    print()


def display_hourly(weather: WeatherData):
    """Renders an hourly forecast table with borderless industrial aesthetic."""
    if not weather.hourly:
        console.print(
            f"[{COLORS['warning']}]No hourly data available.[/{COLORS['warning']}]"
        )
        return

    # Create borderless hourly table
    table = Table(
        title=f"[{COLORS['primary']} bold]HOURLY FORECAST · {weather.city.upper()}[/{COLORS['primary']} bold]",
        show_header=True,
        box=None,  # No borders
        header_style=f"{COLORS['muted']} bold",
        padding=(0, 1),
        width=60,
    )

    # Simplified column headers
    table.add_column("TIME", justify="left", width=6, style=f"{COLORS['accent']} bold")
    table.add_column("", justify="center", width=2, style=COLORS["accent"])
    table.add_column(
        "TEMP", justify="right", width=8, style=f"{COLORS['primary']} bold"
    )
    table.add_column(
        "RAIN%", justify="right", width=6, style=f"{COLORS['accent']} bold"
    )
    table.add_column("CONDITIONS", justify="left", width=18, style=COLORS["concrete"])

    for hour in weather.hourly[:12]:
        time_label = hour.dt.strftime("%-I%p").upper()
        icon, desc = get_weather_icon(hour.weather_code)
        temp_color = get_temp_color(hour.temp, weather.units.temp)

        # Precipitation color
        if hour.precip_prob >= 70:
            rain_color = COLORS["danger"]
        elif hour.precip_prob >= 40:
            rain_color = COLORS["warning"]
        elif hour.precip_prob >= 20:
            rain_color = COLORS["accent"]
        else:
            rain_color = COLORS["muted"]

        table.add_row(
            f"[{COLORS['muted']}]{time_label}[/{COLORS['muted']}]",
            f"[{COLORS['accent']}]{icon}[/{COLORS['accent']}]",
            f"[{temp_color}]{hour.temp}{weather.units.temp}[/{temp_color}]",
            f"[{rain_color}]{hour.precip_prob}%[/{rain_color}]",
            f"[{COLORS['concrete']}]{desc.upper()}[/{COLORS['concrete']}]",
        )

    console.print(table)
    print()
