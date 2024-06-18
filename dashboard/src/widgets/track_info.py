from Dataset import Dataset
from dash import dcc, html
import dash_bootstrap_components as dbc

def create_track_info():

    album_cover = html.Img(id='album-cover', style={'max-width': '90%'}, src='')

    track_title = dbc.Row([html.H4('Title:'), html.Div(id='track-title', children='')])
    artist = dbc.Row([html.H4('Artist:'),html.Div(id='artist', children='')])
    genre = dbc.Row([html.H4('Genre:'), html.Div(id='genre', children='')])
    tempo = dbc.Row([html.H4('Genre:'), html.Div(id='tempo', children='')])

    row = dbc.Row([
        dbc.Col(album_cover, width=8),
        dbc.Col([
            html.H3("Track Info"),
            track_title,
            artist,
            genre,
            tempo
        ], width=1)
    ])
    
    return row