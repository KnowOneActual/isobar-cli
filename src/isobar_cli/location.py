"""Location detection module for automatic city detection via IP."""

from typing import Optional

import requests


def get_auto_location() -> Optional[str]:
    """Detect user's location based on their IP address."""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
        }
        response = requests.get(
            "https://ipwho.is/",
            headers=headers,
            timeout=3,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("success") is True:
            return data.get("city")

        return None

    except Exception:
        return None
