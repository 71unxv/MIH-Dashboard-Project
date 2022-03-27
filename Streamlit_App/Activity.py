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

def GetSubActivity_DF(Activity_DF):
    
    Activity_DF["SubActivity"] = "FALSE/Check"

    idx_logic = Activity_DF["Activity"].isin(["DRILLING FORMATION", 
                                            'CIRCULATE HOLE CLEANING',
                                            'CONNECTION',
                                            'DRILL OUT CEMENT',
                                        ])
    # print((Activity_DF.dtypes))

    idx_logic = idx_logic & ((Activity_DF['woba']>0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Rotary Drilling"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['woba']>0) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Slide Drilling"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    
    idx_logic = ~idx_logic & ((Activity_DF['woba']==0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Reaming"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Wash Up/Down"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label


    idx_logic = ~idx_logic & ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']<50))
    SubActivity_Label="Look and define"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label

    idx_logic = (idx_logic & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Connection"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label


    # ############################
    idx_logic = Activity_DF["Activity"].isin(["DRILLING FORMATION", 
                                            'CIRCULATE HOLE CLEANING',
                                            'CONNECTION',
                                            'DRILL OUT CEMENT',
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
                                            'LAY DOWN BHA',
                                            'MAKE UP BHA',
                                            'WIPER TRIP'
                                        ]
                                        )
    Activity_DF['isBitDepthMoving'] = Activity_DF['bitdepth'].shift(periods=-1) != Activity_DF['bitdepth']

    # Activity_DF["LABEL_SubActivity"] = "Check"
    idx_logic = idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']) & (Activity_DF['rpm']==0) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Wash Up/Down"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    
    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Reaming"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']<100) & (Activity_DF['mudflowin']<50))
    SubActivity_Label = "Moving"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & (~(Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Circulation"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['mudflowin']<10) & (Activity_DF['rpm']<10) & (Activity_DF['hklda']<Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Connection"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['mudflowin']<10) & (Activity_DF['rpm']<10) & (Activity_DF['hklda']<Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Stationary"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label

    ## force to be same as activity
    idx_logic = Activity_DF["Activity"].isin([
                            'CEMENTING JOB',
                            'CONNECTION',
                            'LAY DOWN BHA',
                            'MAKE UP BHA',
                            'NPT',
                            'N/D BOP',
                            'N/U BOP',
                            'RUNNING CASING IN',
                            'STATIONARY',
                            'STUCK PIPE',
                            'WAIT ON CEMENT',
                            'RIG REPAIR',
    ])
    Activity_DF.loc[idx_logic, "SubActivity"] = Activity_DF.loc[idx_logic, "Activity"]



    return Activity_DF.drop(['isBitDepthMoving'], axis=1)

    
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
    ii = 0
    InputActivity_DB = InputActivity_DB.reset_index()
    # print('test')

    for i,row in InputActivity_DB.iterrows():
        # if ii<InputActivity_DB.shape[1]:
        try:
            start_time_temp = InputActivity_DB.loc[ii, 'dt']
            end_time_temp = InputActivity_DB.loc[ii+1, 'dt']
            # print(InputActivity_DB.iloc[ii+1, 0])
            idx_logic = (Activity_DF['dt'] >= start_time_temp) & (Activity_DF['dt'] < end_time_temp)
        except:
            start_time_temp = InputActivity_DB.loc[ii, 'dt']
            # print(InputActivity_DB.iloc[ii, 0])
            # print('test')
            # end_time_temp = InputActivity_DB.loc[ii+1, 'dt']
            print((Activity_DF['dt'].dtypes))
            print(type(start_time_temp))
            print(start_time_temp)
            idx_logic = (Activity_DF['dt'] >= start_time_temp)
            

        activity_label_temp = InputActivity_DB.loc[ii, 'Activity']
        # print(idx_logic)
        # print('----')
        Activity_DF.loc[idx_logic, ("Activity")] = activity_label_temp
        # print(InputActivity_DB)
        activity_label_temp = InputActivity_DB.loc[ii, 'Hook Treshold']
        # print(Activity_DF)
        Activity_DF.loc[idx_logic, ("Hookload Treshold")] = activity_label_temp
        ii = ii+1
    
    return Activity_DF

def GetConnectionActivity_DF(Activity_DF, InputActivity_DB):
    return None


    
def GenerateDuration_DF_v2(RealTime_DB):
    RealTime_DB['dt'] = pd.to_datetime(RealTime_DB['dt'])
    RealTime_DB["LABEL_All"] =RealTime_DB['SubActivity'].astype(str)+'--'+RealTime_DB['Activity'].astype(str)

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
            'LABEL_SubActivity', "LABEL_Activity", "LABEL_StandGroup"
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
        # LABEL_ConnectionActivity = DF_Temp.head(1)['LABEL_ConnectionActivity'].values[0]
        LABEL_SubActivity = DF_Temp.head(1)['SubActivity'].values[0]
        LABEL_Activity = DF_Temp.head(1)['Activity'].values[0]
        # LABEL_MajorActivity = DF_Temp.head(1)['LABEL_MajorActivity'].values[0]

        Duration = round(((DF_Temp['dt'].max()-DF_Temp['dt'].min()).total_seconds())/60,2)
        Hole_Depth_Temp = DF_Temp['md'].max()

        if float(Hole_Depth_Temp)>= float(Hole_Depth):
            Hole_Depth = Hole_Depth_Temp
        

        Bit_Depth = DF_Temp['bitdepth'].mean()

        list_Out = [date, 
                    Time_start,
                    Time_end,
                    date_time, 
                    Duration, 
                    Hole_Depth, 
                    Bit_Depth, 
                    np.empty(1), 
                    np.empty(1), 
                    np.empty(1), 
                    np.empty(1), 
                    np.empty(1), 
                    np.empty(1), 
                    np.empty(1), 
                    LABEL_SubActivity, 
                    LABEL_Activity, 
                    np.nan
                    ]
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
            "LABEL_SubActivity":'str', "LABEL_Activity":'str',"LABEL_StandGroup":'float'
        }
    )
    Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'ROTARY DRILLING', 'RotateDrilling'] = Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'ROTARY DRILLING', 'Duration(minutes)']
    Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'SLIDE DRILLING', 'Slide Drilling'] = Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'SLIDE DRILLING', 'Duration(minutes)']
    Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'REAMING', 'ReamingTime'] = Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'REAMING', 'Duration(minutes)']
    Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'CONNECTION', 'ConnectionTime'] = Duration_DB.loc[Duration_DB['LABEL_SubActivity'] == 'CONNECTION', 'Duration(minutes)']

    DrillingOnlyDB = Duration_DB[Duration_DB["LABEL_Activity"]=="DRILLING FORMATION"]
    # start_idx = DrillingOnlyDB.index.values[0]
    # StandNum_Temp = 1
    # for i,row in DrillingOnlyDB[DrillingOnlyDB['SubActivity'].isin(['CONNECTION'])].iterrows():
        
    #     if row['LABEL_ConnectionActivity'] == 'CONNECTION':
    #         end_idx = i-1
    #         Duration_DB.loc[i, "Meterage(m)(Drilling)"] = Duration_DB.loc[start_idx:end_idx, "Meterage(m)(Drilling)"].fillna(0).sum()
    #         Duration_DB.loc[i, "On Bottom Hours"] = Duration_DB.loc[start_idx:end_idx, "Slide Drilling"].fillna(0).sum() + Duration_DB.loc[start_idx:end_idx, "RotateDrilling"].fillna(0).sum()
    #         Duration_DB.loc[i, "Stand Duration"] = Duration_DB.loc[start_idx:end_idx, "ReamingTime"].fillna(0).sum() + Duration_DB.loc[i, "On Bottom Hours"] + row['ConnectionTime']
    #         Duration_DB.loc[start_idx:end_idx+1, "LABEL_StandGroup"] = StandNum_Temp
    #         StandNum_Temp = StandNum_Temp + 1
    #         start_idx = start_idx + 1
    #     elif row['LABEL_ConnectionActivity'] == "POST CONNECTION":
    #         start_idx = i

        # print(str(start_idx) + " - " + str(end_idx))

    listSetDecimals = [
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
    ]
    for ColumnName in listSetDecimals:
        # print(ColumnName)
        Duration_DB[ColumnName] = Duration_DB[ColumnName].round(decimals=2)

    # rounded_df = df.round(decimals=2)
    return Duration_DB



