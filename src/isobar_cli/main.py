import typer
from rich.console import Console

from isobar_cli.api import get_weather_data
from isobar_cli.location import get_auto_location
from isobar_cli.ui import display_forecast, display_hourly, display_weather

app = typer.Typer(
    help=("Terminal weather focused on what it FEELS LIKE outside right now.")
)
console = Console()


@app.command()
def main(
    city: str = typer.Argument(
        None,
        help="City name (detects automatically if omitted)",
    ),
    city_option: str = typer.Option(
        None,
        "--city",
        "-c",
        help="City name as a flag (alternative to positional argument)",
    ),
    forecast: bool = typer.Option(
        False,
        "--forecast",
        "-f",
        help="Show 7-day forecast after current conditions",
    ),
    hourly: bool = typer.Option(
        False,
        "--hourly",
        "-H",
        help="Show next 12 hours of weather",
    ),
    metric: bool = typer.Option(
        False,
        "--metric",
        "-m",
        help="Show weather in metric units (Celsius, km/h, mm)",
    ),
):
    """
    Get the weather and what it FEELS LIKE outside right now.

    Examples:
        isobar                        # Auto-detect location
        isobar Chicago                # Positional argument
        isobar --city Tokyo           # Flag style
        isobar -c London              # Short flag
        isobar New_York               # Underscores for multi-word cities
        isobar --forecast             # Current + 7-day outlook
        isobar --hourly               # Current + next 12 hours
        isobar --city Paris -f        # Paris with 7-day forecast
        isobar --metric               # Metric units
    """
    # --city flag takes precedence over positional argument
    resolved_city = city_option or city

    # Auto-location if no city provided either way
    if resolved_city is None:
        console.print("[dim]🌍 Detecting location...[/dim]")
        resolved_city = get_auto_location()

        if resolved_city is None:
            console.print(
                "[yellow]⚠️  Could not detect location. "
                "Using Chicago as default.[/yellow]"
            )
            resolved_city = "Chicago"
        else:
            console.print(f"[dim]📍 Detected: {resolved_city}[/dim]")

    # Convert New_York → "New York" and handle underscores
    full_city = resolved_city.replace("_", " ")

    weather = get_weather_data(full_city, metric=metric)
    if not weather:
        console.print(f"[bold red]❌ '{full_city}' not found.[/bold red]")
        console.print("[dim]Try: Chicago, New_York, London, Paris[/dim]")
        raise typer.Exit(code=1)

    display_weather(weather)

    if hourly:
        display_hourly(weather)

    if forecast:
        display_forecast(weather)


if __name__ == "__main__":
    app()
