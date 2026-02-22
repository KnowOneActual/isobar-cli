# Isobar CLI

A visually pleasing terminal weather tool focusing on Real Feel and Windchill. Built with Python and the Rich library.

## Philosophy

Isobar CLI answers a simple question: **"What does it feel like outside right now?"**

Most weather apps overwhelm you with data. Isobar strips away everything except what matters when you're deciding whether to grab a jacket. Every feature serves this core purpose—no feature exists just to add a feature.

### Design Principles

- **Essential over comprehensive** - Show Real Feel, not 47 data points
- **Terminal-native** - Built for quick checks in your workflow, not a GUI replacement
- **Zero friction** - No API keys, no config files, no authentication
- **Information density** - Clean, borderless UI that respects your screen space
- **Intentional features** - Each addition must answer: "Does this help someone understand what it feels like outside?"

## Features

- **Current Weather:** Fetches real-time temperature and wind speed data.
- **Real Feel:** Highlights the apparent temperature so you know exactly what it feels like outside.
- **Clean UI:** Presents data in a highly readable, borderless terminal card.
- **No API Keys Required:** Uses the free Open-Meteo API for instant setup.
- **Color-Coded Temperature:** Visual feedback at a glance—cyan for freezing, red for hot.
- **Comfort Metrics:** Humidity and precipitation data to complete the comfort picture.

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

## Project Direction

Isobar CLI is built using first-principles thinking inspired by:
- **Framestorming** - Questioning assumptions about what weather tools should do
- **Iterative refinement** - Adding features only when they prove necessary

The [ROADMAP](ROADMAP.md) is structured in phases to maintain focus:
- **Phase 1** improves speed and convenience (caching, auto-location)
- **Phase 2** adds contextual comfort data (AQI, sunrise/sunset)
- **Phase 3** enhances visual communication (weather icons, forecasts)

Features that don't serve the core mission are explicitly marked as "Future Roadmap" and will only be implemented if real-world usage demands them.

### What This Project Is Not

- A comprehensive weather dashboard
- A replacement for detailed forecast apps
- A platform for endless customization
- A data visualization showcase

Isobar does one thing well: tells you what it feels like outside, right now, in your terminal.

## Tech Stack

- Python
- [Typer](https://typer.tiangolo.com/) (CLI framework)
- [Rich](https://github.com/Textualize/rich) (Terminal UI)
- [Open-Meteo](https://open-meteo.com/) (Weather Data)

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

When proposing features, ask: "Does this help answer 'What does it feel like outside?'" If not, it probably doesn't belong in Isobar.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
