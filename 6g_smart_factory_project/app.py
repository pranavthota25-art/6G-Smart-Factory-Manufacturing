import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title='6G Smart Factory Analytics', page_icon='🏭', layout='wide')
DEFAULT = Path(__file__).parent / 'data' / 'Thales_Group_Manufacturing.xlsx'
st.title('🏭 6G Network Performance & Smart Factory Efficiency')
st.caption('Exploratory analytics for network reliability, production, quality and operating modes')

@st.cache_data
def load_data(file):
    d = pd.read_excel(file)
    d['Date'] = pd.to_datetime(d['Date'], errors='coerce')
    d['Timestamp'] = pd.to_timedelta(d['Timestamp'].astype(str), errors='coerce')
    d['DateTime'] = d['Date'] + d['Timestamp']
    return d

up = st.sidebar.file_uploader('Upload manufacturing Excel file (optional)', type=['xlsx'])
df = load_data(up if up else DEFAULT)
st.sidebar.header('Filters')
min_date, max_date = df['Date'].min().date(), df['Date'].max().date()
date_range = st.sidebar.date_input('Date range', value=(min_date, max_date), min_value=min_date, max_value=max_date)
if isinstance(date_range, tuple) and len(date_range)==2:
    df = df[df['Date'].dt.date.between(date_range[0], date_range[1])]
modes = st.sidebar.multiselect('Operation mode', sorted(df['Operation_Mode'].dropna().unique()), default=sorted(df['Operation_Mode'].dropna().unique()))
classes = st.sidebar.multiselect('Efficiency class', ['High','Medium','Low'], default=['High','Medium','Low'])
lat_max = st.sidebar.slider('Maximum latency (ms)', 0.0, float(df['Network_Latency_ms'].max()), float(df['Network_Latency_ms'].max()))
loss_max = st.sidebar.slider('Maximum packet loss (%)', 0.0, float(df['Packet_Loss_%'].max()), float(df['Packet_Loss_%'].max()))
df = df[df['Operation_Mode'].isin(modes) & df['Efficiency_Status'].isin(classes)]
df = df[(df['Network_Latency_ms'] <= lat_max) & (df['Packet_Loss_%'] <= loss_max)]
if df.empty:
    st.warning('No rows match the selected filters. Widen the filters.')
    st.stop()

c1,c2,c3,c4 = st.columns(4)
c1.metric('Records', f'{len(df):,}')
c2.metric('Mean latency', f"{df.Network_Latency_ms.mean():.2f} ms")
c3.metric('Mean packet loss', f"{df['Packet_Loss_%'].mean():.2f}%")
c4.metric('Mean production speed', f"{df.Production_Speed_units_per_hr.mean():.1f} units/hr")

st.subheader('1. Network performance overview')
a,b = st.columns(2)
with a:
    fig=px.histogram(df,x='Network_Latency_ms',nbins=35,title='Latency distribution (ms)')
    st.plotly_chart(fig,use_container_width=True)
with b:
    fig=px.histogram(df,x='Packet_Loss_%',nbins=35,title='Packet-loss distribution (%)')
    st.plotly_chart(fig,use_container_width=True)
trend=df.groupby('Date',as_index=False).agg(Latency=('Network_Latency_ms','mean'),Packet_Loss=('Packet_Loss_%','mean'))
fig=px.line(trend,x='Date',y=['Latency','Packet_Loss'],title='Daily average network metrics')
st.plotly_chart(fig,use_container_width=True)

st.subheader('2. Network conditions vs efficiency')
a,b=st.columns(2)
with a:
    dist=df.groupby(['Efficiency_Status','Operation_Mode']).size().reset_index(name='Records')
    fig=px.bar(dist,x='Efficiency_Status',y='Records',color='Operation_Mode',barmode='group',title='Efficiency classes by operating mode')
    st.plotly_chart(fig,use_container_width=True)
with b:
    fig=px.scatter(df.sample(min(12000,len(df)),random_state=42),x='Network_Latency_ms',y='Production_Speed_units_per_hr',color='Efficiency_Status',opacity=.55,title='Latency vs production speed')
    st.plotly_chart(fig,use_container_width=True)

st.subheader('3. Quality and error diagnostics')
a,b=st.columns(2)
with a:
    fig=px.scatter(df.sample(min(12000,len(df)),random_state=42),x='Packet_Loss_%',y='Error_Rate_%',color='Efficiency_Status',opacity=.5,title='Packet loss vs error rate')
    st.plotly_chart(fig,use_container_width=True)
with b:
    fig=px.scatter(df.sample(min(12000,len(df)),random_state=42),x='Packet_Loss_%',y='Quality_Control_Defect_Rate_%',color='Operation_Mode',opacity=.5,title='Packet loss vs defect rate')
    st.plotly_chart(fig,use_container_width=True)

st.subheader('4. Network quality bands')
lat_edges=[-np.inf,10,20,30,40,np.inf]
loss_edges=[-np.inf,1,2,3,4,np.inf]
tab=df.copy()
tab['Latency band']=pd.cut(tab.Network_Latency_ms,lat_edges,labels=['≤10','10–20','20–30','30–40','>40'])
tab['Packet-loss band']=pd.cut(tab['Packet_Loss_%'],loss_edges,labels=['≤1','1–2','2–3','3–4','>4'])
summary=tab.groupby('Latency band',observed=False).agg(Records=('Efficiency_Status','size'),Mean_speed=('Production_Speed_units_per_hr','mean'),Mean_defect=('Quality_Control_Defect_Rate_%','mean'),Mean_error=('Error_Rate_%','mean'),High_share=('Efficiency_Status',lambda x:(x=='High').mean()*100)).reset_index()
st.dataframe(summary.round(3),use_container_width=True)

st.subheader('5. Operation-mode comparison')
mode= df.groupby('Operation_Mode').agg(Records=('Machine_ID','size'),Latency_ms=('Network_Latency_ms','mean'),Packet_loss_pct=('Packet_Loss_%','mean'),Speed=('Production_Speed_units_per_hr','mean'),Defect_rate=('Quality_Control_Defect_Rate_%','mean'),Error_rate=('Error_Rate_%','mean')).reset_index()
st.dataframe(mode.round(3),use_container_width=True)

st.subheader('6. Correlation diagnostics')
cols=['Network_Latency_ms','Packet_Loss_%','Production_Speed_units_per_hr','Quality_Control_Defect_Rate_%','Error_Rate_%','Temperature_C','Vibration_Hz','Predictive_Maintenance_Score']
corr=df[cols].corr(numeric_only=True)
fig=px.imshow(corr,text_auto='.2f',color_continuous_scale='RdBu_r',zmin=-1,zmax=1,title='Pearson correlation matrix')
st.plotly_chart(fig,use_container_width=True)

st.info('Interpretation guardrail: observational associations do not establish causality. The supplied dataset shows very weak marginal correlations between network metrics and production/quality outcomes. Treat any proposed thresholds as exploratory, not validated 6G service-level limits.')
st.download_button('Download filtered records as CSV',df.to_csv(index=False).encode('utf-8'),file_name='filtered_manufacturing_data.csv',mime='text/csv')
