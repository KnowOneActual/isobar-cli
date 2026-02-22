import typer
from src.ui import display_weather
from src.api import get_weather_data

app = typer.Typer(no_args_is_help=True)

@app.command()
def now(city: str = typer.Argument(..., help="The city to fetch weather for")):
    """
    Get the current weather and Real Feel for a specific city.
    """
    # In a real app, you'd convert 'city' to lat/long here.
    # For now, we default to Chicago if they type 'Chicago'
    weather = get_weather_data(city)
    display_weather(weather)

if __name__ == "__main__":
    app()