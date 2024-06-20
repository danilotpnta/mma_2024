from Dataset import Dataset
from dash import dcc, html
import dash_bootstrap_components as dbc

def create_track_info():

    album_cover = html.Img(id='album-cover',
                            style={'width': '100%', 'height': 'auto'},
                            src='', className='border border-dark rounded')

    track_title = html.Tr([html.Td(html.Strong('Title'), style={'width': '40%'}), html.Td(id='track-title', children='')])
    artist = html.Tr([html.Td(html.Strong('Artist')), html.Td(id='artist', children='')])
    genre = html.Tr([html.Td(html.Strong('Genre')), html.Td(id='genre', children='')])
    tempo = html.Tr([html.Td(html.Strong('Tempo (bpm)')), html.Td(id='tempo', children='')])
    key = html.Tr([html.Td(html.Strong('Key')), html.Td(children='A#')])
    loudness = html.Tr([html.Td(html.Strong('Loudness')), html.Td(children='40 dB')])

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
            ), width={"size": 6}
        )
    ])
    
    return row