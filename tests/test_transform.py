import pandas as pd

from src.transform import transform_weather_data


def test_transform_weather_data():

    fake_weather_data = {
        "hourly": {
            "time": [
                "2026-08-02T10:00",
                "2026-08-02T11:00"
            ],
            "temperature_2m": [
                28.5,
                29.0
            ],
            "relative_humidity_2m": [
                75,
                72
            ],
            "apparent_temperature": [
                30.0,
                30.5
            ],
            "precipitation": [
                0.0,
                0.2
            ],
            "rain": [
                0.0,
                0.2
            ],
            "weather_code": [
                1,
                2
            ],
            "surface_pressure": [
                1008.0,
                1007.5
            ],
            "wind_speed_10m": [
                15.0,
                16.0
            ],
            "wind_direction_10m": [
                250,
                260
            ]
        }
    }

    test_run_id = "test-run-001"

    result = transform_weather_data(
        fake_weather_data,
        test_run_id
    )

    # Check number of records
    assert len(result) == 2

    # Check expected columns
    expected_columns = [
        "observation_time",
        "temperature_c",
        "relative_humidity_pct",
        "apparent_temperature_c",
        "precipitation_mm",
        "rain_mm",
        "weather_code",
        "surface_pressure_hpa",
        "wind_speed_kmh",
        "wind_direction_deg",
        "location_id",
        "pipeline_run_id",
        "ingestion_timestamp"
    ]

    assert list(result.columns) == expected_columns

    # Check metadata
    assert result["location_id"].iloc[0] == "MUM001"

    assert result["pipeline_run_id"].iloc[0] == test_run_id

    # Check datetime conversion
    assert pd.api.types.is_datetime64_any_dtype(
        result["observation_time"]
    )
