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
df = conn.query('SELECT periodo,"CERVEZAS","VINOS_COMUNES","VINOS_FINOS","APERITIVOS_ALC","APERITIVOS_RTD","ESPUMANTES","FRIZANTES" FROM scentia_res;', ttl="0")
#st.write(df)

st.subheader('Ventas en el Canal Mayorista, Según datos de Scentia')

if st.checkbox('Ver datos en forma de tabla'):
    st.write(df)

#st.line_chart(df,x="periodo",y=["CERVEZAS","VINOS_COMUNES","VINOS_FINOS"])

#st.dataframe(df)

df['periodo'] = df['periodo'].astype(str)

newdf=df.set_index('periodo',inplace=False).rename_axis(None)
#st.table(newdf)
#st.table(df)

#st.write(json.dumps(df['periodo'].to_list()))
#st.write(json.dumps(df['VINOS_COMUNES'].tolist()))



option = {
    "tooltip": {
        "trigger": 'axis',
        "axisPointer": { "type": 'cross' }
    },
    "legend": {},    
    "xAxis": {
        "type": "category",
        "data": df['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df['VINOS_COMUNES'].to_list(), "type": "line", "name": 'Vinos Comunes'}
               ,{"data": df['VINOS_FINOS'].to_list(), "type": "line","name":'Vinos Finos'}
               ,{"data": df['CERVEZAS'].to_list(), "type": "line","name":'Cervezas'} ],
#    "series": [{"data": df['VINOS_FINOS'].to_list(), "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)




