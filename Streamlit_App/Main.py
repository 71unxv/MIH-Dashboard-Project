import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider
import LogsDisp


st.set_page_config(page_title="PDU Realtime Operation", page_icon=None, layout="wide",)
PageList = [
    "Realtime Analysis",
    "Realtime Editing",
    "Activity Summary"
]
NavBar = st.sidebar.selectbox("Select Module:",PageList)

@st.cache
def get_data(Filepath):
    Realtime_DB = pd.read_csv(Filepath).sort_values(by='dt_DF')
    Realtime_DB.SubActivity_Predict = pd.Categorical(Realtime_DB.SubActivity_Predict)
    Realtime_DB['SubActivity_Predict_code'] = Realtime_DB.SubActivity_Predict.cat.codes

    return Realtime_DB

Realtime_DB = get_data("Data\\Merged\\Merge_DrillTrip_AAE-02.csv")

st.markdown(
    """
    # PDU Realtime Operation
    """
)

# below should be Realtime Monitoring
HeaderColumn = st.columns((0.9,2,2,2,9))
# my_expander = st.expander("Expand")
# with my_expander:
    # clicked = my_widget("second")
with HeaderColumn[1]:
    option_a = st.multiselect(
        'Display Sensor',
        ["bitdepth",
        "md",
        "blockpos",
        "rop",
        "hklda",
        "woba",
        "torqa",
        "rpm",
        "stppress",
        "mudflowin"],
        ['rop'],
        key='plot_a', 
        )
    for i in option_a:
        print(i)
        print(type(i))
    # st.write('You selected:', option_a)
with HeaderColumn[2]:
    option_b = st.multiselect(
        'Display Sensor',
        ["bitdepth",
        "md",
        "blockpos",
        "rop",
        "hklda",
        "woba",
        "torqa",
        "rpm",
        "stppress",
        "mudflowin"],
        ['hklda'],
        key='plot_b', 
        )
    # st.write('You selected:', option_b)
with HeaderColumn[3]:
    option_c = st.multiselect(
        'Display Sensor',
        ["bitdepth",
        "md",
        "blockpos",
        "rop",
        "hklda",
        "woba",
        "torqa",
        "rpm",
        "stppress",
        "mudflowin"],
        ['hklda'],
        key='plot_c',
        )
    # st.write('You selected:', option_c)

VizColumn = st.columns((12,3))
with VizColumn[0]:
# Initialize figure with subplots
    fig = make_subplots(
        rows=1, cols=7,
        column_widths=[0.2, 0.2,0.2, 0.1, 0.1, 0.1, 0.1],
        # row_heights=[0.4, 0.6],
        specs=[
                [{"type": "scatter"}, 
                {"type": "scatter"}, 
                {"type": "scatter"},
                {"type": "bar"},
                {"type": "bar"},
                {"type": "bar"},
                {"type": "bar"},
                ]
            ],
        shared_yaxes=True,
        horizontal_spacing=0.01,
        subplot_titles = ['gadfdfs1','asd2','asd3'],
        row_titles = ['gadfdfs1','asd2','asd3'],
        column_titles =['gadfdfs1','asd2','asd3']
        )
    fig = LogsDisp.addWellLogs(fig,Realtime_DB,option_a,row=1,col=1)
    fig = LogsDisp.addWellLogs(fig,Realtime_DB,option_b,row=1,col=2)
    fig = LogsDisp.addWellLogs(fig,Realtime_DB,option_c,row=1,col=3)
    # fig.add_trace(
    #     go.Scatter(
    #         x=Realtime_DB["rpm"],
    #         y=Realtime_DB["dt_DF"],
    #         mode="lines",
    #         hoverinfo="text",
    #         # showlegend=False,
    #         # marker=dict(color="crimson", size=4, opacity=0.8)
    #         ),
    #     row=1, col=1
    # )
    # fig.add_trace(
    #     go.Scatter(
    #         y=Realtime_DB["dt_DF"],
    #         x=Realtime_DB["stppress"],
    #         mode="lines",
    #         hoverinfo="text",
    #         # showlegend=False,
    #         # marker=dict(color="crimson", size=4, opacity=0.8)
    #         ),
    #     row=1, col=2
    # )
    # fig.add_trace(
    #     go.Scatter(
    #         y=Realtime_DB["dt_DF"],
    #         x=Realtime_DB["hklda"],
    #         mode="lines",
    #         hoverinfo="text",
    #         # showlegend=False,
    #         # marker=dict(color="crimson", size=4, opacity=0.8)
    #         ),
    #     row=1, col=3
    # )

    fig.update_layout(
        autosize=False,
        width=500,
        height=1000,
        xaxis=dict(
            fixedrange=True
        )
    )
    fig.add_trace(
        go.Heatmap(
                x=[0] * Realtime_DB["dt_DF"].shape[0],
                y=Realtime_DB["dt_DF"].tolist(),
                z=Realtime_DB["SubActivity_Predict_code"].tolist(),
                # orientation='v'
                ),
        row=1, col=4
    )
    fig.add_trace(
        go.Heatmap(
                x=[0] * Realtime_DB["dt_DF"].shape[0],
                y=Realtime_DB["dt_DF"].tolist(),
                z=Realtime_DB["SubActivity_Predict_code"].tolist(),
                # orientation='v'
                ),
        row=1, col=5
    )
    fig.add_trace(
        go.Heatmap(
                x=[0] * Realtime_DB["dt_DF"].shape[0],
                y=Realtime_DB["dt_DF"].tolist(),
                z=Realtime_DB["SubActivity_Predict_code"].tolist(),
                # orientation='v'
                ),
        row=1, col=6
    )


    st.plotly_chart(fig,use_container_width=True)
        
    




