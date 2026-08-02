SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT observation_time) AS unique_observations,
    MIN(observation_time) AS earliest_observation,
    MAX(observation_time) AS latest_observation,
    ROUND(AVG(temperature_c), 2) AS avg_temperature_c,
    ROUND(AVG(relative_humidity_pct), 2) AS avg_humidity_pct,
    ROUND(AVG(precipitation_mm), 2) AS avg_precipitation_mm,
    ROUND(AVG(wind_speed_kmh), 2) AS avg_wind_speed_kmh
FROM `weafolk.weather_analytics.fact_weather_forecast`;
