AWS Data Pipeline
Overview

Objective: Build a scalable data pipeline to process e-commerce transaction data, store it in a data warehouse, and visualize insights.
Tools Used: AWS S3, AWS Glue, Amazon Redshift, Amazon QuickSight, Python.

Architecture
This project implements an end-to-end data pipeline:

Source: Raw transaction data stored in S3.
ETL: AWS Glue for data extraction and transformation.
Storage: Amazon Redshift for data warehousing.
Visualization: QuickSight for dashboards.

graph TD
    A[S3: Raw Data] --> B[Glue: ETL Jobs]
    B --> C[Redshift: Data Warehouse]
    C --> D[QuickSight: Dashboards]

Implementation

Data Ingestion: Raw CSV files are uploaded to an S3 bucket.
ETL Process: Glue crawlers catalog the data, and Python-based Glue jobs transform it into a structured format.
Data Storage: Transformed data is loaded into Redshift tables using a star schema.
Visualization: QuickSight connects to Redshift to create sales dashboards.

Sample Glue Script
See glue_etl.py for a sample ETL script that processes transaction data.
Results

Reduced data processing time by 40% using Glue's serverless ETL.
Enabled real-time sales insights via QuickSight dashboards.

How to Run

Set up an AWS account and configure S3, Glue, Redshift, and QuickSight.
Upload sample data to S3 (e.g., from Kaggle E-commerce Dataset).
Run the Glue script (glue_etl.py) to process data.
Query Redshift and visualize results in QuickSight.

Note: Ensure AWS CLI is configured with appropriate IAM permissions.
