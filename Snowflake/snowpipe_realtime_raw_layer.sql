-- Step 1: Storage Integration
CREATE OR REPLACE STORAGE INTEGRATION my_s3_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = '<your-aws-role-arn>'
  STORAGE_ALLOWED_LOCATIONS = ('s3://your-bucket-name/raw/');

-- Step 2: Stage
CREATE OR REPLACE STAGE raw_stage
  URL='s3://your-bucket-name/raw/'
  STORAGE_INTEGRATION = my_s3_integration;

-- Step 3: Table
CREATE OR REPLACE TABLE raw_layer (
  id STRING,
  name STRING,
  value STRING,
  load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Step 4: File Format
CREATE OR REPLACE FILE FORMAT raw_csv_format
  TYPE = 'CSV'
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  SKIP_HEADER = 1;

-- Step 5: Snowpipe (real-time ingestion)
CREATE OR REPLACE PIPE raw_pipe AUTO_INGEST = TRUE AS
  COPY INTO raw_layer
  FROM @raw_stage
  FILE_FORMAT = (FORMAT_NAME = raw_csv_format)
  PATTERN = '.*\.csv'
  ON_ERROR = 'CONTINUE';