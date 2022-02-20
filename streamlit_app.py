import streamlit as st
import pandas as pd

import requests

#%% Test requests
url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=CHXRSA'
r = requests.get(url)
open('temp.csv', 'wb').write(r.content)
df = pd.read_csv('temp.csv')
st.write("fed csv")
st.write(df)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination) 


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