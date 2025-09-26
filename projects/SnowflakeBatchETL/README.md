# SnowflakeBatchETL

## Overview

This project demonstrates a batch ETL process loading data into Snowflake from flat files or databases using Python.

## Technologies

- Python
- Snowflake
- snowflake-connector-python
- SQL

## Steps

1. Extract batch data from source (CSV, database)
2. Transform data in Python
3. Load data into Snowflake using connector
4. Run analytics queries

## Files

- `etl_batch.py`: Batch ETL pipeline script
- `schema.sql`: Snowflake table schema

## How to Use

1. Configure Snowflake connection in the script.
2. Run `etl_batch.py` to load sample data.
3. Query the Snowflake table for results.