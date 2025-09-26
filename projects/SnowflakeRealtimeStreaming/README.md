# SnowflakeRealtimeStreaming

## Overview

This project demonstrates real-time data streaming into Snowflake using Kafka and Python.

## Technologies

- Python
- Snowflake
- Kafka (confluent-kafka Python client)
- snowflake-connector-python
- SQL

## Steps

1. Produce streaming data to Kafka topic
2. Consume data in Python
3. Transform and load into Snowflake in near real-time

## Files

- `streaming_consumer.py`: Kafka consumer streaming to Snowflake
- `schema.sql`: Snowflake table schema

## How to Use

1. Start Kafka broker and topic.
2. Run `streaming_consumer.py` to ingest and load data.
3. Query the Snowflake table for near real-time results.