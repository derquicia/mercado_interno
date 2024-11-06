import streamlit as st
import pandas as pd
import numpy as np

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT año,sum(sup) FROM superficie_m group by año;', ttl="0")
# st.write(df)
st.bar_chart(df)

