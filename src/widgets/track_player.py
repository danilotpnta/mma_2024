from dash import Dash, dcc
import dash_html_components as html


tracks = {
    "Gorillaz - Feel Good Inc": "assets/Gorillaz.mp3",
    "Picasso - Lion's Roar": "assets/Picasso.mp3"
}

def create_track_player():
    return html.Div([
        dcc.Dropdown(
            id='track-dropdown',
            options=[{'label': track, 'value': url} for track, url in tracks.items()],
            value=list(tracks.values())[0]
        ),
        html.Audio(id='track-player', controls=True, src="assets/Picasso.mp3")
    ])