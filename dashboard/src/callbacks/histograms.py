from widgets import scatterplot_3d, scatterplot_2d
from dash import callback, Output, Input, State
from Dataset import Dataset
import numpy as np

# Categorical Histograms

@callback(
    [Output("genre_histogram", "figure", allow_duplicate=True),
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


@callback(
    [Output("key_histogram", "figure", allow_duplicate=True),
    Output("scatterplot-2D", "figure", allow_duplicate=True),
    Output("scatterplot-3D", "figure", allow_duplicate=True)],
    Input("key_histogram", "clickData"),
    State("key_histogram", "figure"),
    State("projection-radio-buttons", "value"),
    State("scatterplot-2D", "figure"),
    prevent_initial_call=True
)
def key_hist_is_clicked(data_selected, figure_hist, radio_button_value, scatterplot_2d_old):
    print("key hist clicked")
    d = Dataset.get()
    clicked_category = data_selected['points'][0]['x']
    selected_rows = d[d['key'] == clicked_category]
    figure_hist['data'][0].update({"marker": {"pattern": {"shape": ["x" if c == clicked_category else "" for c in figure_hist["data"][0]["x"]]}}})
    figure_scatter_2d = scatterplot_2d.highlight_markers_on_scatterplot(set(selected_rows['id']), radio_button_value)
    figure_scatter_3d = scatterplot_3d.highlight_markers_on_scatterplot(set(selected_rows['id']), radio_button_value)
    return figure_hist, {'data': figure_scatter_2d['data'], 'layout': scatterplot_2d_old['layout']}, figure_scatter_3d


# Numerical Histograms

@callback(
    [Output("tempo_histogram", "figure", allow_duplicate=True),
    Output("scatterplot-2D", "figure", allow_duplicate=True),
    Output("scatterplot-3D", "figure", allow_duplicate=True)],
    Input("tempo_histogram", "clickData"),
    State("tempo_histogram", "figure"),
    State("projection-radio-buttons", "value"),
    State("scatterplot-2D", "figure"),
    prevent_initial_call=True
)
def tempo_hist_is_clicked(data_selected, figure_hist, radio_button_value, scatterplot_2d_old):
    print("Tempo hist clicked")

    d = Dataset.get()
    binned_values = np.array(figure_hist['data'][0]['x'])[data_selected['points'][0]['pointNumbers']]
    selected_rows = d[d['tempo'].isin(binned_values)]
    
    category = data_selected['points'][0]['binNumber']
    figure_hist['data'][0].update({"marker": {"pattern": {"shape": ["x" if c == category else "" for c in range(figure_hist['data'][0]['nbinsx'])]}}})
    figure_scatter_2d = scatterplot_2d.highlight_markers_on_scatterplot(set(selected_rows['id']), radio_button_value)
    figure_scatter_3d = scatterplot_3d.highlight_markers_on_scatterplot(set(selected_rows['id']), radio_button_value)
    return figure_hist, {'data': figure_scatter_2d['data'], 'layout': scatterplot_2d_old['layout']}, figure_scatter_3d


@callback(
    [Output("loudness_histogram", "figure", allow_duplicate=True),
    Output("scatterplot-2D", "figure", allow_duplicate=True),
    Output("scatterplot-3D", "figure", allow_duplicate=True)],
    Input("loudness_histogram", "clickData"),
    State("loudness_histogram", "figure"),
    State("projection-radio-buttons", "value"),
    State("scatterplot-2D", "figure"),
    prevent_initial_call=True
)
def loudness_hist_is_clicked(data_selected, figure_hist, radio_button_value, scatterplot_2d_old):
    print("loudness hist clicked")
    
    d = Dataset.get()
    print(d.columns)
    binned_values = np.array(figure_hist['data'][0]['x'])[data_selected['points'][0]['pointNumbers']]
    selected_rows = d[d['loudness'].isin(binned_values)]
    
    category = data_selected['points'][0]['binNumber']
    figure_hist['data'][0].update({"marker": {"pattern": {"shape": ["x" if c == category else "" for c in range(figure_hist['data'][0]['nbinsx'])]}}})
    figure_scatter_2d = scatterplot_2d.highlight_markers_on_scatterplot(set(selected_rows['id']), radio_button_value)
    figure_scatter_3d = scatterplot_3d.highlight_markers_on_scatterplot(set(selected_rows['id']), radio_button_value)
    return figure_hist, {'data': figure_scatter_2d['data'], 'layout': scatterplot_2d_old['layout']}, figure_scatter_3d