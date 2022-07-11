from numerize import numerize
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime as dt
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

st.set_page_config(layout="wide")
df['year']=df['Order Date'].dt.year
year=list(df['year'].unique())
region=list(df['Region'].unique())
df['Month_num']=df['Order Date'].dt.month
df['Month']=df['Order Date'].dt.strftime('%m')




filters=st.empty()
placeholder=st.empty()

out = df.groupby(['Category','Sub-Category','year','Country','Region','Customer ID','Segment','Month'], as_index=False, sort=False).agg({'Sales':'sum','Profit':'sum'})


with filters.container():
    fil1, fil2, fil3 = st.columns(3)
    with fil1:
        year_value = st.selectbox('Select Year',year)
    with fil2:
        region_value=st.selectbox('Select Region',region)
        cotext_country=df[df['Region']==region_value]
        country_list=list(cotext_country['Country'].unique())
    with fil3:
        country_value=st.selectbox('Select Country',country_list)

with placeholder.container():
    # create three columns
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi=df[df['year']==year_value]
    t=kpi['Sales'].sum()
    # fill in those three columns with respective metrics or KPIs 
    with kpi1:
        st.subheader(f'Sales By {year_value}')
        st.metric(label=str(year_value),value=numerize.numerize(t),delta=numerize.numerize(kpi['Sales'].mean()))
   
    kpi_2=df[df['Region']== region_value]
    t2=kpi_2['Sales'].sum()
    with kpi2:
        st.subheader(f'Sales By {region_value}')
        kpi2.metric(label=region_value,value=numerize.numerize(t2),delta=numerize.numerize(kpi_2['Sales'].mean()))
    
    kpi_3=cotext_country[cotext_country['Country']==country_value]
    t3=kpi_3['Sales'].sum()
    with kpi3:
        st.subheader(f'Sales By {country_value}')
        kpi3.metric(label=country_value,value=numerize.numerize(t3),delta=numerize.numerize(kpi_3['Sales'].mean()))

plot=st.empty()

with plot.container():
    col1,col2,col3=st.columns(3)
    with col1:
        filt=out[(out['year']==year_value) & (out['Country']==country_value) & (out['Region']==region_value)].sort_values(by='Sales')
        fig1=px.bar(filt,x='Sales',y='Sub-Category',color='Category',width=450,height=450,orientation='h')
        fig1.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
        fig1.update_layout({'plot_bgcolor':'rgba(0,0,0,0)','paper_bgcolor':'rgba(0,0,0,0)'})
        st.plotly_chart(fig1)
    with col2:
        filt2=out[(out['year']==year_value) & (out['Country']==country_value) & (out['Region']==region_value)]
        fig2=px.pie(filt2,values='Sales',names='Category',color='Category',width=450,height=450,hole=0.5,labels='Sales')
        fig2.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))                
        fig2.update_layout({'plot_bgcolor':'rgba(0,0,0,0)','paper_bgcolor':'rgba(0,0,0,0)'})
        st.plotly_chart(fig2)
    with col3:
        sct=out[out['Region']==region_value]
        fig3=px.scatter(sct,x='year',y='Sales',color='Sales',size='Sales',width=450,height=450)
        fig3.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
        fig3.update_layout({'plot_bgcolor':'rgba(0,0,0,0)','paper_bgcolor':'rgba(0,0,0,0)'})
        st.plotly_chart(fig3)
        
num_value=[i for i in range(5,15)]
range_value=st.select_slider(f'Top Customer',num_value)
butter=st.empty()
with butter.container():
    bar1,bar2,bar3=st.columns(3)
    with bar1:
        data1=out[(out['year']==year_value) & (out['Country']==country_value) & (out['Region']==region_value)].sort_values(by='Sales',ascending=False).head(range_value)
        fig4=px.bar(data1,x='Sales',y='Customer ID',color='Customer ID',text_auto=True)
        fig4.update_yaxes(title='y', visible=False, showticklabels=False)
        #fig4.update_xaxes(title='x', visible=False, showticklabels=False)
        fig4.update_xaxes(autorange='reversed')
        fig4.update_layout({'plot_bgcolor':'rgba(0,0,0,0)','paper_bgcolor':'rgba(0,0,0,0)'})
        fig4.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
        fig4.update_layout(width=500,height=500)
        fig4.update(layout_showlegend=False)
        st.plotly_chart(fig4)  
    with bar2:
        data2=out[(out['year']==year_value) & (out['Country']==country_value) & (out['Region']==region_value)].sort_values(by='Profit',ascending=False).head(range_value)
        fig5=px.bar(data2,x='Profit',y='Customer ID',color='Customer ID',text_auto=True)
        fig5.update_yaxes(title='y', visible=True, showticklabels=True)
        fig5.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
        #fig4.update_xaxes(title='x', visible=False, showticklabels=False)
        fig5.update_layout(
                boxgap=0.25,
                height=500, 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(pad=50)
               )
        fig5.update(layout_showlegend=False)
        fig5.update_layout(width=500,boxgap=0.5)
        fig5.update_layout(height=500)
        st.plotly_chart(fig5)
    with bar3:
        pie_1=out[(out['year']==year_value) & (out['Country']==country_value) & (out['Region']==region_value)]
        fig6=px.pie(pie_1,values='Sales',names='Segment',color='Segment',width=450,height=450,labels='Sales')
        fig6.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))                
        fig6.update_layout({'plot_bgcolor':'rgba(0,0,0,0)','paper_bgcolor':'rgba(0,0,0,0)'})
        st.plotly_chart(fig6)
        
        
data=df[df['year']==year_value]
out2= data.groupby(['Month','Month_num'], as_index=False, sort=False).agg({'Sales':'sum'}).sort_values(by='Month_num')
fig7=px.line(out2,x='Month',y='Sales',width=1200,height=750,text='Sales')
fig7.update_traces(textposition="top right")
fig7.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
fig7.update_layout({'plot_bgcolor':'rgba(0,0,0,0)','paper_bgcolor':'rgba(0,0,0,0)'})
st.plotly_chart(fig7)   

