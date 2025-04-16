from pyspark.sql.functions import col, to_date, datediff

# Set Azure Blob Storage access key
spark.conf.set(
    "fs.azure.account.key.supplychain12.blob.core.windows.net",
    "<your-storage-key-here>"
)

# Define input/output containers
RAW_PATH = "wasbs://raw@supplychain12.blob.core.windows.net"
EXPORT_PATH = "wasbs://exports@supplychain12.blob.core.windows.net"

# Input file paths
ORDERS_PATH = f"{RAW_PATH}/orders.csv"
INVENTORY_PATH = f"{RAW_PATH}/inventory.csv"
SHIPMENTS_PATH = f"{RAW_PATH}/shipments.csv"

# Output paths
ORDERS_OUT = f"{EXPORT_PATH}/orders_shipments"
INVENTORY_OUT = f"{EXPORT_PATH}/inventory"
SHIPMENTS_OUT = f"{EXPORT_PATH}/shipments"  # ✅ Add this

# Read CSVs from Azure Blob
orders = spark.read.option("header", True).csv(ORDERS_PATH)
inventory = spark.read.option("header", True).csv(INVENTORY_PATH)
shipments = spark.read.option("header", True).csv(SHIPMENTS_PATH)

# Parse date columns
orders = orders.withColumn("order_date", to_date(col("order_date")))
shipments = shipments.withColumn("expected_delivery", to_date(col("expected_delivery")))
shipments = shipments.withColumn("actual_delivery", to_date(col("actual_delivery")))

# Calculate delay in days
shipments = shipments.withColumn("delay_days", datediff("actual_delivery", "expected_delivery"))

# Join orders with shipments
order_shipments = orders.join(shipments, on="order_id", how="left")

# Write outputs back to Azure Blob
order_shipments.write.mode("overwrite").parquet(ORDERS_OUT)
inventory.write.mode("overwrite").parquet(INVENTORY_OUT)
shipments.write.mode("overwrite").parquet(SHIPMENTS_OUT)  # ✅ Added this line

print("✅ ETL pipeline completed using Azure Blob Storage.")
