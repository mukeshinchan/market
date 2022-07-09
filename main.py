import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/global_super_store_orders.tsv',sep = '\t')
df.drop(['Unnamed: 0'],axis=1,inplace=True)
df['Sales'] = df['Sales'].str.replace(',','')
df['Sales']=df['Sales'].astype(float)
df['Profit'] = df['Profit'].str.replace(',','')
df['Profit']=df['Profit'].astype(float)
df['Row ID']=df['Row ID'].astype(str)
order_date=list(df['Order Date'])
df['Order Date']=pd.to_datetime(order_date)
ship_date=list(df['Ship Date'])
df['Ship Date']=pd.to_datetime(order_date)
df['Discount'] = df['Discount'].str.replace(',','')
df['Discount']=df['Discount'].astype(float)
df['Shipping Cost'] = df['Shipping Cost'].str.replace(',','')
df['Shipping Cost']=df['Shipping Cost'].astype(float)
df['Postal Code']=df['Postal Code'].astype(str)

col1,col2,col3=st.columns([3,1,2])
with col1:
    ship_mode = df.groupby('Ship Mode', as_index=False, sort=False)['Ship Mode'].agg({'Ship Mode':'count'})
    ship_mode['Ship_Mode_Name']=df['Ship Mode'].unique()
    st.plotly_chart(px.pie(ship_mode,values='Ship Mode',names='Ship_Mode_Name',width=400,height=400,color_discrete_sequence=['#0d0887', '#9999ff', '#3333ff']))
with col3:
    st.write('f')
with col2:
    out = df.groupby('Category', as_index=False, sort=False).agg({'Sales':'sum'})
    st.plotly_chart(px.bar(out,y='Sales',x='Category', color_discrete_sequence=['#0d0887', '#9999ff', '#3333ff'],width=500,height=500))
    
out2 = df.groupby('Customer ID', as_index=False, sort=False).agg({'Sales':'sum','Profit':'sum'})
Cust_above_avg=out2[out2['Sales']>=out2['Sales'].mean()]
st.plotly_chart(px.bar(Cust_above_avg,x='Customer ID', y='Sales',width=400,height=400))