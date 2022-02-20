import streamlit as st
import pandas as pd

import requests

#%% Test requests
# url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=CHXRSA'
# r = requests.get(url)
# open('temp.csv', 'wb').write(r.content)
# df = pd.read_csv('temp.csv')
# st.write("fed csv")
# st.write(df)


csvID = st.secrets['csvID']
# csvID = st.secrets['sp500ID']

df =  download_file_from_google_drive(csvID)
st.title("Ontario Sunshine List Dashboard")
st.write("App in progress...")
st.write("App will load last 10 years of historical public list disclosure from https://www.ontario.ca/page/public-sector-salary-disclosure")
# path = 'https://drive.google.com/uc?export=download&id='+csvID
path = "https://drive.google.com/u/0/uc?id=1xoLBlQMp1V3XLfxz9eNzZg7t6UoHhuPQ&export=download&confirm=t"
# st.write(csvID)

@st.cache
def grab_csv():
    df = pd.read_csv(path)
    return df

df = grab_csv()
st.write(list(df.columns))
st.write(df.head(4))