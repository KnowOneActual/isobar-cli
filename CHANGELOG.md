# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
