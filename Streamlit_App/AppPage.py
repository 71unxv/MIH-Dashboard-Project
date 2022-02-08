import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import LogsDisp

def RealtimeSelection():
    HeaderColumn = st.columns((0.9,2,2,2,9))
    with HeaderColumn[1]:
        option_a = st.selectbox(
            'sensor:',
            ("bitdepth",
            "md",
            "blockpos",
            "rop",
            "hklda",
            "woba",
            "torqa",
            "rpm",
            "stppress",
            "mudflowin"),
            7,
            key='plot_a'
            )

        # st.write('You selected:', option_a)
    with HeaderColumn[2]:
        option_b = st.selectbox(
            'sensor:',
            ("bitdepth",
            "md",
            "blockpos",
            "rop",
            "hklda",
            "woba",
            "torqa",
            "rpm",
            "stppress",
            "mudflowin"),
            4,
            key='plot_b'
            )
        # st.write('You selected:', option_b)
    with HeaderColumn[3]:
        option_c = st.selectbox(
            'sensor:',
            ("bitdepth",
            "md",
            "blockpos",
            "rop",
            "hklda",
            "woba",
            "torqa",
            "rpm",
            "stppress",
            "mudflowin"),
            5,
            key='plot_c'
            )
        # st.write('You selected:', option_c)
    return HeaderColumn
def RealtimeViewer(Realtime_DB,option_a,option_b,option_c):

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
            # subplot_titles = ['gadfdfs1','asd2','asd3'],
            row_titles = ["Date - Time"],
            column_titles =[option_a,option_b,option_c]
            )


        fig.update_layout(
        # update layout
            showlegend=False,
            # autosize=False,
            
            width=500,
            height=1000,
            hovermode="y unified",
            # xaxis=dict(
            #     fixedrange=True
            # )
            yaxis=dict(
                autorange='reversed'
            )
        )
        # display Sensor logs
        fig = LogsDisp.addWellLogs(fig,Realtime_DB,option_a,row=1,col=1)
        fig = LogsDisp.addWellLogs(fig,Realtime_DB,option_b,row=1,col=2)
        fig = LogsDisp.addWellLogs(fig,Realtime_DB,option_c,row=1,col=3)


        #% display Activity label
        fig = LogsDisp.addWellClass(fig,Realtime_DB,"LABEL_ConnectionActivity",row=1,col=4)
        fig = LogsDisp.addWellClass(fig,Realtime_DB,"LABEL_SubActivity",row=1,col=5)
        fig = LogsDisp.addWellClass(fig,Realtime_DB,"LABEL_Activity",row=1,col=6)

        st.plotly_chart(fig,use_container_width=True)

    return Realtime_DB, fig