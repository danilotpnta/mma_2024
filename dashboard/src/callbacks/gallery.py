from dash import dcc, html, State, Input, Output, callback, callback_context, ALL
import dash_bootstrap_components as dbc
from widgets import gallery
from Dataset import Dataset
import config
from PIL import Image
from utils.similar_tracks import get_similar_tracks
import plotly.graph_objs as go
from callbacks.scatterplot_3d import update_track


# Assuming 'app' is your Dash app instance

@callback(
    [Output('album-cover', 'src',allow_duplicate=True),
     Output('track-title', 'children',allow_duplicate=True),
     Output('artist', 'children',allow_duplicate=True),
     Output('tempo', 'children',allow_duplicate=True),
     Output("gallery", "children",allow_duplicate=True),
     Output("gallery-card-header", "children",allow_duplicate=True),
     Output('scatterplot-3D', 'figure',allow_duplicate=True)],
     [Input({'type': 'gallery-card', 'index': ALL}, 'n_clicks'),
     Input('projection-radio-buttons', 'value'),
     Input('scatterplot-3D', 'figure')],
     prevent_initial_call='initial_duplicate'
)
def image_clicked(n_clicks, radio_button_value, current_figure):
    n_clicks = [0 if x is None else x for x in n_clicks]
    if sum(n_clicks) > 0:
        track_id = callback_context.triggered_id['index']
        return update_track(track_id, radio_button_value, current_figure)