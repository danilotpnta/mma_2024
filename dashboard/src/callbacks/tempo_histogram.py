from widgets import scatterplot_3d, scatterplot_2d
from dash import callback, Output, Input, State
from Dataset import Dataset


@callback(
    Output("tempo_histogram", "figure"),
    Input("tempo_histogram", "clickData"),
    State("tempo_histogram", "figure"),
    prevent_initial_call=True
)
def tempo_hist_is_clicked(data_selected, figure):
    print("Tempo hist clicked")

    d = Dataset.get()
    print(data_selected['points'][0]['x'])
    print(figure["data"][0]["x"])
    figure["data"][0]["marker"]["color"] = ["red" if c == data_selected['points'][0]['x'] else "blue" for c in figure["data"][0]["x"]]
    
    return figure