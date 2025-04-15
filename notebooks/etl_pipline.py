from pyspark.sql.functions import col, to_date, datediff

# Define raw and curated paths
RAW_PATH = "/FileStore/tables"
CURATED_PATH = "/FileStore/curated"

# Input file paths
ORDERS_PATH = f"{RAW_PATH}/orders.csv"
INVENTORY_PATH = f"{RAW_PATH}/inventory.csv"
SHIPMENTS_PATH = f"{RAW_PATH}/shipments.csv"

# Output paths
ORDERS_OUT = f"{CURATED_PATH}/orders_shipments"
INVENTORY_OUT = f"{CURATED_PATH}/inventory"

# Read CSVs
orders = spark.read.option("header", True).csv(ORDERS_PATH)
inventory = spark.read.option("header", True).csv(INVENTORY_PATH)
shipments = spark.read.option("header", True).csv(SHIPMENTS_PATH)

# Parse dates
orders = orders.withColumn("order_date", to_date(col("order_date")))
shipments = shipments.withColumn("expected_delivery", to_date(col("expected_delivery")))
shipments = shipments.withColumn("actual_delivery", to_date(col("actual_delivery")))

# Calculate delay days
shipments = shipments.withColumn("delay_days", datediff("actual_delivery", "expected_delivery"))

# Join orders and shipments
order_shipments = orders.join(shipments, on="order_id", how="left")

# Write outputs
order_shipments.write.mode("overwrite").parquet(ORDERS_OUT)
inventory.write.mode("overwrite").parquet(INVENTORY_OUT)

print("✅ ETL pipeline completed successfully.")
