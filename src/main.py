import typer
from rich.console import Console

from src.api import get_weather_data
from src.location import get_auto_location
from src.ui import display_weather

app = typer.Typer(
    help=(
        "Terminal weather focused on what it FEELS LIKE outside right now."
    )
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
):
    """
    Get the weather and what it FEELS LIKE outside right now.

    Examples:
        isobar                    # Auto-detect location
        isobar Chicago            # Positional argument
        isobar --city Tokyo       # Flag style
        isobar -c London          # Short flag
        isobar New_York           # Underscores for multi-word cities
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

    weather = get_weather_data(full_city)
    if not weather:
        console.print(f"[bold red]❌ '{full_city}' not found.[/bold red]")
        console.print("[dim]Try: Chicago, New_York, London, Paris[/dim]")
        raise typer.Exit(code=1)

    display_weather(weather)


if __name__ == "__main__":
    app()
