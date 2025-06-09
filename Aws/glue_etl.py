import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read data from S3
source_data = glueContext.create_dynamic_frame.from_catalog(
    database="test_db",
    table_name="transactions",
    transformation_ctx="source_data"
)

# Transform data (e.g., clean nulls, aggregate)
transformed_data = ApplyMapping.apply(
    frame=source_data,
    mappings=[
        ("order_id", "string", "order_id", "string"),
        ("customer_id", "string", "customer_id", "string"),
        ("amount", "double", "amount", "double"),
        ("order_date", "string", "order_date", "date")
    ],
    transformation_ctx="transformed_data"
)

# Write to Redshift
glueContext.write_dynamic_frame.from_jdbc_conf(
    frame=transformed_data,
    catalog_connection="redshift_connection",
    connection_options={"dbtable": "public.transactions", "database": "test_db"},
    redshift_tmp_dir="s3://temp-dir/",
    transformation_ctx="redshift_output"
)

job.commit()
