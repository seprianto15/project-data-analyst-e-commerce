import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
 
# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule="D", on="order_approved_at").agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })

    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)
    return daily_orders_df

def create_price_products_df(df):
    price_products_df = df.groupby("product_category_name").price.max().sort_values(ascending=False).reset_index()
    return price_products_df

# Load cleaned data
all_df = pd.read_csv(r"C:\Users\dell\Desktop\submission\dashboard\main_data.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)
all_df["order_approved_at"] = pd.to_datetime(all_df["order_approved_at"])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

with st.sidebar:
    st.title("BACK STORE :dizzy: ")

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date,max_date]
    )
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & (all_df["order_approved_at"] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_orders_df = create_daily_orders_df(main_df)
price_products_df = create_price_products_df(main_df)

# Header
st.header ('ミ★ 𝘉𝘈𝘊𝘒 𝘚𝘛𝘖𝘙𝘌 𝘋𝘈𝘚𝘏𝘉𝘖𝘈𝘙𝘋 ★彡')

# Number of daily orders approved
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders_approved = daily_orders_df.order_count.sum()
    st.metric("Total orders approved", value=total_orders_approved)

with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "IDR", locale='es_CO')
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Produk termahal dan terendah
st.subheader('The Most Expensive and Cheapest Product')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(40, 18))

colors = ["#1640D6", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x = "price",
    y = "product_category_name",
    data = price_products_df.head(5),
    palette = colors,
    ax = ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Price", fontsize=40)
ax[0].set_title("Expensive Product", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=40)
ax[0].tick_params(axis='x', labelsize=35)

sns.barplot(
    x = "price",
    y = "product_category_name",
    data = price_products_df.sort_values(by="price", ascending=True).head(5),
    palette = colors,
    ax = ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Price", fontsize=40)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Cheapest Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=40)
ax[1].tick_params(axis='x', labelsize=35)

st.pyplot(fig)

