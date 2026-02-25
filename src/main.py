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
        None,  # Now optional!
        help="City name (detects automatically if omitted)"
    )
):
    """
    Get the weather and what it FEELS LIKE outside right now.

    Examples:
        isobar                # Auto-detect location
        isobar Chicago
        isobar New_York       # ✅ Underscores for multi-word
        isobar San_Francisco
    """

    # Auto-location if no city provided
    if city is None:
        console.print("[dim]🌍 Detecting location...[/dim]")
        city = get_auto_location()

        if city is None:
            # Auto-location failed, fall back to Chicago
            console.print(
                "[yellow]⚠️  Could not detect location. Using Chicago as default.[/yellow]"
            )
            city = "Chicago"
        else:
            console.print(f"[dim]📍 Detected: {city}[/dim]")

    # Convert New_York → "New York" and handle quotes
    full_city = city.replace("_", " ")

    weather = get_weather_data(full_city)
    if not weather:
        console.print(f"[bold red]❌ '{full_city}' not found.[/bold red]")
        console.print("[dim]Try: Chicago, New_York, London, Paris[/dim]")
        raise typer.Exit(code=1)

    display_weather(weather)


if __name__ == "__main__":
    app()
