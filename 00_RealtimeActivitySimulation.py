import pandas as pd 
import time
import sys

# print(sys.argv)

FileInput = sys.argv[1]
FileOutput = sys.argv[2]

# print(FileInput)

initial_row = 2000

# FileInput = "RealTime_Test\AAE-06_RAW.csv"
# FileOutput = "RealTime_Test\AAE-06-RealtimeSimulation.csv"

RawData_DF = pd.read_csv(FileInput) 

# print(RawData_DF.columns)

RawData_DF.iloc[:initial_row,:].to_csv(FileOutput)
for i,row in RawData_DF.iloc[initial_row:,:].iterrows():

    if (i % 800)==0:
        time.sleep(3)
        # print(time.ctime())
        # print(i)
        RawData_DF.iloc[:i+1,:].to_csv(FileOutput)
        print("===========")
        print("Simulation are running")
        print("append time-" + str(row['time']))
        print(row[["LABEL_ConnectionActivity","LABEL_SubActivity","LABEL_Activity"]])


        # tes_read = pd.read_csv(FileOutput)
        # print(tes_read['time'].tail(20).values)









