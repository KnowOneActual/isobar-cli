"""Location detection module for automatic city detection via IP."""
import requests
from typing import Optional


def get_auto_location() -> Optional[str]:
    """
    Detect user's location based on their IP address using ipapi.co.
    
    Returns:
        City name as a string, or None if detection fails.
    
    Examples:
        >>> city = get_auto_location()
        >>> if city:
        ...     print(f"Detected: {city}")
    """
    try:
        # ipapi.co provides free IP geolocation without API keys
        response = requests.get(
            "https://ipapi.co/json/",
            timeout=3  # Quick timeout to avoid hanging
        )
        response.raise_for_status()
        data = response.json()
        
        # Extract city name from response
        city = data.get("city")
        if city:
            return city
        
        return None
        
    except requests.exceptions.Timeout:
        # Timeout - network too slow
        return None
    except requests.exceptions.RequestException:
        # Any other request error (no internet, API down, etc.)
        return None
    except (KeyError, ValueError):
        # JSON parsing error or missing expected fields
        return None
