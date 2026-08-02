SELECT
    EXTRACT(HOUR FROM observation_time) AS hour_of_day,
    ROUND(AVG(temperature_c), 2) AS avg_temperature_c,
    ROUND(AVG(relative_humidity_pct), 2) AS avg_humidity_pct,
    ROUND(AVG(wind_speed_kmh), 2) AS avg_wind_speed_kmh
FROM `weafolk.weather_analytics.fact_weather_forecast`
GROUP BY hour_of_day
ORDER BY hour_of_day;
