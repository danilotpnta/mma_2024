from widgets import scatterplot_3d, scatterplot_2d
from dash import callback, Output, Input, State
from Dataset import Dataset


@callback(
    Output("tempo_histogram", "figure", allow_duplicate=True),
    Input("tempo_histogram", "clickData"),
    State("tempo_histogram", "figure"),
    prevent_initial_call=True
)
def tempo_hist_is_clicked(data_selected, figure):
    print("Tempo hist clicked")

    d = Dataset.get()
    figure["data"][0]["marker"]["color"] = ["red" if i == data_selected['points'][0]['binNumber'] else "blue" for i in range(figure['data'][0]['nbinsx'])]
    return figure