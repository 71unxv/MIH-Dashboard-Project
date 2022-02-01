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



