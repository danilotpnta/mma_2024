from widgets import scatterplot_3d, scatterplot_2d, filter_view
from dash import callback, Output, Input, State
from Dataset import Dataset
import numpy as np
from Collection import Collection

# Categorical Histograms
def histogram_callback(hist_type, feature, data_selected, figure_hist, radio_button_value, scatterplot_2d_old):
    print(f"{feature} hist is clicked")
    
    if hist_type == 'categorical':
        clicked_category = data_selected['points'][0]['x']
        indices = None
        data_aggr = figure_hist["data"][0]["x"]
    elif hist_type == 'numerical':
        clicked_category = data_selected['points'][0]['binNumber']
        indices = data_selected['points'][0]['pointNumbers']
        data_aggr = range(figure_hist['data'][0]['nbinsx'])
    
    clicked_categories, selected_ids = Collection.update_filter(feature, clicked_category, indices)
    figure_hist['data'][0].update({"marker": {"pattern": {"shape": ["x" if c in clicked_categories else "" for c in data_aggr]}}})
    figure_scatter_2d = scatterplot_2d.create_scatterplot_figure(radio_button_value, set(selected_ids))
    figure_scatter_3d = scatterplot_3d.create_scatterplot_figure(radio_button_value, set(selected_ids))

    f_view = filter_view.create_filter_view(Collection.filters)

    return figure_hist, {'data': figure_scatter_2d['data'], 'layout': scatterplot_2d_old['layout']}, figure_scatter_3d, f_view


@callback(
    [Output("genre_histogram", "figure", allow_duplicate=True),
    Output("scatterplot-2D", "figure", allow_duplicate=True),
    Output("scatterplot-3D", "figure", allow_duplicate=True),
    Output("filter-view", "children", allow_duplicate=True)],
    Input("genre_histogram", "clickData"),
    State("genre_histogram", "figure"),
    State("projection-radio-buttons", "value"),
    State("scatterplot-2D", "figure"),
    prevent_initial_call=True
)
def genre_hist_is_clicked(data_selected, figure_hist, radio_button_value, scatterplot_2d_old):
    return histogram_callback('categorical', 'genre', data_selected, figure_hist, radio_button_value, scatterplot_2d_old)


@callback(
    [Output("key_histogram", "figure", allow_duplicate=True),
    Output("scatterplot-2D", "figure", allow_duplicate=True),
    Output("scatterplot-3D", "figure", allow_duplicate=True),
    Output("filter-view", "children", allow_duplicate=True)],
    Input("key_histogram", "clickData"),
    State("key_histogram", "figure"),
    State("projection-radio-buttons", "value"),
    State("scatterplot-2D", "figure"),
    prevent_initial_call=True
)
def key_hist_is_clicked(data_selected, figure_hist, radio_button_value, scatterplot_2d_old):
    return histogram_callback('categorical', 'key', data_selected, figure_hist, radio_button_value, scatterplot_2d_old)


@callback(
    [Output("tempo_histogram", "figure", allow_duplicate=True),
    Output("scatterplot-2D", "figure", allow_duplicate=True),
    Output("scatterplot-3D", "figure", allow_duplicate=True),
    Output("filter-view", "children", allow_duplicate=True)],
    Input("tempo_histogram", "clickData"),
    State("tempo_histogram", "figure"),
    State("projection-radio-buttons", "value"),
    State("scatterplot-2D", "figure"),
    prevent_initial_call=True
)
def tempo_hist_is_clicked(data_selected, figure_hist, radio_button_value, scatterplot_2d_old):
    return histogram_callback('numerical', 'tempo', data_selected, figure_hist, radio_button_value, scatterplot_2d_old)


@callback(
    [Output("loudness_histogram", "figure", allow_duplicate=True),
    Output("scatterplot-2D", "figure", allow_duplicate=True),
    Output("scatterplot-3D", "figure", allow_duplicate=True),
    Output("filter-view", "children", allow_duplicate=True)],
    Input("loudness_histogram", "clickData"),
    State("loudness_histogram", "figure"),
    State("projection-radio-buttons", "value"),
    State("scatterplot-2D", "figure"),
    prevent_initial_call=True
)
def loudness_hist_is_clicked(data_selected, figure_hist, radio_button_value, scatterplot_2d_old):
    return histogram_callback('numerical', 'loudness', data_selected, figure_hist, radio_button_value, scatterplot_2d_old)