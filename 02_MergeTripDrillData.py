import pandas as pd
import glob
from PDU_Func import Activity

ListOfDrilling_Data = glob.glob("Data\\raw_BM\\*Drilling*")
ListOfTripping_Data = glob.glob("Data\\raw_BM\\*Trip*")

# for i in ListOfDrilling_Data+ListOfTripping_Data:
#     print(i)


for DrillFilepath, TripFilepath in zip(ListOfDrilling_Data, ListOfTripping_Data):
    Drilling_Data_DF = pd.read_csv(DrillFilepath)
    Tripping_Data_DF = pd.read_csv(TripFilepath)

    Tripping_Data_DF['Remarks'] = 'Trip_Data'
    Drilling_Data_DF['Remarks'] = 'Drill_Data'
    Merge_DF = Drilling_Data_DF.join(Tripping_Data_DF.set_index('dt'),how='outer',on='dt', rsuffix='_Trip', sort='True')

    for ColumnName in Merge_DF.columns:

        if "_Trip" in ColumnName:

            Temp = ColumnName.split("_")[0] 
            # print(Temp)
            Merge_DF.loc[Merge_DF[Temp].isna(), Temp] = Merge_DF.loc[Merge_DF[Temp].isna(), ColumnName]
            del Merge_DF[ColumnName]
    Merge_DF = Merge_DF.reset_index(drop=True)
    # print(Merge_DF.columns)
    for ii in Merge_DF.columns:
        print(ii)
    print(DrillFilepath.split("\\")[-1].split(' ')[1])
    


    ConnectionWeight = 61
    Merge_DF['dt_DF'] = pd.to_datetime(Merge_DF['date'] + ' ' + Merge_DF['time'])
    DF_Temp = Merge_DF.loc[Merge_DF['Remarks']=="Drill_Data", :]
    Merge_DF.loc[Merge_DF['Remarks']=="Drill_Data", "SubActivity_Predict"]=Activity.GetDrillingActivity_DF(DF_Temp, ConnectionWeight)

    DF_Temp = Merge_DF.loc[Merge_DF['Remarks']=="Trip_Data", :]
    Merge_DF.loc[Merge_DF['Remarks']=="Trip_Data", "SubActivity_Predict"]=Activity.GetTrippingActivity_DF(DF_Temp, ConnectionWeight)

    outfilename = "Data\\Merged\\" + "Merge_DrillTrip_" + DrillFilepath.split("\\")[-1].split(' ')[1] + ".csv"
    Merge_DF.to_csv(outfilename)

    # Drilling_Data_DF["SubActivity_Predict"] = Activity.GetDrillingActivity_DF(Drilling_Data_DF, ConnectionWeight)
    # Tripping_Data_DF["SubActivity_Predict"] = Activity.GetTrippingActivity_DF(Tripping_Data_DF, ConnectionWeight)

    # Drilling_Data_DF.to_csv("Data\\Drill_" + DrillFilepath.split("\\")[-1].split(' ')[1] + ".csv")
    # Tripping_Data_DF.to_csv("Data\\Trip_" + DrillFilepath.split("\\")[-1].split(' ')[1] + ".csv")
    # break


