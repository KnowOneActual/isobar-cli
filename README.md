# Isobar CLI 

![CI](https://github.com/KnowOneActual/isobar-cli/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-98%25-green)
[![PyPI version](https://badge.fury.io/py/isobar-cli.svg)](https://badge.fury.io/py/isobar-cli)
![Version](https://img.shields.io/badge/version-1.0.1-blue)
![Ruff](https://img.shields.io/badge/linting-ruff-purple)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Security Scan](https://github.com/KnowOneActual/isobar-cli/actions/workflows/security.yml/badge.svg)

A terminal weather tool designed to provide a fast, clean sense of what the weather **feels like** outside; right now and for the week ahead. Built with Python and Rich.

## Philosophy

Isobar CLI answers a simple question: **"What does it feel like outside right now, and do I need a jacket?"**

Most weather apps overwhelm with data. Isobar strips away everything except what matters when deciding how to prepare for the day.

### Design Principles
- **Essential over comprehensive** — Show Real Feel, not 47 data points.
- **Terminal-native** — Built for quick checks within a developer workflow.
- **Zero friction** — No API keys or configuration files required.
- **Information density** — Clean, borderless UI for maximum readability.
- **Intentional features** — Each feature must answer: *"Does this help someone understand what it feels like outside?"*

## ✨ Features

- **Auto-Location** — `isobar` detects the city automatically 🌍
- **Weather Condition Icons** — WMO-standard emoji + plain-English description (☀️ Clear sky, 🌨️ Moderate snow, ⛈️ Thunderstorm)
- **Real Feel** — Apparent temperature metrics (what it *actually* feels like).
- **Air Quality Index** — US AQI with health classifications 😷
- **7-Day Forecast** — Full week outlook with color-coded highs/lows and daily rain %
- **Hourly Outlook** — Next 12 hours of temperature and rain chance (`--hourly`)
- **Multiple Cities** — Compare weather across several cities side-by-side.
- **Smart Suggestions** — Fuzzy city name matching if there is a typo.
- **Shell Completion** — Tab-complete city names based on search history.
- **Dynamic Timezone** — Sunrise/sunset shown in the city's local time, not yours.
- **Precipitation Forecast** — Next 6h rain/snow chance and totals.
- **Smart Caching** — 15-minute cache per city (`~/.cache/isobar/`)
- **Color-Coded Temps** — Intuitive color mapping for temperature ranges.
- **Metric Support** — `--metric` or `-m` for Celsius, km/h, and mm.
- **No API Keys** — Free Open-Meteo and ip-api.com.
- **Zero Config** — Works instantly after installation.
- **Phase 7: Intuition & Analysis** — Higher-level context and automated insights:
  - **Preparation Guidance** — Clothing and gear suggestions based on conditions 🧥☂️🧴
  - **Temporal Context** — Comparison with previous day conditions 📈
  - **UV Index Monitoring** — Sun protection guidance with intensity levels ☀️
  - **Wind Gust Alerts** — Highlighting of significant gust events 💨⚠️
  - **Home City Persistence** — Set a default city with `isobar home "Your City"` 🏠

## 🚀 Installation

The recommended way to install Isobar is via [pipx](https://github.com/pypa/pipx):

```bash
pipx install isobar-cli
```

Installation is also supported via [Homebrew](https://brew.sh/):

```bash
brew install KnowOneActual/tap/isobar
```

> **Note:** Installing via Homebrew builds several high-performance dependencies (like `numpy` and `h3`) from source. This ensures a robust, isolated install but may take 5-10 minutes to complete.

Alternatively, install directly from PyPI:

```bash
pip install isobar-cli
```

Or install from source:

```bash
git clone https://github.com/KnowOneActual/isobar-cli.git
cd isobar-cli
pip install .
```

## 📱 Usage

```bash
# Auto-detect location
isobar

# Specify a city
isobar Chicago
isobar London Tokyo Paris     # Multiple cities
isobar "New York"             # Use quotes for multi-word cities

# Hourly outlook (next 12h)
isobar --hourly
isobar -H

# 7-day forecast
isobar --forecast
isobar -f
isobar "San Francisco" --forecast
isobar -f Sydney

# Metric units (Celsius, km/h, mm)
isobar --metric
isobar -m
isobar Tokyo -m

# Home city management
isobar home "New York"    # Set home city
isobar home               # Show current home city
isobar home --clear       # Clear home city
isobar                    # Uses home city if set (otherwise auto-detects)
```

## ⌨️ Shell Completion

Isobar supports tab-completion for city names. To enable it for a shell:

**Zsh:**
```bash
isobar --install-completion zsh
```

**Bash:**
```bash
isobar --install-completion bash
```

*(Note: A terminal restart may be required after installation).*

## 🖥️ Example Output

```
               Chicago, Illinois Weather
 ☀️  Conditions:                        Mainly clear
 🌡️  Temperature:                             75.2°F
 🤔  Real Feel:                               78.5°F
 💨  Wind Speed:                             12.4 mph
 💧  Humidity:                                   65%
 ☔  Precip Chance:  30% (6h) | Light rain likely
 🌅  Sunrise:                                6:29 AM
 🌇  Sunset:                                 5:37 PM
 ☀️  UV Index:                              6.5 (High)
 💨  Wind Alert:                     ⚠️ Gusts up to 25 mph
 😷  Air Quality:                        45 (Good)

↑ 5.2°F warmer than yesterday

Preparation Guidance:
  • 🧥 Light jacket
  • 🧴 Sunscreen recommended
  • 🕶️ Sunglasses recommended

           7-Day Forecast — Chicago, Illinois
  Day            Conditions        High     Low   Rain%  UV
  Today      ☁️  Overcast         78.7°F  63.9°F    30%   7.2
  Tue Apr 1  ⛅  Partly cloudy    82.4°F  65.4°F    20%   8.1
  Wed Apr 2  🌦️  Light drizzle    76.8°F  60.9°F    45%   5.8
  Thu Apr 3  ☀️  Clear sky        80.3°F  63.5°F    10%   8.5
  Fri Apr 4  ☀️  Clear sky        83.6°F  67.1°F     5%   9.0
  Sat Apr 5  ⛅  Partly cloudy    79.8°F  64.9°F    15%   7.8
  Sun Apr 6  🌤️  Mainly clear     81.2°F  66.3°F    10%   8.3
```

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| [Typer](https://typer.tiangolo.com/) | CLI framework |
| [Rich](https://github.com/Textualize/rich) | Terminal UI |
| [Open-Meteo](https://open-meteo.com/) | Weather and forecast data |
| [ipwho.is](https://ipwho.is/) | Auto-location detection |
| [timezonefinder](https://github.com/jannikmi/timezonefinder) | Dynamic timezone resolution |
| [pytest](https://docs.pytest.org/) | Unit testing framework |
| [requests-mock](https://requests-mock.readthedocs.io/) | API testing |
| [Ruff](https://docs.astral.sh/ruff/) | Linting and formatting |
| [pip-audit](https://github.com/pypa/pip-audit) | Dependency security scanning |
| **Phase 7 Features** | **Intuition & Analysis** |
| `config.py` | Persistent home city configuration |
| Enhanced `logic.py` | Preparation guidance, UV monitoring, gust alerts |
| Updated `ui.py` | Contextual display of insights |

## 🔒 Security

Security is a fundamental priority for Isobar CLI. Multiple layers of automated scanning ensure the tool remains safe and secure for all users.

### Security Measures
- **Vulnerability Scanning:** [Trivy](https://github.com/aquasecurity/trivy) scans the filesystem and dependencies for known vulnerabilities.
- **Static Analysis (SAST):** [Bandit](https://github.com/PyCQA/bandit) and [Semgrep](https://semgrep.dev/) analyze the code for insecure patterns.
- **Dependency Auditing:** [pip-audit](https://github.com/pypa/pip-audit) and GitHub Dependabot ensure third-party packages stay updated.
- **Script Linting:** [ShellCheck](https://www.shellcheck.net/) enforces best practices for Bash scripts.
- **Secret Scanning:** Automated checks prevent the accidental commitment of sensitive credentials.

All security scans are integrated into the CI/CD pipeline and run on every push, pull request, and weekly schedule. Results are available via the GitHub Security tab.

## 📈 Project Status

✅ **Phase 1 Complete** — Caching and Auto-Location  
✅ **Phase 2 Complete** — Precipitation, Sunrise/Sunset, and Condition Icons  
✅ **Phase 3 Complete** — 7-Day Forecast, Dynamic Timezone, and UI Refinements  
✅ **Phase 4 Complete** — Quality & Trust (Security, CI/CD)  
✅ **Phase 5 Complete** — Testing & Reliability  
✅ **Phase 6 Complete** — Distribution (PyPI, Homebrew)  
✅ **Phase 7 Complete** — Intuition & Analysis (v1.1.0)  
Refer to [ROADMAP.md](ROADMAP.md) and [CHANGELOG.md](CHANGELOG.md) for details.

## 🤝 Contributing

Detailed instructions are available in [CONTRIBUTING.md](CONTRIBUTING.md). New features must answer: **"Does this help someone understand what it feels like outside?"**

## 📄 License

MIT. See [LICENSE](LICENSE).
