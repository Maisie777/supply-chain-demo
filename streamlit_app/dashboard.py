import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    orders_shipments = pd.read_csv("data/curated/orders_shipments.csv", parse_dates=["order_date", "expected_delivery", "actual_delivery"])
    inventory = pd.read_csv("data/curated/inventory.csv")
    return orders_shipments, inventory

orders_shipments, inventory = load_data()

# --- Header ---
st.title("📦 Supply Chain Analytics Dashboard")
st.markdown("Track shipments, delays, and inventory across your supply chain")

# --- KPIs ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Orders", len(orders_shipments["order_id"].unique()))

with col2:
    st.metric("Total Shipments", orders_shipments["shipment_id"].nunique())

with col3:
    delayed = orders_shipments["delay_days"].dropna()
    st.metric("Avg Delay (days)", round(delayed.mean(), 2))

st.markdown("---")

# --- Delay Distribution ---
st.subheader("📊 Shipment Delay Distribution")

fig1, ax1 = plt.subplots()
ax1.hist(orders_shipments["delay_days"].dropna(), bins=20, color="orange")
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

# --- Raw Data Preview ---
with st.expander("🗃️ View Raw Data"):
    st.write("Orders & Shipments")
    st.dataframe(orders_shipments.head(50))
    st.write("Inventory")
    st.dataframe(inventory.head(50))

fig1.savefig("shipment_delay_histogram.png")
