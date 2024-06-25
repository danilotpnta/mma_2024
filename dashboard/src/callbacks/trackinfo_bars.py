from dash import dcc, html, ClientsideFunction, clientside_callback
from dash.dependencies import Input, Output, State

# Register the JavaScript function
clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='resize_track_info_bars'),
    Output('invisible-store', 'data'),
    Input('scatterplot-3D', 'clickData'),
    State('invisible-store', 'data'),
)