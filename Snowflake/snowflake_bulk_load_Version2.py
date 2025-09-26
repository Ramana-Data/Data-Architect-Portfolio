
1. Assessment & Planning
Data Analysis: Identify data sources, formats, and sensitivity. Clean up unnecessary/obsolete data.
Connectivity: Ensure network connectivity between on-prem and Snowflake (consider VPN or private connectivity for security and speed).
Sizing: Estimate compute and storage needs on Snowflake (use Snowflake’s auto-scaling features).
2. Prepare Data
Data Extraction: Export data from on-prem systems (databases, files, etc.) into staged files, preferably in compressed formats like CSV, Parquet, or Avro.
Data Cleansing: Remove duplicates, fix inconsistencies, and validate the data.
3. Select Transfer Method
Direct Upload: Use Snowflake’s bulk loading tools (Snowpipe, COPY INTO, etc.) to upload files to Snowflake.
Cloud Staging: Upload data to a cloud storage stage (AWS S3, Azure Blob, GCS) and then ingest into Snowflake.
ETL Tools: Consider using ETL solutions (Talend, Informatica, Matillion, Fivetran, etc.) for complex transformations.
4. Optimize Transfer
Parallelism: Split data into smaller files/partitions to enable parallel uploads.
Compression: Compress files to minimize transfer time.
Network: Use high-bandwidth, low-latency connections. For very large datasets, consider Snowflake’s private connectivity (Direct Connect/ExpressRoute).
5. Load Data into Snowflake
Create Tables: Define target tables in Snowflake, matching schema and types.
Bulk Load: Use COPY INTO or Snowpipe for efficient ingestion from cloud staging.
Monitor Load: Track progress and errors using Snowflake’s monitoring features.
6. Validation & Testing
Data Validation: Compare row counts, checksums, and sample queries between source and Snowflake.
Performance Testing: Run queries to validate performance and optimize clustering/partitioning.
7. Cutover & Go-Live
Final Sync: Migrate any delta changes since the initial load.
Switch Over: Point applications to Snowflake.
Monitor: Continuously monitor performance and costs.
Tips:

For 10TB, cloud staging is usually faster and more reliable than direct uploads.
Use COPY INTO from external stage for bulk data loads.
Use Snowflake’s best practices for file sizes (100MB-250MB per file is ideal for parallelism).
import snowflake.connector

# Snowflake connection parameters
conn = snowflake.connector.connect(
    user='<SNOWFLAKE_USER>',
    password='<SNOWFLAKE_PASSWORD>',
    account='<SNOWFLAKE_ACCOUNT>',
    warehouse='<SNOWFLAKE_WAREHOUSE>',
    database='<SNOWFLAKE_DATABASE>',
    schema='<SNOWFLAKE_SCHEMA>'
)

cursor = conn.cursor()

# 1. Create the target table (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS my_table (
    id INT,
    name STRING,
    value FLOAT
)
""")

# 2. Create an external stage (S3)
cursor.execute("""
CREATE OR REPLACE STAGE my_s3_stage
URL='s3://my-bucket/data/'
STORAGE_INTEGRATION = my_s3_integration
""")

# 3. Bulk load data from S3
cursor.execute("""
COPY INTO my_table
FROM @my_s3_stage
FILE_FORMAT = (TYPE = 'CSV', FIELD_OPTIONALLY_ENCLOSED_BY='"')
PATTERN='.*\\.csv'
ON_ERROR='CONTINUE'
""")

# 4. Validate load
cursor.execute("SELECT COUNT(*) FROM my_table")
print("Row count:", cursor.fetchone()[0])

cursor.close()
conn.close()