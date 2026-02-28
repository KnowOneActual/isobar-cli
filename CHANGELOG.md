# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0] - 2026-02-28

### Added
- **Air Quality Index (AQI)** — Integrated US AQI data with color-coded health classifications (Good, Moderate, Unhealthy, etc.).
- **Side-by-Side Multi-City View** — Multiple cities are now displayed in columns when requested together (without detailed forecast flags), significantly improving information density.
- **Smart City Suggestions** — Added "Did you mean?" suggestions using the geocoding API when a city name is misspelled or not found.
- **Extreme Temperature Labels** — The "Real Feel" label now dynamically changes to "Wind Chill" or "Heat Index" when conditions are extreme.

### Changed
- Refactored UI and API modules to clearly separate data processing from rendering.
- Cache metadata is now passed directly from the API layer to the UI.

## [0.5.2] - 2026-02-28

### Added
- **Multiple Cities Support** — Fetch and display weather for multiple cities in a single command (e.g., `isobar London Tokyo Paris`).
- **Visual Separators** — Clean dashed separators between city cards when viewing multiple locations.

### Changed
- The `city` argument is now `cities` (a list), allowing for one or more positional arguments.

## [0.5.1] - 2026-02-28

### Added
- **Hourly Outlook** — Pass `--hourly` or `-H` to see a compact 12-hour forecast including temperature, weather icons, and rain probability.
- **Improved Test Suite** — Updated mocks and tests to cover hourly data parsing and UI rendering.

### Fixed
- **CI Stability** — Resolved CI and coverage failures related to project layout and ANSI color escape codes in test output.
- **Test Isolation** — Aggressively disabled color output in CLI tests to ensure reliable help output matching across different environments.

### Changed
- **API Cache** — Hourly data is now cached alongside daily data. Older caches (v0.5.0) will automatically refresh when hourly data is requested.

## [0.5.0] - 2026-02-28

### Added
- **Metric Unit Support** — Pass `--metric` or `-m` to display weather in Celsius, km/h, and mm.
- **Unit-Aware Color Coding** — Temperature color-coding thresholds automatically adjust for Celsius (e.g., 0°C is cyan, 20°C is green).
- **Comprehensive Test Suite** — Expanded `pytest` coverage to 73%:
  - **`test_main.py`** — New CLI integration tests using `typer.testing.CliRunner`.
  - **Metric Tests** — Unit tests for metric unit API requests and UI rendering.
  - **Cache Isolation** — Added a `pytest` fixture to mock `CACHE_DIR`, preventing tests from being affected by or polluting the local user cache.

### Changed
- **API Results** — Added a `units` metadata dictionary to the weather data structure to track display units.
- **Cache Strategy** — Cache files now include a unit suffix (`_metric.json` or `_imperial.json`) to allow toggling between unit systems without waiting for the cache to expire.

### Fixed
- **Test Reliability** — Fixed a bug where `test_get_weather_data_success` would fail if a local cache file existed for Chicago.
- **UI Logic** — Standardized internal keys for rainfall and snowfall (`rainfall_inch` → `rainfall`) to support both unit systems.

## [0.4.4] - 2026-02-26

### Added
- **GitHub Actions CI** - Automated workflow (`.github/workflows/ci.yml`) runs on every push and pull request to `main` with three parallel jobs:
  - **Ruff Lint** — `ruff check .` enforces code style, catches unused variables, import order, and bugbear rules.
  - **Security Audit** — `pip-audit` scans all dependencies for known CVEs.
  - **Run Tests** — `pytest` runs the full test suite on every commit.
- **Initial Test Suite** — Comprehensive unit tests for `api.py`, `location.py`, and `ui.py` (formatting, icons, precip headlines) in the `tests/` directory.
- **Testing Procedure Document** — New `docs/TESTING.md` guide for running tests, mocking APIs, and checking coverage.
- **README Badges** — CI status, Coverage, Version, Ruff, Python 3.8+, and MIT license badges added.

### Changed
- **Src Layout Refactor** — Moved source files from `src/` to `src/isobar_cli/` and updated `pyproject.toml` to follow modern Python packaging standards.
- **Dependency Management** — Added `[project.optional-dependencies]` for testing (`pip install ".[test]"`), including `pytest-cov`.
- **Contribution Guide** — Updated `CONTRIBUTING.md` with instructions for running the test suite.

