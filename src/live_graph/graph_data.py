import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import time

# CSV file path
CSV_FILE_PATH = "sample_data.csv"
# Number of lines to tail
TAIL_LINES = 1000

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div(
    [
        dcc.Graph(id="live-graph"),
        dcc.Interval(
            id="interval-component",
            interval=1 * 100,  # in milliseconds
            n_intervals=0,
        ),
    ],
)


# Callback to update graph
@app.callback(
    Output("live-graph", "figure"), Input("interval-component", "n_intervals")
)
def update_graph(n):
    # Read the CSV file
    try:
        df = pd.read_csv(CSV_FILE_PATH)
    except FileNotFoundError:
        return {"data": [], "layout": {"title": "CSV file not found"}}

    # Tail the last few lines
    df_tail = df.tail(TAIL_LINES)

    # Create the figure
    fig = {
        "data": [
            {
                # "x": df_tail.index,
                "x": df_tail[
                    df_tail.columns[0]
                ],
                "y": df_tail[
                    df_tail.columns[2]
                ],
                "type": "line",
                "name": "Data",
            }
        ],
        "layout": {
            "title": "Live CSV Data",
            "xaxis": {"title": "Time"},
            "yaxis": {"title": "Value"},
        },
    }
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=5000)
