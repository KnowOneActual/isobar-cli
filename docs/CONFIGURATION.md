# Isobar CLI Configuration Guide

## Overview

Isobar CLI supports advanced configuration through environment variables and optional dependencies. This guide covers all configuration options available in version 1.2.0 and later.

## Environment Variables

### API Endpoint Configuration

Customize API endpoints for different weather providers, testing, or self-hosted services:

| Variable | Description | Default |
|----------|-------------|---------|
| `ISOBAR_GEOCODING_URL` | Geocoding API endpoint | `https://geocoding-api.open-meteo.com/v1/search` |
| `ISOBAR_WEATHER_URL` | Weather forecast API endpoint | `https://api.open-meteo.com/v1/forecast` |
| `ISOBAR_AQI_URL` | Air quality API endpoint | `https://air-quality-api.open-meteo.com/v1/air-quality` |

#### Example: Using Custom APIs

```bash
# Set custom endpoints
export ISOBAR_GEOCODING_URL="https://custom-geocoding.example.com/v1/search"
export ISOBAR_WEATHER_URL="https://custom-weather.example.com/v1/forecast"
export ISOBAR_AQI_URL="https://custom-aqi.example.com/v1/air-quality"

# Run with custom endpoints
isobar "New York"
```

#### Example: Testing Configuration

```bash
# Test with a mock API server
export ISOBAR_WEATHER_URL="http://localhost:8000/weather"
isobar "Test City"
```

### Timeout Configuration

All HTTP requests include timeout protection. The default timeouts are:
- Geocoding API: 10 seconds
- Weather API: 15 seconds  
- Air Quality API: 10 seconds

## Optional Dependencies

### Timezone Support (`pytz`)

For accurate local timezone display of sunrise/sunset times:

```bash
# Install with timezone support
pip install isobar-cli[timezone]

# Or install separately
pip install pytz>=2024.1
```

**Benefits:**
- Sunrise/sunset times display in the city's local timezone
- More accurate time calculations for locations with complex timezone rules
- Graceful fallback to UTC if `pytz` is not installed

**Without `pytz`:**
- Times display in UTC (default behavior)
- Still fully functional with slightly less accurate time display

## Debugging and Logging

### Error Logging

Isobar logs API errors to stderr for debugging while maintaining a clean user interface:

```bash
# Capture debug output
isobar "Test City" 2> error.log

# View API errors in real-time
isobar "Unknown City" 2>&1 | grep -i error
```

### Common Error Messages

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `Geocoding error for 'City': Connection timeout` | Network issue or API unavailable | Check internet connection, try different city |
| `AQI error for (lat,lon): 404 Not Found` | Air quality API endpoint changed | Update `ISOBAR_AQI_URL` or wait for API to recover |
| `Unexpected geocoding error: JSONDecodeError` | API returned invalid response | API may be experiencing issues, try again later |

## Configuration Files

### Home City Configuration

Set a default home city for automatic weather checks:

```bash
# Set home city
isobar home "New York"

# Show current home city
isobar home

# Clear home city
isobar home --clear
```

**Location:** `~/.config/isobar/config.json`

### Cache Configuration

Weather data is cached for 15 minutes to reduce API calls:

**Location:** `~/.cache/isobar/`

**Cache files:** `{city_name}_{unit_system}.json`

**To clear cache:**
```bash
rm -rf ~/.cache/isobar/
```

## Security Considerations

### API Endpoint Security

When configuring custom API endpoints:

1. **Use HTTPS** for production endpoints to prevent MITM attacks
2. **Validate certificates** (default behavior with `requests`)
3. **Consider rate limits** when using paid or limited APIs

### Environment Variable Security

Environment variables are read from the current shell session. For sensitive configurations:

```bash
# Set temporarily (session only)
export ISOBAR_WEATHER_URL="https://secure-api.example.com"

# Use in scripts (not stored in shell history)
ISOBAR_WEATHER_URL="https://secure-api.example.com" isobar "City"
```

## Troubleshooting

### API Endpoints Not Working

1. **Check connectivity:**
   ```bash
   curl "$ISOBAR_GEOCODING_URL?name=London&count=1&format=json"
   ```

2. **Verify format:** Custom APIs must match Open-Meteo response format

3. **Check timeouts:** Increase if using slow APIs
   ```bash
   export REQUESTS_TIMEOUT=30  # Global timeout for requests library
   ```

### Timezone Issues

1. **Install `pytz`** for accurate timezone conversion
2. **Check timezone database:** `pytz` uses system timezone database
3. **Fallback behavior:** Without `pytz`, times display in UTC

### Cache Issues

1. **Stale data:** Cache TTL is 15 minutes
2. **Clear cache:** Delete `~/.cache/isobar/` directory
3. **Unit system:** Separate caches for metric/imperial units

## Best Practices

1. **Use default endpoints** for general use (Open-Meteo is free and reliable)
2. **Install `pytz`** for accurate timezone support
3. **Monitor error logs** when using custom APIs
4. **Clear cache** after changing API endpoints
5. **Test configurations** in development before production use

## Related Documentation

- [README.md](../README.md) - Quick start and basic usage
- [CHANGELOG.md](../CHANGELOG.md) - Version history and changes
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Development guidelines
- [SECURITY.md](../SECURITY.md) - Security practices and scanning