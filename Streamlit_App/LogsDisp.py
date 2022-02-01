import plotly.graph_objects as go
from plotly.subplots import make_subplots


def addWellLogs(fig,data,options,row=1,col=1 ):
    for sensorName in options:
        fig.add_trace(
            go.Scatter(
                x=data[sensorName],
                y=data["dt_DF"],
                mode="lines",
                hoverinfo="text",
                # showlegend=False,
                # marker=dict(color="crimson", size=4, opacity=0.8)
                ),
            row=row, col=col
        )
    return fig
