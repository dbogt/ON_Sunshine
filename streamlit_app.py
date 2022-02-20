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

# df =  download_file_from_google_drive(csvID)
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
st.sidebar.write(list(df.columns))

allEmployers = sorted(df['Employer'].unique())
allYears = sorted(df['Calendar Year'].unique())
allSectors = sorted(df['Sector'].unique())
allJobs = df['Job Title'].unique()
minSalary = df['Salary Paid'].min()
maxSalary = df['Salary Paid'].max()
stdSalary = df['Salary Paid'].std()
avgSalary = df['Salary Paid'].mean()


filterDF = df.copy()

pickEmployer = st.sidebar.multiselect("Pick employers to filter", allEmployers)
pickYear = st.sidebar.multiselect("Pick a year to filter", allYears)
pickSector = st.sidebar.multiselect("Pick a sector to filter", allSectors)
pickJob = st.sidebar.multiselect("Pick a job title to filter", allJobs)
st.write(minSalary, maxSalary, stdSalary, avgSalary)
# pickSalary = st.sidebar.slider('Pick salary range',minSalary, maxSalary, (avgSalary-stdSalary,avgSalary+stdSalary))
pickSalary = st.sidebar.slider('Pick salary range',100000.0, 2000000.0, (120000.0,200000.0))

filterMap = {'Employer':pickEmployer,
            'Calendar Year':pickYear,
            'Sector':pickSector,
            'Job Title':pickJob}

for colName, filterVals in filterMap.items():
    if len(filterVals)>0: 
        filterDF = filterDF[filterDF[colName].isin(filterVals)]

st.write(filterDF.shape)
st.write(filterDF.head(30))
st.write(filterDF.describe())
    