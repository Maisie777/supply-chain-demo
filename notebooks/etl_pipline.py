from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, datediff

# Start Spark session
spark = SparkSession.builder.appName("SupplyChainETL").getOrCreate()

# Load raw data
orders = spark.read.option("header", True).csv("/dbfs/mnt/raw/orders.csv")
inventory = spark.read.option("header", True).csv("/dbfs/mnt/raw/inventory.csv")
shipments = spark.read.option("header", True).csv("/dbfs/mnt/raw/shipments.csv")

# Convert dates
orders = orders.withColumn("order_date", to_date(col("order_date")))
shipments = shipments.withColumn("expected_delivery", to_date(col("expected_delivery")))
shipments = shipments.withColumn("actual_delivery", to_date(col("actual_delivery")))

# Join orders with shipments
order_shipments = orders.join(shipments, on="order_id", how="left")
order_shipments = order_shipments.withColumn("delay_days", datediff("actual_delivery", "expected_delivery"))

# Write transformed data
order_shipments.write.mode("overwrite").format("parquet").save("/mnt/clean/orders_shipments")
inventory.write.mode("overwrite").format("parquet").save("/mnt/clean/inventory")

# (Optional) Save to Azure SQL
# Use JDBC connection if needed (can help set this up too)
