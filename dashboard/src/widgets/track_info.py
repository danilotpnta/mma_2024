from Dataset import Dataset
from dash import dcc, html
import dash_bootstrap_components as dbc

def create_track_info():

    album_cover = html.Img(id='album-cover',
                            style={'width': '100%', 'height': 'auto'},
                            src='', className='border border-dark ')

    track_title = html.Tr([html.Td('Title'), html.Td(id='track-title', children='')])
    artist = html.Tr([html.Td('Artist'), html.Td(id='artist', children='')])
    genre = html.Tr([html.Td('Genre'), html.Td(id='genre', children='')])
    tempo = html.Tr([html.Td('Tempo (bpm)'), html.Td(id='tempo', children='')])

    table_body = [html.Tbody([track_title, artist, genre, tempo])]

    row = dbc.Row([
        dbc.Col(album_cover, width={"size": 2, 'offset': 1}),
        dbc.Col(
            dbc.Table(
                table_body,
                bordered=True,
                hover=True,
                responsive=False,
                striped=True,
            ), width={"size": 8}
        )
    ])
    
    return row