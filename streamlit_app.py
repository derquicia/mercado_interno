import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode



options = {
    "xAxis": {
        "type": "category",
        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    "yAxis": {"type": "value"},
    "series": [
        {"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}
    ],
}
st_echarts(options=options, renderer="svg")



   options = {
            "backgroundColor": "#404a59",
            "title": {
                "text": "全国主要城市空气质量",
                "subtext": "data from PM25.in",
                "sublink": "http://www.pm25.in",
                "left": "center",
                "textStyle": {"color": "#fff"},
            },
            "tooltip": {"trigger": "item"},
            "legend": {
                "orient": "vertical",
                "top": "bottom",
                "left": "right",
                "data": ["pm2.5"],
                "textStyle": {"color": "#fff"},
            },
            "visualMap": {
                "min": 0,
                "max": 300,
                "splitNumber": 5,
                "color": ["#d94e5d", "#eac736", "#50a3ba"],
                "textStyle": {"color": "#fff"},
            },
            "geo": {
                "map": "china",
                "label": {"emphasis": {"show": False}},
                "itemStyle": {
                    "normal": {"areaColor": "#323c48", "borderColor": "#111"},
                    "emphasis": {"areaColor": "#2a333d"},
                },
            },
        }
   st_echarts(options)



conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT año,sum(sup) FROM superficie_m group by año;', ttl="0")
#st.write(df)
st.bar_chart(df)

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT periodo,"CERVEZAS","VINOS_COMUNES","VINOS_FINOS" FROM scentia_res;', ttl="0")
st.write(df)

st.subheader('Ventas en el Canal Mayorista')

if st.checkbox('Ver datos en forma de tabla'):
    st.write(df)

st.line_chart(df,x="periodo",y=["CERVEZAS","VINOS_COMUNES","VINOS_FINOS"])



DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)


