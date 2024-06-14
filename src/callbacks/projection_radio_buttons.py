from src.widgets import scatterplot_3d
from dash import callback, Output, Input


@callback(
    Output("scatterplot-3D", "figure", allow_duplicate=True),
    Input("projection-radio-buttons", "value"),
    prevent_initial_call=True,
)
def projection_radio_is_clicked(radio_button_value):

    print("Radio button clicked")

    return scatterplot_3d.create_scatterplot_figure(radio_button_value)