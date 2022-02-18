import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import LogsDisp
import AppPage
import Activity
import IO_Data
import time
# import datetime
import numpy as np

import requests
import json
from datetime import datetime, timedelta


st.set_page_config(page_title="Realtime Activity Mapping", page_icon=None, layout="wide",)

st.sidebar.image('PDU_Logo.jpg')
# @st.experimental_memo
# @st.cache(allow_output_mutation=True)
def GenerateInputActivity_DB(flag=False):
    if flag:
        InputActivity_DB = pd.read_csv('RealTime_Test/AAE-08_TEST_EDIT.csv', index_col = False)
    else:
        InputActivity_DB = pd.DataFrame(
            columns=[
                'dt',
                'Date',
                'Time',
                "Activity",
                "Hook Treshold",
                "Remarks",
                "PIC"
                ]
            )

    return InputActivity_DB


@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

@st.cache(allow_output_mutation=True)
def cache_RealTime_Data(well_id, StartDateTime_select, EndDateTime_select):
    Activity_DF = IO_Data.getActivityData(well_id, StartDateTime_select, EndDateTime_select)
    Activity_DF['dt'] = Activity_DF['dt'].astype('datetime64')
    Activity_DF['bitdepth'] = Activity_DF['bitdepth'].astype('float64')
    Activity_DF['blockpos'] = Activity_DF['blockpos'].astype('float64')
    Activity_DF['rop'] = Activity_DF['rop'].astype('float64')
    Activity_DF['hklda'] = Activity_DF['hklda'].astype('float64')
    Activity_DF['woba'] = Activity_DF['woba'].astype('float64')
    Activity_DF['torqa'] = Activity_DF['torqa'].astype('float64')
    Activity_DF['rpm'] = Activity_DF['rpm'].astype('float64')
    Activity_DF['stppress'] = Activity_DF['stppress'].astype('float64')
    Activity_DF['mudflowin'] = Activity_DF['mudflowin'].astype('float64')

    return Activity_DF



# InputActivity_DB = GenerateInputActivity_DB()
InputActivity_DB = pd.read_csv('RealTime_Test/Temp_InputActivity.csv', index_col = False)
print(InputActivity_DB)
CompName_JSON = requests.get(
        "https://pdumitradome.id/dome_api/rtdc/get_company/"
    ).json()
CompName_DF = pd.json_normalize(CompName_JSON, record_path = 'result')

CompName_Select = st.sidebar.selectbox("Select Company:",["-"] + CompName_DF['company_name'].to_list())

if CompName_Select == "-":
    WellList =["-"]
    Datetime_min = ['-']
    Datetime_max = ['-']
else:
    # print(CompName_DF.loc[CompName_DF['company_name']==CompName_Select, 'cid'].values)
    getWellAPI = "https://pdumitradome.id/dome_api/rtdc/get_well?cid=" + (CompName_DF.loc[CompName_DF['company_name']==CompName_Select, 'cid'].values)

    WellName_JSON = requests.get(
            getWellAPI[0]
        ).json()

    WellName_DF = pd.json_normalize(WellName_JSON, record_path = 'result')
    WellName_DF['active_date'] = WellName_DF['active_date'].astype('datetime64').dt.date
    WellName_DF['end_date'] = WellName_DF['end_date'].astype('datetime64').dt.date

    WellList = WellName_DF['well_name'].to_list()

WellName_Select = st.sidebar.selectbox("Select Well",WellList)

# twoday_dt_temp = 
try:
    Datetime_start = (WellName_DF.loc[WellName_DF['well_name']==WellName_Select, 'active_date']).to_list()[0]
    Datetime_end = (WellName_DF.loc[WellName_DF['well_name']==WellName_Select, 'end_date']).to_list()[0]
    well_id = (WellName_DF.loc[WellName_DF['well_name']==WellName_Select, 'wid'])
    print(well_id)

    print(Datetime_start)
    print(Datetime_end)
    st.sidebar.table(WellName_DF.loc[WellName_DF['well_name']==WellName_Select, ['active_date', 'end_date']])
    if Datetime_end > datetime.now().date():
        Datetime_end = datetime.now().date()
except Exception as error_msg:
    Datetime_start = datetime.now().date()
    Datetime_end = datetime.now().date()

    print(error_msg)
    # None

PageList = [
    "Activity Mapping",
    "Summary Dashboard",
]
NavBar = st.sidebar.selectbox("Select Module:",PageList)


with st.sidebar.form(key="Input Date-Time"):

    sideStart_col1,sideStart_col2 = st.sidebar.columns(2)
    
    StartDate = sideStart_col1.date_input('Start Date-Time',value=(Datetime_end - timedelta(days=2)), key='StartDate')
    StartTime = sideStart_col2.time_input('',value=datetime.strptime('00:00:00', '%H:%M:%S'), key='StartTime')


    sideEnd_col1,sideEnd_col2 = st.sidebar.columns(2)
    

    EndDate = sideEnd_col1.date_input('End Date-Time',value=Datetime_end, key='EndDate')
    EndTime = sideEnd_col2.time_input('',value=datetime.strptime('00:00:00', '%H:%M:%S'), key='EndTime')

    print(StartDate)
    print(StartTime)
    print(EndDate)
    print(EndTime)

    StartDateTime_select = datetime.combine(StartDate, StartTime)
    EndDateTime_select = datetime.combine(EndDate, EndTime)
    

    # submit_a = 
