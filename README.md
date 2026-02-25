# Isobar CLI

A terminal weather tool designed to give you a simple and efficient sense of what the weather feels like outside. Built with Python and the Rich library.

## Philosophy

Isobar CLI answers a simple question: **"What does it feel like outside right now?"**

Most weather apps overwhelm you with data. Isobar strips away everything except what matters when you're deciding whether to grab a jacket.

### Design Principles
- **Essential over comprehensive** - Show Real Feel, not 47 data points
- **Terminal-native** - Built for quick checks in your workflow
- **Zero friction** - No API keys, no config files
- **Information density** - Clean, borderless UI
- **Intentional features** - Each must answer: "Does this help understand what it feels like outside?"

## ✨ Features

- **Auto-Location** - `isobar` detects your city automatically! 🌍
- **Current Weather** - Real-time temperature and wind data
- **Real Feel** - Apparent temperature (what it *feels* like)
- **Precipitation Forecast** - Next 6h rain/snow chance + totals
- **Smart Caching** - 15min cache (`~/.cache/isobar/`)
- **No API Keys** - Free Open-Meteo + ip-api.com
- **Color-Coded** - Visual temperature feedback
- **Zero Config** - Works instantly

## 🚀 Installation

```bash
git clone https://github.com/KnowOneActual/isobar-cli.git
cd isobar-cli
pip install .
```

## 📱 Usage

```bash
# Auto-detect your location (NEW!)
isobar

# Or specify city
isobar Chicago
isobar "New York"        # Quotes for spaces
isobar New_York          # Underscores work too!

# Examples
isobar San_Francisco
isobar London
```

## 📈 Project Status

✅ **Phase 1 Complete** (Caching + Auto-Location)  
🔄 **Phase 2 Active** (AQI, Sunrise/Sunset)  
See [ROADMAP.md](ROADMAP.md)

## 🛠 Tech Stack

- Python + [Typer](https://typer.tiangolo.com/)
- [Rich](https://github.com/Textualize/rich) (UI)
- [Open-Meteo](https://open-meteo.com/) (Weather)
- [ip-api.com](http://ip-api.com/) (Location)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New features must answer: **"Does this help understand what it feels like outside?"**

## 📄 License

MIT. See [LICENSE](LICENSE).