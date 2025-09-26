"""
Batch ETL pipeline to load data into Snowflake
"""
import pandas as pd
import snowflake.connector

def extract():
    # Example: read CSV
    data = pd.DataFrame({'id': [1,2], 'amount': [100.0, 200.0]})
    return data

def transform(data):
    # Example transformation
    data['amount'] = data['amount'] * 1.1
    return data

def load(data):
    # Placeholder: Connect and load to Snowflake
    print("Connecting to Snowflake...")
    # conn = snowflake.connector.connect(...)
    print("Would load data to Snowflake table here")
    print(data)

if __name__ == "__main__":
    df = extract()
    df = transform(df)
    load(df)