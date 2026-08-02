-- Check 1: Total records
SELECT
    COUNT(*) AS total_records
FROM `weafolk.weather_analytics.fact_weather_forecast`;


-- Check 2: Duplicate observation keys
SELECT
    COUNT(*) AS duplicate_records
FROM (
    SELECT
        location_id,
        observation_time,
        COUNT(*) AS record_count
    FROM `weafolk.weather_analytics.fact_weather_forecast`
    GROUP BY location_id, observation_time
    HAVING COUNT(*) > 1
);


-- Check 3: Invalid humidity
SELECT
    COUNT(*) AS invalid_humidity_records
FROM `weafolk.weather_analytics.fact_weather_forecast`
WHERE relative_humidity_pct < 0
   OR relative_humidity_pct > 100;


-- Check 4: Negative precipitation
SELECT
    COUNT(*) AS invalid_precipitation_records
FROM `weafolk.weather_analytics.fact_weather_forecast`
WHERE precipitation_mm < 0;


-- Check 5: Pipeline failures
SELECT
    COUNT(*) AS failed_pipeline_runs
FROM `weafolk.weather_analytics.pipeline_runs`
WHERE status = 'FAILED';
