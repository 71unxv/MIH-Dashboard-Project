import plotly.graph_objects as go
from plotly.subplots import make_subplots

PastelColor = ['rgb(102, 197, 204)', 'rgb(246, 207, 113)', 'rgb(248, 156, 116)', 'rgb(220, 176, 242)', 'rgb(135, 197, 95)', 'rgb(158, 185, 243)', 'rgb(254, 136, 177)', 'rgb(201, 219, 116)', 'rgb(139, 224, 164)', 'rgb(180, 151, 231)', 'rgb(179, 179, 179)']

def addWellLogs(fig,data,options,row=1,col=1 ):
    print(options)
    if type(options) == list():
        for sensorName in options:
            fig.add_trace(
                go.Scatter(
                    x=data[sensorName],
                    y=data["dt"],
                    mode="lines",
                    hoverinfo="text",
                    # showlegend=False,
                    # marker=dict(color="crimson", size=4, opacity=0.8)
                    ),
                row=row, col=col
            )
    else:
        fig.add_trace(
            go.Scatter(
                x=data[options],
                y=data["dt"],
                name=options,
                mode="lines",
                hoverinfo='x',
                hovertemplate='%{x} <br> %{y}',
                # showlegend=False,
                # marker=dict(color="crimson", size=4, opacity=0.8)
                ),
            row=row, col=col
        )

    return fig


def addWellClass(fig,data,label, row=1,col=1):
    fig.add_trace(
        go.Heatmap(
                x=[0] * data["dt"].shape[0],
                y=data["dt"].tolist(),
                z=data[label + "_code"].tolist(),
                text=data[label].tolist(),
                hoverinfo="text",
                hovertemplate="%{y} <br> %{text}",
                showscale=False
                # colorbar=dict(title='SubActivity')'plotly',
                # color_discrete_sequence=PastelColor
                # orientation='v'
                ),
        row=row, col=col
    )


    return fig

def updateWellLogs(fig,data,options,row=1,col=1 ):
    # print(options)
    if type(options) == list():
        for sensorName in options:
            fig.update_traces(
                go.Scatter(
                    x=data[sensorName],
                    y=data["dt"],
                    mode="lines",
                    hoverinfo="text",
                    # showlegend=False,
                    # marker=dict(color="crimson", size=4, opacity=0.8)
                    ),
                row=row, col=col
            )
    else:
        fig.update_traces(
            go.Scatter(
                x=data[options],
                y=data["dt"],
                name=options,
                mode="lines",
                hoverinfo='x',
                hovertemplate='%{x} <br> %{y}',
                # showlegend=False,
                # marker=dict(color="crimson", size=4, opacity=0.8)
                ),
            row=row, col=col
        )

    return fig



