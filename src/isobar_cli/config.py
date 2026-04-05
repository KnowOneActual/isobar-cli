"""Configuration module for Isobar CLI persistent settings."""

import json
import os
from pathlib import Path
from typing import Optional

CONFIG_DIR = Path.home() / ".config" / "isobar"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Default API endpoints (can be overridden by environment variables)
DEFAULT_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
DEFAULT_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_AQI_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


def ensure_config_dir() -> None:
    """Create config directory if it doesn't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def get_home_city() -> Optional[str]:
    """Get the user's configured home city."""
    ensure_config_dir()

    if not CONFIG_FILE.exists():
        return None

    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
        return config.get("home_city")
    except (OSError, json.JSONDecodeError):
        return None


def set_home_city(city: str) -> None:
    """Set the user's home city in config."""
    ensure_config_dir()

    config = {}
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                config = json.load(f)
        except (OSError, json.JSONDecodeError):
            pass

    config["home_city"] = city

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def clear_home_city() -> None:
    """Remove the home city from config."""
    ensure_config_dir()

    if not CONFIG_FILE.exists():
        return

    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError):
        return

    if "home_city" in config:
        del config["home_city"]

        if config:  # If there are other settings, keep file
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=2)
        else:  # If empty, remove file
            CONFIG_FILE.unlink()


def get_config_path() -> Path:
    """Get the path to the config file (for debugging/info)."""
    return CONFIG_FILE


def get_geocoding_url() -> str:
    """Get geocoding API URL from environment or default."""
    return os.environ.get("ISOBAR_GEOCODING_URL", DEFAULT_GEOCODING_URL)


def get_weather_url() -> str:
    """Get weather API URL from environment or default."""
    return os.environ.get("ISOBAR_WEATHER_URL", DEFAULT_WEATHER_URL)


def get_aqi_url() -> str:
    """Get air quality API URL from environment or default."""
    return os.environ.get("ISOBAR_AQI_URL", DEFAULT_AQI_URL)
