import dash_bootstrap_components as dbc
from dash import (
    html,
    dcc,
    Input,
    Output,
    State,
    callback,
    no_update,
    ALL,
    callback_context,
)

from widgets import (
    scatterplot_2d,
    scatterplot_3d,
    track_info,
    categorical_histogram,
    numerical_histogram,
    filter_view,
)
from Collection import Collection
from utils.utils import feature_key_from_state_string


def create_deselect_button():

    return dbc.Button("Deselect All", id="deselect-button")


@callback(
    Output("scatterplot-2D", "figure"),
    Output("scatterplot-3D", "figure"),
    Output("track-info", "children"),
    Output({"type": "histogram", "feature": ALL}, "figure", allow_duplicate=True),
    Output("filter-view", "children"),
    Input("deselect-button", "n_clicks"),
    State("projection-radio-buttons", "value"),
    State({"type": "histogram", "feature": ALL}, "figure"),
    prevent_initial_call=True,
)
def deselect_all(n_clicks, radio_button_value, _):

    # print(n_clicks)
    if n_clicks is None:
        return no_update, no_update, no_update
    else:

        hist_dict = {
            feature_key_from_state_string(k): v
            for k, v in callback_context.states.items()
            if "histogram" in k
        }

        Collection.load()

        fig_2d = scatterplot_2d.create_scatterplot_figure(radio_button_value)
        fig_3d = scatterplot_3d.create_scatterplot_figure(radio_button_value)
        track_info_widget = track_info.create_track_info_widget()

        hist_dict["genre"] = categorical_histogram.draw_histogram("genre")
        hist_dict["tempo"] = numerical_histogram.draw_histogram("tempo", nbins=30)
        hist_dict["key"] = categorical_histogram.draw_histogram("key")
        hist_dict["loudness"] = numerical_histogram.draw_histogram("loudness", nbins=20)

        filter_widget = filter_view.draw_filter_view()

        return (
            fig_2d,
            fig_3d,
            track_info_widget,
            list(hist_dict.values()),
            filter_widget,
        )
