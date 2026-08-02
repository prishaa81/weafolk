import pandas as pd
import pytest

from src.validate import validate_weather_data


def create_valid_dataframe():
    return pd.DataFrame({
        "observation_time": pd.to_datetime([
            "2026-08-02 10:00:00",
            "2026-08-02 11:00:00"
        ]),
        "temperature_c": [28.5, 29.0],
        "relative_humidity_pct": [75.0, 72.0],
        "apparent_temperature_c": [30.0, 30.5],
        "precipitation_mm": [0.0, 0.2],
        "rain_mm": [0.0, 0.2],
        "weather_code": [1, 2],
        "surface_pressure_hpa": [1008.0, 1007.5],
        "wind_speed_kmh": [15.0, 16.0],
        "wind_direction_deg": [250.0, 260.0],
        "location_id": ["MUM001", "MUM001"],
        "pipeline_run_id": ["test-001", "test-001"],
        "ingestion_timestamp": pd.to_datetime([
            "2026-08-02 10:05:00",
            "2026-08-02 11:05:00"
        ], utc=True)
    })


def test_valid_weather_data_passes():

    df = create_valid_dataframe()

    result = validate_weather_data(df)

    assert len(result) == 2


def test_invalid_humidity_fails():

    df = create_valid_dataframe()

    df.loc[0, "relative_humidity_pct"] = 150

    with pytest.raises(
        ValueError,
        match="Humidity values outside valid range"
    ):
        validate_weather_data(df)


def test_negative_precipitation_fails():

    df = create_valid_dataframe()

    df.loc[0, "precipitation_mm"] = -5

    with pytest.raises(
        ValueError,
        match="Negative precipitation values detected"
    ):
        validate_weather_data(df)
