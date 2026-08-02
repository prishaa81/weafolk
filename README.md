🌦️ WEAFOLK — Weather Data ETL Pipeline

A portfolio-quality **Python ETL pipeline** that extracts weather forecast data from an external API, transforms and validates the data, loads it into Google BigQuery, and performs incremental loading using a MERGE operation. The project also includes automated data-quality checks, pipeline-run logging, unit tests, and SQL analytics queries.


1> Project Overview:
WEAFOLK is a modular data engineering project designed to demonstrate an end-to-end ETL workflow.
The pipeline collects hourly weather forecast data for Mumbai from the Open-Meteo API and processes it through the following stages:

```text
Open-Meteo API
      │
      ▼
   EXTRACT
      │
      ▼
  TRANSFORM
      │
      ▼
 DATA QUALITY
   VALIDATION
      │
      ▼
BIGQUERY STAGING
      │
      ▼
 INCREMENTAL MERGE
      │
      ▼
FACT TABLE
      │
      ▼
PIPELINE LOGGING

```

2> Project Objectives:
The main objectives of WEAFOLK are to:

* Build a complete ETL pipeline using Python
* Extract real-world weather data from an external API
* Transform API responses into structured tabular data
* Perform automated data-quality validation
* Load validated data into Google BigQuery
* Load validated data into Google BigQuery
* Load validated data into Google BigQuery
* Use a staging table before loading production data
* Implement incremental loading using BigQuery MERGE
* Log successful and failed pipeline executions
* Write reusable and modular Python components
* Add automated unit tests using pytest
* Perform analytical queries on the processed data
