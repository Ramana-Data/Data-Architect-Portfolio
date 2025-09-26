import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
import pyspark.sql.functions as F

# Glue job parameters
args = getResolvedOptions(sys.argv, [
    "JOB_NAME",
    "aurora_connection",
    "redshift_connection",
    "redshift_temp_dir"
])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# -------------------------------
# 1. Extract: Read from Aurora
# -------------------------------
aurora_df = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",  # or "postgresql" if Aurora PostgreSQL
    connection_options={
        "database": "your_db",
        "table": "customer_dim"
    },
    connection_name=args["aurora_connection"]
).toDF()

# -------------------------------
# 2. Read target (Redshift) SCD dimension
# -------------------------------
redshift_df = glueContext.create_dynamic_frame.from_options(
    connection_type="redshift",
    connection_options={
        "dbtable": "customer_dim",
        "database": "your_redshift_db"
    },
    redshift_tmp_dir=args["redshift_temp_dir"],
    connection_name=args["redshift_connection"]
).toDF()

# -------------------------------
# 3. SCD2 Logic: Detect changes
# -------------------------------
# Assumed columns: customer_id (key), name, address, is_current, start_date, end_date

# Only current rows from Redshift
current_dim = redshift_df.filter(F.col("is_current") == 1)

# Join Aurora (source) with Redshift (current target) by customer_id
joined_df = aurora_df.alias("a").join(
    current_dim.alias("r"),
    F.col("a.customer_id") == F.col("r.customer_id"),
    "leftouter"
)

# Find new or changed records
change_condition = (
    (F.col("a.name") != F.col("r.name")) |
    (F.col("a.address") != F.col("r.address")) |
    F.col("r.customer_id").isNull()
)

# Prepare new rows for insert
new_rows_df = joined_df.filter(change_condition).select(
    F.col("a.customer_id"),
    F.col("a.name"),
    F.col("a.address"),
    F.lit(1).alias("is_current"),
    F.current_date().alias("start_date"),
    F.lit(None).cast("date").alias("end_date")
)

# End-date previous records for changed keys
end_previous_df = joined_df.filter(change_condition & F.col("r.customer_id").isNotNull()).select(
    F.col("r.customer_id"),
    F.col("r.name"),
    F.col("r.address"),
    F.lit(0).alias("is_current"),
    F.col("r.start_date"),
    F.current_date().alias("end_date")
)

# Union unchanged current records
unchanged_df = current_dim.subtract(end_previous_df)

# Combine all for final dimension
final_df = unchanged_df.union(end_previous_df).union(new_rows_df)

# -------------------------------
# 4. Load: Write to Redshift
# -------------------------------
final_dynamic_frame = glueContext.create_dynamic_frame.from_df(final_df, glueContext, "final_dynamic_frame")

glueContext.write_dynamic_frame.from_options(
    frame=final_dynamic_frame,
    connection_type="redshift",
    connection_options={
        "dbtable": "customer_dim",
        "database": "your_redshift_db"
    },
    redshift_tmp_dir=args["redshift_temp_dir"],
    connection_name=args["redshift_connection"]
)