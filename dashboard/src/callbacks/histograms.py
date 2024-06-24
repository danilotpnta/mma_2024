from widgets import scatterplot_3d, scatterplot_2d, filter_view
from dash import callback, Output, Input, State
from Dataset import Dataset
import numpy as np
from Collection import Collection

# Categorical Histograms

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
    print("Genre hist clicked")
    clicked_category = data_selected['points'][0]['x']
    Collection.add_filter('genre', clicked_category)
    selected_ids = Collection.get_filter_selection_ids()
    print(f'Length of selected ids after selecting a genre: {len(selected_ids)}')

    # figure_hist['data'][0].update({"marker": {"color":["red" if c == clicked_category else "blue" for c in figure_hist["data"][0]["x"]]}})
    figure_hist['data'][0].update({"marker": {"pattern": {"shape": ["x" if c == clicked_category else "" for c in figure_hist["data"][0]["x"]]}}})
    figure_scatter_2d = scatterplot_2d.create_scatterplot_figure(radio_button_value, set(selected_ids))
    figure_scatter_3d = scatterplot_3d.create_scatterplot_figure(radio_button_value, set(selected_ids))

    f_view = filter_view.create_filter_view(Collection.filters)

    return figure_hist, {'data': figure_scatter_2d['data'], 'layout': scatterplot_2d_old['layout']}, figure_scatter_3d, f_view


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
    print("key hist clicked")
    clicked_category = data_selected['points'][0]['x']

    Collection.add_filter('key', clicked_category)
    selected_ids = Collection.get_filter_selection_ids()
    print(f'Length of selected ids after selecting a key: {len(selected_ids)}')

    figure_hist['data'][0].update({"marker": {"pattern": {"shape": ["x" if c == clicked_category else "" for c in figure_hist["data"][0]["x"]]}}})
    figure_scatter_2d = scatterplot_2d.create_scatterplot_figure(radio_button_value, set(selected_ids))
    figure_scatter_3d = scatterplot_3d.create_scatterplot_figure(radio_button_value, set(selected_ids))

    f_view = filter_view.create_filter_view(Collection.filters)
    return figure_hist, {'data': figure_scatter_2d['data'], 'layout': scatterplot_2d_old['layout']}, figure_scatter_3d, f_view


# Numerical Histograms

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
    print("Tempo hist clicked")

    indices = data_selected['points'][0]['pointNumbers']
    category = data_selected['points'][0]['x']
    Collection.add_filter('tempo', category, indices=indices)
    selected_ids = Collection.get_filter_selection_ids()

    print(f'Length of selected ids after selecting a tempo: {len(selected_ids)}')
    
    figure_hist['data'][0].update({"marker": {"pattern": {"shape": ["x" if c == category else "" for c in range(figure_hist['data'][0]['nbinsx'])]}}})
    figure_scatter_2d = scatterplot_2d.create_scatterplot_figure(radio_button_value, set(selected_ids))
    figure_scatter_3d = scatterplot_3d.create_scatterplot_figure(radio_button_value, set(selected_ids))

    f_view = filter_view.create_filter_view(Collection.filters)

    return figure_hist, {'data': figure_scatter_2d['data'], 'layout': scatterplot_2d_old['layout']}, figure_scatter_3d, f_view


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
    print("loudness hist clicked")

    indices = data_selected['points'][0]['pointNumbers']
    category = data_selected['points'][0]['x']
    Collection.add_filter('loudness', category, indices=indices)
    selected_ids = Collection.get_filter_selection_ids()

    print(f'Length of selected ids after selecting a loudness: {len(selected_ids)}')
    
    figure_hist['data'][0].update({"marker": {"pattern": {"shape": ["x" if c == category else "" for c in range(figure_hist['data'][0]['nbinsx'])]}}})
    figure_scatter_2d = scatterplot_2d.create_scatterplot_figure(radio_button_value, set(selected_ids))
    figure_scatter_3d = scatterplot_3d.create_scatterplot_figure(radio_button_value, set(selected_ids))

    f_view = filter_view.create_filter_view(Collection.filters)

    return figure_hist, {'data': figure_scatter_2d['data'], 'layout': scatterplot_2d_old['layout']}, figure_scatter_3d, f_view