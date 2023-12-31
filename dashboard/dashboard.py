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

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name").order_item_id.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_sum_type_payments_df(df):
    sum_type_payments_df = df.groupby("payment_type").customer_id.nunique().sort_values(ascending=False).reset_index()
    return sum_type_payments_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_approved_at": "max", # mengambil tanggal order terakhir yang disetujui
        "order_id": "nunique",
        "payment_value": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_approved_at"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date-x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

    return rfm_df

# Load cleaned data
all_df = pd.read_csv("https://raw.githubusercontent.com/seprianto15/project-data-analyst-e-commerce/master/dashboard/main_data.csv")
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
sum_order_items_df = create_sum_order_items_df(main_df)
sum_type_payments_df = create_sum_type_payments_df(main_df)
rfm_df = create_rfm_df(main_df)
recency_df = rfm_df.groupby("recency").customer_id.nunique().reset_index()
frequency_df = rfm_df.groupby("frequency").customer_id.nunique().reset_index()
monetary_df = rfm_df.groupby("monetary").customer_id.nunique().reset_index()

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

# Price product
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

# Product performance
st.subheader('Best and Worst Performing Product')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(40, 18))

colors = ["#1640D6", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x = "order_item_id",
    y = "product_category_name",
    data = sum_order_items_df.head(5),
    palette = colors,
    ax = ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=40)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=40)
ax[0].tick_params(axis='x', labelsize=35)

sns.barplot(
    x = "order_item_id",
    y = "product_category_name",
    data = sum_order_items_df.sort_values(by="order_item_id", ascending=True).head(5),
    palette = colors,
    ax = ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=40)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=40)
ax[1].tick_params(axis='x', labelsize=35)

st.pyplot(fig)

# Type payment
st.subheader("The Payment Type Used by Customer")

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(40, 18))

colors = ["#0069C0", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x = "customer_id",
    y = "payment_type",
    data = sum_type_payments_df,
    palette = colors
)
ax.set_ylabel(None)
ax.set_xlabel('customer_id', fontsize=40)
ax.tick_params(axis ='y', labelsize=40)
ax.tick_params(axis ='x', labelsize=35)

st.pyplot(fig)

# Best Customer Based on RFM Parameters
st.subheader("Best Customer Based on RFM Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(recency_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(frequency_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = format_currency(monetary_df.monetary.mean(), "IDR", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(
    y="recency", 
    x="customer_id", 
    data=recency_df.sort_values(by="recency", ascending=True).head(5), 
    palette=colors, 
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)

sns.barplot(
    y="frequency", 
    x="customer_id", 
    data=frequency_df.sort_values(by="frequency", ascending=False).head(5), 
    palette=colors, 
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)

sns.barplot(
    y="monetary", 
    x="customer_id", 
    data=monetary_df.sort_values(by="monetary", ascending=False).head(5), 
    palette=colors, ax=ax[2]
)
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)

st.pyplot(fig)

st.caption('Copyright © Seprianto 2023')