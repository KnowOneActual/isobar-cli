# Isobar CLI

A visually pleasing terminal weather tool focusing on Real Feel and Windchill. Built with Python and the Rich library.

## Features

- **Current Weather:** Fetches real-time temperature and wind speed data.
- **Real Feel:** Highlights the apparent temperature so you know exactly what it feels like outside.
- **Clean UI:** Presents data in a highly readable, borderless terminal card.
- **No API Keys Required:** Uses the free Open-Meteo API for instant setup.

## Installation

You can install Isobar CLI locally using pip.

1. Clone the repository:

```bash
git clone https://github.com/KnowOneActual/isobar-cli.git
cd isobar-cli

```

2. Install the package:

```bash
pip install .

```

## Usage

Run the tool by typing `isobar` followed by the city name.

```bash
isobar Chicago

```

_(If your city name has spaces, wrap it in quotes like `isobar "New York"`)_

## Tech Stack

- Python
- [Typer](https://typer.tiangolo.com/) (CLI framework)
- [Rich](https://github.com/Textualize/rich) (Terminal UI)
- [Open-Meteo](https://open-meteo.com/) (Weather Data)

License

Distributed under the MIT License. See LICENSE for more information.
