import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        orders_url = "https://supplychain12.blob.core.windows.net/exports/orders_shipments/part-00000.csv"
        inventory_url = "https://supplychain12.blob.core.windows.net/exports/inventory/part-00000.csv"

        orders_shipments = pd.read_csv(
            orders_url, parse_dates=["order_date", "expected_delivery", "actual_delivery"]
        )
        inventory = pd.read_csv(inventory_url)
        st.success("✅ Loaded data from Azure Blob Storage")
    except Exception as e:
        st.warning(f"⚠️ Azure Blob read failed. Loading local files... ({e})")
        orders_shipments = pd.read_csv(
            "data/curated/orders_shipments.csv", parse_dates=["order_date", "expected_delivery", "actual_delivery"]
        )
        inventory = pd.read_csv("data/curated/inventory.csv")
        st.success("✅ Loaded data from local fallback")
    return orders_shipments, inventory

orders_shipments, inventory = load_data()

# --- Header ---
st.title("📦 Supply Chain Analytics Dashboard")
st.markdown("Track shipments, delays, and inventory across your supply chain")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
product_options = orders_shipments["product_id"].dropna().unique()
warehouse_options = inventory["warehouse"].dropna().unique()

selected_product = st.sidebar.selectbox("Product", options=["All"] + sorted(product_options.tolist()))
selected_warehouse = st.sidebar.selectbox("Warehouse", options=["All"] + sorted(warehouse_options.tolist()))

filtered_orders = orders_shipments.copy()
if selected_product != "All":
    filtered_orders = filtered_orders[filtered_orders["product_id"] == selected_product]
if selected_warehouse != "All":
    filtered_orders = filtered_orders[filtered_orders["warehouse"] == selected_warehouse]

# --- KPIs ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Orders", len(filtered_orders["order_id"].unique()))
with col2:
    st.metric("Total Shipments", filtered_orders["shipment_id"].nunique())
with col3:
    delayed = filtered_orders["delay_days"].dropna()
    st.metric("Avg Delay (days)", round(delayed.mean(), 2) if not delayed.empty else "N/A")

st.markdown("---")

# --- Shipment Delay Distribution ---
st.subheader("📊 Shipment Delay Distribution")
fig1, ax1 = plt.subplots()
ax1.hist(filtered_orders["delay_days"].dropna(), bins=20, color="orange")
ax1.set_xlabel("Delay Days")
ax1.set_ylabel("Number of Shipments")
st.pyplot(fig1)

# --- Inventory Overview ---
st.subheader("🏬 Inventory by Warehouse")
fig2, ax2 = plt.subplots()
warehouse_summary = inventory.groupby("warehouse")["quantity"].sum()
warehouse_summary.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Quantity")
ax2.set_xlabel("Warehouse")
st.pyplot(fig2)

# --- Order Trends ---
st.subheader("📈 Order Trends Over Time")
order_trend = (
    filtered_orders.dropna(subset=["order_date"])
    .groupby("order_date")["order_id"]
    .nunique()
    .reset_index(name="total_orders")
)

fig3, ax3 = plt.subplots()
ax3.plot(order_trend["order_date"], order_trend["total_orders"], marker="o")
ax3.set_xlabel("Date")
ax3.set_ylabel("Total Orders")
ax3.set_title("Order Volume Over Time")
st.pyplot(fig3)

# --- Raw Data Preview ---
with st.expander("🗃️ View Raw Data"):
    st.write("Orders & Shipments")
    st.dataframe(filtered_orders.head(50))
    st.write("Inventory")
    st.dataframe(inventory.head(50))
