import typer
from src.api import get_weather_data
from src.ui import display_weather

app = typer.Typer(help="Terminal weather focused on what it FEELS LIKE outside right now.")

@app.command()
def main(
    city: str = typer.Argument(..., help="City name (e.g. 'Chicago', 'New York')"),
):
    """
    Get the weather and what it FEELS LIKE outside.
    
    Isobar answers: "Should I grab a jacket?" not "What's the full forecast?"
    
    Examples:
        isobar Chicago
        isobar "New York"  
        isobar "Los Angeles"
    """
    weather = get_weather_data(city)
    display_weather(weather)

if __name__ == "__main__":
    app()
