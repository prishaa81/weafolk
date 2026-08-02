import requests


def extract_weather_data(latitude, longitude):
    """
    Extract hourly weather data from the Open-Meteo API.
    """

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "weather_code",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m"
        ],
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    weather_data = response.json()

    records_extracted = len(
        weather_data["hourly"]["time"]
    )

    print("✅ Weather data extracted successfully!")
    print("Records extracted:", records_extracted)

    return weather_data
