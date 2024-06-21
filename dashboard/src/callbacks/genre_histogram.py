from widgets import scatterplot_3d, scatterplot_2d
from dash import callback, Output, Input, State
from Dataset import Dataset


@callback(
    [Output("genre_histogram", "figure", allow_duplicate=True),
    #  Output("tempo_histogram", "figure", allow_duplicate=True),
    Output("scatterplot-2D", "figure", allow_duplicate=True),
    Output("scatterplot-3D", "figure", allow_duplicate=True)],
    Input("genre_histogram", "clickData"),
    State("genre_histogram", "figure"),
    State("projection-radio-buttons", "value"),
    State("scatterplot-2D", "figure"),
    prevent_initial_call=True
)
def genre_hist_is_clicked(data_selected, figure_hist, radio_button_value, scatterplot_2d_old):
    print("Genre hist clicked")
    d = Dataset.get()
    clicked_category = data_selected['points'][0]['x']
    selected_rows = d[d['genre'] == clicked_category]
    # figure_hist['data'][0].update({"marker": {"color":["red" if c == clicked_category else "blue" for c in figure_hist["data"][0]["x"]]}})
    figure_hist['data'][0].update({"marker": {"pattern": {"shape": ["x" if c == clicked_category else "" for c in figure_hist["data"][0]["x"]]}}})
    figure_scatter_2d = scatterplot_2d.highlight_markers_on_scatterplot(set(selected_rows['id']), radio_button_value)
    figure_scatter_3d = scatterplot_3d.highlight_markers_on_scatterplot(set(selected_rows['id']), radio_button_value)
    return figure_hist, {'data': figure_scatter_2d['data'], 'layout': scatterplot_2d_old['layout']}, figure_scatter_3d