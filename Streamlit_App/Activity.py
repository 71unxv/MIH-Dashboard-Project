import pandas as pd
import numpy as np

def GetTrippingActivity(isBitDepthMoving, hklda, rpm, mudflowing, Hookload):

    if((isBitDepthMoving and hklda>Hookload and rpm==0 and mudflowing>10)):
        SubActivity_Label = "Wash Up/Down"
    elif((isBitDepthMoving and hklda>Hookload and rpm>10 and stppress>100 and mudflowing>10)):
        SubActivity_Label = "Reaming"
    elif((isBitDepthMoving and hklda>Hookload and rpm<10 and stppress<100 and mudflowing<50)):
        SubActivity_Label = "Moving"
    elif((isBitDepthMoving and hklda>Hookload and mudflowing>10)):
        SubActivity_Label = "Circulation"
    elif((mudflowing<10 and rpm<10 and hklda<Hookload)):
        SubActivity_Label = "Connection"
    elif((isBitDepthMoving and mudflowing<10 and rpm<10 and hklda>Hookload)):
        SubActivity_Label = "Stationary"
    else:
        SubActivity_Label = "Check"

def GetTrippingActivity_DF(Activity_DF, Hookload):
    Activity_DF['isBitDepthMoving'] = Activity_DF['bitdepth'].shift(periods=1) == Activity_DF['bitdepth']

    Activity_DF["LABEL_SubActivity"] = "Check"
    idx_logic = ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Hookload) & (Activity_DF['rpm']==0) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Wash Up/Down"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label
    
    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Hookload) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Reaming"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Hookload) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']<100) & (Activity_DF['mudflowin']<50))
    SubActivity_Label = "Moving"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Hookload) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Circulation"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['mudflowin']<10) & (Activity_DF['rpm']<10) & (Activity_DF['hklda']<Hookload))
    SubActivity_Label = "Connection"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['mudflowin']<10) & (Activity_DF['rpm']<Hookload) & (Activity_DF['hklda']<Hookload))
    SubActivity_Label = "Stationary"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    return Activity_DF["LABEL_SubActivity"]

def GetDrillingActivity(woba,rpm,stppress,hklda,ConnectionWeight):
    if(woba>0 and rpm>10 and stppress>100 and hklda>ConnectionWeight):
        SubActivity_Label = "Rotary Drilling"
    elif(woba>0 and rpm<10 and stppress>100 and hklda>ConnectionWeight):
        SubActivity_Label = "Slide Drilling"
    elif(woba==0 and rpm>10 and stppress>100 and hklda>ConnectionWeight):
        SubActivity_Label = "Reaming"
    elif(woba==0 and rpm==0 and stppress>100 and hklda>ConnectionWeight):
        SubActivity_Label = "Wash Up/Down"
    # elif(woba=0 and rpm=0 and stppress<50)elif(hklda<ConnectionWeight and "Connection" and "Look and define"))))))
    elif(woba==0 and rpm==0 and stppress<50):
        if(hklda<ConnectionWeight):
            SubActivity_Label = "Connection"
        else:
            SubActivity_Label="Look and define"
    else:
        SubActivity_Label = "FALSE"
    return SubActivity_Label

