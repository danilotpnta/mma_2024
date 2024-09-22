import numpy as np
from Dataset import Dataset
from Collection import Collection
from utils.utils import feature_key_from_state_string
from widgets import scatterplot_3d, scatterplot_2d, filter_view
from dash import callback, Output, Input, State, MATCH, callback_context, ALL, Patch


@callback(
    Output({"type": "histogram", "feature": ALL}, "figure", allow_duplicate=True),
    Output("scatterplot-2D", "figure", allow_duplicate=True),
    Output("scatterplot-3D", "figure", allow_duplicate=True),
    Output("filter-view", "children", allow_duplicate=True),
    Input({"type": "histogram", "feature": ALL}, "clickData"),
    State({"type": "histogram", "feature": ALL}, "figure"),
    State("projection-radio-buttons", "value"),
    State("scatterplot-2D", "figure"),
    State("scatterplot-3D", "figure"),
    prevent_initial_call=True,
)
def hist_is_clicked(
    data_selected, _, radio_button_value, scatterplot_2d_old, scatterplot_3d_old
):

    feature = callback_context.triggered_id["feature"]
    hist_dict = {
        feature_key_from_state_string(k): v
        for k, v in callback_context.states.items()
        if "histogram" in k
    }
    data_selected = data_selected[list(hist_dict.keys()).index(feature)]

    # print(f"{feature} hist is clicked")
    # print(callback_context.triggered_id)
    # print(callback_context.triggered_prop_ids)

    if feature in ["loudness", "tempo"]:
        hist_type = "numerical"
    elif feature in ["genre", "key"]:
        hist_type = "categorical"

    if hist_type == "categorical":
        clicked_category = data_selected["points"][0]["x"]

        # Compatibilty for numerical hists
        clicked_category_bin = clicked_category
        indices = None
        # data_aggr = [i["x"] for i in hist_dict[feature]["data"]][0]
        data_aggr = hist_dict[feature]["data"][0]["x"]

    elif hist_type == "numerical":
        clicked_category = data_selected["points"][0]["binNumber"]
        center_value = data_selected["points"][0]["x"]
        bin_range = 5 if feature == "tempo" else 2
        clicked_category_bin = (
            f"{(center_value - bin_range):.2f} - {(center_value + bin_range):.2f}"
        )
        indices = data_selected["points"][0]["pointNumbers"]
        data_aggr = range(hist_dict[feature]["data"][0]["nbinsx"])

    clicked_categories, selected_ids = Collection.update_filter(
        feature, [clicked_category, clicked_category_bin], indices
    )

    hist_dict[feature]["data"][0]["marker"].update(
        {
            "pattern": {
                "shape": ["x" if c in clicked_categories else "" for c in data_aggr]
            }
        }
    )
    figure_scatter_2d = scatterplot_2d.create_scatterplot_figure(
        radio_button_value, set(selected_ids)
    )
    figure_scatter_3d = scatterplot_3d.create_scatterplot_figure(
        radio_button_value, set(selected_ids)
    )

    f_view = filter_view.create_filter_view(Collection.filters)

    fig_2d = Patch()
    fig_2d["data"] = figure_scatter_2d["data"]
    fig_3d = Patch()
    fig_3d["data"] = figure_scatter_3d["data"]

    # Using old layout to maintain selection window after update
    return list(hist_dict.values()), fig_2d, fig_3d, f_view


# return list(hist_dict.values()), {'data': figure_scatter_2d['data'], 'layout': scatterplot_2d_old['layout']}, {'data': figure_scatter_3d['data'], 'layout': scatterplot_3d_old['layout']}, f_view
