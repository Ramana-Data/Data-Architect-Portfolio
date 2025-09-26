import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Example: Read CSV data from S3, filter, and write to Redshift
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://your-bucket/input-data/"]},
    format="csv",
    format_options={"withHeader": True}
)

# Filter transformation: keep only rows where value > 100
filtered = Filter.apply(frame=datasource, f=lambda x: x["value"] > 100)

# Write to Redshift
glueContext.write_dynamic_frame.from_options(
    frame=filtered,
    connection_type="redshift",
    connection_options={
        "dbtable": "your_table",
        "database": "your_db",
        "redshiftTmpDir": "s3://your-bucket/temp/"
    }
)

job.commit()