### Fixed
- **Repository Cleanup** — Removed legacy build artifacts (`build/`, `*.egg-info/`, `.ruff_cache/`) and unified the project structure.
- **Ruff Config** — Corrected `pyproject.toml` configuration to fix parsing errors and linting issues in tests.

## [0.4.3] - 2026-02-26

### Added
- **7-Day Forecast** - Pass `--forecast` or `-f` to display a full week outlook below the current conditions card. Each day shows the weekday, a WMO condition icon, plain-English description, color-coded high/low temps, and daily rain probability. Rain% is color-coded: cyan (≥60%), yellow (≥30%), dim (dry).
- **`--forecast` / `-f` flag** - New CLI option; composable with `--city` (e.g., `isobar --city Paris -f`).

### Changed
- API now fetches 7 days of daily data (`forecast_days=7`) including `temperature_2m_max`, `temperature_2m_min`, `weather_code`, and `precipitation_probability_max`.
- Stale city caches from before `0.4.3` will show `No forecast data available` until cleared (`rm ~/.cache/isobar/<city>.json`).

## [0.4.2] - 2026-02-26

### Added
- **Weather Condition Icons** - A new `Conditions` row appears at the top of the weather card showing a WMO weather code mapped to an emoji and plain-English description (e.g., `☀️ Clear sky`, `🌧️ Moderate rain`, `⛈️ Thunderstorm`). Covers all 23 standard WMO codes.

## [0.4.1] - 2026-02-26

### Added
- **Dynamic Timezone Detection** - Timezone is now resolved from city coordinates using `timezonefinder` (no API key required). Sunrise/sunset times are always accurate in the city's local time, not the host machine's timezone.
- **`--city` / `-c` flag** - City can now be passed as a named option (`isobar --city Tokyo`) in addition to the existing positional argument (`isobar Tokyo`). Both styles work interchangeably.

### Fixed
- Format sunrise/sunset using 12-hour time (e.g., `6:29 AM`, `5:37 PM`) instead of 24-hour `HH:MM`.
- Fix Ruff `F841` warnings by removing unused `sunrise_iso` / `sunset_iso` variables.

## [0.4.0] - 2026-02-24

### Added
- **Auto-Location Detection** - Run `isobar` without arguments to auto-detect location via IP
  - Uses ip-api.com (1,000 req/day free tier)
  - Browser-like User-Agent to avoid blocking
  - Graceful fallback to Chicago if detection fails
  - **Phase 1 of ROADMAP complete** ✅

### Fixed
- **requests DNS resolution** - Robust handling of DNS/SSL edge cases
- **Ruff linting** - Fixed W293, E501 line length violations

### Changed
- City argument now optional in CLI
- Updated help text/examples to show `isobar` (no args) usage

## [0.3.1] - 2026-02-22

### Added
- **Rain forecast**: 6-hour rainfall totals in inches (`rainfall_inch`) [PR #1]
- **Snow forecast**: 6-hour snowfall totals in inches (converted from cm) [PR #1]
- **Precipitation headline**: Instant comfort summary under Precip Chance row
  - "Dry conditions expected", "Light rain likely", "Snowy conditions likely", etc.
  - Helps answer "what should I wear?" at a glance [PR #1]

### Changed
- Snow display now uses inches consistently with rain (was cm) [PR #1]
- Precip headline moved under "Precip Chance" row for better flow [PR #1]

## [0.3.0] - 2026-02-22

### Added
- **Precipitation Probability** - Next 6h rain chance (%) [Phase 2]
- **Snow Detection** - Expected snowfall warning (>1mm)
- **Underscore Support** - `isobar New_York` → "New York" [no quotes!]
- **Smart Defaults** - `isobar` → Chicago weather

### Fixed
- Graceful "city not found" messaging with examples

## [0.2.0] - 2026-02-22

### Added
- **Local Caching** - 15-minute cache per-city in `~/.cache/isobar/` (~78% faster repeat requests) [#1]
- **Cache Timestamp** - Subtle "Updated X min ago" indicator on cache hits
- **Phase 1 Complete** - Core performance improvements from ROADMAP.md

### Fixed
- Cache filename consistency (handles city names with commas cleanly)

## [0.1.0] - 2026-02-21

### Added
- Core command-line interface to request weather by city name.
- Open-Meteo API integration for free geocoding and forecast data.
- Terminal UI built with Rich featuring a colored, borderless card layout.
- Display for Temperature, Real Feel, and Wind Speed.
- Basic error handling for failed API connections and unrecognized city names.

## [Unreleased]

### Added
- Initial project setup.
