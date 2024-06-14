from dash import Dash, html, Output, Input, callback
from Dataset import Dataset

@callback(
    [Output('selected-track-title', 'children'),
     Output('album-cover', 'src'),
     Output('track-title', 'children'),
     Output('artist', 'children'),
     Output('genre', 'children'),
     Output('tempo', 'children')],
    [Input('scatterplot-3D', 'clickData')])
def update_selected_track(clickData):
    if clickData is None:
        return "No track selected", 'assets/plain_cover.jpg', '', '', '', ''
    else:
        track_id = clickData['points'][0]['customdata'][0]
        d = Dataset.get()
        selected_track = d.loc[d['id'] == track_id].to_dict('records')[0]
        
        album_cover = selected_track['album_cover']
        album_cover = 'assets/plain_cover.jpg'
        
        track_title = selected_track['track_title']
        artist = selected_track['artist']
        genre = selected_track['genre']
        tempo = selected_track['tempo']
        return f"Selected track {track_id}", album_cover, track_title, artist, genre, tempo