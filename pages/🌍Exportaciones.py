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

df2 = conn.query('select name,value from info_expo_anio_variedad ;', ttl="0")
#st.write(df1)
json_list = json.loads(json.dumps(list(df2.T.to_dict().values()))) 
st.subheader('Exportaciones por Variedad')


option = {
    "tooltip": {
        #"trigger": 'axis',
        #"axisPointer": { "type": 'cross' },
        "formatter": JsCode(
            "function(info){var value=info.value;var treePathInfo=info.treePathInfo;var treePath=[];for(var i=1;i<treePathInfo.length;i+=1){treePath.push(treePathInfo[i].name)}return['<div class=\"tooltip-title\">'+treePath.join('/')+'</div>','Ventas Acumuladas: ' + value ].join('')};"
        ).js_code,
    },
    "legend": {"data": ["litros","variedad1"]},   
    "series": [
            {
                "name": "Ventas Totales",
                "type": "treemap",
                "visibleMin": 100,
                "label": {"show": True, "formatter": "{b}"},
                "itemStyle": {"borderColor": "#fff"},
                "levels": [
                    {"itemStyle": {"borderWidth": 0, "gapWidth": 5}},
                    {"itemStyle": {"gapWidth": 1}},
                    {
                        "colorSaturation": [0.35, 0.5],
                        "itemStyle": {"gapWidth": 1, "borderColorSaturation": 0.6},
                    },
                ],
                "data": json_list,
            }
    ]
}
st_echarts(
    options=option, height="600px",
)

