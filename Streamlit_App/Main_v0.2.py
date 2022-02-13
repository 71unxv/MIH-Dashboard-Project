import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import LogsDisp
import AppPage
import Activity
import time
import datetime
import numpy as np

import requests
import json



st.set_page_config(page_title="Realtime Activity Mapping", page_icon=None, layout="wide",)

st.sidebar.image('PDU_Logo.jpg')
@st.cache(persist=True, allow_output_mutation=True)
def GenerateInputActivity_DB():
    InputActivity_DB = pd.DataFrame(
        columns=[
            'Date',
            'Time',
            # 'ConnectionActivity',
            # 'SubActivity',
            "Activity",
            "Hook Treshold",
            "Remarks",
            "PIC"
            ]
        )
    return InputActivity_DB

InputActivity_DB = GenerateInputActivity_DB()

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
    print(CompName_DF.loc[CompName_DF['company_name']==CompName_Select, 'cid'].values)
    getWellAPI = "https://pdumitradome.id/dome_api/rtdc/get_well?cid=" + (CompName_DF.loc[CompName_DF['company_name']==CompName_Select, 'cid'].values)

    WellName_JSON = requests.get(
            getWellAPI[0]
        ).json()

    WellName_DF = pd.json_normalize(WellName_JSON, record_path = 'result')

    WellList = WellName_DF['well_name'].to_list()

WellName_Select = st.sidebar.selectbox("Select Well",WellList)

PageList = [
    "Activity Mapping",
    "Summary Dashboard",
]
NavBar = st.sidebar.selectbox("Select Module:",PageList)

with st.sidebar.form(key="Start Date-Time"):
    # st.sidebar.markdown('###### Start Date-Time')
    sideStart_col1,sideStart_col2 = st.sidebar.columns(2)
    
    StartDate = sideStart_col1.date_input('Start Date-Time', key='StartDate')
    StartTime = sideStart_col2.time_input('', key='StartTime')
    #     # st.text("a")
    # with side_col2:
    #     st.text("b")
# with st.sidebar.form(key="End Date-Time"):
    # st.sidebar.markdown('###### End Date-Time')
    sideEnd_col1,sideEnd_col2 = st.sidebar.columns(2)
    
    EndDate = sideEnd_col1.date_input('End Date-Time', key='EndDate')
    EndTime = sideEnd_col2.time_input('', key='EndTime')




if NavBar == "Activity Mapping" and (CompName_Select != '-') :
    
    st.title("Activity Mapping")
    with st.form(key='Activity Input:'):
        cols = st.columns(6)
        Date_Temp = cols[0].date_input(
                    "Date",
                    )
        Time_Temp = cols[1].time_input(
                    "Time",
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
                            'OTHER',
                            'RUNNING CASING IN',
                            'STATIONARY',
                            'STUCK PIPE',
                            'TRIP IN',
                            'TRIP OUT',
                            'WAIT ON CEMENT',
                            'CIRCULATION',
                            'RIG REPAIR'
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
        print(submitted)
        
        if submitted:
            InputActivity_DB.loc[len(InputActivity_DB.index)] = [
                str(Date_Temp),
                str(Time_Temp),
                # Connection_Temp,
                # SubActivity_Temp,
                Activity_Temp,
                HookTreshold_Temp,
                Remarks_Temp,
                PIC_Temp
            ]

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
        with st.container():
            
            Table_col = st.columns(1)
            Table_col[0].markdown('### Activity Log')
            Table = Table_col[0].dataframe(InputActivity_DB)

            Table_col[0].markdown('### Activity Summary Table')
            Table_2 = Table_col[0].write(InputActivity_DB)

else:
    st.markdown("<h1 style='text-align: center; font-size: 130px;margin-top: 300px;'>  Welcome !</h1>", unsafe_allow_html=True)
