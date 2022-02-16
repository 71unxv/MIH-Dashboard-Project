import requests
import json
import pandas as pd


def getActivityData(wid, start_dt, end_dt):
    Data_params ={
        "wid" : int(wid),
        "start" : start_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "end" : end_dt.strftime("%Y-%m-%d %H:%M:%S")
    }
    # now.strftime("%Y-%m-%d, %H:%M:%S")
    print(Data_params)
    column_list = ["dt", "date", "time", "bitdepth", "md", "blockpos", "rop", "hklda", "woba", "torqa", "rpm", "stppress", "mudflowin",]
    # return None
    WellData = (
        (
            requests.get("https://pdumitradome.id/dome_api/rtdc/get_data", data=json.dumps(Data_params))
        ).text
    )

    Data_DF = pd.json_normalize(json.loads(WellData), record_path='result')
    # print(Data_DF.head(5))
    return Data_DF[column_list]



def get_session_id():
    # Hack to get the session object from Streamlit.

    ctx = ReportThread.get_report_ctx()

    this_session = None
    
    current_server = Server.get_current()
    if hasattr(current_server, '_session_infos'):
        # Streamlit < 0.56        
        session_infos = Server.get_current()._session_infos.values()
    else:
        session_infos = Server.get_current()._session_info_by_id.values()

    for session_info in session_infos:
        s = session_info.session
        if (
            # Streamlit < 0.54.0
            (hasattr(s, '_main_dg') and s._main_dg == ctx.main_dg)
            or
            # Streamlit >= 0.54.0
            (not hasattr(s, '_main_dg') and s.enqueue == ctx.enqueue)
        ):
            this_session = s

    if this_session is None:
        raise RuntimeError(
            "Oh noes. Couldn't get your Streamlit Session object"
            'Are you doing something fancy with threads?')

    return id(this_session)