FormButton_a = st.sidebar.button('load Realtime Data')
if FormButton_a:
    with st.spinner(text="retreive from DOME In progress..."):
        Activity_DF = cache_RealTime_Data(well_id, StartDateTime_select, EndDateTime_select)

## LOAD DATA
# if (CompName_Select != '-'):
# if st.sidebar.button('load Realtime Data', key='Load Well'):
    









if NavBar == "Activity Mapping" and (CompName_Select != '-') and FormButton_a:
    
    st.title("Activity Mapping")
    if st.button('Clear LastRow', key='refresh'):

        InputActivity_DB = InputActivity_DB[:-1]
        InputActivity_DB.to_csv('RealTime_Test/Temp_InputActivity.csv', index = False)
    if st.button('LOAD AAE-08', key='AAE08'):

        # InputActivity_DB = InputActivity_DB[:-1]
        # InputActivity_DB.to_csv('RealTime_Test/Temp_InputActivity.csv', index = False)
        InputActivity_DB = GenerateInputActivity_DB(flag=True)
        InputActivity_DB.to_csv('RealTime_Test/Temp_InputActivity.csv', index = False)
    if st.button('clear AAE-08', key='AAE08'):

        InputActivity_DB = InputActivity_DB[1:1]
        # InputActivity_DB.to_csv('RealTime_Test/Temp_InputActivity.csv', index = False)
        # InputActivity_DB = GenerateInputActivity_DB(flag=True)
        InputActivity_DB.to_csv('RealTime_Test/Temp_InputActivity.csv', index = False)



    with st.form(key='Activity Input:'):
        cols = st.columns(6)
        Date_Temp = cols[0].date_input(
                    "Date", value= Datetime_end, key='InputDate'
                    )
        Time_Temp = cols[1].time_input(
                    "Time",  key='InputTime'
                    )

        
        Activity_Temp = cols[2].selectbox(
                    "Activity",
                    ["N/A",
                         'CEMENTING JOB',
                            'CIRCULATE HOLE CLEANING',
                            'CONNECTION',
                            'DRILL OUT CEMENT',
                            'DRILLING FORMATION',
                            'LAY DOWN BHA',
                            'MAKE UP BHA',
                            'NPT',
                            'N/D BOP',
                            'N/U BOP',
                            'OTHER',
                            'RUNNING CASING IN',
                            'STATIONARY',
                            'STUCK PIPE',
                            'TRIP IN',
                            'TRIP OUT',
                            'WAIT ON CEMENT',
                            'CIRCULATION',
                            'RIG REPAIR',
                            'WIPER TRIP'
                    ],
                    key='Activity'
                    )
        
        HookTreshold_Temp = cols[3].number_input(
                    "HookTreshold",
                    
                    key="HookTreshold"
                    )
        Remarks_Temp = cols[4].text_input(label='Additional Remarks',
                    key="Remarks"
                    )
        PIC_Temp = cols[5].text_input(label='PIC',
                    key="PIC"
                    )

        submitted = st.form_submit_button('Submit')
        # print(submitted)
        
        if submitted:

            # print(InputActivity_DB)
            InputActivity_DB.loc[len(InputActivity_DB.index)] = [
                (datetime.combine(Date_Temp, Time_Temp)),
                str(Date_Temp),
                str(Time_Temp),
                Activity_Temp,
                HookTreshold_Temp,
                Remarks_Temp,
                PIC_Temp
            ]
            InputActivity_DB.to_csv('RealTime_Test/Temp_InputActivity.csv', index = False)
            # print([
            #     Date_Temp,
            #     Time_Temp,
            #     Connection_Temp,
            #     # SubActivity_Temp,
            #     Activity_Temp,
            #     HookTreshold_Temp,
            #     Remarks_Temp,
            #     PIC_Temp
            # ])
            # print(len(InputActivity_DB)) 
            # st.write('Why hello there')



###### Perhitungan summary
        if FormButton_a:
            with st.spinner(text="Generate Activity Summary..."):
                Activity_DF = Activity.GetActivity_DF(Activity_DF, InputActivity_DB)
                Activity_DF = Activity.GetSubActivity_DF(Activity_DF)
            
                SummaryActivity_DF = Activity.GenerateDuration_DF_v2(Activity_DF)

                with st.container():

                    InputActivity_DB = pd.read_csv('RealTime_Test/Temp_InputActivity.csv', index_col = False)
                    
                    Table_col = st.columns(1)
                    Table_col[0].markdown('### Activity Log')
                    Table = Table_col[0].dataframe(InputActivity_DB)
                    Table_col[0].markdown('### Activity Summary Table')
                    Table_2 = Table_col[0].dataframe(SummaryActivity_DF)
        

        # st.table(Activity_DF.head(20))

        # csv = convert_df(my_large_df)
    if FormButton_a:
        st.download_button(
            label="Download Summary data as CSV",
            data=convert_df(SummaryActivity_DF),
            file_name='large_df.csv',
            mime='text/csv',
        )
        st.download_button(
            label="Download Realtime(5second) data as CSV",
            data=convert_df(Activity_DF),
            file_name='large_df.csv',
            mime='text/csv',
        )
    # st.table(SummaryActivity_DF)



else:
    st.markdown("<h1 style='text-align: center; font-size: 130px;margin-top: 300px;'>  Welcome !</h1>", unsafe_allow_html=True)
