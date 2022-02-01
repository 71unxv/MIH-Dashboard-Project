import pandas as pd


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

    Activity_DF["SubActivity_Predict"] = "Check"
    idx_logic = ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Hookload) & (Activity_DF['rpm']==0) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Wash Up/Down"
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label
    
    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Hookload) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Reaming"
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Hookload) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']<100) & (Activity_DF['mudflowin']<50))
    SubActivity_Label = "Moving"
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['hklda']>Hookload) & (Activity_DF['mudflowin']>10))
    SubActivity_Label = "Circulation"
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['mudflowin']<10) & (Activity_DF['rpm']<10) & (Activity_DF['hklda']<Hookload))
    SubActivity_Label = "Connection"
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['isBitDepthMoving']) & (Activity_DF['mudflowin']<10) & (Activity_DF['rpm']<Hookload) & (Activity_DF['hklda']<Hookload))
    SubActivity_Label = "Stationary"
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label

    return Activity_DF["SubActivity_Predict"]

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

    Activity_DF["SubActivity_Predict"] = "FALSE"

    idx_logic = ((Activity_DF['woba']>0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
    SubActivity_Label = "Rotary Drilling"
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['woba']>0) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
    SubActivity_Label = "Slide Drilling"
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label
    
    idx_logic = ~idx_logic & ((Activity_DF['woba']==0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
    SubActivity_Label = "Reaming"
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label

    idx_logic = ~idx_logic & ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
    SubActivity_Label = "Wash Up/Down"
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label


    idx_logic = ~idx_logic & ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']<50))
    SubActivity_Label="Look and define"
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label

    idx_logic = (idx_logic & (Activity_DF['hklda']>ConnectionWeight))
    SubActivity_Label = "Connection"
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label
    

    # v2
    
        # Activity_DF["SubActivity_Predict"] = "FALSE"

        # idx_logic = ((Activity_DF['woba']>0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
        # SubActivity_Label = "Rotary Drilling"
        # Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label

        # idx_logic = ((Activity_DF['woba']>0) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
        # SubActivity_Label = "Slide Drilling"
        # Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label
        
        # idx_logic = ((Activity_DF['woba']==0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
        # SubActivity_Label = "Reaming"
        # Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label

        # idx_logic = ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
        # SubActivity_Label = "Wash Up/Down"
        # Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label


        # idx_logic = ((Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']<50))
        # SubActivity_Label="Look and define"
        # Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label

        # idx_logic = (idx_logic & (Activity_DF['hklda']>ConnectionWeight))
        # SubActivity_Label = "Connection"
        # Activity_DF.loc[idx_logic, "SubActivity_Predict"] = SubActivity_Label
    # def GetDrillingActivity_DF(ConnectionWeight,Activity_DF):
    #     v1
    #     Activity_DF["SubActivity_Predict"] = "Look and define"

    #     idx_logic = ((Activity_DF['woba']>0) & (Activity_DF['rpm']>10)) & ((Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
    #     Activity_DF.loc[idx_logic, "SubActivity_Predict"] = "Rotary Drilling"

    #     idx_logic = (Activity_DF['woba']>0) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight)
    #     Activity_DF.loc[idx_logic, "SubActivity_Predict"] = "Slide Drilling"

    #     idx_logic = (Activity_DF['woba']==0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight)
    #     Activity_DF.loc[idx_logic, "SubActivity_Predict"] = "Reaming"

    #     idx_logic = (Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight)
    #     Activity_DF.loc[idx_logic, "SubActivity_Predict"] = "Wash Up/Down"

    #     idx_logic = (Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']<50) & (Activity_DF['hklda']<ConnectionWeight)
    #     Activity_DF.loc[idx_logic, "SubActivity_Predict"] = "Connection"


    #     return Activity_DF

    return Activity_DF["SubActivity_Predict"]



    
def GenerateDuration_DF(RealTime_DB):
    RealTime_DB['dt'] = pd.to_datetime(RealTime_DB['dt'])
    RealTime_DB["LABEL_All"] =RealTime_DB['LABEL_ConnectionActivity'].astype(str) + '--' +RealTime_DB['LABEL_SubActivity']+'--'+RealTime_DB['LABEL_Activity']

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
            "LABEL_ConnectionActivity", 'LABEL_SubActivity', "LABEL_Activity"
            ]
        )

    for k,DF_Temp in RealTime_DB.groupby((RealTime_DB['LABEL_All'].shift() != RealTime_DB['LABEL_All']).cumsum()):

        if (("Hole_Depth" in locals()) or ("Hole_Depth" in globals())):
            Hole_Depth = 0

        list_temp = []

        date = DF_Temp.head(1)['date'].values[0]
        Time_start = DF_Temp.head(1)['time'].values[0]
        Time_end = DF_Temp.tail(1)['time'].values[0]
        date_time = DF_Temp.head(1)['dt'].values[0]
        LABEL_ConnectionActivity = DF_Temp.head(1)['LABEL_ConnectionActivity'].values[0]
        LABEL_SubActivity = DF_Temp.head(1)['LABEL_SubActivity'].values[0]
        LABEL_Activity = DF_Temp.head(1)['LABEL_Activity'].values[0]

        Duration = round(((DF_Temp['dt'].max()-DF_Temp['dt'].min()).total_seconds())/60,2)
        Hole_Depth_Temp = DF_Temp['md'].max()

        if Hole_Depth_Temp>= Hole_Depth:
            Hole_Depth = Hole_Depth_Temp
        

        Bit_Depth = DF_Temp['bitdepth'].mean()

        list_Out = [date, Time_start,Time_end, date_time, Duration, Hole_Depth, Bit_Depth, "", "", "", "", "", "", "",LABEL_ConnectionActivity, LABEL_SubActivity, LABEL_Activity]
        Duration_DB.loc[len(Duration_DB)] = list_Out

        
    # SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Rotary Drilling', 'RotateDrilling'] = SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Rotary Drilling', 'Duration']
    # SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Slide Drilling', 'Slide Drilling'] = SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Slide Drilling', 'Duration']
    # SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Reaming', 'ReamingTime'] = SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Reaming', 'Duration']
    # SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Connection', 'ConnectionTime'] = SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Connection', 'Duration']
    return Duration_DB