def GetSubActivity_DF_v2(Activity_DF):
    logic_status = 0
    Activity_DF["SubActivity"] = "FALSE/Check"
    Activity_DF["logic_status"] = logic_status


    idx_logic_activity = Activity_DF["Activity"].isin(["DRILLING FORMATION", 
                                            'CIRCULATE HOLE CLEANING',
                                            'CONNECTION',
                                            'DRILL OUT CEMENT',
                                        ])
    # print((Activity_DF.dtypes))

    idx_logic = idx_logic_activity & ((Activity_DF['woba']>0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Rotary Drilling"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    #

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status
    # 1

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status

    idx_logic = idx_logic_activity &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['woba']>0) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Slide Drilling"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    # 2

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status
    
    idx_logic = idx_logic_activity &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['woba']==0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Reaming"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    #3

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status

    idx_logic = idx_logic_activity &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Wash Up/Down"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    #4

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status


    idx_logic = idx_logic_activity &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']<50))
    SubActivity_Label = "Connection"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    #5

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status

    # idx_logic = idx_logic_activity & ((Activity_DF["SubActivity"] == "FALSE/Check") & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    idx_logic = idx_logic & (Activity_DF['hklda']>Activity_DF['Hookload Treshold'])
    SubActivity_Label="Look and define"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    #6

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status
    #7


    # ############################
    idx_logic_activity_2 = Activity_DF["Activity"].isin([
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
                                            'LAY DOWN BHA',
                                            'MAKE UP BHA',
                                            'WIPER TRIP'
                                        ]
                                        )
    Activity_DF['isBitDepthMoving'] = Activity_DF['bitdepth'].shift(periods=-1) != Activity_DF['bitdepth']

    # Activity_DF["LABEL_SubActivity"] = "Check"
    idx_logic_2 = idx_logic_activity_2 & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']) & (Activity_DF['rpm']==0) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Wash Up/Down"
    Activity_DF.loc[idx_logic_2, "SubActivity"] = SubActivity_Label
    # DisplayDF(Activity_DF.loc[idx_logic_2, :])
    #

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_2, "logic_status"] = logic_status
    #8
    
    idx_logic_2 = idx_logic_activity_2 &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Reaming"
    Activity_DF.loc[idx_logic_2, "SubActivity"] = SubActivity_Label
    

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_2, "logic_status"] = logic_status
    #9

    idx_logic_2 = idx_logic_activity_2 &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']<100) & (Activity_DF['mudflowin']<50))
    SubActivity_Label = "Moving"
    Activity_DF.loc[idx_logic_2, "SubActivity"] = SubActivity_Label

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_2, "logic_status"] = logic_status
    #10

    idx_logic_2 = idx_logic_activity_2 &(Activity_DF["SubActivity"] == "FALSE/Check") & (~(Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Circulation"
    Activity_DF.loc[idx_logic_2, "SubActivity"] = SubActivity_Label
    #

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_2, "logic_status"] = logic_status
    #11

    idx_logic_2 = idx_logic_activity_2 &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['mudflowin']<10) & (Activity_DF['rpm']<10) & (Activity_DF['hklda']<Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Connection"
    Activity_DF.loc[idx_logic_2, "SubActivity"] = SubActivity_Label
    #

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_2, "logic_status"] = logic_status
    #12

    idx_logic_2 = idx_logic_activity_2 &(Activity_DF["SubActivity"] == "FALSE/Check") & ((~Activity_DF['isBitDepthMoving']) & (Activity_DF['mudflowin']<10) & (Activity_DF['rpm']<10) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Stationary"
    Activity_DF.loc[idx_logic_2, "SubActivity"] = SubActivity_Label
    #

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_2, "logic_status"] = logic_status
    #13

    ## force to be same as activity
    idx_logic_3 = Activity_DF["Activity"].isin([
                            'CEMENTING JOB',
                            'CONNECTION',
                            'LAY DOWN BHA',
                            'MAKE UP BHA',
                            'NPT',
                            'N/D BOP',
                            'N/U BOP',
                            'RUNNING CASING IN',
                            'STATIONARY',
                            'STUCK PIPE',
                            'WAIT ON CEMENT',
                            'RIG REPAIR',
    ])
    Activity_DF.loc[idx_logic_3, "SubActivity"] = Activity_DF.loc[idx_logic_3, "Activity"]
    #

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_3, "logic_status"] = logic_status
    #14

    # print(Activity_DF.columns)

    return Activity_DF
 



