from dash import callback, Output, Input

@callback(
    Output('track-player', 'src'),
        Input('track-dropdown', 'value'))
def update_song(url):
    return url