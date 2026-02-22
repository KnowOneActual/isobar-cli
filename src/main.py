import typer
from rich.console import Console

from src.api import get_weather_data
from src.ui import display_weather

app = typer.Typer(
    help=(
        "Terminal weather focused on what it FEELS LIKE outside right now."
    )
)
console = Console()

@app.command()
def main(city: str = typer.Argument("Chicago", help="City name")):
    """
        Get the weather and what it FEELS LIKE outside right now.

        Examples:
            isobar Chicago
            isobar New_York      # ✅ Underscores for multi-word
            isobar San_Francisco
            isobar               # Chicago (default)
"""

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
