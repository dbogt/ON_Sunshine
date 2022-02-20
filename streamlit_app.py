import streamlit as st
import pandas as pd

st.title("Ontario Sunshine List Dashboard")
st.write("App in progress...")
st.write("App will load last 10 years of historical public list disclosure from https://www.ontario.ca/page/public-sector-salary-disclosure")
csvID = st.secrets['csvID']
# csvID = st.secrets['sp500ID']
path = 'https://drive.google.com/uc?export=download&id='+csvID
# st.write(csvID)

@st.cache
def grab_csv():
    df = pd.read_csv(path)
    return df

df = grab_csv()
st.write(list(df.columns))
st.write(df.head(4))