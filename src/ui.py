from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Initialize the console object once to use throughout the file
console = Console()

def display_weather(weather_data: dict):
    """
    Renders the weather data in a visually pleasing terminal panel.
    """
    if not weather_data:
        console.print("[bold red]No weather data available.[/bold red]")
        return

    city = weather_data.get("city", "Unknown Location")
    temp = weather_data.get("temp", "--")
    feels_like = weather_data.get("feels_like", "--")
    wind_speed = weather_data.get("wind_speed", "--")

    # A borderless table keeps the labels and values aligned
    table = Table(show_header=False, box=None, padding=(0, 2))
    
    table.add_row("🌡️  Temperature:", f"[bold cyan]{temp}°F[/bold cyan]")
    # Highlighting the Real Feel specifically since it is the core feature
    table.add_row("🤔 Real Feel:", f"[bold yellow]{feels_like}°F[/bold yellow]")
    table.add_row("💨 Wind Speed:", f"{wind_speed} mph")

    # Wrap the table in a styled panel
    weather_panel = Panel(
        table,
        title=f"[bold green]{city} Weather[/bold green]",
        border_style="blue",
        expand=False  # Keeps the box wrapped tightly around the text
    )

    console.print(weather_panel)