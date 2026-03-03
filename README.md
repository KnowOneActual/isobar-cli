# Isobar CLI

![CI](https://github.com/KnowOneActual/isobar-cli/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-98%25-green)
[![PyPI version](https://badge.fury.io/py/isobar-cli.svg)](https://badge.fury.io/py/isobar-cli)
![Version](https://img.shields.io/badge/version-1.0.1-blue)
![Ruff](https://img.shields.io/badge/linting-ruff-purple)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Security Scan](https://github.com/KnowOneActual/isobar-cli/actions/workflows/security.yml/badge.svg)

A terminal weather tool designed to give you a fast, clean sense of what the weather **feels like** outside; right now and for the week ahead. Built with Python and Rich.

## Philosophy

Isobar CLI answers a simple question: **"What does it feel like outside right now, and how do I prepare to be outside?"**

Most weather apps overwhelm you with data. Isobar strips away everything except what matters when you're deciding whether to grab a jacket.

### Design Principles
- **Essential over comprehensive** — Show Real Feel, not 47 data points
- **Terminal-native** — Built for quick checks in your workflow
- **Zero friction** — No API keys, no config files
- **Information density** — Clean, borderless UI
- **Intentional features** — Each must answer: *"Does this help understand what it feels like outside?"*

## ✨ Features

- **Auto-Location** — `isobar` detects your city automatically 🌍
- **Weather Condition Icons** — WMO-standard emoji + plain-English description (☀️ Clear sky, 🌨️ Moderate snow, ⛈️ Thunderstorm)
- **Real Feel** — Apparent temperature (what it *feels* like)
- **Air Quality Index** — US AQI with health classifications 😷
- **7-Day Forecast** — Full week outlook with color-coded highs/lows and daily rain %
- **Hourly Outlook** — Next 12 hours of temp and rain chance (`--hourly`)
- **Multiple Cities** — Compare weather across several cities at once (side-by-side)
- **Smart Suggestions** — Fuzzy city name matching if you make a typo
- **Shell Completion** — Tab-complete city names from your search history
- **Dynamic Timezone** — Sunrise/sunset always shown in the city's local time, not yours
- **Precipitation Forecast** — Next 6h rain/snow chance + totals
- **Smart Caching** — 15-min cache per city (`~/.cache/isobar/`)
- **Color-Coded Temps** — Cyan → Blue → Green → Yellow → Red
- **Metric Support** — `--metric` or `-m` for Celsius, km/h, and mm
- **No API Keys** — Free Open-Meteo + ip-api.com
- **Zero Config** — Works instantly after `pip install .`

## 🚀 Installation

The recommended way to install Isobar is via [pipx](https://github.com/pypa/pipx), which installs the tool in an isolated environment:

```bash
pipx install isobar-cli
```

You can also install via [Homebrew](https://brew.sh/):

```bash
brew install KnowOneActual/tap/isobar
```

> **Note:** Installing via Homebrew builds several high-performance dependencies (like `numpy` and `h3`) from source. This is a robust, isolated install but may take 5-10 minutes to complete as it compiles these C extensions.

Alternatively, you can install directly from PyPI:

```bash
pip install isobar-cli
```

---

> A Personal Note on Homebrew

Isobar is the first project I've ever pushed to Homebrew. It was a rough road with some trial and error involving virtual environments and dependency resource mapping, but it was a good learning experience. If you're installing via `brew`, thanks for being part of that journey!


Or install from source:

```bash
git clone https://github.com/KnowOneActual/isobar-cli.git
cd isobar-cli
pip install .
```

## 📱 Usage

```bash
# Auto-detect your location
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
```

## ⌨️ Shell Completion

Isobar supports tab-completion for city names based on your search history. To enable it for your shell:

**Zsh:**
```bash
isobar --install-completion zsh
```

**Bash:**
```bash
isobar --install-completion bash
```

*(Note: You may need to restart your terminal after installing completion).*

## 🖥️ Example Output

```
               Chicago, Illinois Weather
 ☀️  Conditions:                        Mainly clear
 🌡️  Temperature:                             37.1°F
 🤔  Real Feel:                               30.4°F
 💨  Wind Speed:                             4.3 mph
 💧  Humidity:                                   58%
 ☔  Precip Chance:  0% (6h) | Dry conditions expected
 🌅  Sunrise:                                6:29 AM
 🌇  Sunset:                                 5:37 PM

           7-Day Forecast — Chicago, Illinois
  Day            Conditions        High     Low   Rain%
  Today      ☁️  Overcast         41.7°F  23.9°F    1%
  Fri Feb 27 ⛅  Partly cloudy    66.4°F  32.4°F    2%
  Sat Feb 28 🌨️  Moderate snow    44.0°F  26.5°F   38%
  Sun Mar 1  ☁️  Overcast         29.0°F  26.6°F   36%
  Mon Mar 2  ☁️  Overcast         33.6°F  27.1°F   36%
  Tue Mar 3  🌦️  Light drizzle    36.8°F  30.9°F   27%
  Wed Mar 4  🌦️  Moderate drizzle 41.3°F  33.5°F   46%
```

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| [Typer](https://typer.tiangolo.com/) | CLI framework |
| [Rich](https://github.com/Textualize/rich) | Terminal UI |
| [Open-Meteo](https://open-meteo.com/) | Weather + forecast data (free, no key) |
| [ip-api.com](http://ip-api.com/) | Auto-location detection (free) |
| [timezonefinder](https://github.com/jannikmi/timezonefinder) | Dynamic timezone from coordinates (offline) |
| [pytest](https://docs.pytest.org/) | Unit testing framework |
| [requests-mock](https://requests-mock.readthedocs.io/) | Mocking for API testing |
| [Ruff](https://docs.astral.sh/ruff/) | Linting + formatting |
| [pip-audit](https://github.com/pypa/pip-audit) | Dependency security scanning (CI) |

## 🔒 Security

Security is a top priority for Isobar CLI. We employ multiple layers of automated scanning to ensure the tool remains safe and secure for all users.

### Security Measures
- **Vulnerability Scanning:** [Trivy](https://github.com/aquasecurity/trivy) scans our filesystem and dependencies for known vulnerabilities (CVEs).
- **Static Analysis (SAST):** [Bandit](https://github.com/PyCQA/bandit) and [Semgrep](https://semgrep.dev/) analyze our Python code for insecure patterns and potential exploits.
- **Dependency Auditing:** [pip-audit](https://github.com/pypa/pip-audit) and GitHub Dependabot ensure our third-party packages are up-to-date and free of known issues.
- **Script Linting:** [ShellCheck](https://www.shellcheck.net/) ensures our Bash scripts follow security best practices.
- **Secret Scanning:** Automated checks prevent the accidental commitment of sensitive credentials or API keys.

All security scans are integrated into our CI/CD pipeline and run on every push, pull request, and weekly schedule. Results are monitored via the GitHub Security tab.

## 📈 Project Status

✅ **Phase 1 Complete** — Caching + Auto-Location  
✅ **Phase 2 Complete** — Precipitation, Sunrise/Sunset, Condition Icons  
✅ **Phase 3 Complete** — 7-Day Forecast, Dynamic Timezone, `--city` flag  
✅ **CI/CD** — Ruff lint + security audit on every push and PR  
See [ROADMAP.md](ROADMAP.md) and [CHANGELOG.md](CHANGELOG.md)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New features must answer: **"Does this help understand what it feels like outside?"**

## 📄 License

MIT. See [LICENSE](LICENSE).
