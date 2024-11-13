import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts

pg = st.navigation([
    st.Page("pages/🌍Exportaciones.py", title="Exportaciones", icon="🌍"),
    st.Page("pages/Mercado📊Interno.py", title="Mercado Interno", icon="📊"),
    st.Page("pages/🍇Cosecha.py", title="Cosecha", icon="🍇"),
    st.Page("pages/🍷Mosto.py", title="Mosto", icon="🍷"),
    st.Page("pages/🍾Espumantes.py", title="Espumantes", icon="🍾"),
    st.Page("pages/🚜Superficie.py", title="Superficie", icon="🚜"),

])
pg.run()

conn = st.connection("postgresql", type="sql")
df = conn.query('select anio,litros,fob from inf_expo_anio ;', ttl="0")
#st.write(df)
 
st.subheader('Evolución Exportaciones de vimos por año')

if st.checkbox('Ver datos en forma de tabla'):
    st.write(df)


df['anio'] = df['anio'].astype(str)

newdf=df.set_index('anio',inplace=False).rename_axis(None)

option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df['anio'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df['litros'].to_list(), "type": "line", "name": 'Litros'}
               ,{"data": df['fob'].to_list(), "type": "line","name":'Fob'}]
}
st_echarts(
    options=option, height="400px",
)
