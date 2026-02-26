# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2026-02-26
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
