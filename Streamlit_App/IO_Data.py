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
