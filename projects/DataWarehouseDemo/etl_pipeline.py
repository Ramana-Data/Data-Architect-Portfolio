"""
Example ETL pipeline for DataWarehouseDemo
"""
import pandas as pd

def extract():
    # Placeholder for extraction logic
    data = pd.DataFrame({'id': [1, 2], 'value': [100, 200]})
    return data

def transform(data):
    # Placeholder for transformation logic
    data['value'] = data['value'] * 2
    return data

def load(data):
    # Placeholder for load logic
    print("Loading data to warehouse...")
    print(data)

if __name__ == "__main__":
    raw_data = extract()
    transformed_data = transform(raw_data)
    load(transformed_data)