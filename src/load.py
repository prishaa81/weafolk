from google.cloud import bigquery


def load_to_staging(client, weather_df, schema):
    """
    Load validated weather data into the BigQuery staging table.
    """

    staging_table_id = (
        "weafolk.weather_analytics.stg_weather_forecast"
    )

    staging_job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    staging_job = client.load_table_from_dataframe(
        weather_df,
        staging_table_id,
        job_config=staging_job_config
    )

    staging_job.result()

    print("✅ Staging load completed!")
    print("Records staged:", len(weather_df))

    return len(weather_df)


def merge_to_fact(client):
    """
    Incrementally merge staging data into the BigQuery fact table.
    """

    merge_query = """
    MERGE `weafolk.weather_analytics.fact_weather_forecast` AS target

    USING `weafolk.weather_analytics.stg_weather_forecast` AS source

    ON target.location_id = source.location_id
    AND TIMESTAMP(target.observation_time) = source.observation_time

    WHEN MATCHED THEN
      UPDATE SET
        temperature_c = source.temperature_c,
        relative_humidity_pct = source.relative_humidity_pct,
        apparent_temperature_c = source.apparent_temperature_c,
        precipitation_mm = source.precipitation_mm,
        rain_mm = source.rain_mm,
        weather_code = source.weather_code,
        surface_pressure_hpa = source.surface_pressure_hpa,
        wind_speed_kmh = source.wind_speed_kmh,
        wind_direction_deg = source.wind_direction_deg,
        pipeline_run_id = source.pipeline_run_id,
        ingestion_timestamp = source.ingestion_timestamp

    WHEN NOT MATCHED THEN
      INSERT (
        observation_time,
        temperature_c,
        relative_humidity_pct,
        apparent_temperature_c,
        precipitation_mm,
        rain_mm,
        weather_code,
        surface_pressure_hpa,
        wind_speed_kmh,
        wind_direction_deg,
        location_id,
        pipeline_run_id,
        ingestion_timestamp
      )

      VALUES (
        source.observation_time,
        source.temperature_c,
        source.relative_humidity_pct,
        source.apparent_temperature_c,
        source.precipitation_mm,
        source.rain_mm,
        source.weather_code,
        source.surface_pressure_hpa,
        source.wind_speed_kmh,
        source.wind_direction_deg,
        source.location_id,
        source.pipeline_run_id,
        source.ingestion_timestamp
      )
    """

    merge_job = client.query(merge_query)
    merge_job.result()

    print("✅ Incremental MERGE completed successfully!")
