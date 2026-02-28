from typing import Annotated, Optional

import typer
from rich.console import Console

from isobar_cli.api import get_city_suggestions, get_weather_data
from isobar_cli.location import get_auto_location
from isobar_cli.ui import (
    display_forecast,
    display_hourly,
    display_multi_weather,
    display_weather,
)

app = typer.Typer(
    help=("Terminal weather focused on what it FEELS LIKE outside right now.")
)
console = Console()


@app.command()
def main(
    cities: Annotated[
        Optional[list[str]],
        typer.Argument(
            help="City name(s) (detects automatically if omitted). Use underscores for multi-word cities.",
        ),
    ] = None,
    city_option: Annotated[
        Optional[str],
        typer.Option(
            "--city",
            "-c",
            help="City name as a flag (alternative to positional argument)",
        ),
    ] = None,
    forecast: Annotated[
        bool,
        typer.Option(
            "--forecast",
            "-f",
            help="Show 7-day forecast after current conditions",
        ),
    ] = False,
    hourly: Annotated[
        bool,
        typer.Option(
            "--hourly",
            "-H",
            help="Show next 12 hours of weather",
        ),
    ] = False,
    metric: Annotated[
        bool,
        typer.Option(
            "--metric",
            "-m",
            help="Show weather in metric units (Celsius, km/h, mm)",
        ),
    ] = False,
):
    """
    Get the weather and what it FEELS LIKE outside right now.

    Examples:
        isobar                        # Auto-detect location
        isobar Chicago                # Single city
        isobar London Tokyo Paris     # Multiple cities
        isobar --city Tokyo           # Flag style
        isobar New_York               # Underscores for multi-word cities
        isobar --forecast             # Current + 7-day outlook
        isobar --hourly               # Current + next 12 hours
        isobar --metric               # Metric units
    """
    # Resolve cities list
    cities_to_fetch = []
    if city_option:
        cities_to_fetch.append(city_option)
    if cities:
        cities_to_fetch.extend(cities)

    # Auto-location if no city provided either way
    if not cities_to_fetch:
        console.print("[dim]🌍 Detecting location...[/dim]")
        auto_city = get_auto_location()

        if auto_city is None:
            console.print(
                "[yellow]⚠️  Could not detect location. "
                "Using Chicago as default.[/yellow]"
            )
            cities_to_fetch = ["Chicago"]
        else:
            console.print(f"[dim]📍 Detected: {auto_city}[/dim]")
            cities_to_fetch = [auto_city]

    # Process each city
    results = []
    for city_name in cities_to_fetch:
        full_city = city_name.replace("_", " ")
        weather = get_weather_data(full_city, metric=metric)
        if weather:
            results.append(weather)
        else:
            console.print(f"[bold red]❌ '{full_city}' not found.[/bold red]")
            suggestions = get_city_suggestions(full_city)
            if suggestions:
                suggest_str = ", ".join(suggestions[:3])
                console.print(f"[dim]Did you mean: {suggest_str}?[/dim]")

    if not results:
        raise typer.Exit(code=1)

    # UI Rendering
    # If multiple cities AND no detail flags, show side-by-side
    if len(results) > 1 and not (hourly or forecast):
        display_multi_weather(results)
    else:
        # Show sequentially (best for hourly/forecast details)
        for i, weather in enumerate(results):
            if i > 0:
                console.print("[dim]───────────────────────────────────────[/dim]")

            display_weather(weather)

            if hourly:
                display_hourly(weather)

            if forecast:
                display_forecast(weather)


if __name__ == "__main__":
    app()
