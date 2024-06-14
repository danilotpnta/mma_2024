from Dataset import Dataset
from dash import dcc, html
import dash_bootstrap_components as dbc

def create_track_table():

    album_cover = html.Img(id='album-cover', src='assets/plain_cover.jpg')

    track_title = html.Div(id='track-title', children='')
    artist = html.Div(id='artist', children='')
    genre = html.Div(id='genre', children='')
    tempo = html.Div(id='tempo', children='')

    row = dbc.Row([
        dbc.Col(album_cover, width=4),
        dbc.Col([
            html.H3("Track Info"),
            track_title,
            artist,
            genre,
            tempo
        ], width=8)
    ])
    
    return row