def GenerateDuration_DF_v3(RealTime_DB):

    RealTime_DB['dt'] = pd.to_datetime(RealTime_DB['dt'])
    RealTime_DB['SubActivity'] = RealTime_DB['SubActivity'].str.upper()
    RealTime_DB['Activity'] = RealTime_DB['Activity'].str.upper()
    RealTime_DB["LABEL_All"] =RealTime_DB['SubActivity'].astype(str)+'--'+RealTime_DB['Activity'].astype(str)

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
            'SubActivity', "Activity", "LABEL_StandGroup"
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
        # LABEL_ConnectionActivity = DF_Temp.head(1)['LABEL_ConnectionActivity'].values[0]
        SubActivity = DF_Temp.head(1)['SubActivity'].values[0]
        Activity = DF_Temp.head(1)['Activity'].values[0]
        # LABEL_MajorActivity = DF_Temp.head(1)['LABEL_MajorActivity'].values[0]

        Duration = ((DF_Temp['dt'].max()-DF_Temp['dt'].min()).total_seconds())/60
        Hole_Depth_Temp = DF_Temp['md'].max()

        if float(Hole_Depth_Temp)>= float(Hole_Depth):
            Hole_Depth = Hole_Depth_Temp
        

        Bit_Depth = DF_Temp['bitdepth'].mean()

        list_Out = [date, Time_start,Time_end, date_time, Duration, Hole_Depth, Bit_Depth, np.empty(1), np.empty(1), np.empty(1), np.empty(1), np.empty(1), np.empty(1), np.empty(1), SubActivity, Activity, np.nan]
        Duration_DB.loc[len(Duration_DB)] = list_Out

    Duration_DB = Duration_DB.astype(
        {
            'Duration(minutes)':'float',
            'Hole Depth(max)':'float',
            'Bit Depth(mean)':'float',
            "Meterage(m)(Drilling)":'float',
            'RotateDrilling':'float',
            'Slide Drilling':'float',
            'ReamingTime':'float',
            'ConnectionTime':'float',
            'On Bottom Hours':'float',
            'Stand Duration':'float',
            "SubActivity":'str', "Activity":'str',"LABEL_StandGroup":'float'
        }
    )

    Duration_DB.loc[Duration_DB['SubActivity'] == 'ROTARY DRILLING', 'RotateDrilling'] = Duration_DB.loc[Duration_DB['SubActivity'] == 'ROTARY DRILLING', 'Duration(minutes)']
    Duration_DB.loc[Duration_DB['SubActivity'] == 'SLIDE DRILLING', 'Slide Drilling'] = Duration_DB.loc[Duration_DB['SubActivity'] == 'SLIDE DRILLING', 'Duration(minutes)']
    Duration_DB.loc[Duration_DB['SubActivity'] == 'REAMING', 'ReamingTime'] = Duration_DB.loc[Duration_DB['SubActivity'] == 'REAMING', 'Duration(minutes)']
    Duration_DB.loc[Duration_DB['SubActivity'] == 'CONNECTION', 'ConnectionTime'] = Duration_DB.loc[Duration_DB['SubActivity'] == 'CONNECTION', 'Duration(minutes)']

    # DrillingOnlyDB = Duration_DB[Duration_DB["Activity"]=="DRILLING FORMATION"]
    # start_idx = DrillingOnlyDB.index.values[0]
    # StandNum_Temp = 1
    # for i,row in DrillingOnlyDB[DrillingOnlyDB['SubActivity'].isin(['CONNECTION', 'REAMING'])].iterrows():
        
        # if row['LABEL_ConnectionActivity'] == 'CONNECTION' and StandNum==1:
            # end_idx = i-1
    #         Duration_DB.loc[i, "Meterage(m)(Drilling)"] = Duration_DB.loc[start_idx:end_idx, "Meterage(m)(Drilling)"].fillna(0).sum()
    #         Duration_DB.loc[i, "On Bottom Hours"] = Duration_DB.loc[start_idx:end_idx, "Slide Drilling"].fillna(0).sum() + Duration_DB.loc[start_idx:end_idx, "RotateDrilling"].fillna(0).sum()
    #         Duration_DB.loc[i, "Stand Duration"] = Duration_DB.loc[start_idx:end_idx, "ReamingTime"].fillna(0).sum() + Duration_DB.loc[i, "On Bottom Hours"] + row['ConnectionTime']
    #         Duration_DB.loc[start_idx:end_idx+1, "LABEL_StandGroup"] = StandNum_Temp
    #         StandNum_Temp = StandNum_Temp + 1
    #         start_idx = start_idx + 1
    #     elif row['LABEL_ConnectionActivity'] == "POST CONNECTION":
    #         start_idx = i

        # print(str(start_idx) + " - " + str(end_idx))

    listSetDecimals = [
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
    ]
    for ColumnName in listSetDecimals:
        # print(ColumnName)
        Duration_DB[ColumnName] = Duration_DB[ColumnName].round(decimals=2)

    # rounded_df = df.round(decimals=2)
    return Duration_DB



