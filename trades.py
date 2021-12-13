import numpy as np
import streamlit as st
from PIL import Image
import pandas as pd
from pymongo import MongoClient
import numpy 
import altair as alt
import plotly_express as px
import datetime
from datetime import timedelta
#---------------------------------#

# Page layout :Page expands to full width
st.set_page_config(layout="wide")
#---------------------------------#

# Title
image = Image.open('Capture3.png')
st.image(image, width = 850)
st.title('Crypto Price App')
original_title = '<p style="font-family:Courier; color:#07F7F7; font-size: 15px;">This app retrieves cryptocurrency prices for cryptocurrency from the **CoinCap**!</p>'
st.markdown(original_title, unsafe_allow_html=True)
#---------------------------------# 

# About
expander_bar = st.expander("ABOUT")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, datetime
* **Data source:** [CoinMarketCap](http://coincap.com).
""")
#---------------------------------#

# Mongo Connection
client = MongoClient("mongodb+srv://Admin:TPLink123@coincap.dzreb.mongodb.net/Coincap?retryWrites=true&w=majority")
db = client.Coincap
collection = db['Trades']
#---------------------------------#

# header
col1 = st.sidebar
col1.header('Input Options')
#---------------------------------#

# function defn
@st.cache
def date_query(x):
    cursor = collection.find({"timestamp": {"$gt": today - timedelta(x)}})
    df =  pd.DataFrame(list(cursor))
    return df

@st.cache
def find_currency(x):
    mydoc = collection.find({"quote":{"$in":x}})
    df1 =  pd.DataFrame(list(mydoc)) 
    return df1
#---------------------------------#

# select date range for data
today = datetime.datetime.today()
d3 = col1.date_input("Select the desired Date range", [],min_value=None, max_value=today)
#st.write(d3[0])
#st.write(type(d3[1]))
delta= d3[1] - d3[0]
#st.write(delta)
days= delta.days
#---------------------------------#

# get data with selected time range
df= date_query(days)
df=df.drop('_id', axis=1)
#---------------------------------#

# get a list crypto currency available
coins = df["quote"].to_numpy()
sorted_coins = sorted(np.unique(coins))
sorted_coins.append("All")
#st.write(sorted_coins)

cols=[]
df_cols = pd.DataFrame(cols)
df_cols = col1.multiselect('Select your fav Cryptooo!', sorted_coins)
if "All" in df_cols:
    df_cols = sorted_coins
#st.write(df_cols)
#---------------------------------#

# get data with selected crypto currency
df1 = find_currency(df_cols)
#---------------------------------#

# get direction of sale
unique_coins= df1.direction.unique()
direction = col1.selectbox('Select direction of trade', unique_coins)
#---------------------------------#

# get data with selected direction of trade
newdf = df1.query('direction ==  @direction')
#---------------------------------#

# chart of price 
st.subheader('Chart of Price Change')
price_chart_data = pd.DataFrame(newdf,columns=['price','timestamp','quote'])
price_chart = ( getattr(alt.Chart(price_chart_data), "mark_" + "line")().encode(alt.X("timestamp", title=""),alt.Y("price", title=""),alt.Color("quote", title="", type="nominal"),alt.Tooltip(["timestamp", "price", "quote"]))).properties( width=1400,height=600).interactive()
st.altair_chart(price_chart)
#---------------------------------#

# chart of volume
volume_chart_data = pd.DataFrame(newdf, columns=['volume','timestamp','quote'])
st.subheader('Chart of Volume Change')
volume_chart = ( getattr(alt.Chart(volume_chart_data), "mark_" + "line")().encode(alt.X("timestamp", title=""),alt.Y("volume", title=""),alt.Color("quote", title="", type="nominal"),alt.Tooltip(["timestamp", "volume", "quote"]))).properties( width=1400,height=600).interactive()
st.altair_chart(volume_chart)   