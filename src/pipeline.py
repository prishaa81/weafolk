import uuid
from datetime import datetime, timezone

from google.cloud import bigquery

from src.extract import extract_weather_data
from src.transform import transform_weather_data
from src.validate import validate_weather_data
from src.load import load_to_staging, merge_to_fact


# --------------------------------------------------
# BigQuery configuration
# --------------------------------------------------

PROJECT_ID = "weafolk"

DATASET_ID = "weather_analytics"

LOCATION_ID = "MUM001"

LATITUDE = 19.086115

LONGITUDE = 72.85291


# --------------------------------------------------
# BigQuery client
# --------------------------------------------------

client = bigquery.Client(project=PROJECT_ID)


# --------------------------------------------------
# BigQuery schema
# --------------------------------------------------

schema = [
    bigquery.SchemaField(
        "observation_time",
        "TIMESTAMP"
    ),

    bigquery.SchemaField(
        "temperature_c",
        "FLOAT"
    ),

    bigquery.SchemaField(
        "relative_humidity_pct",
        "FLOAT"
    ),

    bigquery.SchemaField(
        "apparent_temperature_c",
        "FLOAT"
    ),

    bigquery.SchemaField(
        "precipitation_mm",
        "FLOAT"
    ),

    bigquery.SchemaField(
        "rain_mm",
        "FLOAT"
    ),

    bigquery.SchemaField(
        "weather_code",
        "INTEGER"
    ),

    bigquery.SchemaField(
        "surface_pressure_hpa",
        "FLOAT"
    ),

    bigquery.SchemaField(
        "wind_speed_kmh",
        "FLOAT"
    ),

    bigquery.SchemaField(
        "wind_direction_deg",
        "FLOAT"
    ),

    bigquery.SchemaField(
        "location_id",
        "STRING"
    ),

    bigquery.SchemaField(
        "pipeline_run_id",
        "STRING"
    ),

    bigquery.SchemaField(
        "ingestion_timestamp",
        "TIMESTAMP"
    )
]


# --------------------------------------------------
# Pipeline logging
# --------------------------------------------------

def log_pipeline_run(
    run_id,
    start_time,
    end_time,
    status,
    records_extracted,
    records_staged,
    error_message=None
):
    """
    Log pipeline execution details to BigQuery.
    """

    table_id = (
        "weafolk.weather_analytics.pipeline_runs"
    )

    row = {
        "run_id": run_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "status": status,
        "records_extracted": records_extracted,
        "records_staged": records_staged,
        "error_message": error_message
    }

    errors = client.insert_rows_json(
        table_id,
        [row]
    )

    if errors:
        print(
            "⚠️ Failed to write pipeline log:",
            errors
        )
    else:
        print("📝 Pipeline run logged to BigQuery")


# --------------------------------------------------
# Main ETL pipeline
# --------------------------------------------------

def run_pipeline():

    run_id = str(uuid.uuid4())

    start_time = datetime.now(timezone.utc)

    records_extracted = 0

    records_staged = 0

    print("=" * 60)

    print("WEAFOLK ETL PIPELINE STARTED")

    print("Run ID:", run_id)

    print("Start time:", start_time)

    print("=" * 60)

    try:

        # ==================================================
        # STEP 1 — EXTRACT
        # ==================================================

        print("\n[1/5] Extracting weather data...")

        weather_data = extract_weather_data(
            LATITUDE,
            LONGITUDE
        )

        records_extracted = len(
            weather_data["hourly"]["time"]
        )

        # ==================================================
        # STEP 2 — TRANSFORM
        # ==================================================

        print("\n[2/5] Transforming data...")

        weather_df = transform_weather_data(
            weather_data,
            run_id
        )

        print("✅ Transformation completed!")

        print(
            "Transformed records:",
            len(weather_df)
        )

        # ==================================================
        # STEP 3 — VALIDATE
        # ==================================================

        print("\n[3/5] Running data quality checks...")

        weather_df = validate_weather_data(
            weather_df
        )

        print(
            "Validated records:",
            len(weather_df)
        )

        # ==================================================
        # STEP 4 — LOAD TO STAGING
        # ==================================================

        print(
            "\n[4/5] Loading validated data into staging..."
        )

        records_staged = load_to_staging(
            client,
            weather_df,
            schema
        )

        # ==================================================
        # STEP 5 — INCREMENTAL MERGE
        # ==================================================

        print(
            "\n[5/5] Merging data into fact table..."
        )

        merge_to_fact(client)

        # ==================================================
        # SUCCESS LOGGING
        # ==================================================

        end_time = datetime.now(timezone.utc)

        log_pipeline_run(
            run_id=run_id,
            start_time=start_time,
            end_time=end_time,
            status="SUCCESS",
            records_extracted=records_extracted,
            records_staged=records_staged,
            error_message=None
        )

        print("\n🎉 WEAFOLK PIPELINE COMPLETED SUCCESSFULLY!")

    except Exception as e:

        # ==================================================
        # FAILURE HANDLING
        # ==================================================

        end_time = datetime.now(timezone.utc)

        print("\n❌ PIPELINE FAILED")

        print("Error:", str(e))

        log_pipeline_run(
            run_id=run_id,
            start_time=start_time,
            end_time=end_time,
            status="FAILED",
            records_extracted=records_extracted,
            records_staged=records_staged,
            error_message=str(e)
        )

        print("📝 FAILED run logged to BigQuery")

        # Re-raise the error so external schedulers
        # can detect that the pipeline failed.
        raise


# --------------------------------------------------
# Run pipeline
# --------------------------------------------------

if __name__ == "__main__":
    run_pipeline()
