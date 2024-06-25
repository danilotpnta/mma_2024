from Dataset import Dataset
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np

def create_track_info():

    album_cover = html.Img(id='album-cover',
                            style={'width': '100%', 'height': 'auto'},
                            src='', className='border border-dark rounded')

    track_title = html.Tr([html.Td(html.Strong('Title'), style={'width': '40%'}), html.Td(id='track-title', children='')])
    artist = html.Tr([html.Td(html.Strong('Artist')), html.Td(id='artist', children='')])
    genre = html.Tr([html.Td(html.Strong('Genre')), html.Td(id='genre', children=create_barplot('genre'))])
    tempo = html.Tr([html.Td(html.Strong('Tempo (bpm)')), html.Td(id='tempo', children='')])
    key = html.Tr([html.Td(html.Strong('Key')), html.Td(id='key', children=create_barplot('key'))])
    loudness = html.Tr([html.Td(html.Strong('Loudness')), html.Td(children='-40dB')])

    table_body = [html.Tbody([track_title, artist, genre, tempo, key, loudness])]

    row = dbc.Row([
        dbc.Col(album_cover, width={"size": 2, 'offset': 2}),
        dbc.Col(
            dbc.Table(
                table_body,
                hover=True,
                responsive=False,
                striped=True,
                className='table'
            ), 
            width={"size": 6}
        )
    ])
    
    return row


def create_barplot(feature):
    
    if feature == 'key':
        data = [60, 30, 10]
        classif = ["A", "B#m", "F#"]
    elif feature == 'genre':
        data = [80, 15, 5]
        classif = ["Pop", "Hip-Hop", "Classical"]

    progress = html.Div(children=[
            html.Div(f"{classif[0]} ({data[0]}%)", className=f'cool {feature}_1'),
            html.Div(f"{classif[1]} ({data[1]}%)", className=f'cool {feature}_2'),
            html.Div(f"{classif[2]} ({data[2]}%)", className=f'cool {feature}_3'),
        ],
        className="wraap"
    )
    return progress