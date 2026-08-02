def validate_weather_data(weather_df):
    """
    Run data quality checks on the transformed weather DataFrame.

    Returns:
        Validated Pandas DataFrame
    """

    required_columns = [
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

    # --------------------------------------------------
    # Check 1: Required columns
    # --------------------------------------------------

    missing_columns = [
        col
        for col in required_columns
        if col not in weather_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    print("✅ Required-column check passed")

    # --------------------------------------------------
    # Check 2: Missing values
    # --------------------------------------------------

    missing_values = weather_df[required_columns].isnull().sum()
    total_missing = missing_values.sum()

    print("Missing values:", total_missing)

    if total_missing > 0:

        weather_df = weather_df.dropna(
            subset=required_columns
        )

        print(
            "⚠️ Missing values removed."
        )

        print(
            "Rows after missing-value removal:",
            len(weather_df)
        )

    else:
        print("✅ Missing-value check passed")

    # --------------------------------------------------
    # Check 3: Duplicate observation keys
    # --------------------------------------------------

    duplicate_count = weather_df.duplicated(
        subset=[
            "location_id",
            "observation_time"
        ]
    ).sum()

    print("Duplicate records:", duplicate_count)

    if duplicate_count > 0:

        weather_df = weather_df.drop_duplicates(
            subset=[
                "location_id",
                "observation_time"
            ]
        )

        print("⚠️ Duplicates removed")

    else:
        print("✅ Duplicate check passed")

    # --------------------------------------------------
    # Check 4: Humidity range
    # --------------------------------------------------

    invalid_humidity = (
        (weather_df["relative_humidity_pct"] < 0) |
        (weather_df["relative_humidity_pct"] > 100)
    ).sum()

    print(
        "Invalid humidity records:",
        invalid_humidity
    )

    if invalid_humidity > 0:
        raise ValueError(
            "Humidity values outside valid range 0-100%"
        )

    print("✅ Humidity range check passed")

    # --------------------------------------------------
    # Check 5: Precipitation cannot be negative
    # --------------------------------------------------

    invalid_precipitation = (
        weather_df["precipitation_mm"] < 0
    ).sum()

    print(
        "Invalid precipitation records:",
        invalid_precipitation
    )

    if invalid_precipitation > 0:
        raise ValueError(
            "Negative precipitation values detected"
        )

    print("✅ Precipitation check passed")

    # --------------------------------------------------
    # Final validation
    # --------------------------------------------------

    if len(weather_df) == 0:
        raise ValueError(
            "Validation failed: No records remaining"
        )

    print("\n✅ ALL DATA QUALITY CHECKS PASSED")

    return weather_df
