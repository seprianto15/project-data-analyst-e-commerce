import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
 
def create_price_products_df(df):
    price_products_df = df.groupby("product_category_name").price.max().sort_values(ascending=False).reset_index()
    return price_products_df

all_df = pd.read_csv(r"C:\Users\dell\Desktop\submission\dashboard\main_data.csv")

price_products_df = create_price_products_df(all_df)

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
