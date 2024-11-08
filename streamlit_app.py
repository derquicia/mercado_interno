import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts


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



with st.echo("below"):
     b = (
        Bar()
        .add_xaxis(["Microsoft", "Amazon", "IBM", "Oracle", "Google", "Alibaba"])
        .add_yaxis(
            "2017-2018 Revenue in (billion $)", [21.2, 20.4, 10.3, 6.08, 4, 2.2]
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Top cloud providers 2018", subtitle="2017-2018 Revenue"
            ),
            toolbox_opts=opts.ToolboxOpts(),
        )
    )
st_pyecharts(b)


conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT año,sum(sup) FROM superficie_m group by año;', ttl="0")
#st.write(df)
st.bar_chart(df)


conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT periodo,"CERVEZAS","VINOS_COMUNES","VINOS_FINOS" FROM scentia_res;', ttl="0")
#st.write(df)

st.subheader('Ventas en el Canal Mayorista')

if st.checkbox('Ver datos en forma de tabla'):
    st.write(df)

st.line_chart(df,x="periodo",y=["CERVEZAS","VINOS_COMUNES","VINOS_FINOS"])

#st.dataframe(df)

df['periodo'] = df['periodo'].astype(str)

newdf=df.set_index('periodo',inplace=False).rename_axis(None)
#st.table(newdf)
#st.table(df)

st.write(json.dumps(df['periodo'].to_list()))
st.write(json.dumps(df['VINOS_COMUNES'].tolist()))

bar_options = {
    "xAxis": {
         "type":'value',

        "axisTick": {"alignWithLabel": True},
        "series":[{"data":json.dumps(df['periodo'].to_list()),"type":'bar'}]
    },
    "yAxis": {
        "type":'value',
        "data":json.dumps(df['VINOS_COMUNES'].tolist())
        #"axisLabel": {formatter: "{MMM} {yyyy}" },
        #"series": [{"data":json.dumps(df['periodo'].to_list()),"type": 'bar'}],
    }
}
st_echarts(options=bar_options)



option = {
    "xAxis": {
        "type": "category",
        "data": df['periodo'].to_list(),
    },
    "yAxis": {"type": "value"},
    "series": [{"data": df['VINOS_COMUNES'].to_list(), "type": "line"}],
    "series": [{"data": df['VINOS_FINOS'].to_list(), "type": "line"}],
}
st_echarts(
    options=option, height="400px",
)



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


