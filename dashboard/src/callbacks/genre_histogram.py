from widgets import scatterplot_3d, scatterplot_2d
from dash import callback, Output, Input, State
from Dataset import Dataset


@callback(
    Output("genre_histogram", "figure"),
    Input("genre_histogram", "clickData"),
    State("genre_histogram", "figure"),
    prevent_initial_call=True
)
def genre_hist_is_clicked(data_selected, figure):
    print("Genre hist clicked")
    print(data_selected)
    
    d = Dataset.get()
    figure["data"][0]["marker"]["color"] = ["red" if c == data_selected['points'][0]['x'] else "blue" for c in figure["data"][0]["x"]]
    
    return figure