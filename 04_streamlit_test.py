import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import numpy as np 
import pandas as pd
from IPython.display import display as display_DF
from plotly.subplots import make_subplots

ListOfDrilling_Data = ["Data/raw_BM/ASCII AAE-06 Drilling.csv"]
ListOfDrilling_Data = ["Data/raw_BM/ASCII AAE-05 Drilling.csv"]


number = 0

Drilling_Data_DF = pd.read_csv(ListOfDrilling_Data[number])

def GetDrillingActivity_DF(ConnectionWeight,Activity_DF):
    Activity_DF["SubActivity_Predict"] = "Look and define"

    idx_logic = ((Activity_DF['woba']>0) & (Activity_DF['rpm']>10)) & ((Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight))
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = "Rotary Drilling"

    idx_logic = (Activity_DF['woba']>0) & (Activity_DF['rpm']<10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight)
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = "Slide Drilling"

    idx_logic = (Activity_DF['woba']==0) & (Activity_DF['rpm']>10) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight)
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = "Reaming"

    idx_logic = (Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']>100) & (Activity_DF['hklda']>ConnectionWeight)
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = "Wash Up/Down"

    idx_logic = (Activity_DF['woba']==0) & (Activity_DF['rpm']==0) & (Activity_DF['stppress']<50) & (Activity_DF['hklda']<ConnectionWeight)
    Activity_DF.loc[idx_logic, "SubActivity_Predict"] = "Connection"


    return Activity_DF

    # return SubActivity_Label

# Tripping_Data_DF
ConnectionWeight = 61
Activity_New = GetDrillingActivity_DF(ConnectionWeight,Drilling_Data_DF)
Activity_New['dt_DF'] = pd.to_datetime(Activity_New['date'] + ' ' + Activity_New['time'])






SubActivityOutput = pd.DataFrame(columns=['date', 'Time_start','Time_end', 'date_time', 'Duration', 'Hole Depth', 'Bit Depth(mean)', 'RotateDrilling', 'Slide Drilling', 'ReamingTime', 'ConnectionTime', 'SubActivity'])
Hole_Depth=0
for k,DF_Temp in Activity_New.groupby((Activity_New['SubActivity_Predict'].shift() != Activity_New['SubActivity_Predict']).cumsum()):
    # print(f'[group {k}]')
    list_temp = []
    # display_DF(DF_Temp)
    date = DF_Temp.head(1)['date'].values[0]
    Time_start = DF_Temp.head(1)['time'].values[0]
    Time_end = DF_Temp.tail(1)['time'].values[0]
    date_time = DF_Temp.head(1)['dt'].values[0]
    SubActivity_Predict_Class = DF_Temp.head(1)['SubActivity_Predict'].values[0]

    Duration = round(((DF_Temp['dt_DF'].max()-DF_Temp['dt_DF'].min()).total_seconds())/60,2)
    Hole_Depth_Temp = DF_Temp['md'].max()

    if Hole_Depth_Temp>= Hole_Depth:
        Hole_Depth = Hole_Depth_Temp
    
    # Bit_Depth = DF_Temp['md'].max()
    Bit_Depth = DF_Temp['bitdepth'].mean()
    # date = DF_Temp.head(1)['t'].values
    list_Out = [date, Time_start,Time_end, date_time, Duration, Hole_Depth, Bit_Depth, "", "", "", "",SubActivity_Predict_Class]
    SubActivityOutput.loc[len(SubActivityOutput)] = list_Out






SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Rotary Drilling', 'RotateDrilling'] = SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Rotary Drilling', 'Duration']
SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Slide Drilling', 'Slide Drilling'] = SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Slide Drilling', 'Duration']
SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Reaming', 'ReamingTime'] = SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Reaming', 'Duration']
SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Connection', 'ConnectionTime'] = SubActivityOutput.loc[SubActivityOutput['SubActivity'] == 'Connection', 'Duration']

# SubActivityOutput.to_excel("AAE-05_SubActivity_Test_v1.xlsx")


forPlot_DF = SubActivityOutput.groupby('SubActivity')['Duration'].sum()

#Data Set
# countries=['India', 'Australia',
#            'Jepang', 'America',
#            'Russia']
 
# values = [4500, 2500, 1053, 500,
#           3200]

#The plot
# import plotly.graph_objects as go

fig = make_subplots(rows=1, cols=4, 
specs=[[{"type": "pie"}, {"type": "bar"}, {"type": "bar"}, {"type": "bar"}],]
)


dict = {'X_axis': np.random.randint(10, 50, 20),
            'Y_axis': [i for i in range(20)]}

df_tes = pd.DataFrame(dict)



# import plotly.graph_objs as go
# fig = go.Figure(
#     go.Pie(
#     labels = forPlot_DF.index,
#     values = forPlot_DF.values/60,
#     hoverinfo = "label+percent",
#     textinfo = "value+label"
#     )
# )



# fig.add_trace(
#     go.Scatter(
#         x=[20, 30, 40], 
#         y=[50, 60, 70]),
#         row=1, col=2
#     )
fig.add_trace(
    go.Pie(
    labels = forPlot_DF.index,
    values = forPlot_DF.values/60,
    hoverinfo = "label+percent",
    textinfo = "value+label"
    ),
    row=1, col=1

    )
fig.add_trace(
    go.Bar(
        x=df_tes["X_axis"],
        y=df_tes["Y_axis"],
        offsetgroup=0,
        marker_color = '#1f77b4', 
        name='tes'
      ),
    row=1,
    col=2,
)
fig.add_trace(
    go.Bar(
        x=df_tes["X_axis"],
        y=df_tes["Y_axis"],
        offsetgroup=0,
        marker_color = '#1f77b4', 
        name='tes'
      ),
    row=1,
    col=3,
)
fig.add_trace(
    go.Bar(
        x=df_tes["X_axis"],
        y=df_tes["Y_axis"],
        offsetgroup=0,
        marker_color = '#1f77b4', 
        name='tes'
      ),
    row=1,
    col=4,
)
# fig.add_trace(
#     go.Bar(
#     x=df_pivot["Country"],
#     y=df_pivot["developing"],
#     offsetgroup=0,
#     # base=df_pivot["develop"],
#     marker_color = "rgba(255, 0, 0, 0.6)",
#     name='developing'
#     ),
#     row=2,
#     col=1,
# )
st.header("SubActivityTest of AAE-05 Drilling.csv")
st.plotly_chart(fig)