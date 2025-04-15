import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")
st.title("📦 Supply Chain Analytics Dashboard")

# Load data
@st.cache_data
def load_data():
    orders = pd.read_csv("data/raw/orders.csv", parse_dates=["order_date"])
    inventory = pd.read_csv("data/raw/inventory.csv")
    shipments = pd.read_csv("data/raw/shipments.csv", parse_dates=["expected_delivery", "actual_delivery"])
    return orders, inventory, shipments

orders, inventory, shipments = load_data()

# Inventory Section
st.header("📦 Inventory Levels")
low_stock = inventory[inventory["quantity"] < 50]
fig_inventory = px.bar(inventory, x="product_name", y="quantity", color="warehouse",
                       title="Inventory by Product")
st.plotly_chart(fig_inventory, use_container_width=True)

if not low_stock.empty:
    st.warning("⚠️ Low stock detected:")
    st.dataframe(low_stock)

# Shipment Delays Section
st.header("🚚 Shipment Delays")
shipments["delay_days"] = (shipments["actual_delivery"] - shipments["expected_delivery"]).dt.days
delayed = shipments[shipments["delay_days"] > 0]

fig_delays = px.histogram(delayed, x="delay_days", nbins=10, title="Shipment Delay Distribution")
st.plotly_chart(fig_delays, use_container_width=True)

# Order Trends Section
st.header("📈 Order Volume Over Time")
orders_daily = orders.groupby(orders["order_date"].dt.date).size().reset_index(name="orders")
fig_orders = px.line(orders_daily, x="order_date", y="orders", title="Orders per Day")
st.plotly_chart(fig_orders, use_container_width=True)
