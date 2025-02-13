import math
from pathlib import Path
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import time


# CSV STUFF:
X_COLUMN = "timestamp"
Y_COLUMN = "value"
CSV_FILE_PATH = Path("sample_data.csv").expanduser().resolve()

# OTHER STUFF
MAX_DATA_POINTS = 1000
SHORT_WINDOW_SECONDS = 60
LONG_WINDOW_SECONDS = 300
REFRESH_INTERVAL = 200  # in milliseconds


# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div(
    [
        dcc.Graph(id="live-graph-short-window"),
        dcc.Graph(id="live-graph-long-window"),
        dcc.Graph(id="live-graph-all"),
        dcc.Interval(
            id="interval-component",
            interval=REFRESH_INTERVAL,
            n_intervals=0,
        ),
    ],
)


# Callback to update graphs
@app.callback(
    Output("live-graph-all", "figure"), 
    Output("live-graph-short-window", "figure"), 
    Output("live-graph-long-window", "figure"),
    Input("interval-component", "n_intervals")
)
def update_graphs(n):
    # Read the CSV file
    try:
        df = pd.read_csv(
            CSV_FILE_PATH,
            parse_dates=[
                X_COLUMN,
            ],
        )
    except FileNotFoundError:
        return (
            {"data": [], "layout": {"title": "CSV file not found"}},
            {"data": [], "layout": {"title": "CSV file not found"}},
            {"data": [], "layout": {"title": "CSV file not found"}}
        )

    df_all = df
    df_short_window = df[df[X_COLUMN] > df[X_COLUMN].max() - pd.Timedelta(seconds=SHORT_WINDOW_SECONDS)]
    df_long_window = df[df[X_COLUMN] > df[X_COLUMN].max() - pd.Timedelta(seconds=LONG_WINDOW_SECONDS)]

    # If the data is too long, take equally spaced subsets
    if len(df_all) > MAX_DATA_POINTS:
        df_all = df_all.iloc[:: math.ceil(len(df_all) / MAX_DATA_POINTS)]
    if len(df_short_window) > MAX_DATA_POINTS:
        df_short_window = df_short_window.iloc[:: math.ceil(len(df_short_window) / MAX_DATA_POINTS)]
    if len(df_long_window) > MAX_DATA_POINTS:
        df_long_window = df_long_window.iloc[:: math.ceil(len(df_long_window) / MAX_DATA_POINTS)]

    # df_short_window: pd.DataFrame = df_short_window
    # df_last_600_seconds: pd.DataFrame = df_long_window

    # print(f"{len(df_short_window)=} {len(df_last_600_seconds)=} {len(df_all)=}")
    
    # Create the figures
    fig_all = {
        "data": [
            {
                "x": df_all[X_COLUMN],
                "y": df_all[Y_COLUMN],
                "type": "line",
                "name": "Data",
            }
        ],
        "layout": {
            "title": "Live CSV Data (all)",
            "xaxis": {"title": "Time"},
            "yaxis": {"title": "Value"},
        },
    }

    fig_short_window = {
        "data": [
            {
                "x": df_short_window[X_COLUMN],
                "y": df_short_window[Y_COLUMN],
                "type": "line",
                "name": "Data",
            }
        ],
        "layout": {
            "title": f"Live CSV Data (Last {SHORT_WINDOW_SECONDS:,} seconds)",
            "xaxis": {"title": "Time"},
            "yaxis": {"title": "Value"},
        },
    }

    fig_long_window = {
        "data": [
            {
                "x": df_long_window[X_COLUMN],
                "y": df_long_window[Y_COLUMN],
                "type": "line",
                "name": "Data",
            }
        ],
        "layout": {
            "title": f"Live CSV Data (Last {LONG_WINDOW_SECONDS:,} seconds)",
            "xaxis": {"title": X_COLUMN},
            "yaxis": {"title": Y_COLUMN},
        },
    }

    return (
        fig_all,
        fig_short_window,
        fig_long_window,
    )


if __name__ == "__main__":
    print(f"Tailing {CSV_FILE_PATH}")
    app.run_server(debug=True, port=5000)