def GetDrillingActivity_DF(Activity_DF,ConnectionWeight):
    # v3

    Activity_DF["LABEL_SubActivity"] = "FALSE"

    idx_logic = ((Activity_DF['woba']>0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
    SubActivity_Label = "Rotary Drilling"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['woba']>0) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
    SubActivity_Label = "Slide Drilling"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label
    
    idx_logic = ~idx_logic & ((Activity_DF['woba']==0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
    SubActivity_Label = "Reaming"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
    SubActivity_Label = "Wash Up/Down"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label


    idx_logic = ~idx_logic & ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']<50))
    SubActivity_Label="Look and define"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = (idx_logic & (Activity_DF['hklda']>ConnectionWeight))
    SubActivity_Label = "Connection"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label
    

    # v2
    
        # Activity_DF["LABEL_SubActivity"] = "FALSE"

        # idx_logic = ((Activity_DF['woba']>0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
        # SubActivity_Label = "Rotary Drilling"
        # Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

        # idx_logic = ((Activity_DF['woba']>0) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
        # SubActivity_Label = "Slide Drilling"
        # Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label
        
        # idx_logic = ((Activity_DF['woba']==0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
        # SubActivity_Label = "Reaming"
        # Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

        # idx_logic = ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
        # SubActivity_Label = "Wash Up/Down"
        # Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label


        # idx_logic = ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']<50))
        # SubActivity_Label="Look and define"
        # Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

        # idx_logic = (idx_logic & (Activity_DF['hklda']>ConnectionWeight))
        # SubActivity_Label = "Connection"
        # Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label
    # def GetDrillingActivity_DF(ConnectionWeight,Activity_DF):
    #     v1
    #     Activity_DF["LABEL_SubActivity"] = "Look and define"

    #     idx_logic = ((Activity_DF['woba']>0) & (Activity_DF['rpm']>10)) & ((Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
    #     Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = "Rotary Drilling"

    #     idx_logic = (Activity_DF['woba']>0) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight)
    #     Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = "Slide Drilling"

    #     idx_logic = (Activity_DF['woba']==0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight)
    #     Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = "Reaming"

    #     idx_logic = (Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight)
    #     Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = "Wash Up/Down"

    #     idx_logic = (Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']<50) & (Activity_DF['hklda']<ConnectionWeight)
    #     Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = "Connection"


    #     return Activity_DF

    return Activity_DF["LABEL_SubActivity"]

def GetSubActivity_DF(Activity_DF, Hookload_Treshold):
    
    Activity_DF["LABEL_SubActivity"] = "FALSE/Check"
    Activity_DF['isBitDepthMoving'] = Activity_DF['bitdepth'].shift(periods=1) == Activity_DF['bitdepth']

    idx_logic = Activity_DF["LABEL_MajorActivity"] == "Drilling"
    idx_logic = ~idx_logic & ((Activity_DF['woba']>0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Hookload_Treshold))
    SubActivity_Label = "Rotary Drilling"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['woba']>0) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Hookload_Treshold))
    SubActivity_Label = "Slide Drilling"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label
    
    idx_logic = ~idx_logic & ((Activity_DF['woba']==0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Hookload_Treshold))
    SubActivity_Label = "Reaming"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Hookload_Treshold))
    SubActivity_Label = "Wash Up/Down"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label


    idx_logic = ~idx_logic & ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']<50))
    SubActivity_Label="Look and define"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = (idx_logic & (Activity_DF['hklda']>Hookload_Treshold))
    SubActivity_Label = "Connection"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label


    # ############################
    idx_logic = Activity_DF["LABEL_MajorActivity"] == "Tripping"

    # Activity_DF["LABEL_SubActivity"] = "Check"
    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Hookload_Treshold) & (Activity_DF['rpm']==0) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Wash Up/Down"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label
    
    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Hookload_Treshold) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Reaming"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Hookload_Treshold) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']<100) & (Activity_DF['mudflowin']<50))
    SubActivity_Label = "Moving"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Hookload_Treshold) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Circulation"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['mudflowin']<10) & (Activity_DF['rpm']<10) & (Activity_DF['hklda']<Hookload_Treshold))
    SubActivity_Label = "Connection"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['mudflowin']<10) & (Activity_DF['rpm']<10) & (Activity_DF['hklda']<Hookload_Treshold))
    SubActivity_Label = "Stationary"
    Activity_DF.loc[idx_logic, "LABEL_SubActivity"] = SubActivity_Label
    return Activity_DF['LABEL_SubActivity']

    