def GetSubActivity_DF_v3(Activity_DF):
    Activity_DF = Activity_DF.astype(
        {
            "dt":"datetime64",
            # "date":"object",
            # "time":"object",
            "bitdepth":"float64",
            "md":"float64",
            "blockpos":"float64",
            "rop":"float64",
            "hklda":"float64",
            "woba":"float64",
            "torqa":"float64",
            "rpm":"float64",
            "stppress":"float64",
            "mudflowin":"float64",
            # "Activity":"object",
            "Hookload Treshold":"float64",
            # "SubActivity":"object",
            # "logic_status":"int64",
            # "isBitDepthMoving":"bool",
            # "LABEL_All":"object",
        }
    )
    
    logic_status = 0
    Activity_DF["SubActivity"] = "FALSE/Check"
    Activity_DF["logic_status"] = logic_status


    idx_logic_activity = Activity_DF["Activity"].isin(["DRILLING FORMATION", 
                                            'CIRCULATE HOLE CLEANING',
                                            'CONNECTION',
                                            'DRILL OUT CEMENT',
                                        ])
    # print((Activity_DF.dtypes))

    idx_logic = idx_logic_activity & ((Activity_DF['woba']>0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Rotary Drilling"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    #

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status
    # 1

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status

    idx_logic = idx_logic_activity &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['woba']>0) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Slide Drilling"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    # 2

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status
    
    idx_logic = idx_logic_activity &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['woba']==0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Reaming"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    #3

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status

    idx_logic = idx_logic_activity &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Wash Up/Down"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    #4

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status


    idx_logic = idx_logic_activity &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']<50))
    SubActivity_Label = "Connection"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    #5

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status

    # idx_logic = idx_logic_activity & ((Activity_DF["SubActivity"] == "FALSE/Check") & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    idx_logic = idx_logic & (Activity_DF['hklda']>Activity_DF['Hookload Treshold'])
    SubActivity_Label="Look and define"
    Activity_DF.loc[idx_logic, "SubActivity"] = SubActivity_Label
    #6

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic, "logic_status"] = logic_status
    #7


    # ############################
    idx_logic_activity_2 = Activity_DF["Activity"].isin([
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
                                            'LAY DOWN BHA',
                                            'MAKE UP BHA',
                                            'WIPER TRIP'
                                        ]
                                        )
    Activity_DF['isBitDepthMoving'] = Activity_DF['bitdepth'].shift(periods=-1) != Activity_DF['bitdepth']

    # Activity_DF["LABEL_SubActivity"] = "Check"
    idx_logic_2 = idx_logic_activity_2 & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']) & (Activity_DF['rpm']==0) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Wash Up/Down"
    Activity_DF.loc[idx_logic_2, "SubActivity"] = SubActivity_Label
    # DisplayDF(Activity_DF.loc[idx_logic_2, :])
    #

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_2, "logic_status"] = logic_status
    #8
    
    idx_logic_2 = idx_logic_activity_2 &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Reaming"
    Activity_DF.loc[idx_logic_2, "SubActivity"] = SubActivity_Label
    

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_2, "logic_status"] = logic_status
    #9

    idx_logic_2 = idx_logic_activity_2 &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']<100) & (Activity_DF['mudflowin']<50))
    SubActivity_Label = "Moving"
    Activity_DF.loc[idx_logic_2, "SubActivity"] = SubActivity_Label

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_2, "logic_status"] = logic_status
    #10

    idx_logic_2 = idx_logic_activity_2 &(Activity_DF["SubActivity"] == "FALSE/Check") & (~(Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Circulation"
    Activity_DF.loc[idx_logic_2, "SubActivity"] = SubActivity_Label
    #

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_2, "logic_status"] = logic_status
    #11

    idx_logic_2 = idx_logic_activity_2 &(Activity_DF["SubActivity"] == "FALSE/Check") & ((Activity_DF['mudflowin']<10) & (Activity_DF['rpm']<10) & (Activity_DF['hklda']<Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Connection"
    Activity_DF.loc[idx_logic_2, "SubActivity"] = SubActivity_Label
    #

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_2, "logic_status"] = logic_status
    #12

    idx_logic_2 = idx_logic_activity_2 &(Activity_DF["SubActivity"] == "FALSE/Check") & ((~Activity_DF['isBitDepthMoving']) & (Activity_DF['mudflowin']<10) & (Activity_DF['rpm']<10) & (Activity_DF['hklda']>Activity_DF['Hookload Treshold']))
    SubActivity_Label = "Stationary"
    Activity_DF.loc[idx_logic_2, "SubActivity"] = SubActivity_Label
    #

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_2, "logic_status"] = logic_status
    #13

    ## force to be same as activity
    idx_logic_3 = Activity_DF["Activity"].isin([
                            'CEMENTING JOB',
                            'CONNECTION',
                            'LAY DOWN BHA',
                            'MAKE UP BHA',
                            'NPT',
                            'N/D BOP',
                            'N/U BOP',
                            'RUNNING CASING IN',
                            'STATIONARY',
                            'STUCK PIPE',
                            'WAIT ON CEMENT',
                            'RIG REPAIR',
    ])
    Activity_DF.loc[idx_logic_3, "SubActivity"] = Activity_DF.loc[idx_logic_3, "Activity"]
    #

    logic_status = logic_status + 1
    Activity_DF.loc[idx_logic_3, "logic_status"] = logic_status
    #14

    # print(Activity_DF.columns)

    return Activity_DF




def GenerateDuration_DF_v3(RealTime_DB):
    RealTime_DB['dt'] = pd.to_datetime(RealTime_DB['dt'])
    RealTime_DB["LABEL_All"] =RealTime_DB['SubActivity'].astype(str)+'--'+RealTime_DB['Activity'].astype(str)


    list_dict_out = []
    for k,DF_Temp in RealTime_DB.groupby((RealTime_DB['LABEL_All'].shift() != RealTime_DB['LABEL_All']).cumsum()):

        if not(("Hole_Depth" in locals()) or ("Hole_Depth" in globals())):
            Hole_Depth = 0

        list_temp = []

        date = DF_Temp.head(1)['date'].values[0]
        Time_start = DF_Temp.head(1)['time'].values[0]
        Time_end = DF_Temp.tail(1)['time'].values[0]
        date_time = DF_Temp.head(1)['dt'].values[0]
        # LABEL_ConnectionActivity = DF_Temp.head(1)['LABEL_ConnectionActivity'].values[0]
        LABEL_SubActivity = DF_Temp.head(1)['SubActivity'].values[0]
        LABEL_Activity = DF_Temp.head(1)['Activity'].values[0]
        # LABEL_MajorActivity = DF_Temp.head(1)['LABEL_MajorActivity'].values[0]

        Duration = round(((DF_Temp['dt'].max()-DF_Temp['dt'].min()).total_seconds())/60,2)
        Hole_Depth_Temp = DF_Temp['md'].max()

        if float(Hole_Depth_Temp)>= float(Hole_Depth):
            Hole_Depth = Hole_Depth_Temp
        

        Bit_Depth = DF_Temp['bitdepth'].mean()

        RotateDrilling = 0
        SlideDrilling = 0
        ReamingTime = 0
        ConnectionTime = 0

        OnBottomHours = 0
        MeterageDrilling = 0
        StandDuration = 0


        if LABEL_Activity in ["DRILLING FORMATION", 
                                'CIRCULATE HOLE CLEANING',
                                'CONNECTION',
                                'DRILL OUT CEMENT'
                                ]:
            if LABEL_SubActivity == "Rotary Drilling":
                RotateDrilling = Duration

            if LABEL_SubActivity == "Slide Drilling":
                SlideDrilling = Duration

            if LABEL_SubActivity == "Reaming":
                ReamingTime = Duration
            if LABEL_SubActivity == "Connection":
                ConnectionTime = Duration

            MeterageDrilling = round((DF_Temp['md'].max()-DF_Temp['md'].min()),2)

        list_dict_out.append(
            {
            'date':date,
            'Time_start':Time_start,
            'Time_end':Time_end,
            'date_time':date_time,
            'Duration(minutes)':Duration,
            'Hole Depth(max)':Hole_Depth,
            'Bit Depth(mean)':Bit_Depth,
            "Meterage(m)(Drilling)": MeterageDrilling,
            'RotateDrilling':RotateDrilling,
            'Slide Drilling':SlideDrilling,
            'ReamingTime':ReamingTime,
            'ConnectionTime':ConnectionTime,
            'On Bottom Hours':OnBottomHours,
            'Stand Duration': StandDuration,
            'LABEL_SubActivity': LABEL_SubActivity,
            "LABEL_Activity": LABEL_Activity,

            }
        )
    Duration_DB = pd.DataFrame.from_dict(list_dict_out, orient='columns')
    Duration_DB = Duration_DB.astype(
        {
            'date':'datetime64',
            'Duration(minutes)':'float',
            'Hole Depth(max)':'float',
            'Bit Depth(mean)':'float',
            "Meterage(m)(Drilling)":'float',
            'RotateDrilling':'float',
            'Slide Drilling':'float',
            'ReamingTime':'float',
            'ConnectionTime':'float',
            'On Bottom Hours':'float',
            'Stand Duration':'float',
            "LABEL_SubActivity":'str', 
            "LABEL_Activity":'str',
        }
    )

    listSetDecimals = [
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
    ]
    for ColumnName in listSetDecimals:
        # print(ColumnName)
        Duration_DB[ColumnName] = Duration_DB[ColumnName].round(decimals=2)

    # rounded_df = df.round(decimals=2)
    return Duration_DB




def cleanFalseSensor(MasterReport_DF_Web):
    MasterReport_DF_Web = MasterReport_DF_Web.reset_index(drop=True)
    # while ("FALSE/Check" in MasterReport_DF_Web['LABEL_SubActivity'].values) or ("Look and define" in MasterReport_DF_Web['LABEL_SubActivity'].values):
    idx_same = MasterReport_DF_Web.index[MasterReport_DF_Web['LABEL_SubActivity']=="Look and define"]
    idx_before = idx_same - 1

    idx_same = idx_same[idx_before>0]
    idx_before = idx_before[idx_before>0]
    
    MasterReport_DF_Web.loc[idx_same, 'LABEL_SubActivity'] = MasterReport_DF_Web.loc[idx_before, 'LABEL_SubActivity'].values
    MasterReport_DF_Web['MERGE_SubActivity-Activity'] = MasterReport_DF_Web['LABEL_Activity'] + "--"+MasterReport_DF_Web['LABEL_SubActivity']

    idx_same = MasterReport_DF_Web.index[MasterReport_DF_Web['LABEL_SubActivity']=="FALSE/Check"]
    # print(idx_same)
    idx_before = idx_same - 1

    idx_same = idx_same[idx_before>0]
    # print(idx_same)
    idx_before = idx_before[idx_before>0]
    # print(idx_before)
    
    MasterReport_DF_Web.loc[idx_same, 'LABEL_SubActivity'] = MasterReport_DF_Web.loc[idx_before, 'LABEL_SubActivity'].values
    MasterReport_DF_Web['MERGE_SubActivity-Activity'] = MasterReport_DF_Web['LABEL_Activity'] + "--"+MasterReport_DF_Web['LABEL_SubActivity']


    idx_same = MasterReport_DF_Web.index[MasterReport_DF_Web['LABEL_SubActivity']=="FALSE/Check"]
    idx_before = idx_same - 1

    idx_same = idx_same[idx_before>0]
    idx_before = idx_before[idx_before>0]
    
    MasterReport_DF_Web.loc[idx_same, 'LABEL_SubActivity'] = MasterReport_DF_Web.loc[idx_before, 'LABEL_SubActivity'].values
    MasterReport_DF_Web['MERGE_SubActivity-Activity'] = MasterReport_DF_Web['LABEL_Activity'] + "--"+MasterReport_DF_Web['LABEL_SubActivity']

    idx_same = MasterReport_DF_Web.index[MasterReport_DF_Web['LABEL_SubActivity']=="Look and define"]
    # print(idx_same)
    idx_before = idx_same - 1

    idx_same = idx_same[idx_before>0]
    # print(idx_same)
    idx_before = idx_before[idx_before>0]
    # print(idx_before)
    
    MasterReport_DF_Web.loc[idx_same, 'LABEL_SubActivity'] = MasterReport_DF_Web.loc[idx_before, 'LABEL_SubActivity'].values
    MasterReport_DF_Web['MERGE_SubActivity-Activity'] = MasterReport_DF_Web['LABEL_Activity'] + "--"+MasterReport_DF_Web['LABEL_SubActivity']


    MasterReport_DF_Web = MasterReport_DF_Web.groupby((MasterReport_DF_Web['MERGE_SubActivity-Activity'].shift() != MasterReport_DF_Web['MERGE_SubActivity-Activity']).cumsum(), as_index=False).agg(
        {
            'date':'max',
            'Time_start':'min',
            'Time_end':'max',
            'date_time':'min',
            'Duration(minutes)':'sum',
            'Hole Depth(max)':'max',
            'Bit Depth(mean)': 'mean',

            'Meterage(m)(Drilling)':'sum',
            'RotateDrilling':'sum',
            'Slide Drilling':'sum',
            'ReamingTime':'sum',
            'ConnectionTime':'sum',
            'On Bottom Hours':'sum',
            'Stand Duration':'sum',
            'LABEL_SubActivity':'first',
            'LABEL_Activity':'first',
            'MERGE_SubActivity-Activity':'first'
        }
    )
    # list_col = [
    #         # 'Meterage(m)(Drilling)',
    #         'RotateDrilling',
    #         'Slide Drilling',
    #         'ReamingTime',
    #         # 'ConnectionTime',
    #         # 'On Bottom Hours',
    #         # 'Stand Duration'
    # ]
    # for ColName in list_col:
    idx_temp = MasterReport_DF_Web['LABEL_SubActivity']=='RotateDrilling'
    MasterReport_DF_Web.loc[idx_temp,'RotateDrilling'] = MasterReport_DF_Web.loc[idx_temp,'Duration(minutes)'].values 

    idx_temp = MasterReport_DF_Web['LABEL_SubActivity']=='Slide Drilling'
    MasterReport_DF_Web.loc[idx_temp,'Slide Drilling'] = MasterReport_DF_Web.loc[idx_temp,'Duration(minutes)'].values 

    idx_temp = MasterReport_DF_Web['LABEL_SubActivity']=='ReamingTime'
    MasterReport_DF_Web.loc[idx_temp,'ReamingTime'] = MasterReport_DF_Web.loc[idx_temp,'Duration(minutes)'].values 

    return MasterReport_DF_Web

def labelStand(MasterReport_DF):
    # date
    # Time_start
    # Time_end
    # date_time
    # Duration(minutes)
    # Hole Depth(max)
    # Bit Depth(mean)
    # Meterage(m)(Drilling)
    # RotateDrilling
    # Slide Drilling
    # ReamingTime
    # ConnectionTime
    # On Bottom Hours
    # Stand Duration
    # LABEL_SubActivity
    # LABEL_Activity
    # MasterReport_DF = pd.read_excel('Data\\Master_Report\\MasterReportTest.xlsx')
    # print(MasterReport_DF.dtypes)
    MasterReport_DF['Stand Meterage (m) (Drilling)'] = np.NaN
    MasterReport_DF['Stand Stand Duration (hrs)'] = np.NaN
    MasterReport_DF['Stand On Bottom Hours'] = np.NaN
    MasterReport_DF = MasterReport_DF.astype(
            {
                'Duration(minutes)':'float',
                'Hole Depth(max)':'float',
                'Bit Depth(mean)':'float',
                "Meterage(m)(Drilling)":'float',
                "Stand Meterage (m) (Drilling)":'float',
                "RotateDrilling":'float',
                'Slide Drilling':'float',
                'ReamingTime':'float',
                'ConnectionTime':'float',
                'On Bottom Hours':'float',
                'Stand On Bottom Hours':'float',
                'Stand Duration':'float',
                'Stand Stand Duration (hrs)':'float',

            }
    )
    MasterReport_DF = MasterReport_DF.reset_index(drop=True).fillna(0)

    ii = 0
    for idx,row in MasterReport_DF[(MasterReport_DF['LABEL_SubActivity']=='Connection')].iterrows():
        # print(idx)
        if ii==0:

            idx_start = idx + 1

        else:
            idx_end = idx - 1
        
            MasterReport_DF.loc[idx_start:idx_end, 'Stand Group_Pred'] = 'Stand Group - ' + str(ii)


            OnBottomHours =  MasterReport_DF.loc[idx_start:idx_end, 'RotateDrilling'].sum() + MasterReport_DF.loc[idx_start:idx_end, 'Slide Drilling'].sum()
            StandDuration =  MasterReport_DF.loc[idx_start:idx_end+1, 'Duration(minutes)'].sum()
            StandMeterageDrilling = MasterReport_DF.loc[idx_start:idx_end, 'Meterage(m)(Drilling)'].sum()


            MasterReport_DF.loc[idx, 'Stand On Bottom Hours'] = OnBottomHours
            MasterReport_DF.loc[idx, 'Stand Stand Duration (hrs)'] = StandDuration
            MasterReport_DF.loc[idx, "Stand Meterage (m) (Drilling)"] = StandMeterageDrilling

            # print(str(idx_start) + " - " + str(idx_end))
            idx_start = idx + 1

        ii = ii + 1
    return MasterReport_DF


def SummaryTranslator(summaryDB, WellName, CompName, PIC_Info, Remarks_Info, Section_Info):
    summaryDB['comp'] = WellName
    summaryDB['well'] = CompName
    summaryDB['pic'] = PIC_Info
    summaryDB['section'] = Remarks_Info
    summaryDB['remarks'] = Section_Info
    summaryDB['time_start'] = pd.to_datetime(summaryDB.date + " " + summaryDB.Time_start)
    summaryDB['time_end'] = pd.to_datetime(summaryDB.date + " " + summaryDB.Time_end)
    # summaryDB['time_start'] = pd.to_datetime(summaryDB.date.dt.strftime('%Y-%m-%d') + " " + summaryDB.Time_start)
    # summaryDB['time_end'] = pd.to_datetime(summaryDB.date.dt.strftime('%Y-%m-%d') + " " + summaryDB.Time_end)
    summaryDB['date'] = pd.to_datetime(summaryDB['date']).dt.date
    listcolumn = ['comp',
    'well',
    'time_start',
    'time_end',
    'duration_minutes',
    'hole_depth',
    'bit_depth',
    'meterage_drilling',
    'rotate_drilling_time',
    'slide_drilling_time',
    'reaming_time',
    'connection_time',
    'on_bottom_hours',
    'stand_duration',
    'label_subactivity',
    'label_activity',
    'stand_meterage_drilling',
    'stand_durationx',
    'stand_on_bottom',
    'stand_group',
    'pic',
    'section',
    'remarks']
    ColumnName_Dict = {
    'duration_minutes':'Duration(minutes)',
    'hole_depth':'Hole Depth(max)',
    'bit_depth':'Bit Depth(mean)',
    'meterage_drilling':'Meterage(m)(Drilling)',
    'rotate_drilling_time':'RotateDrilling',
    'slide_drilling_time':'Slide Drilling',
    'reaming_time':'ReamingTime',
    'connection_time':'ConnectionTime',
    'on_bottom_hours':'On Bottom Hours',
    'stand_duration':'Stand Duration',
    'label_subactivity':'LABEL_SubActivity',
    'label_activity':'LABEL_Activity',
    'stand_meterage_drilling':'Stand Meterage (m) (Drilling)',
    'stand_durationx':'Stand Stand Duration (hrs)',
    'stand_on_bottom':'Stand On Bottom Hours',
    'stand_group':'Stand Group_Pred'
    }
    ColumnName_Dict_fin = dict((y,x) for x,y in ColumnName_Dict.items())

    summaryDB.rename(columns = ColumnName_Dict_fin, inplace = True)
    return summaryDB[listcolumn]