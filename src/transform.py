import pandas as pd


def transform_weather_data(weather_data, run_id):
    """
    Transform raw Open-Meteo hourly weather data
    into an analytics-ready Pandas DataFrame.
    """

    hourly = weather_data["hourly"]

    weather_df = pd.DataFrame({
        "observation_time": hourly["time"],
        "temperature_c": hourly["temperature_2m"],
        "relative_humidity_pct": hourly["relative_humidity_2m"],
        "apparent_temperature_c": hourly["apparent_temperature"],
        "precipitation_mm": hourly["precipitation"],
        "rain_mm": hourly["rain"],
        "weather_code": hourly["weather_code"],
        "surface_pressure_hpa": hourly["surface_pressure"],
        "wind_speed_kmh": hourly["wind_speed_10m"],
        "wind_direction_deg": hourly["wind_direction_10m"]
    })

    # Convert observation time into datetime
    weather_df["observation_time"] = pd.to_datetime(
        weather_df["observation_time"]
    )

    # Add pipeline metadata
    weather_df["location_id"] = "MUM001"

    weather_df["pipeline_run_id"] = run_id

    weather_df["ingestion_timestamp"] = pd.Timestamp.now(
        tz="UTC"
    )

    return weather_df
