import os
import pathlib
import time

import dash
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dotenv import load_dotenv

from api import get_gps_data, get_temp_data

DOTENV_FILE = pathlib.Path(__file__).resolve().parent.joinpath(".env").resolve()
load_dotenv(DOTENV_FILE)
GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 10000)

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "RPI GPS Monitor"

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [html.H6("GPS MONITOR")],
                ),
                dcc.Graph(
                    id="gps-monitor",
                    figure=dict(
                        layout=dict(
                            plot_bgcolor=app_color["graph_bg"],
                            paper_bgcolor=app_color["graph_bg"],
                        )
                    ),
                ),
                dcc.Interval(
                    id="gps-monitor-update",
                    interval=int(GRAPH_INTERVAL),
                    n_intervals=0,
                ),
                html.Div(
                    [html.H6("TEMP MONITOR")],
                ),
                dcc.Graph(
                    id="temp-monitor",
                    figure=dict(
                        layout=dict(
                            plot_bgcolor=app_color["graph_bg"],
                            paper_bgcolor=app_color["graph_bg"],
                        )
                    ),
                ),
            ]
        )
    ]
)


@app.callback(
    Output("gps-monitor", "figure"), [Input("gps-monitor-update", "n_intervals")]
)
def gen_gps_monitor(interval):
    end = time.time()
    df = get_gps_data(end - 300, end)

    # fig = go.Figure(
    #    data=[
    #        go.Scattermapbox(
    #            lat=df["lat"],
    #            lon=df["lon"],
    #            mode="markers+lines",
    #            # mapbox_style="open-street-map",
    #        )
    #    ],
    # )
    # fig.update_layout(mapbox_style="open-street-map")

    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        zoom=18,
        mapbox_style="open-street-map",
        color="alt",
    )
    fig.update_layout(uirevision=True)

    return fig


@app.callback(
    Output("temp-monitor", "figure"), [Input("gps-monitor-update", "n_intervals")]
)
def gen_temp_monitor(interval):
    end = time.time()
    df = get_temp_data(end - 60 * 60 * 24, end)
    df["datetime"] = pd.to_datetime(df["timestamp"], unit="s", utc=True) + pd.Timedelta(
        "9:00:00"
    )
    df["avg"] = df["degC"].rolling(60, center=True).mean()

    fig = px.scatter(
        df,
        x="datetime",
        y=["degC", "avg"],
    )
    fig.update_layout(uirevision=True)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
