import streamlit as st
import pandas as pd
import requests
import re

st.set_page_config(layout="wide",page_title='Ontario Sunshine List')
csvID = st.secrets['csvID']

st.title("Ontario Sunshine List Dashboard")

if st.checkbox("Intersting finds"):
    finds = """
    - Search for YELLE-WEATHERALL as last name, looks like there was a typo in 2006, should be $127,455 not $12,745,500
    - Search for HARRIS STEPHEN (last, first), looks like there was a typo in 2006, should be $128k not 12.8mm 
    
    """
    st.write(finds)

st.write("App in progress...")
st.write("App will load last 10 years of historical public list disclosure from https://www.ontario.ca/page/public-sector-salary-disclosure")
# path = 'https://drive.google.com/uc?export=download&id='+csvID
path = "https://drive.google.com/u/0/uc?id={}&export=download&confirm=t".format(csvID)

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

pickEmployer = st.sidebar.multiselect("Pick employers to filter", allEmployers,'York University')
pickYear = st.sidebar.multiselect("Pick a year to filter", allYears)
pickSector = st.sidebar.multiselect("Pick a sector to filter", allSectors)
pickJob = st.sidebar.multiselect("Pick a job title to filter", allJobs)

st.header("Entire Data Set")
col1, col2, col3, col4 = st.columns(4)
output = "${:,.0f}"
with col1:
    st.metric("Min Salary",output.format(minSalary))
with col2:
    st.metric("Avg Salary",output.format(avgSalary))
with col3:
    st.metric("Max Salary",output.format(maxSalary))
with col4:
    st.metric("Salary Stand Deviation",output.format(stdSalary))
st.write("Summary stats")
st.write(df.describe())
# pickSalary = st.sidebar.slider('Pick salary range',minSalary, maxSalary, (avgSalary-stdSalary,avgSalary+stdSalary))
# pickSalary = st.sidebar.slider('Pick salary range',100000.0, 2000000.0, (120000.0,200000.0))
lastName = st.sidebar.text_input("Last name search")
firstName = st.sidebar.text_input("First name search")
filterMap = {'Employer':pickEmployer,
            'Calendar Year':pickYear,
            'Sector':pickSector,
            'Job Title':pickJob}

for colName, filterVals in filterMap.items():
    if len(filterVals)>0: 
        filterDF = filterDF[filterDF[colName].str.strip().str.lower().isin([x.lower() for x in filterVals])]

filterDF = filterDF[filterDF['Last Name'].str.contains(lastName, flags=re.IGNORECASE, regex=True) & filterDF['First Name'].str.contains(firstName, flags=re.IGNORECASE, regex=True)]

minSalaryPick = st.sidebar.number_input("Min salary", value=100000.0)
maxSalaryPick = st.sidebar.number_input("Max salary", value=maxSalary)

filterDF = filterDF[filterDF['Salary Paid'].between(minSalaryPick, maxSalaryPick)]
st.header("Filtered Data Set")
colf1, colf2, colf3, colf4 = st.columns(4)
minFSalary = filterDF['Salary Paid'].min()
maxFSalary = filterDF['Salary Paid'].max()
stdFSalary = filterDF['Salary Paid'].std()
avgFSalary = filterDF['Salary Paid'].mean()

output = "${:,.0f}"
with colf1:
    st.metric("Min Salary",output.format(minFSalary))
with colf2:
    st.metric("Avg Salary",output.format(avgFSalary))
with colf3:
    st.metric("Max Salary",output.format(maxFSalary))
with colf4:
    st.metric("Salary Stand Deviation",output.format(stdFSalary))

st.write(filterDF.shape)
st.write(filterDF.head(300))
st.write("Summary stats")
st.write(filterDF.describe())
    