def GenerateDuration_DF(RealTime_DB):
    RealTime_DB['dt'] = pd.to_datetime(RealTime_DB['dt'])
    RealTime_DB["LABEL_All"] =RealTime_DB['LABEL_ConnectionActivity'].astype(str) + '--' +RealTime_DB['LABEL_SubActivity'].astype(str)+'--'+RealTime_DB['LABEL_Activity'].astype(str)+'--'+RealTime_DB['LABEL_MajorActivity'].astype(str)

    Duration_DB = pd.DataFrame(
        columns=[
            'date',
            'Time_start',
            'Time_end',
            'date_time',
            'Duration(minutes)',
            'Hole Depth(max)',
            'Bit Depth(mean)',
            "Meterage(m)(Drilling)",
            'RotateDrilling',
            'Slide Drilling',
            'ReamingTime',
            'ConnectionTime',
            'On Bottom Hours',
            'Stand Duration',
            "LABEL_ConnectionActivity", 'LABEL_SubActivity', "LABEL_Activity", "LABEL_MajorActivity", "LABEL_StandGroup"
            ]
        )

    for k,DF_Temp in RealTime_DB.groupby((RealTime_DB['LABEL_All'].shift() != RealTime_DB['LABEL_All']).cumsum()):

        if not(("Hole_Depth" in locals()) or ("Hole_Depth" in globals())):
            Hole_Depth = 0

        list_temp = []

        date = DF_Temp.head(1)['date'].values[0]
        Time_start = DF_Temp.head(1)['time'].values[0]
        Time_end = DF_Temp.tail(1)['time'].values[0]
        date_time = DF_Temp.head(1)['dt'].values[0]
        LABEL_ConnectionActivity = DF_Temp.head(1)['LABEL_ConnectionActivity'].values[0]
        LABEL_SubActivity = DF_Temp.head(1)['LABEL_SubActivity'].values[0]
        LABEL_Activity = DF_Temp.head(1)['LABEL_Activity'].values[0]
        LABEL_MajorActivity = DF_Temp.head(1)['LABEL_MajorActivity'].values[0]

        Duration = round(((DF_Temp['dt'].max()-DF_Temp['dt'].min()).total_seconds())/60,2)
        Hole_Depth_Temp = DF_Temp['md'].max()

        if Hole_Depth_Temp>= Hole_Depth:
            Hole_Depth = Hole_Depth_Temp
        

        Bit_Depth = DF_Temp['bitdepth'].mean()

        list_Out = [date, Time_start,Time_end, date_time, Duration, Hole_Depth, Bit_Depth, np.empty(1), np.empty(1), np.empty(1), np.empty(1), np.empty(1), np.empty(1), np.empty(1),LABEL_ConnectionActivity, LABEL_SubActivity, LABEL_Activity, LABEL_MajorActivity, np.nan]
        Duration_DB.loc[len(Duration_DB)] = list_Out

    Duration_DB = Duration_DB.astype(
        {
            'Duration(minutes)':'float32',
            'Hole Depth(max)':'float32',
            'Bit Depth(mean)':'float32',
            "Meterage(m)(Drilling)":'float32',
            'RotateDrilling':'float32',
            'Slide Drilling':'float32',
            'ReamingTime':'float32',
            'ConnectionTime':'float32',
            'On Bottom Hours':'float32',
            'Stand Duration':'float32',
            "LABEL_ConnectionActivity":'str', 'LABEL_SubActivity':'str', "LABEL_Activity":'str', "LABEL_MajorActivity":'str',"LABEL_StandGroup":'float'
        }
    )
    Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'ROTARY DRILLING', 'RotateDrilling'] = Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'ROTARY DRILLING', 'Duration(minutes)']
    Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'SLIDE DRILLING', 'Slide Drilling'] = Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'SLIDE DRILLING', 'Duration(minutes)']
    Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'REAMING', 'ReamingTime'] = Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'REAMING', 'Duration(minutes)']
    Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'CONNECTION', 'ConnectionTime'] = Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'CONNECTION', 'Duration(minutes)']

    DrillingOnlyDB = Duration_DB[Duration_DB["LABEL_MajorActivity"]=="Drilling"]
    start_idx = DrillingOnlyDB.index.values[0]
    StandNum_Temp = 1
    for i,row in DrillingOnlyDB[DrillingOnlyDB['LABEL_ConnectionActivity'].isin(['CONNECTION', "POST CONNECTION"])].iterrows():
        if row['LABEL_ConnectionActivity'] == 'CONNECTION':
            end_idx = i-1
            Duration_DB.loc[i, "Meterage(m)(Drilling)"] = Duration_DB.loc[start_idx:end_idx, "Meterage(m)(Drilling)"].fillna(0).sum()
            Duration_DB.loc[i, "On Bottom Hours"] = Duration_DB.loc[start_idx:end_idx, "Slide Drilling"].fillna(0).sum() + Duration_DB.loc[start_idx:end_idx, "RotateDrilling"].fillna(0).sum()
            Duration_DB.loc[i, "Stand Duration"] = Duration_DB.loc[start_idx:end_idx, "ReamingTime"].fillna(0).sum() + Duration_DB.loc[i, "On Bottom Hours"] + row['ConnectionTime']
            Duration_DB.loc[start_idx:end_idx+1, "LABEL_StandGroup"] = StandNum_Temp
            StandNum_Temp = StandNum_Temp + 1
        elif row['LABEL_ConnectionActivity'] == "POST CONNECTION":
            start_idx = i

        # print(str(start_idx) + " - " + str(end_idx))
    return Duration_DB


def GetActivity_DF(Activity_DF, InputActivity_DB):
    ii = 1
    InputActivity_DB['DateTime'] = pd.to_datetime(InputActivity_DB['Date'] + ' ' + InputActivity_DB['Time'])
    for i,row in InputActivity_DB.iterrows():
        if ii<InputActivity_DB.shape[1]:
            start_time_temp = InputActivity_DB.iloc[ii, 'DateTime']
            end_time_temp = InputActivity_DB.iloc[ii+1, 'DateTime']

            idx_logic = (Activity_DF['dt'] >= start_time_temp) & (Activity_DF['dt'] < end_time_temp)

            activity_label_temp = InputActivity_DB.iloc[ii, 'Activity']
            InputActivity_DB.loc[idx_logic, "LABEL_Activity"] = activity_label_temp
            activity_label_temp = InputActivity_DB.iloc[ii, 'ConnectionActivity']
            InputActivity_DB.loc[idx_logic, "LABEL_ConnectionActivity"] = activity_label_temp
            activity_label_temp = InputActivity_DB.iloc[ii, 'MajorActivity']
            InputActivity_DB.loc[idx_logic, "LABEL_MajorActivity"] = activity_label_temp
        # ii = ii+1
    
    return None

def GetConnectionActivity_DF(Activity_DF, InputActivity_DB):
    return None


