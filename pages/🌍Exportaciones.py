import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts

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
    options=option, height="400px" ,
)


df1 = conn.query('select periodo,litros,fob from info_expo_anio_mes ;', ttl="0")
#st.write(df1)
 
st.subheader('Evolución Exportaciones de vimos por Mes')

if st.checkbox('Ver datos en  tabla'):
    st.write(df1)



df1['periodo'] = df1['periodo'].astype(str)

newdf1=df1.set_index('periodo',inplace=False).rename_axis(None)

option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df1['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df1['litros'].to_list(), "type": "line", "name": 'Litros'}
               ,{"data": df1['fob'].to_list(), "type": "line","name":'Fob'}]
}
st_echarts(
    options=option, height="400px" ,
)

df2 = conn.query('select variedad1,litros,fob from info_expo_anio_variedad ;', ttl="0")
#st.write(df1)
json_list = json.loads(json.dumps(list(df2.T.to_dict().values()))) 
st.subheader('Exportaciones por Variedad')


option = {
        "title": {
            "text": "WORLD COFFEE RESEARCH SENSORY LEXICON",
            "subtext": "Source: https://worldcoffeeresearch.org/work/sensory-lexicon/",
            "textStyle": {"fontSize": 14, "align": "center"},
            "subtextStyle": {"align": "center"},
            "sublink": "https://worldcoffeeresearch.org/work/sensory-lexicon/",
        },
        "series": {
            "type": "sunburst",
            "data": json_list,
            "radius": [0, "95%"],
            "sort": None,
            "emphasis": {"focus": "ancestor"},
            "levels": [
                {},
                {
                    "r0": "15%",
                    "r": "35%",
                    "itemStyle": {"borderWidth": 2},
                    "label": {"rotate": "tangential"},
                },
                {"r0": "35%", "r": "70%", "label": {"align": "right"}},
                {
                    "r0": "70%",
                    "r": "72%",
                    "label": {"position": "outside", "padding": 3, "silent": False},
                    "itemStyle": {"borderWidth": 3},
                },
            ],
        },
    }
st_echarts(option, height="700px")

