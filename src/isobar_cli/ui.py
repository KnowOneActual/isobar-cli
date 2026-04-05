import time

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.table import Table

from .logic import (
    WMO_CODES,
    get_aqi_label,
    get_feels_like_label,
    get_precip_headline,
    get_preparation_guidance,
    get_temp_color,
    get_temporal_context,
    get_uv_guidance,
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

# Weather severity indicators
SEVERITY_ICONS = {
    "extreme": "⚡",
    "high": "▲",
    "medium": "●",
    "low": "○",
    "normal": "◇",
}


def get_weather_icon(code: int) -> tuple[str, str]:
    """Return (emoji, description) for a WMO weather code."""
    return WMO_CODES.get(code, ("🌡️", "Unknown"))


def build_weather_table(weather: WeatherData) -> Table:
    """Constructs the current conditions weather table with industrial aesthetic."""
    icon, desc = get_weather_icon(weather.weather_code)
    temp_color = get_temp_color(weather.temp, weather.units.temp)
    feels_color = get_temp_color(weather.feels_like, weather.units.temp)
    feels_label = get_feels_like_label(
        weather.temp, weather.feels_like, weather.units.temp
    )

    # Create industrial-style table with heavy borders
    table = Table(
        title=f"[{COLORS['primary']} bold]┌─ WEATHER OBSERVATORY ─┐[/{COLORS['primary']} bold]\n"
        f"[{COLORS['steel']}]{weather.city.upper()}[/{COLORS['steel']}]",
        show_header=False,
        box=box.HEAVY,
        border_style=COLORS["secondary"],
        title_style=f"{COLORS['primary']} bold",
        padding=(0, 2),
        width=60,
    )

    # Add columns with industrial styling
    table.add_column("", justify="center", width=4, style=COLORS["accent"])
    table.add_column("METRIC", justify="left", width=20, style=COLORS["muted"])
    table.add_column("READING", justify="right", width=15, style=COLORS["primary"])
    table.add_column("STATUS", justify="right", width=15, style=COLORS["secondary"])

    # Weather condition row with severity indicator
    severity = (
        "medium" if weather.weather_code in [95, 96, 99, 65, 75, 86] else "normal"
    )
    table.add_row(
        f"[{COLORS['accent']}]{icon}[/{COLORS['accent']}]",
        "[bold]CONDITIONS[/bold]",
        f"[{COLORS['primary']} bold]{desc.upper()}[/{COLORS['primary']} bold]",
        f"[{COLORS['warning']}]{SEVERITY_ICONS[severity]}[/{COLORS['warning']}]",
    )

    # Temperature with industrial gauge visualization
    temp_gauge = create_gauge(
        weather.temp, weather.units.temp, 100 if weather.units.temp == "°F" else 40
    )
    table.add_row(
        "🌡️",
        "[bold]TEMPERATURE[/bold]",
        f"[{temp_color}]{weather.temp}{weather.units.temp}[/{temp_color}]",
        temp_gauge,
    )

    # Feels like with difference indicator
    temp_diff = weather.feels_like - weather.temp
    diff_symbol = "▲" if temp_diff > 0 else "▼" if temp_diff < 0 else "▬"
    diff_color = (
        COLORS["danger"]
        if temp_diff > 5
        else COLORS["success"]
        if temp_diff < -5
        else COLORS["muted"]
    )
    table.add_row(
        "🤔",
        f"[bold]{feels_label.upper()}[/bold]",
        f"[{feels_color}]{weather.feels_like}{weather.units.temp}[/{feels_color}]",
        f"[{diff_color}]{diff_symbol} {abs(temp_diff):.1f}{weather.units.temp}[/{diff_color}]",
    )

    # Wind with speed category
    wind_category = get_wind_category(weather.wind_speed, weather.units.wind)
    table.add_row(
        "💨",
        "[bold]WIND SPEED[/bold]",
        f"{weather.wind_speed} {weather.units.wind}",
        f"[{COLORS['steel']}]{wind_category}[/{COLORS['steel']}]",
    )

    # Humidity with moisture indicator
    humidity_indicator = "▓" * (weather.humidity // 20) + "░" * (
        5 - weather.humidity // 20
    )
    table.add_row(
        "💧",
        "[bold]HUMIDITY[/bold]",
        f"{weather.humidity}%",
        f"[{COLORS['accent']}]{humidity_indicator}[/{COLORS['accent']}]",
    )

    # Air Quality with health impact
    if weather.aqi is not None:
        label, color = get_aqi_label(weather.aqi)
        aqi_severity = (
            "high" if weather.aqi > 100 else "medium" if weather.aqi > 50 else "low"
        )
        table.add_row(
            "😷",
            "[bold]AIR QUALITY[/bold]",
            f"[{color}]{weather.aqi}[/{color}]",
            f"[{color}]{label.upper()} {SEVERITY_ICONS[aqi_severity]}[/{color}]",
        )

    # Precipitation with visual indicator
    precip_indicator = "●" * min(weather.precip_prob // 20, 5)
    headline = get_precip_headline(
        weather.precip_prob, weather.rainfall, weather.snowfall, weather.units.precip
    )
    table.add_row(
        "☔",
        "[bold]PRECIPITATION[/bold]",
        f"{weather.precip_prob}% (6h)",
        f"[{COLORS['accent']}]{precip_indicator}[/{COLORS['accent']}]",
    )

    if headline:
        table.add_row(
            "",
            "[dim]FORECAST[/dim]",
            f"[{COLORS['warning']} italic]{headline.upper()}[/{COLORS['warning']} italic]",
            "",
        )

    # Sunrise/Sunset with day progress
    table.add_row(
        "🌅",
        "[bold]SUNRISE[/bold]",
        f"[{COLORS['warning']}]{weather.sunrise}[/{COLORS['warning']}]",
        "[dim]DAWN[/dim]",
    )

    table.add_row(
        "🌇",
        "[bold]SUNSET[/bold]",
        f"[{COLORS['danger']}]{weather.sunset}[/{COLORS['danger']}]",
        "[dim]DUSK[/dim]",
    )

    # UV Index with protection level
    if weather.uv_index is not None:
        uv_label, uv_color = get_uv_guidance(weather.uv_index)
        uv_level = min(int(weather.uv_index / 2), 5)
        uv_indicator = "☀️" * uv_level
        table.add_row(
            "☀️",
            "[bold]UV INDEX[/bold]",
            f"[{uv_color}]{weather.uv_index:.1f}[/{uv_color}]",
            f"[{uv_color}]{uv_label.upper()} {uv_indicator}[/{uv_color}]",
        )

    # Wind Gust with alert styling
    if weather.wind_gust is not None:
        gust_alert = get_wind_gust_alert(weather.wind_speed, weather.wind_gust)
        if gust_alert:
            table.add_row(
                "⚡",
                "[bold yellow]GUST ALERT[/bold yellow]",
                f"[bold yellow]{weather.wind_gust} {weather.units.wind}[/bold yellow]",
                "[bold yellow]⚠️ SEVERE[/bold yellow]",
            )
        else:
            gust_ratio = (
                weather.wind_gust / weather.wind_speed if weather.wind_speed > 0 else 1
            )
            gust_indicator = "!" * min(int(gust_ratio * 2), 3)
            table.add_row(
                "💨",
                "[bold]WIND GUST[/bold]",
                f"{weather.wind_gust} {weather.units.wind}",
                f"[{COLORS['steel']}]{gust_indicator}[/{COLORS['steel']}]",
            )

    return table


def create_gauge(value: float, unit: str, max_value: float) -> str:
    """Create a text-based gauge visualization."""
    if unit == "°F":
        ranges = [
            (32, "bold cyan"),
            (60, "bold blue"),
            (80, "bold green"),
            (95, "bold yellow"),
            (max_value, "bold red"),
        ]
    else:
        ranges = [
            (0, "bold cyan"),
            (15, "bold blue"),
            (26, "bold green"),
            (35, "bold yellow"),
            (max_value, "bold red"),
        ]

    # Find appropriate color
    gauge_color = "bold white"
    for threshold, color in ranges:
        if value <= threshold:
            gauge_color = color
            break

    # Create gauge visualization
    gauge_width = 10
    filled = min(int((value / max_value) * gauge_width), gauge_width)
    gauge = "[" + gauge_color + "]" + "█" * filled + "[/" + gauge_color + "]"
    gauge += "[dim]" + "░" * (gauge_width - filled) + "[/dim]"

    return gauge


def get_wind_category(speed: float, unit: str) -> str:
    """Categorize wind speed."""
    if unit == "mph":
        if speed < 1:
            return "CALM"
        elif speed < 7:
            return "LIGHT"
        elif speed < 12:
            return "GENTLE"
        elif speed < 18:
            return "MODERATE"
        elif speed < 24:
            return "FRESH"
        elif speed < 31:
            return "STRONG"
        elif speed < 38:
            return "GALE"
        elif speed < 46:
            return "SEVERE"
        else:
            return "STORM"
    else:  # km/h
        if speed < 2:
            return "CALM"
        elif speed < 12:
            return "LIGHT"
        elif speed < 20:
            return "GENTLE"
        elif speed < 29:
            return "MODERATE"
        elif speed < 39:
            return "FRESH"
        elif speed < 50:
            return "STRONG"
        elif speed < 62:
            return "GALE"
        elif speed < 75:
            return "SEVERE"
        else:
            return "STORM"


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
            f"[{COLORS['secondary']}]┌─ TREND ANALYSIS ─┐[/{COLORS['secondary']}]"
        )
        console.print(
            f"[{COLORS['muted']}]{temporal_context.upper()}[/{COLORS['muted']}]"
        )
        console.print(
            f"[{COLORS['secondary']}]└──────────────────┘[/{COLORS['secondary']}]"
        )
        print()

    # Create industrial guidance panel
    console.print(
        f"[{COLORS['primary']} bold]┌─ PREPARATION PROTOCOL ─┐[/{COLORS['primary']} bold]"
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
            f"[{COLORS['danger']} bold]  ⚠️  HIGH PRIORITY[/{COLORS['danger']} bold]"
        )
        for suggestion in high_priority:
            console.print(
                f"    [{COLORS['danger']}]▶[/{COLORS['danger']}] {suggestion}"
            )
        print()

    # Display medium priority items with warning styling
    if medium_priority:
        console.print(
            f"[{COLORS['warning']} bold]  ▲  RECOMMENDED[/{COLORS['warning']} bold]"
        )
        for suggestion in medium_priority:
            console.print(
                f"    [{COLORS['warning']}]▶[/{COLORS['warning']}] {suggestion}"
            )
        print()

    # Display low priority items with muted styling
    if low_priority:
        console.print(f"[{COLORS['muted']} bold]  ○  ADVISORY[/{COLORS['muted']} bold]")
        for suggestion in low_priority:
            console.print(f"    [{COLORS['muted']}]▶[/{COLORS['muted']}] {suggestion}")

    console.print(
        f"[{COLORS['primary']} bold]└─────────────────────────┘[/{COLORS['primary']} bold]"
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
    """Renders a 7-day forecast table with industrial aesthetic."""
    if not weather.forecast:
        console.print(
            f"[{COLORS['warning']}]No forecast data available.[/{COLORS['warning']}]"
        )
        return

    # Create industrial forecast table
    table = Table(
        title=f"[{COLORS['primary']} bold]┌─ FORECAST PANEL ─┐[/{COLORS['primary']} bold]\n"
        f"[{COLORS['steel']}]{weather.city.upper()}[/{COLORS['steel']}]",
        show_header=True,
        header_style=f"{COLORS['muted']} bold",
        box=box.HEAVY,
        border_style=COLORS["secondary"],
        padding=(0, 1),
        width=70,
    )

    # Industrial column headers
    table.add_column("DAY", justify="left", width=12, style=f"{COLORS['accent']} bold")
    table.add_column("", justify="center", width=2, style=COLORS["accent"])
    table.add_column("CONDITIONS", justify="left", width=20, style=COLORS["muted"])
    table.add_column(
        "HIGH", justify="right", width=10, style=f"{COLORS['primary']} bold"
    )
    table.add_column(
        "LOW", justify="right", width=10, style=f"{COLORS['primary']} bold"
    )
    table.add_column(
        "RAIN%", justify="right", width=8, style=f"{COLORS['accent']} bold"
    )
    table.add_column("STATUS", justify="center", width=8, style=COLORS["secondary"])

    for i, day in enumerate(weather.forecast):
        day_label = "TODAY" if i == 0 else day.dt.strftime("%a").upper()
        icon, desc = get_weather_icon(day.weather_code)

        # Temperature colors
        high_color = get_temp_color(day.high, weather.units.temp)
        low_color = get_temp_color(day.low, weather.units.temp)

        # Precipitation severity indicator
        if day.precip_prob >= 70:
            rain_color = COLORS["danger"]
        elif day.precip_prob >= 40:
            rain_color = COLORS["warning"]
        elif day.precip_prob >= 20:
            rain_color = COLORS["accent"]
        else:
            rain_color = COLORS["muted"]

        # Day severity based on weather conditions
        if day.weather_code in [95, 96, 99, 65, 75, 86]:
            day_severity = "▲"
            severity_color = COLORS["warning"]
        elif day.precip_prob > 60:
            day_severity = "●"
            severity_color = COLORS["accent"]
        else:
            day_severity = "○"
            severity_color = COLORS["success"]

        table.add_row(
            f"[{COLORS['primary']} bold]{day_label}[/{COLORS['primary']} bold]"
            if i == 0
            else f"[{COLORS['muted']}]{day_label}[/{COLORS['muted']}]",
            f"[{COLORS['accent']}]{icon}[/{COLORS['accent']}]",
            f"[{COLORS['concrete']}]{desc.upper()}[/{COLORS['concrete']}]",
            f"[{high_color}]{day.high}{weather.units.temp}[/{high_color}]",
            f"[{low_color}]{day.low}{weather.units.temp}[/{low_color}]",
            f"[{rain_color}]{day.precip_prob}%[/{rain_color}]",
            f"[{severity_color}]{day_severity}[/{severity_color}]",
        )

    console.print(table)
    print()


def display_hourly(weather: WeatherData):
    """Renders an hourly forecast table with industrial aesthetic."""
    if not weather.hourly:
        console.print(
            f"[{COLORS['warning']}]No hourly data available.[/{COLORS['warning']}]"
        )
        return

    # Create industrial hourly table
    table = Table(
        title=f"[{COLORS['primary']} bold]┌─ HOURLY TRACKER ─┐[/{COLORS['primary']} bold]\n"
        f"[{COLORS['steel']}]{weather.city.upper()}[/{COLORS['steel']}]",
        show_header=True,
        header_style=f"{COLORS['muted']} bold",
        box=box.HEAVY,
        border_style=COLORS["secondary"],
        padding=(0, 1),
        width=65,
    )

    # Industrial column headers
    table.add_column("TIME", justify="left", width=8, style=f"{COLORS['accent']} bold")
    table.add_column("", justify="center", width=2, style=COLORS["accent"])
    table.add_column(
        "TEMP", justify="right", width=10, style=f"{COLORS['primary']} bold"
    )
    table.add_column("GAUGE", justify="left", width=12, style=COLORS["muted"])
    table.add_column(
        "RAIN%", justify="right", width=8, style=f"{COLORS['accent']} bold"
    )
    table.add_column("CONDITIONS", justify="left", width=20, style=COLORS["concrete"])
    table.add_column("", justify="center", width=2, style=COLORS["secondary"])

    for hour in weather.hourly[:12]:
        time_label = hour.dt.strftime("%-I%p").upper()
        icon, desc = get_weather_icon(hour.weather_code)
        temp_color = get_temp_color(hour.temp, weather.units.temp)

        # Temperature gauge
        temp_gauge = create_gauge(
            hour.temp, weather.units.temp, 100 if weather.units.temp == "°F" else 40
        )

        # Precipitation indicator
        if hour.precip_prob >= 70:
            rain_color = COLORS["danger"]
        elif hour.precip_prob >= 40:
            rain_color = COLORS["warning"]
        elif hour.precip_prob >= 20:
            rain_color = COLORS["accent"]
        else:
            rain_color = COLORS["muted"]

        # Hour severity indicator
        if hour.weather_code in [95, 96, 99]:
            severity_icon = "⚡"
            severity_color = COLORS["warning"]
        elif hour.precip_prob > 60:
            severity_icon = "☔"
            severity_color = COLORS["accent"]
        else:
            severity_icon = "○"
            severity_color = COLORS["success"]

        table.add_row(
            f"[{COLORS['muted']}]{time_label}[/{COLORS['muted']}]",
            f"[{COLORS['accent']}]{icon}[/{COLORS['accent']}]",
            f"[{temp_color}]{hour.temp}{weather.units.temp}[/{temp_color}]",
            temp_gauge,
            f"[{rain_color}]{hour.precip_prob}%[/{rain_color}]",
            f"[{COLORS['concrete']}]{desc.upper()}[/{COLORS['concrete']}]",
            f"[{severity_color}]{severity_icon}[/{severity_color}]",
        )

    console.print(table)
    print()
