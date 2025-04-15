from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, datediff

# Create Spark session
spark = SparkSession.builder.appName("SupplyChainETL").getOrCreate()

# Load raw data (assumes mounted Blob or local CSVs for demo)
orders = spark.read.option("header", True).csv("/dbfs/FileStore/raw/orders.csv")
inventory = spark.read.option("header", True).csv("/dbfs/FileStore/raw/inventory.csv")
shipments = spark.read.option("header", True).csv("/dbfs/FileStore/raw/shipments.csv")

# Parse dates
orders = orders.withColumn("order_date", to_date(col("order_date")))
shipments = shipments.withColumn("expected_delivery", to_date(col("expected_delivery")))
shipments = shipments.withColumn("actual_delivery", to_date(col("actual_delivery")))

# Calculate delay days
shipments = shipments.withColumn("delay_days", datediff("actual_delivery", "expected_delivery"))

# Join orders with shipment info
order_shipments = orders.join(shipments, on="order_id", how="left")

# Write output to a curated zone (Parquet format for now)
order_shipments.write.mode("overwrite").parquet("/dbfs/FileStore/curated/orders_shipments/")
inventory.write.mode("overwrite").parquet("/dbfs/FileStore/curated/inventory/")
