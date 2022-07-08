import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/global_super_store_orders.tsv',sep = '\t')
df['Sales_2'] = df['Sales'].str.replace(',','')
df['New_sales']=pd.to_numeric(df['Sales_2']) 
df['Profit_2'] = df['Profit'].str.replace(',','')
df['New_Profit']=pd.to_numeric(df['Profit_2'])
out = df.groupby('Category', as_index=False, sort=False).agg({'New_sales':'sum'})
pie=px.pie(out,values='New_sales',names='Category', color_discrete_sequence=['#0d0887', '#9999ff', '#3333ff'])
st.plotly_chart(pie)

out2 = df.groupby('Customer ID', as_index=False, sort=False).agg({'New_sales':'sum','New_Profit':'sum'})
bar=out2[out2['New_sales']>=out2['New_sales'].mean()]
bar_chart=px.bar(bar,x='Customer ID', y='New_sales')
st.plotly_chart(bar_chart)
sub_cat = df.groupby('Sub-Category', as_index=False, sort=False).agg({'New_sales':'sum','New_Profit':'sum'})
l=list(df['Order Date'])
type(l[-1])
Date=pd.to_datetime(l)
df['New_Date']=Date
df['year']=df['New_Date'].dt.year
year = df.groupby('year', as_index=False, sort=False).agg({'New_sales':'sum','New_Profit':'sum'})
year_sales=px.bar(year,x='year',y='New_sales')
st.plotly_chart(year_sales)
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        y=bar['New_sales'],
        x=bar['Customer ID']
    ))

fig.add_trace(
    go.Bar(
        y=bar['New_sales'],
        x=bar['Customer ID']
    ))

fig.show()