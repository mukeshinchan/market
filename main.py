import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/global_super_store_orders.tsv',sep = '\t')
df.drop(['Unnamed: 0'],axis=1,inplace=True)
df['Sales'] = df['Sales'].str.replace(',','')
df.astype({'Sales':int})
df['Profit'] = df['Profit'].str.replace(',','')
df.astype({'Profit':int})
df.astype({'Row ID':str})
order_date=list(df['Order Date'])
df['Order Date']=pd.to_datetime(date)
ship_date=list(df['Ship Date'])
df['Ship Date']=pd.to_datetime(date)
df['Discount'] = df['Discount'].str.replace(',','')
df.astype({'Discount':int})
df['Shipping Cost'] = df['Shipping Cost'].str.replace(',','')
df.astype({'Shipping Cost':int})
new_df=df.astype({'Postal Code':str})


